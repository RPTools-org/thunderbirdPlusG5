#-*- coding:utf-8 -*

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, utils115 as utils, sharedVars
from api import getForegroundObject
del sys.path[-1]
addonHandler.initTranslation()
from ui import message
from wx import Menu, EVT_MENU, ITEM_CHECK, MenuItem,CallAfter,CallLater
from keyboardHandler import KeyboardInputGesture
import speech
from time import sleep
import globalVars

# translator "Onglet" stands for "tab"
msgName = _("Tab {0} of {1} {2}")

def getTabType(nm, idx, oFocused) :
	# Translator : in getTabType(), the strings come  from the main window title bar when a tab is active. You have to copy   them from the title bar of  Thunderbird in your language.
	#  Translator : "Chargement en" vient de "Chargement en cours", "Accueil"  vient aussi du nom de l'onglet 
	if not nm or _("Loading") in nm or _("Home -") in nm:
		return "loading"
	if idx == 0 : tabType = "main"
	else : tabType = getMainTabType(idx, oFocused)
	if tabType != "sp:" :
		return tabType

		# Translator :  title bar when Address book tab is active. Must be the same as in the user interface of TB
	if _("Address Bo") in nm :
		tabType = "sp:addressbook"
		# Translators: title bar when Saved tab is active. must be the same as in  the user interface 
	elif _("Saved Files") in nm :
		tabType = "sp:downloads"
		# 2022-12-96 : paramètres des comptes monté devant paramètres pour corriger erreur
		# Translators: title bar when Account Settings tab is active.must be the same as in  the user interface 
	elif _("Account Settings") in nm :
		tabType = "sp:accounts"
		# Translators: title bar when Settings tab is active.must be the same as in  the user interface 
	elif _("Settings") in nm :
		tabType = "sp:preferences"
		# Translators: titlebar when addons manager tab is active.must be the same as in  the user interface 
	elif _("Add-ons Manager") in nm :
		tabType = "sp:addons"
		# Translators: Title bar when  New account creation tab is active. must be the same as in  the user interface 
	elif _("Account Setup") in nm :
		tabType = "sp:newaccount"
		#Translators: title bar when addons search results tab is active.  
	elif _("Add-ons for Thunderbird") in nm: 
		tabType = "sp:addonsearch"
	elif "chichi" in nm: 
		tabType = "sp:chichi"
	else :
		tabType = "sp:"
	# if sharedVars.debug :sharedVars.log(None, " sortie de getTabType : " + tabType + ", " + nm)
	return tabType

# def getMainTabType(tabIdx, oFocus) :
	# # if tabIdx > 0
	# if not oFocus :  oFocus = globalVars.foregroundObject
	# if   oFocus.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.TABLEROW) :
		# return "main"
	# # determine if a folderTree exists in the page
	# try :
		# prevLooping = sharedVars.objLooping
		# sharedVars.objLooping = True
		# if  oFocus.role != controlTypes.Role.FRAME : 
			# while oFocus :
				# if oFocus.role == controlTypes.Role.FRAME :
					# break
				# oFocus = oFocus.parent
		# if not oFocus : return "frameNotFound"
		# if oFocus.role != controlTypes.Role.FRAME :
			# return "frameNotFound"
		# # search for grouping
		# try : o = oFocus.lastChild
		# except : return "frameLastChildNotFound"
		# while o :
			# if o.role == controlTypes.Role.GROUPING :
				# break
			# o = o.previous
		# if not o : return "groupingNotFound"
		# try :
			# o = o.firstChild # propertypage
		# except :
			# return "propertyPageNotFound"
		# # in main tab, path : : role FRAME=34| i31, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i1, role-TREEVIEW=20, , 
		# # in message Tab : role.INTERNALFRAME=115, IA2ID : messagepane path  : role FRAME=34| i31, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i10, role-INTERNALFRAME=115, , IA2ID : messagepane 
		# # search Treeview or internalframe
		# o = o.firstChild
		# while o :
			# if o.role == controlTypes.Role.TREEVIEW :
				# return "main"
			# if o.role == controlTypes.Role.INTERNALFRAME :
				# if str(utis.getIA2Attribute(o)) == "messagepane" :
					# return "message"
			# o = o.next
		# return "treeNotFound"
	# finally :
		# sharedVars.objLooping = prevLooping
		# if sharedVars.debug : sharedVars.log(o, u"doit être tabToolbar")

def getMainTabType(tabIdx, oFocus) :
	if  oFocus and  oFocus.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.TABLEROW) :
		return "main"
	# determine if if property page is offscreen or not
	try :
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# sharedVars.log(sharedVars.oCurFrame, "mainTabType fg ")
		# search for grouping : level 1,  46 of 49, Role.GROUPING, IA2ID : tabpanelcontainer Tag: tabpanels, States : , childCount  : 3 Path : Role-FRAME| i46, Role-GROUPING, , IA2ID : tabpanelcontainer , IA2Attr : display : -moz-deck, class : plain, tag : tabpanels, id : tabpanelcontainer, , Actions : click ancestor,  ;
		try : o = sharedVars.oCurFrame.getChild(45)
		except : return "sp:no45"
		while o :
			if o.role == controlTypes.Role.GROUPING :
				break
			o = o.next
		if not o : return "sp:"
		# search  level 2,   0 of 3, Role.PROPERTYPAGE, IA2ID : mailContent Tag: box, States : , OFFSCREEN, childCount  : 5 Path : Role-FRAME| i46, Role-GROUPING, , IA2ID : tabpanelcontainer | i0, Role-PROPERTYPAGE, , IA2ID : mailContent , IA2Attr : display : -moz-box, id : mailContent, tag : box, , Actions : click ancestor,  ;
		# we are on the main Tab if property page  is not offscreen
		try :
			o = o.firstChild # propertypage
		except : return "propertyPageNotFound"
		if controlTypes.State.OFFSCREEN not in o.states :
			# in main tab, path : : role FRAME=34| i31, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i1, role-TREEVIEW=20, , 
			# in message Tab : role.INTERNALFRAME=115, IA2ID : messagepane path  : role FRAME=34| i31, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i10, role-INTERNALFRAME=115, , IA2ID : messagepane 
			# search Treeview or internalframe
			o = o.firstChild
			while o :
				if o.role == controlTypes.Role.TREEVIEW :
					return "main"
				if o.role == controlTypes.Role.INTERNALFRAME :
					if str(utis.getIA2Attribute(o)) == "messagepane" :
						return "message"
				o = o.next
		return "sp:"
	finally :
		sharedVars.objLooping = prevLooping
		# if sharedVars.debug : sharedVars.log(o, u"doit être tabToolbar")

def findCurTab(oFrame=None ) :
	# returns : oCurtab, tabIndex, tabLastIdx
	# TB115 Path : Role-FRAME| i31, Role-TOOLBAR, , IA2ID : tabs-toolbar | i0, Role-TABCONTROL, , IA2ID : tabmail-tabs
	try :
		sharedVars.setLooping(True)
			# get frame object
		o = getForegroundObject()
		# sharedVars.debugLog = ""
		# get | i31, Role-TOOLBAR, , IA2ID : tabs-toolbar 
		o = utils.findChildByRoleID(o, controlTypes.Role.TOOLBAR, "tabs-toolbar", 30) # 40 is startIdx
		if not o : return None, -1, -1
		# if sharedVars.debug : sharedVars.log(o, " tabstool bar 35 ? ")
		# | i0, Role-TABCONTROL, , IA2ID : tabmail-tabs
		o = utils.findChildByRoleID(o, controlTypes.Role.TABCONTROL, "tabmail-tabs")
		if not o : return None, -1, -1
		tabLastIdx = o.childCount - 1
		# if sharedVars.debug : sharedVars.log(o, u"tabControl  trouvé")
		# role.TAB=22 Tag: tab, ertats : , SELECTED, SELECTABLE, 
		i = 0 
		pos = -1 
		o = o.firstChild # firstTab
		while o :
			# if sharedVars.debug : sharedVars.log(o, "tab " + str(i))
			if o.role == controlTypes.Role.TAB and controlTypes.State.SELECTED in o.states :
				pos = i
				# if sharedVars.debug : sharedVars.log(o, _("tab Sélectionné"))
				break
			i += 1
			o = o.next
		if o : return o, pos, tabLastIdx
		if sharedVars.debug : sharedVars.log(None, _("tab not found"))
		return None, -1, -1
	finally :
		sharedVars.setLooping(False)
def getTabCount(oFrame=None) :
	# v5 path  : role FRAME=34| i41, role-TOOLBAR=35, , IA2ID : tabs-toolbar | i1, role-TABCONTROL=23, , IA2ID : tabmail-tabs , IA2Attr : id : tabmail-tabs, display : -moz-box, child-item-count : 1, tag : tabs, , Actions : click ancestor,  ;  
	try :
		sharedVars.setLooping(True)
		# if oFrame and oFrame.role == controlTypes.Role.FRAME: o = oFrame 
		# else : o = globalVars.foregroundObject 
		o = SharedVars.oCurFrame
		# sharedVars.debugLog = ""
		# | i41, role-TOOLBAR=35, , IA2ID : tabs-toolbar 
		# replaced by the line vbelow : o = utis.findChildByIDRev
		(o, "tabs-toolbar")
		o = utis.findChildByRoleID(o, "tabs-toolbar", controlTypes.Role.TOOLBAR, 40)
		# if sharedVars.debug : sharedVars.log(o, " tabstool bar 35 ? ")
		# | i1, role-TABCONTROL=23, , IA2ID : tabmail-tabs 
		o = utis.findChildByID(o, "tabmail-tabs") # if spacesbar is displayed, the child is noy yhe same 
		if not o : return 0
		return o.childCount
	finally :
		sharedVars.setLooping(False)

def activateTab(appMod,obj, newTabIdx) :
	global msgName
	oTab , idx, lastIdx = findCurTab(obj)
	if not oTab : return False
	oTabCtrl = oTab.parent
	# if sharedVars.debug : sharedVars.log(oTab, "ancien tab : " + str(idx))
	if newTabIdx > lastIdx : 
		newTabIdx = lastIdx   
	activate   = (newTabIdx != idx)
	oTab = oTabCtrl.getChild(newTabIdx)
	appMod.curTab = sharedVars.curTab = getTabType(oTab.name, newTabIdx, obj)
	if activate  : 
		message(msgName.format(newTabIdx+1, lastIdx+1, "")) # oTab.name))
		sleep(.5)
		oTab.doAction()
	else :
		message(msgName.format(newTabIdx+1, lastIdx+1, "")) # oTab.name))
	return True
def changeTab(appMod, obj, direct) : # control+tab
	global msgName
	oTab , idx, lastIdx = findCurTab(obj)
	if not oTab : return False
	#if sharedVars.debug : sharedVars.log(oTab, "ancien tab : " + str(idx) + "direction : " + str(direct))
	oTabCtrl = oTab.parent
	#if sharedVars.debug : sharedVars.log(oTabCtrl, "lastIdx : " + str(lastIdx))
	if direct == 1 : 
		if idx < lastIdx : idx+= 1
		else : idx = 0
	else : 
		if idx > 0  : idx -= 1
		else : idx = lastIdx
	oTab = oTabCtrl.getChild(idx)
	appMod.curTab = sharedVars.curTab = getTabType(oTab.name, idx, obj)
	message(msgName.format(idx+1, lastIdx+1, "")) # oTab.name))
	sleep(.5)
	oTab.doAction() # selects the new tab
	return True
appModule = tabObjects = None


def showTabMenu(appMod, obj) :
	global tabObjects, appModule
	appModule = appMod
	oTab , curIdx, lastIdx = findCurTab(obj)
	if not oTab : return
	oTabCtrl = oTab.parent
	if lastIdx == 0 :
		CallLater(100, message, _("There is only one tab open."))
		return
	tabObjects = []
	mainMenu = Menu ()
	i = 0
	for e in oTabCtrl.children :
		menuitem =MenuItem (mainMenu,i, "{0}\tcontrol+{1}".format(e.name, i+1 if i !=10 else 0), kind =ITEM_CHECK)
		mainMenu.AppendItem (menuitem)
		tabObjects.append(e)
		if i == curIdx :
			menuitem.Enable (False)
			# superflu ->  menuitem.Check (True)
		i += 1

	mainMenu.Bind (EVT_MENU, onMenuTabs)
	utis.showNVDAMenu (mainMenu)

def onMenuTabs(evt):
	global tabObjects, appModule
	idx = int(evt.Id)
	oTab = tabObjects[idx]
	#message(u"Sélection de l'onglet " + tabObjects[idx].name)
	appModule.curTab = sharedVars.curTab = getTabType(oTab.name, idx, globalVars.focusObject)
	tabObjects = None
	appModule = None
	oTab.doAction()

def tabContextMenu(appMod, obj) :
	oTab , curIdx, lastIdx = findCurTab(obj)
	if not oTab : return
	oTab.setFocus()
	CallAfter(message, _("Active tab {0} of {1} : {2}, ").format(curIdx+1, lastIdx+1, oTab.name))
	CallLater(200, KeyboardInputGesture.fromName("shift+f10").send) # affiche menu contextuel

