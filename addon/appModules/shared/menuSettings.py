#-*- coding:utf-8 -*
import addonHandler

import api, config, sys, glob, shutil
import gui, wx # Ajouté par Abdel.
from checkListMenu import CheckListMenu # Ajouté par Abdel.
from startupDlg import  StartupDialog
from configobj import ConfigObj
import re
import os, sys
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
		self.options = self.option_messengerWindow = self.option_mainWindow = self.option_msgcomposeWindow = self.option_deactiv = None
		self.regex_removeInSubject = None
		curAddon=addonHandler.getCodeAddon()
		self.addonName =  curAddon.name
		self.iniFile = api.config.getUserDefaultConfigPath()+"\\" + self.addonName + "-1.ini"
		# if sharedVars.debug : sharedVars.log(None, "-1IniFile : " + self.iniFile) 

		self.responseMode = 0 
		basePath = os.path.join(curAddon.path) 
		# sharedVars.log(None, "basepath : " + basePath)
		self.addonPath =basePath# + "\\AppModules"
		# self.copyTB4Ini()
		# sharedVars.log(None, "addonpath : " + self.addonPath)
		self.load()
		# sharedVars.log(None, "Option VirtualSpellChk : " + str(self.options["msgcomposeWindow"]["virtualSpellChk"]))
		# sharedVars.log(None, "virtualSpellChk avant initDegfaults : " + str(sharedVars.virtualSpellChk)) 

	def initDefaults(self) :
		# default option values if ini file does not exist
		if   os.path.exists(self.iniFile) : return
		
		self.options["messengerWindow"]["responseMentionGroup"] = True
		self.options["messengerWindow"]["junkStatusCol"] = True
		self.options["messengerWindow"]["delayFocusDoc"] = "25"
		sharedVars.delayFocusDoc = 25
		# if 			not self.options["messengerWindow"]["focusMode"] :

		self.options["messengerWindow"]["deleteDelays"] = "50 50"
		sharedVars.deleteDelays = [50, 50]


		# self.options["messengerWindow"]["focusMode"] = "1"
		
		if "spellcancelSpeech" not in self.options["msgcomposeWindow"] : self.options["msgcomposeWindow"].update({"spellcancelSpeech":False})
		self.options["msgcomposeWindow"]["closeMessageWithEscape"] = True
		self.options["msgcomposeWindow"]["spellWords"] = True 
		# self.options["msgcomposeWindow"]["virtualSpellChk"] = False
		self.options["msgcomposeWindow"]["onePress"] = True

	def load(self):
		adPath = self.addonPath
		# adPath is the root of the addon path
		self.option_messengerWindow ={
		"TTClean" : _("custom vocalization of rows."),
		# Translators : A smart  folder is a folder that unifies folders of the same type through all  mail accounts
		"delContextMenu" : _("Message deletion: emulate the context menu."),
		"TTnoFolderName" : _("Do not say the window and folder names when entering the list."),		"responseMentionGroup" : _("Combine multiple 'RE' mentions into one"),
		"responseMentionRemove" : _("Delete the 'Re' mentions in the subject column"),
		"responseMentionDelColon" : _("Delete the colons  in the 'Re:' mentions"),
		"namesCleaned" : _("Delete digits and dots from the name of the correspondents"),
		"listGroupName" : _("Hide mailing list names"),
		"junkStatusCol" : _("Announce 'junk' if displayed in the 'junk Status' column"),
		}

		self.option_mainWindow={
		"ftNoEscape" : _("Folder tree: escape does not bring focus to the message list"),
		"ttNoEscape" : _("message list: escape does not bring focus to the folder tree"),
		"firstTabActivation" : _("Access the first unread message when first activating the first tab, otherwise the last message."),
		"withoutReceipt" : _("Ignore acknowledgment requests"),
		"CleanPreview" : _("Partially purify the message when reading it with Space or F4, otherwise purify it completely."),
		"browsePreview" : _("Always display the  cleaned messages when reading them with Space or F4"),
		"browseTranslation" : _("Always display the translation of messages when reading them with Space or F4"),
		}

		self.option_msgcomposeWindow={
		"spellWords" : _("Spell Check: Spell the misspelled word and the suggested word."),
		"spellCancelSpeech" : _("Spell Check: Cancel speech before announcing and spelling these words"),
		# "virtualSpellChk" : _("Enable improved Spell Check while typing."),
		"closeMessageWithEscape" : _("The Esc key closes the message being written"),
		"onePress" : _("Single press on Shift+the key above the tab key to show the option menus, double press to write the corresponding printable character.")
	}


		self.option_deactiv = {
			"TTnoTags" : _("Message list : deactivate  tag management   to improve responsiveness."),
			"TTnoFilterSnd" : _("Message list : do not play sound when list is filtered and gets focus."),
			"SWRnoRead" : _("Separate reading window: do not read the cleaned version of the message when the window is opened."),
			"noAddressBook" : _("Address book : disable additional features of Thunderbird+G5."),
		}

		self.options = ConfigObj(self.iniFile, encoding="utf8") # Ajout du second paramètre par Abdel (L'encodage utf8 est très important afin d'éviter les erreurs d'encodage pour les caractères accentués".
		all_options = (("messengerWindow", self.option_messengerWindow), ("mainWindow", self.option_mainWindow), ("msgcomposeWindow",self.option_msgcomposeWindow), ("deactiv", self.option_deactiv))
		for x in all_options :
			section, keyValue =x 
			if not section in self.options: self.options.update({section:{}})
			for key in keyValue : 
				if not key in self.options[section] : self.options[section].update({key:False})

		self.initDefaults()
		self.setSharedVars(section="messengerWindow")
		section = self.options["messengerWindow"]
		if "delayFocusDoc" not in section  : self.options["messengerWindow"].update({"delayFocusDoc":"25"})
		sharedVars.delayFocusDoc = section.as_int("delayFocusDoc")
		if "focusStartWithInbox" not in section  :
			self.options["messengerWindow"].update({"focusStartWithInbox":"False"})
		if "deleteDelays" not in section  : self.options["messengerWindow"].update({"deleteDelays":"50 50"})
		temp = section["deleteDelays"]
		temp = temp.split(" ")
		sharedVars.deleteDelays = [int(temp[0]), int(temp[1])]
		# startup management
		if "onStartupAction" not in section  :
			self.options["messengerWindow"].update({"onStartupAction":"1"}) # 0=do nothing, 1=apply focusMode, 2=display inbox menu
		else :
			section["onStartupAction"]= section.as_int("onStartupAction")
		if "focusMode" not in section  :
			self.options["messengerWindow"].update({"focusMode":"1"}) # lastmessage in message list
			# self.options.write()
			self.options["messengerWindow"]["focusMode"] = "1"
			self.options["messengerWindow"]["onStartupAction"] = 0
		else : # options are in section, we change their type
			# obsolete section["focusOnStartup"]= section.as_bool("focusOnStartup")
			section["focusStartWithInbox"]= section.as_bool("focusStartWithInbox")
			section["focusMode"]= section.as_int("focusMode")
			
		# words to remove from subject in the message list
		if not "removeInSubject" in self.options["messengerWindow"] : 
			self.options["messengerWindow"].update({"removeInSubject":""})
		else : # option  exists   as string  in the ini file
			self.regex_removeInSubject = re.compile(makeRegex(section["removeInSubject"]))

		# coptions for deactiv : speed needed
		self.setSharedVars(section="deactiv")
		
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
		# utis.playSound("ding")
		# print("soundFiles= " + str(utis.objSoundFiles))
		# set sharedVars for optimization
		sharedVars.virtualSpellChk = False # self.getOption ("msgcomposeWindow", "virtualSpellChk")
		if   not os.path.exists(self.iniFile) :
			self.options.write()
		return
		
	def setSharedVars(self, section) :
		pSection = self.options[section]
		if section == "messengerWindow" :
			sharedVars.TTClean = pSection.as_bool ("TTClean")
			sharedVars.TTFillRow = False # removed : pSection.as_bool ("TTFillRow")
			sharedVars.namesCleaned = pSection.as_bool ("namesCleaned") # correspondent names
			sharedVars.TTnoFolderName = pSection.as_bool ("TTnoFolderName")
			sharedVars.listGroupName = pSection.as_bool("listGroupName")
			sharedVars.junkStatusCol = pSection.as_bool("junkStatusCol")
			sharedVars.delContextMenu  = pSection.as_bool("delContextMenu")
			sharedVars.unread = _("Unread")
			#  merge 3 mutually exclusive boolean  variables into one numeric variable 
			if pSection.as_bool("responseMentionGroup") : self.responseMode = 1
			elif pSection.as_bool("responseMentionRemove") : self.responseMode = 2
			elif pSection.as_bool("responseMentionDelColon") : self.responseMode = 3
			else : self.responseMode = 0
		elif  section == "mainWindow" :  # other options
			sharedVars.oQuoteNav = None
			# elif  section == "msgComposeWindow" : 
				# pass
		elif  section == "deactiv" : 
			sharedVars.TTnoTags = pSection.as_bool ("TTnoTags")
			sharedVars.noAddressBook = pSection.as_bool ("noAddressBook")
		# CallLater(1000, message, "setSharedVars section : " + section) 

	def editWords(self) :
		wrds = self.options["messengerWindow"]["removeInSubject"] 
		utis.inputBox(label=_("Words separated by semicolons :"), title= _("Edit words to hide in the subject of messages"), postFunction=saveWords, startValue=wrds)

	def editDelay(self) :
		utis.inputBox(label=_("Delay before document focusing, 20 to 2000 ms::"), title= _("Special tabs"), postFunction=saveDelay, startValue=sharedVars.delayFocusDoc)

	def editDeleteDelays(self) :
		stVal = str(sharedVars.deleteDelays[0]) + " " + str(sharedVars.deleteDelays[1])
		utis.inputBox(label=_("Delay 1 space Delay 2 in ms:"), title= _("Focusing delays after deleting a message"), postFunction=saveDeleteDelays, startValue=stVal)

	def openSoundFolder(self) :
		soundPath = api.config.getUserDefaultConfigPath() + "\\TB+Sounds"
		if  not os.path.exists(soundPath) :  return beep(100, 30)
		# libPath =  adPath + "\\SoundLib"
		os.startfile(soundPath)

	def backup(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + "-1.inibak"
		if   not os.path.exists(self.iniFile) :		
			self.options.write()
		shutil.copyfile(self.iniFile, bakFile) 
		CallLater(30, utis.noSpeechMessage, u"La configuration actuelle  a été sauvegardée dans un fichier .bakini.")
	def restore(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + "-1.inibak"
		if   os.path.exists(bakFile) :		
			shutil.copyfile(bakFile, self.iniFile) 
			self.load()
			CallLater(30, utis.noSpeechMessage,u"La configuration sauvegardée a été restaurée.")
		else :
			CallLater(30, utis.noSpeechMessage,_("Backup file does not exist."))

	def reset(self) :
		bakFile = api.config.getUserDefaultConfigPath() + "\\" + self.addonName + "-1.inibak"
		if   os.path.exists(self.iniFile) :
			if not os.path.exists(bakFile) :
				os.rename(self.iniFile, bakFile)
			else : 
				os.remove(self.iniFile) 
			self.load()
			self.initDefaults()
			CallLater(30, utis.noSpeechMessage,_("The configuration has been reset to its default values"))

	# def copyTB4Ini(self) :
		# if   os.path.exists(self.iniFile) : return
		# tb4File = api.config.getUserDefaultConfigPath() + "\\Thunderbird+4.ini"
		# if   os.path.exists(tb4File) :		
			# shutil.copyfile(tb4File, self.iniFile) 

	def getOption(self, iniSect, iniKey="", kind="b") : # si iniKey == "", retourne la section entière 
		# kind Valuses : "" = no type  conversion, b = bool, s = string, i = int
		if iniSect == "messenger" : iniSect = "messengerWindow"
		elif iniSect == "compose" : iniSect = "msgcomposeWindow"
		if iniKey == "" : return self.options[iniSect]
		else : 
			try : 
				if kind == "b" : return self.options[iniSect].as_bool(iniKey)
				elif kind == "" : return self.options[iniSect][iniKey]
				elif kind == "i" : return self.options[iniSect].as_int(iniKey)
			except : return False

	def showOptionsMenu(self, frame) :
		mainMenu  = Menu ()
		# menu IDs :0=messenger, 100=compose, 200=startup
		# messengerWindow
		if frame == "messengerWindow" :
			"""
			Le bloc mulgilignes ci-dessous a été mis en commentaire par Abdel.
			menu, options, keys = Menu(), self.options, list(self.option_messengerWindow.keys())
			#keys.sort ()
			for e in range (len(keys)) :
				lbl = self.option_messengerWindow [keys[e]]
				if keys[e].endswith("_str") : # == "editWords" :
					menu.Append(e, lbl)
				else :
					menu.AppendCheckItem (0 + e, lbl).Check (options["messengerWindow"].as_bool (keys[e]))
			""" # Fin du bloc multilignes mis en commentaire par Abdel.
			menu = Menu() # Ajouté par Abdel.
			item = None # Ajouté par Abdel.
			for key in self.options["messengerWindow"].keys(): # Ajouté par Abdel.
				if key.endswith("_str"): # Ajouté par Abdel.
					item = key # Ajouté par Abdel.
			if item: # Ajouté par Abdel.
				self.options["messengerWindow"].pop(key) # Ajouté par Abdel.
			menu.Append(1993, _("MessageList")) # Ajouté par Abdel.
			menu.Append(1994, _("Edit words to hide in message subject")) # Ajouté par Abdel.
			menu.Append(1997, _("Other Options")) # Added by PL 1995 to 1996 are already taken
			mainMenu.AppendSubMenu (menu, _("Main window options"))
			mainMenu.Bind(EVT_MENU, self.onOptMenu)
		# msgCompose submenu
		if frame in ("messengerWindow", "msgcomposeWindow") :
			"""
			Le bloc multilignes ci-dessous a étémis en commentaire par Abdel.
			menu, options, keys = Menu (), self.options, list(self.option_msgcomposeWindow.keys())
			#keys.sort ()
			for e in range (len (keys)): menu.AppendCheckItem (100+e, self.option_msgcomposeWindow[keys[e]]).Check (options["msgcomposeWindow"].as_bool (keys[e]))
			mainMenu.AppendSubMenu (menu, _("Write window options"))
		""" # Fin du bloc multilignes mis en commentaire par Abdel.
			mainMenu.Append (1995, _("Write window options")) # Ajouté par Abdel.
			mainMenu.Bind (EVT_MENU,self.onOptMenu)
			"""
			Le bloc multilignes ci-dessous a été mis en commentaire par Abdel.
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
		""" # Fin du bloc multilignes mis en commentaire par Abdel.
		# deactiv submenu
		if frame == "messengerWindow" :
			"""
			Le bloc multilignes ci-dessous a été mis en commentaire par Abdel.
			menu, options, keys = Menu (), self.options, list(self.option_deactiv.keys())
			for e in range (len (keys)): menu.AppendCheckItem (300+e, self.option_deactiv[keys[e]]).Check (options["deactiv"].as_bool (keys[e]))	
			mainMenu.AppendSubMenu (menu, _("Deactivations"))
			""" # Fin du bloc multilignes mis en commentaire par Abdel.
			mainMenu.Append (1996, _("Deactivations")) # Ajouté par Abdel.
			mainMenu.Bind (EVT_MENU,self.onOptMenu)
			mainMenu.Append(895, _("&Focus and Startup Options"))
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

		#if eID < 100 : # messengerWindow, options fenêtre principale  -- Mis en commentaire par Abdel.
		if eID == 1993: # Id créé par Abdel.
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				CheckListMenu, title=_("Message list options"), frame="messengerWindow", options=self, 
				fakeRadioGroups=[(4,5,6)],
				postFunction=self.setSharedVars)
			return
		if eID==  1994 :  # is not a check item  -- ID créé par Abdel.
			return CallLater(30, self.editWords)
		if eID == 1997 : # other options 
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				CheckListMenu, title=_("Other  options"), frame="mainWindow", options=self,
				fakeRadioGroups=None,
				postFunction=self.setSharedVars(section="mainWindow"))
			return
		#if eID < 200: # msgcomposeWindow -- Mis en commentaire par Abdel.
		if eID == 1995: # ID créé par Abdel.
			IDRange = 100
			#section, keys, options = "msgcomposeWindow", list(self.option_msgcomposeWindow.keys()), self.options -- Mis en commentaire par Abdel.
			#key=keys[eID-IDRange] -- Mis en commentaire par Abdel.
			#options[section][key]= evt.IsChecked () -- Mis en commentaire par Abdel.
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				CheckListMenu, title=_("Write window options"), frame="msgcomposeWindow", options=self)
			#if key == "virtualSpellChk" : -- Mis en commentaire par Abdel, la clé "virtualSpellChk" n'existe plus dans self.options["msgcomposeWindow"].keys().
				#sharedVars.virtualSpellChk = self.options[section][key]  -- Mis en commentaire par Abdel pour les mêmes raisons.
			#return options.write ()   -- Mis en commentaire par Abdel pour les mêmes raisons.
		if eID < 300  : # update options
			IDRange = 200
			section, keys, options = "startup", list(self.option_startup.keys()), self.options
			if eID == IDRange +4 : # old + len(keys)) : # last option :update
				CallLater(40, toggleUpdateState)
				return
			key = list(self.options["msgcomposeWindow"].keys())[4] #   =# keys[eID-IDRange]
			options["msgcomposeWindow"][key]= evt.IsChecked ()
			if key == "logging" :
				sharedVars.debug = options["msgcomposeWindow"][key]
				sharedVars.debugLog = ""
			return options.write () 	
		# deactiv
		if eID == 1996: # ID créé par Abdel.
			IDRange = 300
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				CheckListMenu, title=_("Deactivations"), frame="deactiv", options=self, 
				fakeRadioGroups=None,
				postFunction=self.setSharedVars)
		elif eID == 895 : # Focus and startup options
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				StartupDialog, title=_("Focus and Startup Options"), options=self)
			return
		elif eID == 899 : # sound folder
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
	# sharedVars.delayFocusDoc = iDelay
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
	sharedVars.delayFocusDoc = iDelay
	sharedVars.oSettings.options["messengerWindow"].update({"delayFocusDoc":strDelay})
	sharedVars.oSettings.options.write()

def saveDeleteDelays(strDelays) :
	if strDelays == "ibCancel" : return
	cancelSpeech()
	delays = strDelays.split(" ")
	if len(delays) != 2 :
		beep(100, 40)
		return
	try :
		delays[0] = int(delays[0])
		delays[1] = int(delays[1])
	except : return beep(100, 50) # return CallLater(50, message, u"La valeur doit être un nombre")
	sharedVars.deleteDelays = delays
	sharedVars.oSettings.options["messengerWindow"].update({"deleteDelays":strDelays})
	sharedVars.oSettings.options.write()
