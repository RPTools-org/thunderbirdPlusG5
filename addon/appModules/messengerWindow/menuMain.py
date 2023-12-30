#-*- coding:utf-8 -*
# Thunderbird+ 4.x, context menu for main Window

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import globalVars
import utis, sharedVars
from wx import Menu,EVT_MENU, CallAfter, CallLater, ScreenDC
from oleacc import ROLE_SYSTEM_ALERT, ROLE_SYSTEM_LINK, ROLE_SYSTEM_TOOLBAR, ROLE_SYSTEM_TEXT,STATE_SYSTEM_MARQUEED, STATE_SYSTEM_PRESSED, ROLE_SYSTEM_SEPARATOR, STATE_SYSTEM_SELECTED, STATE_SYSTEM_SELECTABLE, STATE_SYSTEM_FOCUSABLE
from UIAHandler import handler, UIA_ControlTypePropertyId, UIA_ToolBarControlTypeId, TreeScope_Children, TreeScope_Descendants, UIA_ButtonControlTypeId, UIA_LegacyIAccessibleRolePropertyId, UIA_LegacyIAccessibleValuePropertyId, UIA_TextControlTypeId, UIA_LegacyIAccessibleStatePropertyId, UIA_ListControlTypeId, UIA_ListItemControlTypeId, IUIAutomationInvokePattern, UIA_LegacyIAccessibleKeyboardShortcutPropertyId, UIA_LegacyIAccessibleNamePropertyId, UIA_DocumentControlTypeId, UIA_EditControlTypeId, UIA_CustomControlTypeId,UIA_NamePropertyId, UIA_LegacyIAccessibleDescriptionPropertyId , UIA_TreeItemControlTypeId , UIA_NamePropertyId 
from UIAHandler import UIA_SelectionItemIsSelectedPropertyId ,UIA_ItemStatusPropertyId,UIA_TreeControlTypeId  
clientObject =handler.clientObject
GetFirstChildElement, GetNextSiblingElement, GetParentElement, GetLastChildElement    = clientObject.RawViewWalker.GetFirstChildElement, clientObject.RawViewWalker.GetNextSiblingElement, clientObject.RawViewWalker.GetParentElement, clientObject.RawViewWalker.GetLastChildElement
CPC=clientObject.CreatePropertyCondition 
from ui import message
from keyboardHandler import KeyboardInputGesture
from tones import beep
import os
import addonHandler
addonHandler.initTranslation()

class MainMenu() :
	def __init__(self, appMod) :
		self.appMod= appMod
		self.objFirstGrouping = None
		self.focused = globalVars.focusObject
		self.tbVersion = utis.TBVersion()

	def showMenu (self, fo):
		mainMenu = Menu ()
		# 2023-09-13 : no longer necessary : 4 Choose columns
		# mainMenu.Append (4, _("Choose and arrange the columns of the message list"))
		mainMenu.Append (8, _("Help\tCtrlF1"))

		mainMenu.Append (12, _("Change log"))
		mainMenu.Append (13, _("Notification page"))
		mainMenu.Append (14, _("Donate"))

		# mainMenu.Append (11, _("Chichi's page"))
		mainMenu.Append (9, _("Write to support (after reading the manual and the change history)"))
		mainMenu.Append (10, _("Join the thunderbird-dv mailing list (French)"))
		# #divers		
		# subMenu =Menu ()
		# #s=u"Convertir un lien &vidéo en flu RSS,Choisir et agencer les colonnes de la liste de messages".split (",")
		# #for a,b  in enumerate (s) :subMenu.Append (a+40,b)  ##<<
		# subMenu.Append (41,"Choisir et agencer les colonnes de la liste de messages")
		# #subMenu.Append (42,"Organisation des colonnes  \tNVDA+ù")
		# mainMenu.AppendSubMenu (subMenu,"Divers")
		mainMenu.Bind (EVT_MENU,self.onMenu)
		utis.showNVDAMenu  (mainMenu)

	def onMenu(self, evt):
		#beep(440, 20)
		ID =evt.Id
		#message ("menu ID : " + str(ID))
		# if ID == 4 : # choisir les colonnes à afficher
			# return CallAfter(self.showColumnPicker)
		if ID == 8 :
			return CallAfter(utis.showHelp)
		elif ID == 9 :
			return CallAfter(utis.toSupport, self.tbVersion)
		elif ID == 10 :
			return CallAfter(os.startfile, "http://rptools.org/thunderbird-dv.html")
		elif ID == 11 :
			lang = utis.getLang()
			return CallAfter(os.startfile, "http://www.rptools.org/Outils-DV/thunderbird-chichi-" + lang + ".html")
		elif ID == 12 : #history
			return CallAfter(showTranslatedHTML, "TB+G5-history.html")
		elif ID == 13 : # notifications
			return CallAfter(showTranslatedHTML, "notificationsG5.html")
		elif ID == 14 : # donate
			return CallAfter(os.startfile, "https://www.paypal.com/donate/?business=QQJT2CCNR66G4&no_recurring=0&item_name=Thunderbird%2Badd-on+for+NVDA++donations.+%0AMany+thanks+%21+%3B&currency_code=EUR")
	def showColumnPicker(self) :
		utis.setSpeech(False)
		#sharedVars.debugMess(self.focused, " focused ")
		o2=self.focused.parent # threadTree
		#sharedVars.debugMess(o2, " parent ")
		if  utis.getIA2Attribute(o2)  != "threadTree" : 
			CallLater (10, message, _("Please select  the message list and try again."))
			utis.setSpeech(True)
			return
		else : 
			CallLater (20, chooseCols, o2.firstChild.lastChild)
			return

	def script_clickToolBarAttachment (self,gesture = None):
		CPC=clientObject.CreatePropertyCondition
		versionTB=utis.versionTB()
		objFirstGrouping=(utis.getObjFirstGrouping(self) if utis.getObjFirstGrouping(self) else utis.getObjFirstGrouping2(self))
		if versionTB<68 :
			o = objFirstGrouping.FindAll (TreeScope_Children,CPC(UIA_ControlTypePropertyId, UIA_ToolBarControlTypeId))
			GetFirstChildElement (o.GetElement (o.Length-1)).GetCurrentPattern (10000 ).QueryInterface (IUIAutomationInvokePattern).Invoke ()
		else :
			condition1=CPC(UIA_ControlTypePropertyId, UIA_ButtonControlTypeId)
			condition2=clientObject.CreateOrCondition (CPC(30005,"Enregistrer"),CPC(30005,"Tout enregistrer"))	 #Tout enregistrer	
			o =objFirstGrouping.FindFirst (TreeScope_Children,clientObject.CreateAndCondition (condition1, condition2))
			if not o :
				message(_("No attachment to save"))
				# ne pas faire ici de gesture.send () car ctrl+alt+p peut-être défini comme un raccourci global du bureau Windows.
				return 
			o.GetCurrentPattern (10000 ).QueryInterface (IUIAutomationInvokePattern).Invoke ()
		if not getObjAttachment (self) : return gesture.send ()
	script_clickToolBarAttachment.__doc__ = _("Open attachments toolbar")
	script_clickToolBarAttachment.category = sharedVars.scriptCategory

	def getSubMenuAttachment (self,objFirstGrouping):
		menu,o  = Menu (), globalVars.focusObject
		while o and not utis.getIA2Attribute (o,"mailContent"):o=o.parent
		if not o: return False
		x =(e for e in range (o.childCount, o.childCount-16,-1)) # -5,-1
		for e in x:
			if utis.getIA2Attribute (o.getChild (e),"attachmentCount"): 
				o=o.getChild (e)
				break
		else: return False

		self.objSizeAttachment  = o
		oPrevious = o.previous
		if oPrevious.role  == controlTypes.Role.LINK :
			menu.Append (400, _("Open"))
			menu.Append(401, _("More options \tControl+alt+p"))
			return  (menu, _("attachment \"") + oPrevious.name + "\". " + o.name)
		objFirstGrouping=(utis.getObjFirstGrouping(self) if utis.getObjFirstGrouping(self) else utis.getObjFirstGrouping2(self))
		buttonAttachment = objFirstGrouping.FindAll (TreeScope_Children, CPC( UIA_ControlTypePropertyId, UIA_ButtonControlTypeId))
		while not _("attached") in o.name :o=o.previous  # ajout 
		name =o.name  # ajout 
		name = name+ " " + o.next.name  # ajout
		#name =o.previous.name
		#name = name+" "+o.name
		menu.Append (501, _("All ... \tControl+Alt+p. "))
		menu.Append (500, _("move to list alt+p"))
		if  not buttonAttachment.GetElement (buttonAttachment.Length-1).GetCurrentPropertyValue (UIA_LegacyIAccessibleStatePropertyId) &STATE_SYSTEM_PRESSED:
			return (menu,name)
		attachments  = objFirstGrouping.FindFirst(TreeScope_Children, CPC(UIA_ControlTypePropertyId, UIA_ListControlTypeId)).FindAll (TreeScope_Children, CPC(UIA_ControlTypePropertyId, UIA_ListItemControlTypeId))
		max =attachments.Length*2
		for e in range (max,0,-2 ):
			menuSingleAttachment = Menu ()
			menuSingleAttachment.Append (e+600, _("Open"))
			menuSingleAttachment.Append (e+601, _("More options"))
			menu.AppendSubMenu  (menuSingleAttachment,attachments.GetElement (e/2-1).CurrentName)
		return (menu,name)

	def getSubMenuLabels (self,labels, startIndex):
		menu = Menu ()
		#message ("getSubMenuLabel labels.Length = " + str(labels.Length))
		for labelIndex  in range (labels.Length):
			label =labels.GetElement (labelIndex)
			name =label.CurrentName
			#message ("menu label name : " + str(name) + ", labelindex = " + str(labelIndex))
			try:
				if label.GetCurrentPropertyValue (UIA_LegacyIAccessibleRolePropertyId) != ROLE_SYSTEM_LINK:
					name = name[name.index (" ")+1:]
			except : 
				#message ("Exception obtention name si pas role system_link")
				pass
			#print ("Menu name :" + str(name))
			#print ("Menu labelIndex :" + str(labelIndex))
			if name : # v 2.1.3
				menu.Append (startIndex+labelIndex,name)
		try:			
			label1=GetNextSiblingElement(GetParentElement(label))
			if label1  and "de plus" in label1.CurrentName : 
				index  =int (str (startIndex)[:len (str (startIndex))-3])-10
				menu.Append (20+index,label1.CurrentName) 
		except : pass
		return menu

# normal functions
def getObjAlerts (windowHandle): return clientObject.ElementFromHandle (windowHandle).FindAll(TreeScope_Descendants,clientObject.CreatePropertyCondition (UIA_LegacyIAccessibleRolePropertyId,ROLE_SYSTEM_ALERT))	

def getObjAlert2(pp=None) :
	try :
		#role.ALERT=138 Tag: div, états : , childCount  : 6 Chemin : role FRAME=34| i34, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i13, role-TEXTFRAME=91,  | i0, role-ALERT=138,  , IA2Attr : class : container infobar, display : flex, tag : div, xml-roles : alert,  ;
		if not pp :
			pp = utis.getPropertyPageFromFG()
		if sharedVars.debug : sharedVars.log(pp, " pp  : ", False)
		sharedVars.objLooping = True
		#| i13of 19 , role-TEXTFRAME=91,  | i0, role-ALERT=138
		o = pp.lastChild
		#if sharedVars.debug : sharedVars.log(o, " o : ", False)
		while o and o.role != controlTypes.Role.TEXTFRAME :
			#if sharedVars.debug : sharedVars.log(o, " o : ", False)
			o = o.previous
		if not o : return None
		# i0, role-ALERT=138
		#if sharedVars.debug : sharedVars.log(o.firstChild, " objet alert : ", False)
		return o.firstChild 
	finally :
		sharedVars.objLooping = False

def getMenuFromAlert (windowHandle):
	o = getObjAlert2() # getObjAlerts (windowHandle)
	if not o :return  False
	mainMenu, IDMenu =  Menu (),199

	subMenu =Menu ()
	o =o.firstChild.next # label we need 
	lblMenu = o.name
	#sharedVars.debugLog = ""	
	#if sharedVars.debug : sharedVars.log(o, " label ", False)
	while o : 
		if o.role == controlTypes.Role.BUTTON :
			#if sharedVars.debug : sharedVars.log(o, " bo ", False)
			IDMenu += 1
			itemText = o.name
			hk = o.keyboardShortcut
			subMenu.Append (IDMenu,itemText+" "+hk)
			sharedVars.menuCommands[str(IDMenu)] = o
		o = o.next

	mainMenu.AppendSubMenu (subMenu,  lblMenu)
	return mainMenu		

def alertClickButton(menuID, evt):
	#hk =	evt.GetEventObject ().GetLabelText (evt.Id).split (" ")[-1]
	sharedVars.menuCommands[str(menuID)].doAction()
	sharedVars.menuCommands = {}

def getObjAttachment (self, UIAElement =False):  
	o  = globalVars.focusObject # api.getFocusObject()
	while o and not utis.getIA2Attribute (o, "mailContent"):o=o.parent
	if not o: return False
	x =(e for e in range (o.childCount, o.childCount-5,-1))
	for e in x:
		if utis.getIA2Attribute (o.getChild (e),"attachmentSize"): 
			o=o.getChild (e)
			break
	#else: return False
	if not o: return False
	#self.objSizeAttachment  = o
	oPrevious = o.previous
	return  o
from api import  config

def headersToFile (lstHeaders) : # v 2.1.3
	#pth = config.getUserDefaultConfigPath() + u"\\addons\\thunderbird+\\Entêtes-mail.txt"
	pth =  sharedVars.oSettings.addonPath + "\\Entêtes-mail.txt"
	if lstHeaders.count("\n") < 15 :
		lstHeaders = _("To get all headers, please open the View Menu, go down to 'Headers' and then press Enter on 'All'  in the submenu. Then display the grave menu again.")
	oFile = open (pth, "w")
	if not oFile : return
	n = oFile.write(lstHeaders)
	oFile.close()
	return

def chooseCols(oBtnPicker) :
	utis.setSpeech(True)
	oBtnPicker.doAction()
	# w
	return

def showTranslatedHTML(pageName) :
	from languageHandler import getLanguage
	lang = getLanguage()
	if "fr" in lang :
		url = "https://www.rptools.org/NVDA-Thunderbird/" + pageName
	else :
		url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/" + pageName + "?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		url = url.replace("@lg", lang)
	#  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	os.startfile (url)
