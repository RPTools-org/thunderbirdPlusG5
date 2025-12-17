#-*- coding:utf-8 -*
# G5
import controlTypes
from api import getFocusObject, getForegroundObject, setNavigatorObject
from tones import beep
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, utils115 as utils, sharedVars
from utils115 import message
del sys.path[-1]
from wx import Menu, EVT_MENU, ITEM_CHECK, MenuItem,CallAfter
from core import callLater
from keyboardHandler import KeyboardInputGesture
import speech
from time import sleep
import globalVars

addonHandler.initTranslation()

# translator "Onglet" stands for "tab"
msgName = _("Tab {0} of {1} {2}")

def findCurTab(oFrame=None ) :
	# returns : oCurTab, tabIndex, tabLastIdx
	# TB115 Path : Role-FRAME| i31, Role-TOOLBAR, , IA2ID : tabs-toolbar | i0, Role-TABCONTROL, , IA2ID : tabmail-tabs
	try : # finally
		prevLooping = sharedVars.objLooping
		sharedVars.setLooping(False)
		# get frame object
		if oFrame : o = oFrame
		else : o = getForegroundObject()
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
		# if sharedVars.debug : sharedVars.log(None, _("tab not found"))
		return None, -1, -1
	finally :
		sharedVars.setLooping(prevLooping)

def  selectTab(oFrame, index) :
	#  returns True if tab is changd 
	if  not oFrame :
		oFrame = 	getForegroundObject()
	oTab , idx, lastIdx = findCurTab(oFrame)
	if not oTab or idx == -1 : # not in main window
			return False # tab not changed
	if idx ==  0 and index == 0:
		sharedVars.curTab = "main" 
		sharedVars.curFrame = "messengerWindow"
		return False # tab not changed
	oTabCtrl =  oTab.parent
	oTab = oTabCtrl.getChild(index)
	if oTab :
		oTab.doAction()
	if idx == 0 :
		sharedVars.curTab = "main" 
		sharedVars.curFrame = "messengerWindow"	
	return True			 # tab changed
def showTabMenu(appMod, obj) :
	global tabObjects, appModule
	appModule = appMod
	oTab , curIdx, lastIdx = findCurTab()
	if not oTab : return
	oTabCtrl = oTab.parent
	if lastIdx == 0 :
		callLater(100, message, _("There is only one tab open."))
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
	# sharedVars.curTab = getTabTypeFromName(oTab.name, "onMenuTab")
	tabObjects = None
	oTab.doAction()


def tabContextMenu(appMod, obj) :
	oTab , curIdx, lastIdx = findCurTab()
	if not oTab : return
	oTab.setFocus()
	CallAfter(message, _("Active tab {0} of {1} : {2}, ").format(curIdx+1, lastIdx+1, oTab.name))
	callLater(200, KeyboardInputGesture.fromName("shift+f10").send) # affiche menu contextuel

def getTabFromPropertyPage(ppID, oPP) :
	dbg = False
	if dbg : 
		sharedVars.log(oPP, "getTabFromPP : " + ppID)
		sharedVars.curFrame = "messengerWindow"
	if  ppID.startswith("mail3PaneTab") : sharedVars.curTab = "main"
	elif  ppID.startswith("mailMessageTab") : sharedVars.curTab = "messageTab"
	elif  ppID.startswith("address") : sharedVars.curTab = "sp:addressbook"
	elif  ppID.startswith("preferences") : sharedVars.curTab = "sp:preferences"
	elif  ppID.startswith("contentTabWrapper") :
		sharedVars.curTab = "sp:" + ppID
		o = oPP.firstChild
		oDoc = None
		while o :
			if o.role == controlTypes.Role.DOCUMENT :
				oDoc = o
				break
			o = o.firstChild
		# end while
		if oDoc : 
			oContainer = oDoc
			o = oDoc.parent
			if o and o.role == controlTypes.Role.INTERNALFRAME and utils.hasID(o, "messagepane") :
				if dbg : sharedVars.curTab = "message"
				return
		else :
				oContainer = oPP
		# we search an non None ID
		ID = "False"
		for o in oContainer.recursiveDescendants :
			if o.role in (controlTypes.Role.LANDMARK, controlTypes.Role.TABCONTROL,controlTypes.Role.BUTTON, controlTypes.Role.LINK) :
				ID =  str(utils.getIA2Attr(o))
				if ID != "False" and ID != "aux-nav" :
					if dbg : sharedVars.log(o, "search in oPP, ID found = " + ID)
					break

		# sharedVars.log(o, "oDoc ID=" + ID)
		match ID :
			case "categories" : # add-ons :  categories
				sharedVars.curTab = "sp:addons"  
			case "clearDownloads" : # downloads  ID : =clearDownloads BUTTON
				sharedVars.curTab = "sp:downloads"
			case "accountTreeBox" : #  ID=accountTreeBox LANDMARK
				sharedVars.curTab = "sp:accounts"
			case "other-apps" : # role LANDMARK, 
				sharedVars.curTab = "sp:addonsearch"
			case _ : # default
				sharedVars.curTab = ppID
				
def onTabSelect(oTab) :
	global msgName
	speech.cancelSpeech()
	oTabCtrl = oTab.parent
	tabCount = oTabCtrl.childCount
	curIdx = -1
	i = 0
	for t in oTabCtrl.children :
		if t.name == oTab.name :
			curIdx = i
			break
		i += 1
	# end for
	message(msgName.format(curIdx+1, tabCount, oTab.name))
	# oTab.doAction()
	
def onPropertyPageChange(oPP) :
	fo = getFocusObject()
	if not fo : return
	# sharedVars.log(fo, "onPropertyPageChange role.")
	if fo.role == controlTypes.Role.FRAME :
		setFocusTo(frame=fo, propertyPage=oPP, curTab=sharedVars.curTab)
	else : 
		# beep(440, 10)
		# setNavigatorObject(fo)
		# if controlTypes.State.FOCUSABLE in fo.states :
			# fo.setFocus()
		message(str(fo.name) + ", " + fo.role.displayString)
	
def getDocumentFromPP(oPP) :
	if not oPP.firstChild : return None
	o = oPP.firstChild
	while o :
		if o.role == controlTypes.Role.DOCUMENT :
			return o
		if o.firstChild : o = o.firstChild
	return None
def findControl(obj, role, ID="", getNextLink=False, removeURL=False)  :
	oFound = None
	for o in obj.recursiveDescendants:
		if removeURL :
			if hasattr(o, "value") and str(o.value).startswith("http") : o.value = "" 
		# sharedVars.log(o, "findControl o")
		if not oFound and o.role == role :
			if not ID : oFound = o
			elif ID and  utils.hasID(o, ID) : oFound = o
			# sharedVars.log(oFound, "findControl oFound")
		if oFound and (controlTypes.State.FOCUSABLE  in oFound.states or not getNextLink) :
			# sharedVars.log(oFound, "findControl returned oFound")
			return oFound
		# the search continues until a link in a heading
		if oFound and o.role == controlTypes.Role.LINK and o.parent.role == controlTypes.Role.HEADING :
			# sharedVars.log(o, "findControl returned o")
			return o
	# end for
	# if not oFound :
		# return None
	
	# if controlTypes.State.FOCUSABLE  in oFound.states or not getNextLink : 
		# sharedVars.log(oFound, "findControl returned oFound")
		# return oFound
	# # continue search until the next link in a heading
	# for j in range(i+1, lenDesc) : 
		# o = oDesc[j]
		# if o.role == controlTypes.Role.LINK and o.parent.role == controlTypes.Role.HEADING :
			# sharedVars.log(o, "findControl returned o")
			# return o 
	return None
					
def setFocusTo(frame, propertyPage, curTab) :
	# frame and propertyPage are objects, curTab is a string
	if curTab == "main" :
		fo = getFocusObject()
		if fo.role != controlTypes.Role.FRAME :
			return
		obj = findControl(propertyPage, controlTypes.Role.TREEVIEW, ID="folderTree")
		if obj :
			obj.setFocus()
			callLater(500, message, obj.role.displayString) 
	elif curTab == "sp:addressbook" :
		obj = getDocumentFromPP(oPP=propertyPage)
		obj = findControl(obj, controlTypes.Role.EDITABLETEXT,ID="")
		if obj :
			obj.setFocus()
	elif curTab == "sp:downloads" :
		obj = findControl(propertyPage, controlTypes.Role.LIST, "msgDownloadsRichListBox")
		if obj :
			oCurTab, tabIndex, tabLastIdx = findCurTab(frame)
			obj.setFocus()
			callLater(50, message, str(oCurTab.name))
	elif curTab == "sp:addons" :
		obj = getDocumentFromPP(oPP=propertyPage)
		obj = findControl(obj, controlTypes.Role.TABCONTROL, "categories")
		if obj :
			obj.getChild(1).setFocus()
	elif curTab == "sp:accounts" :
		obj = getDocumentFromPP(oPP=propertyPage)
		obj = findControl(obj, controlTypes.Role.TREEVIEW, "accounttree")
		if obj :
			oCurTab, tabIndex, tabLastIdx = findCurTab(frame)
			obj.setFocus()
			callLater(500, message, str(oCurTab.name))
	elif curTab == "sp:addonsearch" :
		obj = findControl(propertyPage, controlTypes.Role.SECTION, "pjax-results", getNextLink=True, removeURL=True)
		sharedVars.log(obj, "obj after findControl")
		if obj :
			obj.value = ""
			if obj.firstChild :
				o = obj.firstChild
				if hasattr(o, "value") : o.value = ""
			utis.setSpeech(False)
			obj.setFocus()
			utis.setSpeech(True)
			speech.cancelSpeech()
			message("{}, {}".format(obj.name, obj.parent.role.displayString))
		else : # no search  results
			KeyboardInputGesture.fromName("shift+f6").send()
	elif curTab == "sp:accounts" :
		obj = getDocumentFromPP(oPP=propertyPage)
		obj = findControl(obj, controlTypes.Role.TREEVIEW, "accounttree")
		if obj :
			oCurTab, tabIndex, tabLastIdx = findCurTab(frame)
			obj.setFocus()
			callLater(500, message, str(oCurTab.name)) 
	elif curTab == "sp:preferences" :
		obj = getDocumentFromPP(oPP=propertyPage)
		obj = findControl(obj, controlTypes.Role.EDITABLETEXT, "")
		if obj :
			obj.setFocus()
