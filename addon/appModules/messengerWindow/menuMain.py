#-*- coding:utf-8 -*
# Thunderbird+ G5, context menu for main Window
import sys
import addonHandler
addonHandler.initTranslation()
import api
import controlTypes
import globalPluginHandler
import utis, sharedVars
from utils115 import message
from wx import Menu,EVT_MENU, CallAfter, CallLater, ScreenDC
from keyboardHandler import KeyboardInputGesture
from tones import beep
import os

class MainMenu():
	def __init__(self, appMod):
		self.appMod= appMod
		self.focused = api.getFocusObject()
		self.tbVersion = utis.TBVersion()

	def showMenu (self, fo):
		mainMenu = Menu ()
		# 2023-09-13: no longer necessary: 4 Choose columns
		# mainMenu.Append (4, _("Choose and arrange the columns of the message list"))
		mainMenu.Append (8, _("Help\tCtrlF1"))

		mainMenu.Append (12, _("Change log"))
		# mainMenu.Append (13, _("Notification page"))
		mainMenu.Append (14, _("Donate"))

		# mainMenu.Append (11, _("Chichi's page"))
		mainMenu.Append (9, _("Write to support (after reading the manual and the change history)"))
		mainMenu.Append (10, _("Join the thunderbird-dv mailing list (French)"))
		# removed 2411.22mainMenu.Append (15, _("Update"))
		# #divers		
		# subMenu =Menu ()
		# #s=u"Convertir un lien &vidéo en flu RSS,Choisir et agencer les colonnes de la liste de messages".split (",")
		# #for a,b  in enumerate (s):subMenu.Append (a+40,b)  ##<<
		# subMenu.Append (41,"Choisir et agencer les colonnes de la liste de messages")
		# #subMenu.Append (42,"Organisation des colonnes  \tNVDA+ù")
		# mainMenu.AppendSubMenu (subMenu,"Divers")
		mainMenu.Bind (EVT_MENU,self.onMenu)
		utis.showNVDAMenu  (mainMenu)

	def onMenu(self, evt):
		#beep(440, 20)
		ID =evt.Id
		#message ("menu ID: " + str(ID))
		# if ID == 4: # choisir les colonnes à afficher
			# return CallAfter(self.showColumnPicker)
		if ID == 8:
			return CallAfter(utis.showHelp)
		elif ID == 9: # write to support
			return CallAfter(utis.toSupport, self.tbVersion)

		elif ID == 10: # join Thunderbird_DV
			return CallAfter(utis.toSupport, self.tbVersion)
			return CallAfter(os.startfile, "http://rptools.org/thunderbird-dv.html")
		elif ID == 11:
			lang = utis.getLang()
			return CallAfter(os.startfile, "http://www.rptools.org/Outils-DV/thunderbird-chichi-" + lang + ".html")
		elif ID == 12: #changelog
			return CallAfter(showTranslatedHTML, "TB+G5-history.html")
		# elif ID == 13: # notifications
			# return CallAfter(showTranslatedHTML, "notificationsG5.html")
		elif ID == 14: # donate
			return CallAfter(os.startfile, "https://www.paypal.com/donate/?business=QQJT2CCNR66G4&no_recurring=0&item_name=Thunderbird%2Badd-on+for+NVDA++donations.+%0AMany+thanks+%21+%3B&currency_code=EUR")
		elif ID == 15: 
			# for p in globalPluginHandler.runningPlugins:
				# sharedVars.logte("Running global plugin:" + p.__module__) 
			# Result of this test: Running global plugin:globalPlugins.ThunderbirdGlob 
			gp = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.ThunderbirdGlob'][0]
			gp.script_searchUpdate(None)
			

	def showColumnPicker(self):
		utis.setSpeech(False)
		#sharedVars.debugMess(self.focused, " focused ")
		o2=self.focused.parent # threadTree
		#sharedVars.debugMess(o2, " parent ")
		if utis.getIA2Attribute(o2)  != "threadTree": 
			CallLater (10, message, _("Please select  the message list and try again."))
			utis.setSpeech(True)
			return
		else: 
			CallLater (20, chooseCols, o2.firstChild.lastChild)
			return

# normal functions
def getObjAlerts (windowHandle): return clientObject.ElementFromHandle (windowHandle).FindAll(TreeScope_Descendants,clientObject.CreatePropertyCondition (UIA_LegacyIAccessibleRolePropertyId,ROLE_SYSTEM_ALERT))	

# def getObjAlert2(pp=None):
	# try:
		# #role.ALERT=138 Tag: div, états: , childCount: 6 Chemin: role FRAME=34| i34, role-GROUPING=56, , IA2ID: tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID: mailContent | i13, role-TEXTFRAME=91,  | i0, role-ALERT=138,  , IA2Attr: class: container infobar, display: flex, tag: div, xml-roles: alert,  ;
		# if not pp:
			# pp = utis.getPropertyPageFromFG()
		# if sharedVars.debug: sharedVars.log(pp, " pp: ", False)
		# sharedVars.objLooping = True
		# #| i13of 19 , role-TEXTFRAME=91,  | i0, role-ALERT=138
		# o = pp.lastChild
		# #if sharedVars.debug: sharedVars.log(o, " o: ", False)
		# while o and o.role != controlTypes.Role.TEXTFRAME:
			# #if sharedVars.debug: sharedVars.log(o, " o: ", False)
			# o = o.previous
		# if o is None: return None
		# # i0, role-ALERT=138
		# #if sharedVars.debug: sharedVars.log(o.firstChild, " objet alert: ", False)
		# return o.firstChild 
	# finally:
		# sharedVars.objLooping = False

# def getMenuFromAlert (windowHandle):
	# o = getObjAlert2() # getObjAlerts (windowHandle)
	# if o is None:return  False
	# mainMenu, IDMenu =  Menu (),199

	# subMenu =Menu ()
	# o =o.firstChild.next # label we need 
	# lblMenu = o.name
	# #sharedVars.debugLog = ""	
	# #if sharedVars.debug: sharedVars.log(o, " label ", False)
	# while o is not None: 
		# if o.role == controlTypes.Role.BUTTON:
			# #if sharedVars.debug: sharedVars.log(o, " bo ", False)
			# IDMenu += 1
			# itemText = o.name
			# hk = o.keyboardShortcut
			# subMenu.Append (IDMenu,itemText+" "+hk)
			# sharedVars.menuCommands[str(IDMenu)] = o
		# o = o.next

	# mainMenu.AppendSubMenu (subMenu,  lblMenu)
	# return mainMenu		

# def alertClickButton(menuID, evt):
	# #hk =	evt.GetEventObject ().GetLabelText (evt.Id).split (" ")[-1]
	# sharedVars.menuCommands[str(menuID)].doAction()
	# sharedVars.menuCommands = {}

# def getObjAttachment (self, UIAElement =False):  
	# o  = api.getFocusObject() # api.getFocusObject()
	# while o and not utis.getIA2Attribute (o, "mailContent"):o=o.parent
	# if o is None: return False
	# x =(e for e in range (o.childCount, o.childCount-5,-1))
	# for e in x:
		# if utis.getIA2Attribute (o.getChild (e),"attachmentSize"): 
			# o=o.getChild (e)
			# break
	# #else: return False
	# if o is None: return False
	# #self.objSizeAttachment  = o
	# oPrevious = o.previous
	# return  o
# from api import  config

# def headersToFile (lstHeaders): # v 2.1.3
	# #pth = config.getUserDefaultConfigPath() + u"\\addons\\thunderbird+\\Entêtes-mail.txt"
	# pth =  sharedVars.oSettings.addonPath + "\\Entêtes-mail.txt"
	# if lstHeaders.count("\n") < 15:
		# lstHeaders = _("To get all headers, please open the View Menu, go down to 'Headers' and then press Enter on 'All'  in the submenu. Then display the grave menu again.")
	# oFile = open (pth, "w")
	# if not oFile: return
	# n = oFile.write(lstHeaders)
	# oFile.close()
	# return

# def chooseCols(oBtnPicker):
	# utis.setSpeech(True)
	# oBtnPicker.doAction()
	# # w
	# return

def showTranslatedHTML(pageName):
	from languageHandler import getLanguage
	lang = getLanguage()
	if "fr" in lang:
		url = "https://www.rptools.org/NVDA-Thunderbird/" + pageName
	else:
		url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/" + pageName + "?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		url = url.replace("@lg", lang)
	#  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	os.startfile (url)
