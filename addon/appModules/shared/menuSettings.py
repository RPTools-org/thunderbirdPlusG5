#-*- coding:utf-8 -*

import api, config, sys, glob, shutil
from configobj import ConfigObj
import re
import addonHandler,  os, sys
import globalPluginHandler
import  sharedVars, utis
from wx import Menu, EVT_MENU, EVT_MENU_CLOSE, CallAfter, CallLater 
from ui import  message
from speech import cancelSpeech
from tones import beep
addonHandler.initTranslation()


class  Settings() :
	def __init__(self, fromClass) :
		# fromClass doit être une référence sur la classe AppModule ou GlobalPlugin 
		self.refClass  = fromClass
		self.options = self.option_messengerWindow = self.option_msgcomposeWindow = self.option_startup = self.option_chichi = None
		self.regex_removeInSubject = None
		curAddon=addonHandler.getCodeAddon()
		self.addonName =  curAddon.name
		self.iniFile = api.config.getUserDefaultConfigPath()+"\\" + self.addonName + ".ini"
		# if sharedVars.debug : sharedVars.log(None, "IniFile : " + self.iniFile) 

		self.responseMode = 0 
		basePath = os.path.join(curAddon.path) 
		# sharedVars.log(None, "basepath : " + basePath)
		self.addonPath =basePath# + "\\AppModules"
		self.copyTB4Ini()
		# sharedVars.log(None, "addonpath : " + self.addonPath)
		self.load()
		# sharedVars.log(None, "Option VirtualSpellChk : " + str(self.options["msgcomposeWindow"]["virtualSpellChk"]))
		# sharedVars.log(None, "virtualSpellChk avant initDegfaults : " + str(sharedVars.virtualSpellChk)) 
		self.initDefaults()

	def initDefaults(self) :
		# default option values if ini file does not exist
		if  not os.path.exists(self.iniFile) :
			# self.options = self.option_messengerWindow = self.option_msgcomposeWindow = self.option_startup = None
			self.options["messengerWindow"]["namesCleaned"] = True
			self.options["messengerWindow"]["separateCols"] = True
			self.options["messengerWindow"]["responseMentionGroup"] = True
			self.options["messengerWindow"]["junkStatusCol"] = True
			# made by Chichi or the  "start with inbox" thunderbird addon ->self.options["startup"]["alwaysMainTab"] = True

			self.options["msgcomposeWindow"]["closeMessageWithEscape"] = True
			self.options["msgcomposeWindow"]["spellWords"] = True 
			# self.options["msgcomposeWindow"]["virtualSpellChk"] = False
			self.options["msgcomposeWindow"]["onePress"] = True
		#if self.getOption ("messengerWindow", "separateCols") : self.colSepar = ", "
		# debug logging
		# désactivé sharedVars.debug = self.getOption("startup", "logging")

	def load(self):
		adPath = self.addonPath
		# adPath is the root of the addon path
		self.option_messengerWindow ={
		"TTClean" : _("Message list : custom vocalization of rows."),
		"TTFillRow" : _("Message list : force rows to be filled if always blank."),
		"TTnoFolderName" : _("Message list : Do not say the window and folder names when entering the list."),		"responseMentionGroup" : _("Combine multiple 'RE' mentions into one"),
		"responseMentionRemove" : _("Delete the 'Re' mentions in the subject column"),
		"responseMentionDelColon" : _("Delete the colons  in the 'Re:' mentions"),
		"namesCleaned" : _("Clean the names of correspondents in the message list"),
		# "separateCols" : _("Add punctuation between columns"),
		"listGroupName" : _("Hide mailing list names"),
		"editWords_str" : _("Edit words to hide in message subject"),
		"junkStatusCol" : _("Announce 'junk' if displayed in the 'junk Status' column"),
		# "TTFirstUnread" : _("Spacebar on a folder with unread searches for the first unread message from the beginning of the list"),
		# "withoutFolderKeyNav" : _("Do not use first character navigation in the folder tree"),
		# "noDirectKeyNav" : _("Character navigation via an edit box"),
		"withoutReceipt" : _("Ignore acknowledgment requests"),
		"displayTranslations" : _("Always display the translations"),
		"firstTabActivation" : _("Access the first unread message when first activating the first tab, otherwise the last message."),
		# "sayContact" : _("Address book : explicit announcement of contacts in the contact list."),

		# "WwithUnread" : _("Show only folders with unread in the 'Folders in Tree' dialog"),
		# "WithoutAutoRead" : _("separate reading window: do not automatically read the mmessage if it causes NVDA hangs"),
		# "editDelay_str" : _("Edit the delay before the automatic reading of the separate message window.\\tAlt+d,n")
		}

		self.option_msgcomposeWindow={
		"spellWords" : _("Spell Check: Spell the misspelled word and the suggested word."),
		# "virtualSpellChk" : _("Enable improved Spell Check while typing."),
		"closeMessageWithEscape" : _("The Esc key closes the message being written"),
		"onePress" : _("Single press to show the context menus, double press to write a grave accent  or Tilde or ¬¬.")
	}

		self.option_startup= {}
			# # "alwaysMainTab" : _("Toujours activer l'onglet principal au démarrage de Thunderbird"),
			# # "logging" : _("Journalisation (peut ralentir)")
		# }

		self.option_chichi = {
			# "TTnoClean" : _("Message list : Do not clean table rows before announcement  to improve responsiveness."),
			# "TTAltReading" : _("Message list : use the alternate method to read the lines."),
			"TTnoTags" : _("Message list : deactivate  tag management   to improve responsiveness."),
			"TTnoFilterSnd" : _("Message list : do not play sound when list is filtered and gets focus."),
			"SWRnoRead" : _("Separate reading window: do not read the cleaned version of the message when the window is opened."),
			"noAddressBook" : _("Address book : disable additional features of Thunderbird+G5."),
			# "FTnoSpace" : _("Folders: Spacebar does not select the next unread message in the list and does not show the list of unread folders"),
			# "FTnoNavLetter" : _("Folders: no first character navigation "),
			# "TTnoSpace" : _("Message list: Spacebar does not read message from preview pane"),
			# "TTNoExpand" : _("Message list: Spacebar reads the preview pane conversation summary."),
			# "TTnoSmartReply" : _("Message list : No SmartReply"),
			# "TTnoFilterBar" : _("Message list: do not manage the quick filter bar"),
			# "TTnoEscape" : _("Message list: Escape does not return to folder tree"),
			# "MainNoTab" : _("main window: Tab does not move to next pane"),
			# "mainNoEscape" : _("Main window: restore the default behavior of the escape key"),
			# "closeTBWithCtrlF4" : _("Allow Thunderbird to close with control+w or control+F4")
		}

		self.options = ConfigObj(self.iniFile)
		all_options = (("messengerWindow", self.option_messengerWindow),("msgcomposeWindow",self.option_msgcomposeWindow),("startup", self.option_startup), ("chichi", self.option_chichi))
		for x in all_options :
			section, keyValue =x 
			if not section in self.options: self.options.update({section:{}})
			for key in keyValue : 
				if not key in self.options[section] : self.options[section].update({key:False})
		section = self.options["messengerWindow"]
		sharedVars.TTClean = section.as_bool ("TTClean")
		sharedVars.TTFillRow = section.as_bool ("TTFillRow")
		sharedVars.TTnoFolderName = section.as_bool ("TTnoFolderName")
		#sharedVars.useKeyNav =  not section.as_bool ("FKN1_withoutFolderKeyNav")		
		#sharedVars.directKeyNav =   not section.as_bool ("FKN2_noDirectKeyNav")		
		if not"delayReadWnd" in self.options["messengerWindow"] : 
			self.options["messengerWindow"].update({"delayReadWnd":"100"})
		sharedVars.delayReadWnd =    int(section.as_int ("delayReadWnd")		)
		# words to remove from subject in the message list
		if not "removeInSubject" in self.options["messengerWindow"] : 
			self.options["messengerWindow"].update({"removeInSubject":""})
		else : # option  exists   as string  in the ini file
			self.regex_removeInSubject = re.compile(makeRegex(section["removeInSubject"]))
		
		# coptions for chichi : speed needed
		section = self.options["chichi"]
		# sharedVars.TTnoClean = section.as_bool ("TTnoClean")
		# sharedVars.TTAltReading = section.as_bool ("TTAltReading")
		sharedVars.TTnoTags = section.as_bool ("TTnoTags")
		sharedVars.noAddressBook = section.as_bool ("noAddressBook")
		# sharedVars.FTnoNavLetter = False # section.as_bool ("FTnoNavLetter")
		# sharedVars.FTnoSpace = False # section.as_bool ("FTnoSpace")
		# sharedVars.TTnoSpace = False # section.as_bool ("TTnoSpace")
		# sharedVars.TTnoFilterBar = False # section.as_bool ("TTnoFilterBar")

		# self.withFoldersList = section.as_bool ("WwithFoldersList")		
		#sound
		import shutil
		soundPath = api.config.getUserDefaultConfigPath() + "\\TB+Sounds"
		#print("confPath :" + confPath)
		if  not os.path.exists(soundPath) : 
			libPath =  adPath + "\\SoundLib"
			os.makedirs(soundPath, exist_ok=True)
			shutil.copy2(libPath + "\\filtre.wav" , soundPath + "\\filter.wav")
		from os.path import basename
		soundFilePath = glob.glob(soundPath + "\\*.wav")
		utis.objSoundFiles = {}
		for path in soundFilePath:
			utis.objSoundFiles[basename(path)]= open (path,"rb").read ()
		#utis.playSound("ding")
		# sharedVars.log(None, str(utis.objSoundFiles))
		self.setResponseMode()
		self.setfolderTreeNav()
		# set sharedVars for optimization
		sharedVars.virtualSpellChk = False # self.getOption ("msgcomposeWindow", "virtualSpellChk")
		return
	def editWords(self) :
		wrds = self.options["messengerWindow"]["removeInSubject"] 
		utis.inputBox(label=_("Words separated by semicolons :"), title= _("Edit words to hide in the subject of messages"), postFunction=saveWords, startValue=wrds)

	def editDelay(self) :
		utis.inputBox(label=_("Delay between 20 and 2000 milliseconds before filtered reading (default: 100):"), title= _("Separate reading window"), postFunction=saveDelay, startValue=sharedVars.delayReadWnd)
	def openSoundFolder(self) :
		soundPath = api.config.getUserDefaultConfigPath() + "\\TB+Sounds"
		if  not os.path.exists(soundPath) :  return beep(100, 30)
		# libPath =  adPath + "\\SoundLib"
		os.startfile(soundPath)

	def backup(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + ".inibak"
		if   not os.path.exists(self.iniFile) :		
			self.options.write()
		shutil.copyfile(self.iniFile, bakFile) 
		CallLater(30, utis.noSpeechMessage, u"La configuration actuelle  a été sauvegardée dans un fichier .bakini.")
	def restore(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + ".inibak"
		if   os.path.exists(bakFile) :		
			shutil.copyfile(bakFile, self.iniFile) 
			self.load()
			CallLater(30, utis.noSpeechMessage,u"La configuration sauvegardée a été restaurée.")
		else :
			CallLater(30, utis.noSpeechMessage,_("Backup file does not exist."))

	def reset(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + ".inibak"
		if   os.path.exists(self.iniFile) :
			if not os.path.exists(bakFile) :
				os.rename(self.iniFile, bakFile)
			else : 
				os.remove(self.iniFile) 
			self.load()
			self.initDefaults()
			CallLater(30, utis.noSpeechMessage,_("The configuration has been reset to its default values"))

	def copyTB4Ini(self) :
		if   os.path.exists(self.iniFile) : return
		tb4File = api.config.getUserDefaultConfigPath() + "\\Thunderbird+4.ini"
		if   os.path.exists(tb4File) :		
			shutil.copyfile(tb4File, self.iniFile) 

	def getOption(self, iniSect, iniKey="") : # si iniKey == "", retourne la section entière 
		if iniSect == "messenger" : iniSect = "messengerWindow"
		elif iniSect == "compose" : iniSect = "msgcomposeWindow"
		if iniKey == "" : return self.options[iniSect]
		else : 
			try : return self.options[iniSect].as_bool(iniKey)
			except : return False

	def setResponseMode(self):
		if self.getOption("messengerWindow", "responseMentionGroup") : self.responseMode = 1
		elif self.getOption("messengerWindow", "responseMentionRemove") : self.responseMode = 2
		elif self.getOption("messengerWindow", "responseMentionDelColon") : self.responseMode = 3
		else : self.responseMode = 0

	def setfolderTreeNav(self) :
		sharedVars.useKeyNav = (False if  self.getOption("messengerWindow", "withoutFolderKeyNav") else True)
		sharedVars.directKeyNav = (False if  self.getOption("messengerWindow", "noDirectKeyNav") else True)

	def showOptionsMenu(self, frame) :
		mainMenu  = Menu ()
		# menu IDs :0=messenger, 100=compose, 200=startup
		# messengerWindow
		if frame == "messengerWindow" :
			menu, options, keys = Menu(), self.options, list(self.option_messengerWindow.keys())
			#keys.sort ()
			
			for e in range (len(keys)) : 
				lbl = self.option_messengerWindow [keys[e]]
				if keys[e].endswith("_str") : # == "editWords" :
					menu.Append(e, lbl)
				else : 
					menu.AppendCheckItem (0 + e, lbl).Check (options["messengerWindow"].as_bool (keys[e]))
				
			mainMenu.AppendSubMenu (menu, _("Main window options"))
		# msgCompose submenu
		if frame in ("messengerWindow", "msgcomposeWindow") :
			menu, options, keys = Menu (), self.options, list(self.option_msgcomposeWindow.keys())
			#keys.sort ()
			for e in range (len (keys)): menu.AppendCheckItem (100+e, self.option_msgcomposeWindow[keys[e]]).Check (options["msgcomposeWindow"].as_bool (keys[e]))	
			mainMenu.AppendSubMenu (menu, _("Write window options"))
			mainMenu.Bind (EVT_MENU,self.onOptMenu)
			# mainMenu.Bind (EVT_MENU_CLOSE,self.onOptMenuClose)
		# startup submenu)
		if frame == "messengerWindow" :
			menu, options, keys = Menu (), self.options, list(self.option_startup.keys())
			#keys.sort ()
			for e in range (len (keys)): menu.AppendCheckItem (200+e, self.option_startup[keys[e]]).Check (options["startup"].as_bool (keys[e]))
			# # ajout de activer/ désactiver mise à jour
			# menu.Append(200+e+1, getUpdateLabel())
			# mainMenu.AppendSubMenu (menu, _("Update options"))
			mainMenu.Bind (EVT_MENU,self.onOptMenu)
		# Chichi submenu
		if frame == "messengerWindow" :
			menu, options, keys = Menu (), self.options, list(self.option_chichi.keys())
			for e in range (len (keys)): menu.AppendCheckItem (300+e, self.option_chichi[keys[e]]).Check (options["chichi"].as_bool (keys[e]))	
			mainMenu.AppendSubMenu (menu, _("Deactivations"))
			mainMenu.Bind (EVT_MENU,self.onOptMenu)
			mainMenu.Append(899, _("Open sound folder..."))
			mainMenu.Append(900, _("Backup current configuration file"))
			mainMenu.Append(901, _("Restore backed up configuration file"))
			mainMenu.Append(902, _("Reset configuration"))
	# mainMenu.Bind (EVT_MENU,self.onOptMenu)

		utis.showNVDAMenu  (mainMenu)	
	# def onOptMenuClose(self, evt) :
		# evt.Skip(False)
		# beep(440, 10)
		
	def onOptMenu(self, evt) :
		eID =evt.Id
		# menu IDs :0=messenger, 100=compose, 200=startup
		# sharedVars.debugLog = ", menu ID : " + str(eID)

		if eID < 100 : # messengerWindow, options fenêtre principale
			IDRange = 0
			section, keys, options = "messengerWindow", list(self.option_messengerWindow.keys()), self.options
			key = keys[eID-IDRange]			
			# sharedVars.log(None, "choosen Key " + str(key))
			if key ==  "editWords_str" :  # is not a check item
				return CallLater(30, self.editWords)
			if key ==  "editDelay_str" :  # is not a check item
				return CallLater(30, self.editDelay)
# =====
			toFind = _("Mentions")
			if evt.EventObject.GetLabelText(eID).find (toFind)!=-1 :
				for k in ("responseMentionGroup","responseMentionRemove","responseMentionDelColon"):
					options[section][k] = False
			# ====
			options[section][key]= evt.IsChecked ()
			if key == "TTClean" : sharedVars.TTClean = self.options[section][key]
			if key == "TTFillRow" : sharedVars.TTFillRow = self.options[section][key]
			if key == "TTnoFolderName" : sharedVars.TTnoFolderName = self.options[section][key]
			self.setResponseMode()
			self.setfolderTreeNav()
			options.write () 	
			# beep(700, 40)
			# evt.Skip(False)
			return
		elif eID < 200  : # msgcomposeWindow
			IDRange = 100
			section, keys, options = "msgcomposeWindow", list(self.option_msgcomposeWindow.keys()), self.options
			key=keys[eID-IDRange]			
			options[section][key]= evt.IsChecked ()
			if key == "virtualSpellChk" :
				sharedVars.virtualSpellChk = self.options[section][key]
			return options.write () 	
		elif eID < 300  : # update options
			IDRange = 200
			section, keys, options = "startup", list(self.option_startup.keys()), self.options
			if eID == IDRange +4 : # old + len(keys)) : # last option :update
				CallLater(40, toggleUpdateState)
				return
			key = keys[4] #   =# keys[eID-IDRange]
			options[section][key]= evt.IsChecked ()
			if key == "logging" :
				sharedVars.debug = options[section][key]
				sharedVars.debugLog = ""
			return options.write () 	
		# chichi
		elif eID < 400  : # chichi
			IDRange = 300
			section, keys, options = "chichi", list(self.option_chichi.keys()), self.options
			# if eID == (IDRange + len(keys)) : # last option :update
				# CallLater(40, toggleUpdateState)
				# return
			key=keys[eID-IDRange]			
			options[section][key]= evt.IsChecked ()
			# if key == "TTnoSpace" : sharedVars.TTnoSpace = self.options[section][key]
			# elif key == "TTnoFilterBar" : sharedVars.TTnoFilterBar = self.options[section][key]
			# if key == "TTnoClean" : sharedVars.TTnoClean = self.options[section][key]
			if key == "TTnoTags" : sharedVars.TTnoTags = self.options[section][key]
			# elif key ==  "SWRnoRead :"
			elif key == "noAddressBook" : sharedVars.noAddressBook = self.options[section][key]
			# elif key == "FTnoSpace" : sharedVars.FTnoSpace = self.options[section][key]
			return options.write () 	
		elif eID == 899 :
			self.openSoundFolder()
		elif eID == 900 :
			self.backup()
		elif eID == 901 :
			self.restore()
		elif eID == 902 :
			self.reset()
		return


# import os
# def getUpdateLabel() :
	# addonName = "Thunderbird+4"
	# nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  addonName + "-nextUpdate.pickle"
	# exists =  (True if  os.path.exists(nextUpdateFile) else False)
	# if exists and  os.path.getsize(nextUpdateFile) < 5 : # mise à jour désactivée # maj désactivée
		# return  _("Enable automatic update")
	# return _("Disable automatic update")

# def toggleUpdateState() :
	# addonName = "Thunderbird+4"
	# nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  addonName + "-nextUpdate.pickle"
	# if  os.path.exists(nextUpdateFile) and   os.path.getsize(nextUpdateFile) < 5 : 
		# os.remove(nextUpdateFile) # réactive la maj
		# cancelSpeech()
		# CallAfter(message, _("Automatic update has been enabled. You can restart NVDA to check for an update."))
		# return 1
	# # désactivation maj : écrit le fichier de longueur < 5 et contenant 0
	# cancelSpeech()
	# try :
		# ut = "0"
		# with open(nextUpdateFile, mode="w") as fileObj :
			# #pickle.dump(ut, fileObj)  #, protocol=0
			# fileObj.write(ut)
	# except :
		# return CallAfter(message, _("Error saving update settings file."))
	# CallAfter(message, _("Automatic update has been disabled."))
	# return

	def removeLabel(value, label) :
		return  value[len(label):]

def makeRegex(words) :
	words = re.escape(str(words))
	words = words.replace(";", "|")
	return words

def saveWords(words) :
	words = str(words)
	if words == "ibCancel" : return
	# sharedVars.log(None, "Mots saisis " + words)
	# speech.cancelSpeech()
	sharedVars.oSettings.options["messengerWindow"]["removeInSubject"] = words
	# sharedVars.delayReadWnd = iDelay
	sharedVars.oSettings.options["messengerWindow"].update({"removeInSubject" : words})
	sharedVars.oSettings.options.write()
	sharedVars.oSettings.regex_removeInSubject = re.compile(makeRegex(words))

def saveDelay(strDelay) :
	if strDelay == "ibCancel" : return
	cancelSpeech()
	try : iDelay = int(strDelay)
	except : return beep(100, 50) # return CallLater(50, message, u"La valeur doit être un nombre")
	if iDelay < 20 or iDelay > 2000 :
		return beep(250, 50) # CallLater(50, message, u"Le délai doit être compris entre 20 et 2000 milli-secondes !")
	sharedVars.delayReadWnd = iDelay
	sharedVars.oSettings.options["messengerWindow"].update({"delayReadWnd":strDelay})
	sharedVars.oSettings.options.write()
