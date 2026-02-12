# ThunderbirdPlusG5 for Thunderbird 115+

from nvdaBuiltin.appModules import thunderbird
from time import time, sleep
from datetime import datetime
from NVDAObjects.IAccessible import IAccessible
from tones import beep
import controlTypes
import api
import ui
import scriptHandler
import winUser
import speech
import gui
import wx
from core import callLater
import globalCommands, globalVars	
import config
from re import compile,IGNORECASE

# shared modules import
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import utis, sharedVars, utils115 as utils # , sendInput
from utils115 import message
import  langUtils
import textDialog
# dbg = sharedVars.log
# from  py3compatibility import *
# from  py3compatibility import utis._unicode
del sys.path[-1]

import api

sharedVars.scriptCategory = _curAddon.manifest['summary']

# Extension modules import
from . import messengerWindow, msgComposeWindow # , addressbookWindow
from scriptHandler import getLastScriptRepeatCount

addonHandler.initTranslation()

def sayTreeItem(fo=None) :
	try : # finally 
		done = False
		if not fo :
			fo = api.getFocusObject()
		ID = str(utils.getIA2Attr(fo))
		if   ID.startswith("threadTree-"):
			roleName = controlTypes.Role.TABLE.displayString
		elif utils.isFolderTreeItem(fo, ID) :
			roleName = controlTypes.Role.TREEVIEW.displayString
		else :
			roleName = fo.role.displayString
		utis.setSpeech(True)
		done = True
		message("{}, {}, {}".format(utis.getWinTitle(appName=False), roleName, fo.name))
	finally :
		sharedVars.mainTabInit = True
		sharedVars.starting = False
		if not done :
			utis.setSpeech(True)

def applyFocusModeFromThreadTree(focusMode) :
			# we are on role = textFrame and id=threadTree
	if focusMode == 1 : # last message
		gest = "end"
	elif focusMode == 2 : # first  message
		gest = "home"			
	elif focusMode == 3 : # first  unread message
		gest = "n"
	else :
		return utis.setSpeech(True)
	KeyboardInputGesture.fromName("f6").send()
	sleep(0.1)
	KeyboardInputGesture.fromName(gest).send()
	callLater(100, sayTreeItem)

def applyFocusMode() :
	# from script_Grave
	try : # finally
		focusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
		if focusMode == 0 : return
		if focusMode == 4 : # folderTree
			oTree = utils.getFolderTreeFromFG()
			if oTree : oTree.setFocus()
			return
		# else threadTree
		oTree = utils.getThreadTreeFromFG()
		if not oTree : 
			return
		oTree = utils.getThreadTreeListOrTable(oTree)
		oTree.setFocus()

		if focusMode == 1 : # last message
			gest = "end"
		elif focusMode == 2 : # first  message
			gest = "home"
		elif focusMode == 3 : # first  unread message
				gest = "n"
		callLater(50, KeyboardInputGesture.fromName(gest).send)
	finally :
		speech.setSpeechMode(speech.SpeechMode.talk)

# def handleFirstFocus(oTreeItem, focusMode) :
	# ID = str(utils.getIA2Attr(oTreeItem))
	# if ID.startswith("threadTree-") :
		# applyFocusModeFromThreadTree(focusMode)
	# elif utils.isFolderTreeItem(oTreeItem, ID) :
		# role = controlTypes.Role.TREEVIEW
		# applyFocusModeFromFolderTree(focusMode)

def processTrees(oFolders, oThreads) :
	if sharedVars.mainTabInit : return
	sharedVars.mainTabInit= True
	sharedVars.starting = False
	onStartupAction  = sharedVars.oSettings.getOption("messengerWindow","onStartupAction", kind="i")
	match onStartupAction :
		case 0 : # do nothing
			return
		case 1 : # apply option below
			focusMode  = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
		case 2 : # Show All inboxes menu
			callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=False)
		case 3 : # Show all unread inboxes menu
			callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=True)
		case 4 : # Show All unread folders menu
			wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)
		case 5 : # Show all folders menu 
			wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)

class ListTreeView(IAccessible) :
	def initOverlayClass (self):
		self.bindGesture ("kb:f", "goFilterBar")
	def script_goFilterBar(self, gesture) :
		if sharedVars.curTab != "main" : return gesture.send() 
		KeyboardInputGesture.fromName ("shift+control+k").send() 

class QuickFilterBar(IAccessible) :
	def initOverlayClass (self):
		self.bindGesture ("kb:downArrow", "goMessageList")
	def script_goMessageList(self, gesture) :
		if sharedVars.curTab != "main" : return gesture.send() 
		KeyboardInputGesture.fromName ("f6").send() 


class TabAddons(IAccessible) :
	def initOverlayClass (self):
		self.bindGesture ("kb:enter", "validateEdit")
	def script_validateEdit(self, gesture) :
		gesture.send()
		ParentPP  = utils.findParentByRole(self, controlTypes.Role.PROPERTYPAGE)
		callLater(200, self.waitForAddonSearchFrame, self.value + " :: ", ppStart=parentPP) 

	def waitForAddonSearchFrame(self, titleStart, ppStart) :
		# we are on an editabletext
		title = utis.getWinTitle()
		if title.startswith(titleStart) :
			sharedVars.curTab = "sp:addonsearch"
			pp =  utils.getActivePropertyPage(oFrame=None, ppExcluded=ppStart,   debug=False)
			wx.CallAfter(messengerWindow.tabs.setFocusTo, frame=None, propertyPage=pp, curTab=sharedVars.curTab)
		else :
			callLater(200, self.waitForAddonSearchFrame, titleStart, ppStart)

class AppModule(thunderbird.AppModule):
	timer = None
	counter = 0

	def __init__(self, *args, **kwargs):
		super(thunderbird.AppModule, self).__init__(*args, **kwargs)
		self.logEvents = False
		# Thunderbird+G5
		if self.logEvents : sharedVars.logte("Thunderbird+G5 _init")
		utis.disableOvl(True) # set objLooping = True
		speech.cancelSpeech()
		self.disabMode = 0
		# self.columnID= []
		sharedVars.initSettingsMenu(self) # then use  sharedVars.oSettings.*
		# initQuotenav  will be run at first use of quote Navigator >sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		# all  self.regExp moved to sharedVars
		k =  utis.gestureFromScanCode(41)
		self.bindGesture("kb:control+" + k, "showContextMenu") # 41 is the scancode of the key above Tab
		self.bindGesture("kb:shift+" + k,  "showOptionMenu") 
		self.bindGesture("kb:" + k, "sharedGrave") # 41 is the scancode of the key above Tab
		globalVars.TBPropertyPage = None
		globalVars.TBFolderTree = None
		globalVars.TBThreadTree = None
		globalVars.TBThreadPane = None
		globalVars.TBFolderTree = None
		sharedVars.curFrame = "unknown"
		sharedVars.curTab = "unknown"
		self.startupAction = sharedVars.oSettings.getOption("messengerWindow","onStartupAction", kind="i") 
		self.startupFocusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i") 
		if self.logEvents : 
				sharedVars.logte("Call of self.tbStartup")
				sleep(0.2)
		callLater(1500, self.tbStartup)

	# ====
	def waitForTree(self, oFrame) :
		dbg = False
		if sharedVars.loopCount == 10 : 
			sharedVars.loopCount = 0
			sharedVars.error(None, "waitForTree timeout", sound=dbg)
			return self.endStartup()
		frame = api.getForegroundObject()
		if sharedVars.loopCount == 1 : 
			# select first tab, only  if it is not already selected
			if messengerWindow.tabs.selectTab(oFrame, 0) :
				# tab has changed
				utis.setSpeech(True)
				speech.cancelSpeech()
				message(oFrame.name)
				utis.setSpeech(False)
			if dbg : sharedVars.logte("tb startup, first tab selected curTab=" + sharedVars.curTab)
		elif sharedVars.loopCount > 1 and sharedVars.curTab == "main" : 
			if dbg : beep(350, 40)
			if dbg : sharedVars.log(frame, "waitForTree oFrame")
			pp = folderTree = threadTree = None
			oGrouping = utils.getMainGrouping(frame, True)
			if oGrouping : 
				pp = utils.getPropertyPage(frame, debug=dbg)
			if pp : 
				folderTree = utils.getFolderTreeFromPP(oPP=pp, debug=dbg)
				if dbg : sharedVars.log(folderTree, "waitForTree after getFolderTreeFromPP")  
				threadTree = utils.getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, oPP=pp, debug=dbg)
			else : # pp is None
				dbg = True
			if dbg : 
				sharedVars.logte("waitForTree loppCount".format(sharedVars.loopCount))
				sharedVars.log(pp, "waitForTree, propertyPage")
				sharedVars.log(folderTree, "waitForTree, folderTree") 
				sharedVars.log(threadTree, "waitForTree, threadTree")

			if folderTree and threadTree :
				return self.processTrees(oFrame, folderTree, threadTree)
		sharedVars.loopCount += 1	
		callLater(200, self.waitForTree, oFrame)

	def processTrees(self, oFrame, oFolders, oThreads) :
		match self.startupAction :
			case 0 : # do nothing
				return self.endStartup()
			case 1 : # apply option below
				focusMode = self.startupFocusMode
				if focusMode in (1, 2) : #skip to last message in threadTree or firstMessage
					oThreads.setFocus()
					# applyFocusModeFromThreadTree restores speech
					applyFocusModeFromThreadTree(focusMode)
				elif focusMode == 3 : # skip to next unread message
					callLater(100, KeyboardInputGesture.fromName("n").send)
				elif focusMode == 4 : # skip to folderTree
					self.endStartup()
					oFolders.setFocus()
					return
			case 2 : # Show All inboxes menu
				callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=False)
			case 3 : # Show all unread inboxes menu
				callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=True)
			case 4 : # Show All unread folders menu
				wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)
			case 5 : # Show all folders menu 
				wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)
		self.endStartup()

	def endStartup(self) :
		sharedVars.starting = False
		sharedVars.mainTabInit = True 
		sharedVars.objLooping = False
		utis.setSpeech(True)

	def tbStartup(self) :
		dbg = False
		oFocused = api.getFocusObject()
		if self.logEvents : sharedVars.log(oFocused, "tbStartup oFocused, curTab=" + sharedVars.curTab) 
		# # if oFocused.role !=  controlTypes.Role.FRAME :
			# return
		# message(controlTypes.State.BUSY.displayString)
		# if sharedVars.curFrame != "unknown" and sharedVars.curTab != "unknown" :
			# return

		utis.setSpeech(False)
		if dbg : sharedVars.debugLog = "Start of Thunderbird+G5\n"
		
		# sharedVars.logte("Before first waitForTree")
		sharedVars.starting = True
		sharedVars.loopCount = 1
		oFrame = api.getForegroundObject()
		callLater(300, self.waitForTree, oFrame)  

	# ====
	def initTimer(self):
		if self.timer is not None:
			self.timer.Stop()
			self.timer = None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if sharedVars.objLooping  or self.disabMode == 1 : return
		role = obj.role
		if role == controlTypes.Role.DOCUMENT  and  controlTypes.State.EDITABLE in obj.states :
			sharedVars.oEditing = obj ; sharedVars.curFrame = "msgcomposeWindow" ; sharedVars.curTab = "comp"
			return
		# reduce verbosity
		if role == controlTypes.Role.GROUPING : obj.name = "" ; return 
		
		ID = str(utils.getIA2Attr(obj))
		if role == controlTypes.Role.FRAME : 
			sharedVars.curWinTitle = obj.name
			return # deactivated since  2025.08.27 > m essengerWindow.tabs.setCurFrameTab(obj)
		# if role == controlTypes.Role.PROPERTYPAGE :
			# sharedVars.logte("Overlay, curTab:{}, curFrame: {}, title: {}".format(sharedVars.curTab, sharedVars.curFrame, obj.name))
		
		if role == controlTypes.Role.DOCUMENT and sharedVars.curTab in ("main", "message") :
			if obj.name : sharedVars.curWinTitle = obj.name
			obj.name = ""
		#  list of messages 			
		try :
			if  role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) and utils.hasID(obj.parent.parent, "threadTree") :
				clsList.insert(0, ListTreeView)
		except :
			pass
			return
		if role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) :
			if ID.startswith("threadTree-row") :
				# sharedVars.logte(" Overlay:" + obj.name)
				sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "main"
				clsList.insert(0, messengerWindow.messageListItem.MessageListItem)
				return
			if role == controlTypes.Role.TREEVIEWITEM and utils.isFolderTreeItem(obj, ID) :
				clsList.insert(0, messengerWindow.folderTreeItem.FolderTreeItem)
				sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "main"
				return
		# quick filter bar
		if role ==  controlTypes.Role.TOGGLEBUTTON and ID.startswith("qfb-") :
			clsList.insert (0, QuickFilterBar); return
		# spellCheck dialog
		if ID.startswith("ReplaceWordInput") or (role == controlTypes.Role.LISTITEM and utils.hasID(obj.parent, "SuggestedList")) :
			clsList.insert (0,msgComposeWindow.spellCheckDlg.SpellCheckDlg); return
			return
	# special tabs documents 
		if sharedVars.TBMajor < 115 : sharedVars.TBMajor = utis.TBMajor()

		if sharedVars.curTab == "sp:addressbook" :
			if not  sharedVars.noAddressBook :  # and role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.BUTTON, controlTypes.Role.EDITABLETEXT) :
				if sharedVars.TBMajor < 128 :  clsList.insert(0, messengerWindow.tabAddressBook.AddressBook115)
				else : clsList.insert(0, messengerWindow.tabAddressBook.AddressBook)

		if sharedVars.curTab == "sp:addons" :
			if role == controlTypes.Role.EDITABLETEXT :
				clsList.insert (0, TabAddons)

	def event_foreground(self, obj,nextHandler):
		role = obj.role
		if self.logEvents : sharedVars.log(obj, "* Event foreground start :" )
		if role == controlTypes.Role.FRAME and  sharedVars.replyTo :
			sharedVars.replyTo = False
			speech.setSpeechMode(speech.SpeechMode.talk)			
			msgComposeWindow.msgComposeWindow.announceFildTo(obj)
			return # nextHandler()
		# set context  
		# if not sharedVars.starting and role == controlTypes.Role.FRAME :
		if role == controlTypes.Role.FRAME :
			if obj.windowClassName == "MozillaDialogClass" :
				ID = str(utils.getIA2Attr(obj.firstChild))
				if ID == "MisspelledWordLabel" :
					sharedVars.curFrame = sharedVars.curTab = "spellcheckDlg"
				# filterRules
				elif utils.hasID(obj.firstChild, "filterNameBox") :
					sharedVars.curFrame = sharedVars.curTab = "filterRules"
				return nextHandler()
			ID = str(utils.getIA2Attr(obj))
			childCount = obj.childCount
			# sharedVars.log(obj, "event_foreground, childCount=" + str(childCount))
			if childCount == 0 :
				return nextHandler()
			elif childCount < 2 :
				# activities
				if utils.hasID(obj.firstChild, "activityContainer") :
					sharedVars.curFrame = sharedVars.curTab = "activity"
				return nextHandler()
			# separate message reading window : 6 children
			elif childCount < 7 :
				o = utils.findChildByRoleID(obj, controlTypes.Role.INTERNALFRAME, "messageBrowser", 3)
				if o :
					sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab =  "message" 
				return nextHandler()
			# compose window : 14 children
			elif childCount < 15 :
				o = utils.findChildByRoleID(obj,controlTypes.Role.POPUPMENU, ID="msgComposeContext", startIdx=1)
				if o :
					sharedVars.curTab = "comp" ; sharedVars.curFrame="msgcomposeWindow" 
				return nextHandler()
			# filterList
			elif childCount < 20 : 
				if utils.hasID(obj.getChild(1), "serverMenu") :
					sharedVars.curFrame = sharedVars.curTab = "filterlist"
				return nextHandler()
			# sharedVars.logte("event_foreground, First Grouping and descendants\n")
			oGrouping = utils.getMainGrouping(obj, False)
			if not oGrouping :  # we are not in main window
				utils.setFontextFromFirstID(obj)
				return nextHandler()
			# sharedVars.log(oGrouping, "event_foreground, After call of getFirstGrouping")
			# sharedVars.logte("* List of in Screen property pages")
			curPPID = ""
			curPP = None
			for c in oGrouping.children :
				if c.role == controlTypes.Role.PROPERTYPAGE :
					ppID = str(utils.getIA2Attr(c))
					if controlTypes.State.OFFSCREEN not in c.states :
						curPPID = ppID
						curPP = c
						# sharedVars.log(c, "_foreground current ppID" + ppID) 
					if ppID == "mail3PaneTab" :
						globalVars.TBPropertyPage = c
						# sharedVars.log(c, "stored in globalVars.PropertyPage")
						# sharedVars.log(c, "pp")
						# sharedVars.log(c.firstChild, "pp.firstChild")

			folderTree = utils.getFolderTreeFromPP(globalVars.TBPropertyPage, debug=False)
			# sharedVars.log(globalVars.TBFolderTree, "globalVars.TBFolderTree")
			threadTree = utils.getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, oPP=globalVars.TBPropertyPage, debug=False)
			# sharedVars.log(globalVars.TBThreadTree, "globalVars.TBThreadTree")
			sharedVars.curFrame = "messengerWindow"
			messengerWindow.tabs.getTabFromPropertyPage(curPPID, curPP)
			return
		if role == controlTypes.Role.DIALOG :
			if "|dlg" not  in sharedVars.curFrame : sharedVars.curFrame += "|dlg"
			# sharedVars.log(obj, "Dialog, curframe = " +  sharedVars.curFrame) 
		elif role == controlTypes.Role.FRAME :
			sharedVars.curFrame = sharedVars.curFrame.replace("|dlg", "")
			# sharedVars.log(obj, "FRAME, curframe = " +  sharedVars.curFrame) 
		nextHandler()


	def event_gainFocus (self,obj,nextHandler):
		if self.logEvents : sharedVars.log(obj, "Event gainFocus start: ")
		if sharedVars.speechOff :
			speech.setSpeechMode(speech.SpeechMode.talk)
			sharedVars.speechOff = False
		if  sharedVars.curFrame == "msgcomposeWindow" :
			return nextHandler()
		role = obj.role
		if sharedVars.delPressed and role == controlTypes.Role.POPUPMENU and  utils.hasID(obj, "mailContext") :
			sharedVars.delPressed = False
			wx.CallAfter(activateMenuItem, obj, "navContext-delete")
			return nextHandler()

		# if sharedVars.nPressed : 
			# sharedVars.nPressed = False
			# if role == controlTypes.Role.TABLE :
				# callLater(100, self.focusMessageItem, "gainFocus", time(), obj)
			# return nextHandler()
		# if self.disabMode == 3 : return nextHandler()
		# api.setNavigatorObject(obj) # 2311.12.08
		if sharedVars.menuClosing and role == controlTypes.Role.TREEVIEWITEM :
			sharedVars.menuClosing = False
			utis.setSpeech(True)
		# if sharedVars.TBMajor > 135 and sharedVars.curTab == "main" and role in  (controlTypes.Role.LIST, controlTypes.Role.TABLE) :
			# callLater(100, self.focusMessageItem, "gainFocus", time())
			# return nextHandler()

		if  role == controlTypes.Role.UNKNOWN :
			if obj.parent and obj.parent.role in(controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) :
				# beep(100, 10)
				self.initTimer()
				self.timer = callLater(300, KeyboardInputGesture.fromName("control+space").send)
			return nextHandler()
		elif sharedVars.msgOpened and role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in obj.states :
			speech.cancelSpeech()
			sharedVars.msgOpened = False
			sharedVars.curTab = "message"
			if not sharedVars.oQuoteNav.translate :
				return nextHandler()
			else :
				return wx.CallAfter(sharedVars.oQuoteNav.readMail, obj, obj, rev=False, spkMode=1) # spkMode=1 : with utils.sayLongText,  =10 with ui.message
		if sharedVars.curTab == "sp:addressbook" and sharedVars.TBMajor > 127 :
			messengerWindow.tabAddressBook.abGainFocus(obj)

		nextHandler()
		
	def event_focusEntered (self,obj,nextHandler):
		if self.logEvents : sharedVars.log(obj, "Event focusEntered start: ")
		role, ID  = obj.role, str(utils.getIA2Attr(obj))
		if  sharedVars.curFrame == "msgcomposeWindow" and ID == "msgIdentity" :
			return #  No nextHandler()
			
		# sharedVars.log(obj, "focusEntered")
		if role == controlTypes.Role.GROUPING and ID == "tabpanelcontainer" :
			globalVars.TBGrouping = obj
			return nextHandler()
		if role == controlTypes.Role.SECTION and ID == "threadPane" :
			globalVars.TBThreadPane = obj
			return nextHandler()
		if role == controlTypes.Role.TREEVIEW and ID == "folderTree" : 
			globalVars.TBFolderTree = obj
			if sharedVars.TTnoFolderName : obj.name = "" ; globalVars.foregroundObject.name  = ""
			return nextHandler()		
		if role == controlTypes.Role.TEXTFRAME and ID == "threadTree" :
			globalVars.TBThreadTree = obj
		#   silencify threadTree list or table
		if sharedVars.curTab == "main"  and role in  (controlTypes.Role.LIST, controlTypes.Role.TABLE, controlTypes.Role.TREEVIEW) :
			speech.cancelSpeech()
			if sharedVars.TTnoFolderName  and hasattr(obj, "name") : 
				obj.name = ""
		if not sharedVars.oSettings.getOption("deactiv", "TTnoFilterSnd") and ID == "threadTree" : 
			if hasFilter(obj, ID) : 
				# beep(440, 10)
				utis.playSound("filter")
		nextHandler()

	def focusMessageItem(self, context, startTime, oFocus=None) :
		# beep(700, 100)
		return
		if not oFocus :
			o =  api.getFocusObject()
		else :
			o = oFocus
		if o.role in   (controlTypes.Role.LIST, controlTypes.Role.TABLE) :
			# beep(700, 40)
			# sharedVars.logte(context  + " : " + now.strftime("%H:%M:%S.%f")[:-4])
			# prevSpeak = config.conf["keyboard"]["speakTypedCharacters"]
			# config.conf["keyboard"]["speakTypedCharacters"] = False
			speech.cancelSpeech()
			speech.setSpeechMode(speech.SpeechMode.off)
			KeyboardInputGesture.fromName("control+space").send()
			# sleep(0.02)
			api.processPendingEvents()
			o = api.getFocusObject()
			KeyboardInputGesture.fromName("control+space").send()
			speech.setSpeechMode(speech.SpeechMode.talk)
			message(o.name)
			# config.conf["keyboard"]["speakTypedCharacters"] = prevSpeak
			
	
	# G5 : buildColumnID() : used in messageListItem.
	# def buildColumnID(self, oTT):
		# try :
			# # oTT must be the threadTree
			# oTT = utis.findParentByID(oTT, controlTypes.Role.TEXTFRAME, "threadTree")
			# sharedVars.objLooping = True
				# # flat list mode : path Role-TEXTFRAME, , IA2ID : threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
			# o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
			# self.columnID =[]
			# while o and o.role == controlTypes.Role.TABLECOLUMNHEADER :
				# if int(o.location[2]) > 0 : # width
					# # append couple (location, IA2ID)
					# ID = utils.getIA2Attr(o)
					# if ID and str(ID) not in "flaggedCol,junkStatusCol,	threadCol,unreadButtonColHeader" :
					# # left must be int for correct sorting
						# left = int(o.location[0])
						# name = str(o.name).replace(_("Sort by "), "")
						# self.columnID.append((left, ID, name))
				# o = o.next
			# self.columnID.sort()
			# # self.columnID =[e[1] for e in self.columnID]
			# # debug test
			# # for e in self.columnID  :
				# # sharedVars.logte("header left:{}, ID:{}, name:{}".format( str(e[0]), e[1], e[2]))
		# finally :
			# # self.lenColID = len(self.columnID)
			# sharedVars.objLooping = False

	# def buildColumnNames(self, oRow) :
		# colSepar = ", " 
		# # sharedVars.logte("Option junkStatusCol:" + str(junkStatusCol))
		# # playSound_unread = False #options.as_bool ("playsound_unread")
		# # sharedVars.logte("Original rowName:" + sharedVars.curTTRow)
		# # l is the line we are going to build
		# if controlTypes.State.COLLAPSED in oRow.states : l = _("Collapsed") + ", "
		# else : l = ""

		# # sharedVars.debugLog +="* Columns properties\n"
		# try : # finally
			# sharedVars.objLooping = True
			# oCell = oRow.firstChild
			# while oCell :
				# s = ""
				# longID = str(utils.getIA2Attr(oCell, False, "class"))
				# sharedVars.logte("Col longID : " + longID)
				# ID = longID.split(" ")
				# ID = str(ID[len(ID)-1])
				# ID = ID.split("-")[0]
				# # begin test
				# # nm = ", name:" +  str(oCell.name)
				# # testChild =", no children" 
				# # if oCell.firstChild :
					# # testChild = ", firstChild role:" + str(oCell.firstChild.role)
					# # if oCell.firstChild.name : testChild += ", cname:" +  oCell.firstChild.name
				# # sharedVars.logte(str(oCell.location.left) + ", short ID:" + ID + ", longID:" + longID + nm + testChild)
				# # end of test 
				# # if "unread" in longID == "statuscol" :
					# # s = oCell.FirstChild
					# # s = "col non lu, "
				# if ID == "statuscol" :
					# o = oCell.firstChild
					# if not o :
						# s =  sharedVars.unread if sharedVars.unread not in l else "" # 2023.11.15 
					# else :
						# s = o.name
						# if s == _("Read") : s = ""
				# elif "unreadbuttoncolheader" in longID :
					# if sharedVars.unread  + ", " in oRow.name : s = sharedVars.unread
					# else : s = ""
				# elif "flaggedcol" in longID :
					# if _("Starred") + ", " in oRow.name : s = _("Starred")
				# elif ID == "subjectcol" :
					# o = oCell.firstChild.firstChild.firstChild
					# s= ""
					# while  o :
						# if o.role == controlTypes.Role.STATICTEXT :
							# s = o.name
							# break
						# o = o.next
					# s=removeResponseMention (self, s,1).strip (" -_*#").replace(" - "," ")
					# if sharedVars.oSettings.regex_removeInSubject is not None : 
						# s =sharedVars.oSettings.regex_removeInSubject.sub ("", s)

					# # listgroup name repeats
					# grp = utis.strBetween(s, "[", "]")
					# # api.copyToClip("groupe " + grp)
					# if grp :
						# s= self.regExp_nameListGroup.sub (" ",s)
						# if  not sharedVars.listGroupName :
							# s = "[" + grp + "] " +  s 
					# # sharedVars.curSubject = s
				# elif ID in ("correspondentcol","sendercol","recipientcol") :  # clean
					# if  oCell.firstChild :
						# s= oCell.firstChild.name
						# if sharedVars.namesCleaned : # corresp name 
							# s = self.regExp_removeSymDigits.sub (" ", s)
						# else : 
							# s = self.regExp_removeSymbols.sub (" ", s)
						# s = utis.truncateAfter(s, "<")
				# elif "attachmentcol" in longID :
					# if oCell.firstChild :
						# s = _("attachment") 
				# elif ID =="junkstatuscol" :
					# # Translators : junk mail column in the list of messages : You dshould write here exactly what  Thunderbird says in your language.
					# if sharedVars.junkStatusCol :
						# s =  _("Spam")
						# if   s not in sharedVars.curTTRow :
							# s =""

				# else : #  elif ID in ("datecol, ","receivedcol, "tagscol", "sizecol", "accountcol", "totalcol", "locationcol", "idcol") :
					# try : s = oCell.firstChild.name
					# except : pass
				# if s : l += s + colSepar
				# oCell = oCell.next
				
			# # positon info
			# # posInfo = oRow.positionInfo
			# # # example : PosInfo={'level': 1, 'similarItemsInGroup': 973, 'indexInGroup': 971}posInfo = oRow.positionInfo 
			# # # Remarhs :  the level info  and oRow.childcount are both erroneous.
			# # l += " " + str(posInfo['indexInGroup']) + _(" of ") + str(posInfo['similarItemsInGroup'])
			# # # for testing, duration
			# # ms = time () - t
			# # ms = int(ms *1000)
			# # l += ", duration : " + str(ms) 
			# if not l :
				# return "Card, " + str(oRow.name)
			# return l  # + ", Original : " + oRow.name
		# finally :
			# sharedVars.objLooping = False
			
	def event_stateChange(self,obj,nextHandler) :
		if self.logEvents : sharedVars.log(obj, "Event stateChange start: ")
		if obj.role == controlTypes.Role.TAB and controlTypes.State.SELECTED in obj.states :
			# sharedVars.log(api.getFocusObject(), "event_stateChange")
			if utils.hasID(obj.parent, "tabmail-tabs") :
				wx.CallAfter(messengerWindow.tabs.onTabSelect, obj) 
		elif obj.role == controlTypes.Role.PROPERTYPAGE and controlTypes.State.OFFSCREEN not in obj.states :
			ID = str(utils.getIA2Attr(obj))
			messengerWindow.tabs.getTabFromPropertyPage(ID, obj)
			callLater(100, messengerWindow.tabs.onPropertyPageChange, obj)
			if sharedVars.curTab == "main" :
				globalVars.TBPropertyPage = obj
		nextHandler()

	# def event_nameChange(self,obj,nextHandler) :
		# # detects content change in the current row of the message liste. When m or s are  pressed for example
		# if obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and  utils.hasID(obj, "threadTree-row") :
			# # sharedVars.logte("nameChange" + str(obj.name))
			# sharedVars.curTTRow = obj.name
			# if sharedVars.TTClean :
				# try :  # 2023 11 05 necessary when quick deletions
					# sharedVars.curTTRowCleaned = self.buildColumnNames(obj)
				# except : 
					# beep(100, 15)
					# sharedVars.curTTRowCleaned = sharedVars.curTTRow
					# pass
		# nextHandler()
		
	# def event_alert (self,obj,nextHandler):
		# # fo = api.getFocusObject()
		# # isThreadTree = utils.hasID(fo, "threadTree") 
		
		# role = obj.role
		# if role != controlTypes.Role.ALERT  : return # nextHandler()
		# try :
			# o = obj.getChild(1).firstChild
		# except :
			# return nextHandler()
		# msg = str(o.name)
		# msg = msg.replace("bird Beta", "bird") 
		# #Translators: alert : this is a draft
		# if _("draft") in msg :
			# return
		# #Translators: alert : Thunderbird thinks this message is fraudulent
		# elif _("bird thinks this message is Junk") in msg : # indésirable
			# beep (200, 2)
			# return
		# #Translators: alert : remote content 
		# elif _("remote content") in msg :
			# # beep(250, 70)
			# return
		# #Translators: 2022-12-12 alert X @gmail.com has asked to be notified when you read this message.
		# elif _("notified when you") in msg :  # demande accusé réception
			# if sharedVars.oSettings.getOption("mainWindow", "withoutReceipt") :
				# return
			# #Translators:  Ignore button in alert in TB
			# oBtn = findButtonByName(obj, _("Ignore"))
			# if oBtn :
				# wx.CallLater (30, focusAlert, "", oBtn)
			# return
		# nextHandler

	def event_alert (self,obj,nextHandler):
		label = ""
		lButtons = []
		# log = "Alert dialog\n"
		for child in obj.recursiveDescendants:
			role = child.role
			ID = str(utils.getIA2Attr(child))
			if role in (controlTypes.Role.LABEL, controlTypes.Role.STATICTEXT) :
				lbl = str(child.name)
				if lbl not in label :
					label += ID + "|" + lbl
				else :
					child.name = ""
				# log += label + "\n"
			elif role == controlTypes.Role.BUTTON :
				lButtons.append(child)
				IA2Class = utils.getIA2Attr(child, False, "class") # for addon adding
				if not	 IA2Class : IA2Class = ""
				if "popup-notification-primary" in IA2Class :
					speech.cancelSpeech()
					# sharedVars.logte("button prmary message = " + label)
					child.setFocus()
					# beep(600, 30)
					return # nextHandler()
				# log += "Button Id=" + ID + ", " + str(IA2Class) + " " + str(child.name) + "\n"
		# log += "end alert\n"
		# sharedVars.logte(log)
		#Translators: alert : this is a draft
		if _("draft") in label :
			return
		#Translators: alert : Thunderbird thinks this message is fraudulent
		elif _("bird thinks this message is Junk") in label : # indésirable
			beep (200, 2)
			return
		#Translators: alert : remote content 
		elif _("remote content") in label :
			return
		#Translators: 2022-12-12 alert X @gmail.com has asked to be notified when you read this message.
		elif _("notified when you") in label :  # demande accusé réception
			if sharedVars.oSettings.getOption("mainWindow", "withoutReceipt") :
				return
			else :
				speech.cancelSpeech()
				lButtons[1].setFocus()

		# nextHandler()
		
	# gesture scripts
	def script_sharedTab(self, gesture) :
		o=globalVars.focusObject 
		ID = str(utils.getIA2Attr(o))
		if ID.startswith("threadTree-row") :
			rc = int(getLastScriptRepeatCount())
			self.initTimer()
			if rc > 0 :
				self.timer = wx.CallLater(25, utis.sendKey, keyName="tab", num=2, delay=0.01)
			else :
				self.timer = wx.CallLater(200, specialSendKey, "f6")
			return
		elif utils.isFolderTreeItem(o, ID) : 
			return wx.CallAfter(specialSendKey, "f6")
		elif sharedVars.curTab == "sp:addressbook" :
			if utis.TBMajor() > 127 :
				nextGesture = messengerWindow.tabAddressBook.getNextControl(o, ID)
				return KeyboardInputGesture.fromName(nextGesture).send()
			# tb 115
			if ID.startswith("searchInput") :
				return KeyboardInputGesture.fromName ("f6").send () 
		return gesture.send()

	def script_sharedEscape(self, gesture) :
		if sharedVars.curTab == "msgPreview" :
			# sharedVars.logte("sharedEscape, curTab = msgPreview, send shift+f6")
			return KeyboardInputGesture.fromName ("shift+f6").send()  
		o=api.getFocusObject()
		role = o.role
		curTreeType = utils.currentTree(o, role)
		if curTreeType == "f" :
			if not sharedVars.oSettings.getOption("mainWindow", "ftNoEscape") :
				return KeyboardInputGesture.fromName ("f6").send()  
			else :
				message(o.name + ", " + str(messengerWindow.folderTreeItem.fGetAccountNode(o).name))
		if role == controlTypes.Role.FRAME :
			return KeyboardInputGesture.fromName ("shift+f6").send()
		ID = str(utils.getIA2Attr(o))
		if curTreeType == "t" : # threadTree
			if hasFilter(o, ID) :
				gesture.send()
				if hasFilter(o, ID) :
					gesture.send()
				wx.CallAfter(sayFilterRemoved, o)
			else :
				if not sharedVars.oSettings.getOption("mainWindow", "ttNoEscape") :
					return KeyboardInputGesture.fromName ("shift+f6").send() # utils.getFolderTreeFromFG(True)
				else :
					message(o.name)
		if sharedVars.curTab == "message" :
			if sharedVars.debug :
				beep(600, 40)
				sharedVars.debugLog= "sharedEscape, curTab = message, send alt+f4" + "\n" + sharedVars.debugLog
			# this closes TB sometimes -> return KeyboardInputGesture.fromName ("alt+f4").send()  
			return KeyboardInputGesture.fromName ("escape").send()  
		elif  "Recipient" in ID  or "expandedsubjectBox" in ID or "Recipient" in str(utils.getIA2Attr(o.parent)) : # header pane
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role in  (controlTypes.Role.BUTTON, controlTypes.Role.TOGGLEBUTTON)  and ID.startswith("attachment") :
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role == controlTypes.Role.LISTITEM and utils.hasID(o.parent, "attachmentList") :
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif  utils.hasID(o.parent, "attachmentBucket") :  # attachment list in write window
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif sharedVars.curTab == "sp:addressbook"   and role !=  controlTypes.Role.MENUITEM :
			if utis.TBMajor() > 127 :
				messengerWindow.tabAddressBook.getPreviousControl(o, ID)
			else : # TB 115
				if ID.startswith("cards-row") or ID.startswith("searchInput") or ID.startswith("cards") :
					return KeyboardInputGesture.fromName ("shift+f6").send () 
				elif role == controlTypes.Role.TREEVIEWITEM and (ID.startswith("list") or utils.hasID(o.parent, "books")) :
					return KeyboardInputGesture.fromName ("f6").send () 
				elif role == controlTypes.Role.BUTTON :
					return KeyboardInputGesture.fromName ("shift+tab").send () 
				else : return gesture.send()
		elif role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in o.states :
			#sharedVars.debugLog = "sharedEscape document readonly\n"
			context, oFound = utils.whichMessagePane(o, landMark=False)
			# sharedVars.log(oFound, "sharedEscape, context : " + str(context))
			if not oFound :
				#  beep(100, 40)
				return gesture.send()
			elif context == "preview" :
					return KeyboardInputGesture.fromName ("shift+f6").send ()
			elif context == "msgWindow" :
					# return KeyboardInputGesture.fromName ("alt+f4").send ()
					return KeyboardInputGesture.fromName ("escape").send ()
		elif role ==  controlTypes.Role.LINK  : # in preview Pane document or accountCentral doc
			# before 135 Role.INTERNALFRAME, IA2ID : messagepane Tag: browser, States : , FOCUSABLE, childCount  : 1 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID : messagepane , 
			# tb 135 : level -6   : TEXTFRAME, ID : messagePane, class : MozillaWindowClass, childCount : 1
			if utis.TBMajor() < 135 :
				if  utis.findParentByID(o, controlTypes.Role.SECTION, "messagePane") : return KeyboardInputGesture.fromName("shift+f6").send()
			else : # >= 135
				if  utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "messagePane") or utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") : return KeyboardInputGesture.fromName("shift+f6").send()
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") : return KeyboardInputGesture.fromName("shift+f6").send()
		if str(utils.getIA2Attr(o.parent)) in "messageEditor,MsgHeadersToolbar" :
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape") :
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "quickFilterBarContainer") :
			# if o.value is not None : message(_("Keyword removed."))
			# return gesture.send()
		elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "MsgHeadersToolbar") : # write window
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape") :
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif  role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW, controlTypes.Role.TABLE) and utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "threadTree") :  # modified 2025-01-09
		elif o.parent.role == controlTypes.Role.INTERNALFRAME and  utils.hasID(o.parent, "accountCentralBrowser") :
			return KeyboardInputGesture.fromName ("shift+f6").send () 
		elif role == controlTypes.Role.BUTTON :
			# preview Pane or separate message window :
			context, oFound = utils.whichMessagePane(o, landMark=True)
			# sharedVars.log(oFound, "sharedEscape, context : " + str(context))
			if not oFound :
				#  beep(100, 40)
				pass
			elif context == "preview" :
					return KeyboardInputGesture.fromName ("shift+f6").send ()
			elif context == "msgWindow" :
					return KeyboardInputGesture.fromName ("escape").send () # was alt+f4
			# level 1,  40 of 51, name : Aller au jour précédent, Role.BUTTON, IA2ID : previous-day-button
			if ID == "previous-day-button" : return KeyboardInputGesture.fromName ("shift+f6").send ()
			# spaces button
			if ID in "spacesPinnedButton|folderPaneMoreButton" :
				return self.script_sharedGrave(gesture)
			# accountCentral
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") :
				return KeyboardInputGesture.fromName ("shift+f6").send ()
		return gesture.send()
		
	def script_sharedAltEnd(self, gesture) :
		# o = api.getFocusObject()
		# if utils.currentTree(o, o.role) == "t"  or utils.hasID(o.parent, "quickFilterBarContainer") :
		if sharedVars.curTab == "main" :
			msg = utils.getMessageStatus()
			if not msg  : msg = _("Blank")
			message(msg)
			return
		msg = utis.getStatusBarText()
		if not msg : msg = _("Status line without data")
		return message(msg)
	script_sharedAltEnd.__doc__ = _("Announces abbreviated status line and message filtering information if applicable")
	script_sharedAltEnd.category = sharedVars.scriptCategory

	# def script_sharedCtrlTab(self, gesture) :
		# # for test
		# return gesture.send()
		# fo = globalVars.focusObject # api.getFocusObject()
		# speech.cancelSpeech()
		# # beep(440, 5)
		# direct = (-1 if "shift" in gesture.modifierNames else 1)
		# if not messengerWindow.tabs.changeTab(self, fo, direct) :
			# return gesture.send()


	def script_smartReplyToSender(self, gesture) :
		wx.CallLater(25, utils.smartReplyV3,False, 0)
	script_smartReplyToSender.__doc__ = _("Smart reply : replies to the sender or to the  group")
	script_smartReplyToSender.category = sharedVars.scriptCategory

	def script_smartReplyToAll(self, gesture) :
		wx.CallLater(25, utils.smartReplyV3, True, 0)
	script_smartReplyToAll.__doc__ = _("Smart reply : with Shift,  replies to all or to the sender in a group")
	script_smartReplyToAll.category = sharedVars.scriptCategory


	def  script_sharedAltEqual(self, gesture) : # native context menu of active tab
		if sharedVars.curFrame != "messengerWindow" : return
		messengerWindow.tabs.tabContextMenu(self, sharedVars.oCurFrame)
	script_sharedAltEqual.__doc__ = _("Tabs: Displays the context menu of the selected tab in the main window.")
	script_sharedAltEqual.category = sharedVars.scriptCategory

	def  script_sharedCtrlF8(self, gesture) : # show tabs menu
		if sharedVars.curFrame != "messengerWindow" : return gesture.send()
		speech.cancelSpeech()
		messengerWindow.tabs.showTabMenu(self, api.getFocusObject())
	script_sharedCtrlF8.__doc__ = _("Tabs: Displays the open tabs menu in the main window.")
	script_sharedCtrlF8.category = sharedVars.scriptCategory

	def script_sendCtrlF4(self, gesture) :
		if "shift"  in gesture.modifierNames :  return gesture.send()
		fo = api.getFocusObject()
		if gesture.mainKeyName == "backspace" :
			if fo.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT) and controlTypes.State.READONLY  not in fo.states :
				return gesture.send()
		KeyboardInputGesture.fromName("control+f4").send()
	script_sendCtrlF4.__doc__ = _("Sends Control+F4 to the current window.")
	script_sendCtrlF4.category=sharedVars.scriptCategory

	def script_sharedAltN(self, gesture) :
		fo = api.getFocusObject()
		ID = str(utils.getIA2Attr(fo))
		parID = str(utils.getIA2Attr(fo.parent))
		# sharedVars.logte("parentID=" + parID)
		rc = int(getLastScriptRepeatCount())
		mk = int(gesture.mainKeyName)
		if parID in ("MsgHeadersToolbar", "messageEditor") :
			# self.initTimer ()
			if rc > 0 :
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, mk, rc)
			else :
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, mk, rc)
			return
		elif ID.startswith("threadTree") or parID == "messagepane" :
			if  ID.startswith("threadTree") and controlTypes.State.SELECTED not in fo.states : # for TB 128
				fo.doAction()
			self.initTimer ()
			if rc> 1 : # 3 press, force update
				self.timer = wx.CallLater(10, utils.getHeader, fo, mk, rc)
			elif rc == 1: # 1 press : search new update 
				self.timer = wx.CallLater(300, utils.getHeader, fo, mk, rc)
			elif rc == 0: # 1 press : search new update 
				self.timer = wx.CallLater(10, utils.getHeader, fo, mk, rc)
	script_sharedAltN.__doc__ = _("In the main window, 1 press: Alt+1 to 8: reads the message header, Alt+9 announces the number of attachments, 2 presses: displays the header in an edit box or for Alt+9, reaches the list of attachments, 3 presses: reaches the header in the headers area. In the Write window, Alt1 to 4, reads the headers, 2 presses reaches the header.")
	script_sharedAltN.category=sharedVars.scriptCategory

	def script_sharedAltArrow(self, gesture) :
		mainKey = gesture.mainKeyName
		fo = o =   api.getFocusObject() # globalVars.focusObject api.getFocusObject()
		role = o.role
		# Optimization for write window
		if role == controlTypes.Role.DOCUMENT and mainKey in ("leftArrow", "rightArrow") : return gesture.send() 
		if mainKey in ("downArrow", "upArrow") : 
			if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
			if role == controlTypes.Role.DOCUMENT :
				return sharedVars.oQuoteNav.readMail(fo , o,(mainKey == "upArrow")) # with quote list
			ID = str(utils.getIA2Attr(o))
			if ID.startswith("threadTree-row") :
				if controlTypes.State.COLLAPSED in o.states : 
					# sending right arrow after  a alt+downArrow does not work
					return message(_("Press right arrow and retry, please."))
				utils.setMLIState(o) # select or expand
				for i in range(0, 20) :
					o2, retryNeeded = utils.getPreviewDoc()
					if o2 : 
						o = o2
						break
					if not retryNeeded : break
					sleep(0.1)
					api.processPendingEvents()
				if not o : 
					beep(110, 10)
					return 
				return sharedVars.oQuoteNav.readMail(fo, o,(mainKey == "upArrow")) # with quote list
			elif utils.isFolderTreeItem(o, ID) :
				# sharedVars.log(o, "folderTreeItem before call of fmenuFolder")
				return messengerWindow.folderTreeItem.fMenuFolders(o, (mainKey == "downArrow"))
			elif  ID.startswith("ReplaceWordInput") : 
				# spellCheckDialog
				if mainKey == "upArrow" :
					return fo.script_reportFocus(gesture)
				elif mainKey == "downArrow" :
					return o.script_focusSuggested(gesture)
			elif  utils.hasID(o.parent, "SuggestedList") :
				# spellCheckDialog
				return o.script_focusEdit(gesture)
		return gesture.send()
		
	def script_sharedF4(self, gesture) :
		# document or preview reading
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		o = api.getFocusObject()
		role = o.role
		if role in  (controlTypes.Role.DOCUMENT, controlTypes.Role.LINK) :
			return sharedVars.oQuoteNav.readMail(o, o, ("shift" in gesture.modifierNames))
		elif   utils.hasID(o, "threadTree-row") :
			fo = o
			utils.setMLIState(o)
			for i in range(0, 20) :
				o2, retryNeeded = utils.getPreviewDoc()
				if o2 : 
					o = o2
					break
				if not retryNeeded : break
				sleep(0.1)
				api.processPendingEvents()
			if not o : 
				beep(110, 40)
				return gesture.send()
			else : return sharedVars.oQuoteNav.readMail(fo, o, ("shift" in gesture.modifierNames))
		else : return gesture.send()
	script_sharedF4.__doc__ = _("Filtered reading of the document in the preview pane, reading tab, reading or Write window, from the list of messages or the document.")
	script_sharedF4.category = sharedVars.scriptCategory

	def script_toggleTranslation(self, gesture) :
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		sharedVars.oQuoteNav.toggleTranslation()
	script_toggleTranslation.__doc__ = _("Enables or disables  the translation mode of a message.")
	script_toggleTranslation.category = sharedVars.scriptCategory

	def script_toggleBrowseMessage(self, gesture) :
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		sharedVars.oQuoteNav.toggleBrowseMessage()
	script_toggleBrowseMessage.__doc__ = _("Enables or disables the display of the cleaned or translated   message in a window.")
	script_toggleBrowseMessage.category = sharedVars.scriptCategory

	def script_sharedAltC(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		# type 1 : read and unread
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAccounts, 1)
	script_sharedAltC.__doc__ = _("Folders : displays the accounts menu then  the folders menu for the chosen account.")
	script_sharedAltC.category = sharedVars.scriptCategory

	def script_sharedAltX(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuInboxes, False)
	script_sharedAltX.__doc__ = _("Folders : displays the menu of all inbox folders")
	script_sharedAltX.category = sharedVars.scriptCategory

	def script_sharedAltB(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)
	script_sharedAltB.__doc__ = _("Folders :, displays the menu of all folders")
	script_sharedAltB.category = sharedVars.scriptCategory

	def script_sharedAltW(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)
	script_sharedAltW.__doc__ = _("Folders :, displays the menu of all unread folders")
	script_sharedAltW.category = sharedVars.scriptCategory


	def script_sharedAltV(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuInboxes, True)
	script_sharedAltV.__doc__ = _("Folders : displays the menu of unread inbox folders")
	script_sharedAltV.category = sharedVars.scriptCategory


	def script_sharedAltCtrlC(self, gesture) :
		if sharedVars.curTab !=  "main" : return gesture.send()
		# type 2 : unread only
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAccounts, 2)
	script_sharedAltCtrlC.__doc__ = _("Folders : displays the accounts menu then the unread folders menu for the chosen account.")
	script_sharedAltCtrlC.category = sharedVars.scriptCategory

	def script_sharedAltHome(self, gesture) :
		# if sharedVars.curTab != "main" : return gesture.send()
		rc = int(getLastScriptRepeatCount())
		d = 100
		self.initTimer ()
		if rc == 0: # 1 press : search new update 
			self.timer = wx.CallLater(d, utils.getFolderTreeFromFG, True)
		elif rc == 1: # 1 press : search new update 
			tp = 2 if "control" in gesture.modifierNames else 1
			self.timer = wx.CallLater(d, messengerWindow.folderTreeItem.fMenuAccounts, tp)
	script_sharedAltHome.__doc__ = _("Focus : 1 press select the current folder in the folder tree, 2 presesses display a menu  allowings to choose an mail account to reach in the folder tree")
	script_sharedAltHome.category = sharedVars.scriptCategory

	def script_sharedGrave(self, gesture) :
		fo = api.getFocusObject()
		if fo.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT) and controlTypes.State.READONLY not in fo.states :
			return gesture.send()
		if sharedVars.curTab == "main" :
			speech.setSpeechMode(speech.SpeechMode.off)
			return callLater(50, applyFocusMode)
		elif sharedVars.curTab == "sp:addressbook" :
			return self.script_showContextMenu(None)
		elif  sharedVars.curFrame == "messengerWindow" :
			speech.setSpeechMode(speech.SpeechMode.off)
			messengerWindow.tabs.selectTab(None, 0)
			return callLater(50, applyFocusMode)
		return gesture.send()
		fo = api.getFocusObject()
		if not  globalVars.TBPropertyPage and fo.role == controlTypes.Role.FRAME :
				return KeyboardInputGesture.fromName("shift+f6").send()
		# determine curFrame and curTab
		utils.setCurFrameTabFromFO(fo)
		# msg = "curTab : {}, curFrame : {}".format(sharedVars.curTab, sharedVars.curFrame)
		# message(msg)
		# return
		if sharedVars.curFrame != "messengerWindow"  or getLastScriptRepeatCount() > 0 : return gesture.send()
		if sharedVars.curTab == "main" and utils.hasID(fo, "threadTree-"):
			# focus modes : 0 nothing, 1 : last msg, 2 : first msg, 3 : first unread, 4 : folderTree
			gestList = ["", "end", "home", "n", "shift+f6"] 
			focusMode = 4 # sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
			if focusMode > 0 :
				wx.CallAfter(KeyboardInputGesture.fromName(gestList[focusMode]).send)
			
			# # we are not in folderTree nor in threadTree
			# wx.CallAfter(utils.getFolderTreeFromFG, focus=True)
		# elif sharedVars.curTab == "sp:addressbook" :
			# return self.script_showContextMenu(None)
		# else : # other active tab, we activate the first tab 
			# if not messengerWindow.tabs.activateTab(self, api.getFocusObject(), 0) :
				# return gesture.send()
	script_sharedGrave.__doc__ = _("Focus : selects a message in the message list from anywhere in the main window.")
	script_sharedGrave.category = sharedVars.scriptCategory

	def script_sharedAltPageDown(self, gesture) :
		fo = api.getFocusObject()
		ID = str(utils.getIA2Attr(fo))
		parID = str(utils.getIA2Attr(fo.parent))
		rc = int(getLastScriptRepeatCount())
		if parID in ("MsgHeadersToolbar", "messageEditor") : # write window 
			self.initTimer ()
			if rc > 0 :
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, 3, rc)
			else :
				self.timer = wx.CallLater(20, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, 3, rc)
			return
		elif ID.startswith("threadTree") or parID == "messagepane"  or fo.role == controlTypes.Role.LINK :
			if  ID.startswith("threadTree") and not utils.getMessagePane() :
				return message(_("The headers pane is not displayed. Please press F8 then try again"))
			if ID.startswith("threadTree") and controlTypes.State.COLLAPSED in fo.states :
				# beep(432, 2)
				self.counter += 1
				utis.sendKey("rightArrow", num=1, delay=0.05)
				return wx.CallLater(100, self.script_sharedAltPageDown, gesture)
			self.counter = 0
			# sharedVars.log(fo,"altPageDown focus")
			self.initTimer ()
			if rc> 0 : 
				# beep(440, 40)
				self.timer = wx.CallLater(10, utils.getAttachment, fo, rc)
				return
			elif rc == 0: 
				self.timer = wx.CallLater(200, utils.getAttachment, fo, rc)
				return
		return gesture.send()
	script_sharedAltPageDown.__doc__ = _("Attachments : announces or displays the attachment pane.")
	script_sharedAltPageDown.category =sharedVars.scriptCategory

	def script_sharedWinArrow(self, gesture) :
		# quote navigator
		#beep(440, 5)
		mainKey = gesture.mainKeyName
		if not sharedVars.oQuoteNav :
			return message(_("Press alt+upArrow before navigating through quotes in a message."))
		if mainKey == "upArrow" :
			sharedVars.oQuoteNav.skip(-1)
		elif mainKey == "downArrow" :
			sharedVars.oQuoteNav.skip()
		if mainKey == "leftArrow" :
			sharedVars.oQuoteNav.skipQuote(-1)
		elif mainKey == "rightArrow" :
			sharedVars.oQuoteNav.skipQuote()
	script_sharedWinArrow.__doc__ = _("Navigates through quotes in a message")
	script_sharedWinArrow.category = sharedVars.scriptCategory

	def script_showContextMenu(self, gesture) :
		if getLastScriptRepeatCount () > 0 : return gesture.send()
		if sharedVars.curTab == "sp:addressbook" :
			o = api.getFocusObject()
			if hasattr(o, "script_menuAB") :
				o.script_menuAB(gesture)
		elif sharedVars.curFrame == "messengerWindow" :
			oMenu = messengerWindow.menuMain.MainMenu(self)
			oMenu.showMenu(globalVars.focusObject)
		elif sharedVars.curFrame == "msgcomposeWindow" :
			if globalVars.focusObject.role != controlTypes.Role.DOCUMENT : return
			oMenu = msgComposeWindow.menuCompose.ComposeMenu(self)
			oMenu.showMenu()
	script_showContextMenu.__doc__ = _("Shows the context menu of actions available in the various Thunderbird windows.")
	script_showContextMenu.category =sharedVars.scriptCategory

	def script_showOptionMenu(self, gesture) :
		repeats = getLastScriptRepeatCount ()
		if sharedVars.curFrame != "msgcomposeWindow" :
			sharedVars.oSettings.showOptionsMenu(sharedVars.curFrame) # menu dépendant du frame actif
		else :  # msgcomposeWindow
			self.initTimer()
			if not sharedVars.oSettings.getOption("msgcomposeWindow", "onePress") : # not onePress to showMenu
				if repeats > 0 :
					self.timer = wx.CallLater(10, sharedVars.oSettings.showOptionsMenu, sharedVars.curFrame)
				elif repeats == 0 : 
					self.timer = wx.CallLater(200, gesture.send)
			else : # menu with onePress
				if repeats > 0 :
					self.timer = wx.CallLater(10, gesture.send)
				elif repeats == 0 : # (dblPress and repeats== 0) or (not dblPress and repeats == 1) : 
					self.timer = wx.CallLater(200, sharedVars.oSettings.showOptionsMenu, sharedVars.curFrame) # menu dépendant du frame acti
			return
	script_showOptionMenu.__doc__ = _("Shows the Options context menu of Thunderbird+")
	script_showOptionMenu.category = sharedVars.scriptCategory

	def script_sharedAltD(self,gesture):
		if sharedVars.curFrame == "messengerWindow" :
			wx.CallLater(10, sharedVars.oSettings.editDelay)
			return
		return gesture.send()
	script_sharedAltD.__doc__ = _("Shows the dialog for editing the delay before reading the message of the separate reading window.")
	script_sharedAltD.category = sharedVars.scriptCategory

	def script_sharedAltDelete(self,gesture):
		if sharedVars.curFrame == "messengerWindow" :
			wx.CallLater(20, sharedVars.oSettings.editDeleteDelays)
			return
		return gesture.send()
	script_sharedAltDelete__doc__ = _("Shows the dialog for editing the two delays used for focusing after deleting a message.")
	script_sharedAltDelete.category = sharedVars.scriptCategory

	def script_previewPane(self, gesture) :
		if globalVars.focusObject.role  not in (controlTypes.Role.TREEVIEWITEM , controlTypes.Role.LISTITEM) : 
			return gesture.send()
		KeyboardInputGesture.fromName ("f8").send()
		if sharedVars.debug : sharedVars.debugLog = "Search for previewPane\n"
		o =  utils.getMessagePane()
		if o :
			message(_("Present: Headers and message pane."))
		else :
			message(_("Missing : headers and message pane."))
	script_previewPane.__doc__ = _("Turn on or off the preview messages panel")
	script_previewPane.category = sharedVars.scriptCategory

	def script_showHelp(self, gesture) :
		utis.showHelp()
	script_showHelp.__doc__ = _("Shows the add-on help in a web page")
	script_showHelp.category = sharedVars.scriptCategory

	def script_displayDebug(self, gesture) :
		debugShow(self, False)

	def script_listObjects(self, gesture) :
		prevMode = sharedVars.debug
		sharedVars.debug = True
		message("Listing objects, please wait...")
		sharedVars.debugLog = "Object list in Thunderbird\n"
		fo = api.getFocusObject()
		utils.listAscendants(-12, fo)
		utils.listDescendants(fo, 0, "* List of descendants")
		textDialog.showText(title="Log", text=sharedVars.debugLog)
		sharedVars.debug = prevMode
		sharedVars.debugLog = "New log\n"


	def script_initDebug(self, gesture) :
		if self.logEvents :
			self.logEvents = False
			message("logEvents mode is disabled")
		else :
			self.logEvents = True
			message("logEvents mode is enabled")
			sharedVars.debugLog = "logEvents = True\n"
		# if sharedVars.debug :
			# sharedVars.debug = False
			# message("Debug mode is disabled")
		# else :
			# sharedVars.debug = True
			# message("Debug mode is enabled")
		# sharedVars.debugLog = "New log\n"
		# # disabModes : 0 nothing, 1 choose overlay, 2 : object init, 3 gainFocus 
		# self.disabMode +=1
		# if self.disabMode > 3 : self.disabMode = 0
		# if self.disabMode == 0 : mode = u"Aucune désactivation"
		# elif self.disabMode == 1 : mode = u"Désactivation de l'intercepteur."
		# elif self.disabMode == 2 : mode = u"Désactivation de l'initialisation des objets NVDA."
		# elif self.disabMode == 3 : mode = u"Désactivation de  gain focus."
		# else : mode = "disabMode = " + str(self.disabMode)

		# message(mode)

	__gestures = {
		# utis.gestureFromScanCode(41, "kb:") :"showContextMenu", # 41 is the scancode of the key above Tab
		# utis.gestureFromScanCode(41, "kb:shift+") :"showOptionMenu", 
		#"kb(desktop):NVDA+End": "statusBar",
		"kb:tab": "sharedTab",
		"kb:escape": "sharedEscape",
		"kb:alt+1": "sharedAltN",
		"kb:alt+2": "sharedAltN",	
		# utis.gestureFromScanCode(3, "kb:alt+") :"sharedAltN", # 41 is the scancode of the key above Tab
		"kb:alt+3": "sharedAltN",	
		# utis.gestureFromScanCode(4, "kb:alt+") :"sharedAltN", # 41 is the scancode of the key above Tab
		"kb:alt+4": "sharedAltN",
		"kb:alt+5": "sharedAltN",
		"kb:alt+6": "sharedAltN",
		"kb:alt+7": "sharedAltN",
		"kb:alt+8": "sharedAltN",
		"kb:alt+9": "sharedAltPageDown", # attachments
		"kb:alt+c": "sharedAltC",
		"kb:alt+control+c": "sharedAltCtrlC",
		"kb:alt+x": "sharedAltX",
		"kb:alt+v": "sharedAltV",
		"kb:alt+b": "sharedAltB",
		"kb:alt+home": "sharedAltHome",
		"kb:alt+control+home": "sharedAltHome",
		"kb:alt+pagedown":"sharedAltPageDown",
		"kb:alt+pagedown":"sharedAltPageDown",
		"kb:alt+leftArrow": "sharedAltArrow",
		"kb:alt+rightArrow": "sharedAltArrow",
		"kb:alt+downArrow": "sharedAltArrow",
		
		"kb:alt+shift+downArrow": "sharedAltArrow",
		"kb:alt+upArrow": "sharedAltArrow",
		"kb:f4": "sharedF4",
		"kb:scrolllock": "toggleTranslation",
		"kb:shift+scrolllock": "toggleBrowseMessage",
		"kb:windows+downarrow": "sharedWinArrow",
		"kb:windows+uparrow": "sharedWinArrow",
		"kb:windows+leftarrow": "sharedWinArrow",
		"kb:windows+rightarrow": "sharedWinArrow",
		"kb:shift+f4": "sharedF4",
		"kb:alt+End": "sharedAltEnd",
		utis.gestureFromScanCode(12, "kb:alt+") : "sharedAltEnd", # 2th  key at the left  of backspace
		# "kb:control+tab": "sharedCtrlTab",
		# "kb:control+shift+tab": "sharedCtrlTab",
		# "kb:control+1": "sharedCtrlN",
		# "kb:control+2": "sharedCtrlN",
		# "kb:control+3": "sharedCtrlN",	
		# "kb:control+4": "sharedCtrlN",
		# "kb:control+5": "sharedCtrlN",
		# "kb:control+6": "sharedCtrlN",
		# "kb:control+7": "sharedCtrlN",
		# # "kb:control+8": "sharedCtrlN",
		# "kb:control+9": "sharedCtrlN",
		# "kb:control+0": "sharedCtrlN",
		utis.gestureFromScanCode(13, "kb:control+") : "sharedCtrlF8", # 13 : first hey at the left of backspace
		utis.gestureFromScanCode(13, "kb:alt+") : "sharedAltEqual",
		"kb:control+f8": "sharedCtrlF8", # show tabs menu
		# "kb:alt+pageup": "smartReplyToSender", # smart reply
		"kb:control+t": "smartReplyToSender",
		"kb:control+shift+t": "smartReplyToAll", 
		# "kb:control+f4": "sendCtrlF4",
		# "kb:control+w": "sendCtrlF4",
		"kb:control+f4": "sendCtrlF4",
		# _("kb:shift+control+²") :"showOptionMenu",
		# _("kb:control+²") :"showContextMenu",
		"kb:alt+d":"sharedAltD",
		"kb:alt+delete":"sharedAltDelete",
		"kb:f8":"previewPane",
		"kb:control+f1": "showHelp",
		"kb:alt+f12": "displayDebug",
		"kb:windows+f12": "initDebug",
		"kb:windows+control+f12": "listObjects"
	}

def debugShow(appMod, auto) :
	sharedVars.debugLog += "Debug mode : {}, TB branch : {}".format(str(sharedVars.debug), utis.TBMajor()) + "\n" + "\n" + "\n" + sharedVars.debugLog
	utils.setBrailleMode()
	sharedVars.logte("Braille Mode after setBrailleMode: " + str(utils.getBrailleParam("mode")))
	sharedVars.test(None, "curTab={}, curFrame={}, objLooping={}".format(sharedVars.curTab, sharedVars.curFrame, str(sharedVars.objLooping)))
	# sharedVars.test(utils.getPropertyPage(True), "Test getPropertyPage forced")
	# sharedVars.test(utils.getFolderTreeFromFG(False, True), "Test getFolderTree forced")
	fo = api.getFocusObject()
	sharedVars.test(fo, "* FocusObject")
	sharedVars.test(api.getNavigatorObject(), "* NavigatorObject")
	# sharedVars.logte("curWinTitle=" + sharedVars.curWinTitle)
	# nom = utils.getColValue(api.getFocusObject(), "subjectcol")
	# sharedVars.logte("Valeur colonne=" + nom) 
	# oRow = api.getFocusObject()
	# sharedVars.logte("curSubject=" + sharedVars.curSubject)
	# no = api.getNavigatorObject()
	# if no.role == controlTypes.Role.GRAPHIC :
		# utils.listAscendants(-6, no, "Nav Object * Ascendents")
		# utils.listDescendants(no, 0, "* Nav object   descendants")
		# textDialog.showText(title="Log", text=sharedVars.debugLog)
		# return
	# provisoire
	# textDialog.showText(title="Log", text=sharedVars.debugLog)
	# sharedVars.test(no, "Nav object")
	# if utils.hasID(fo, "threadTree-row"	) :
		# sharedVars.logte("Current row original name :\n" + sharedVars.curTTRow)
		# utils.listAscendants(-6)
		# utils.listDescendants(fo, 0, "* List of descendants")
		# utils.listColumnNames(fo) 
	# else :
		# utils.listAscendants(-6)
		# utils.listDescendants(fo, 0, "* List of descendants")
	#sharedVars.debugLog += "\ncurFrame : {0}, curTab : {1},".format(appMod.curFrame, sharedVars.curTab) + "\n"
	sharedVars.debugLog += "\ncurTab : {0}, curFrame : {1},".format(sharedVars.curTab, sharedVars.curFrame) + "\n"
	# sharedVars.test(None, "sharedVars.curSubject :" + sharedVars.curSubject)
	# if sharedVars.oQuoteNav :
		# sharedVars.test(None, "oQuoteNav.subject : " + sharedVars.oQuoteNav.subject)
	# sharedVars.test(None, "GroupingIdx = " + str(sharedVars.groupingIdx))
	# ui.browseableMessage (message = sharedVars.debugLog, title = "TB+G5 log", isHtml = False)
	textDialog.showText(title="Log", text=sharedVars.debugLog)
	if not auto : 
		sharedVars.debugLog = ""

from keyboardHandler import KeyboardInputGesture


# normal function
def specialSendKey(key) :
	KeyboardInputGesture.fromName (key).send() 
	sleep(.05)
	api.processPendingEvents()

# functions for event alert
def focusAlert (message, oButton) :
	speech.cancelSpeech()
	speech.speak ([message])
	if oButton :
		oButton.setFocus()

def findButtonByName(o, nm) :
	o = o.firstChild
	while o :
		r = (o.role if hasattr(o, "role") else 0)
		if r == 9 :
			if nm in str(o.name) : return o
		o = o.next
	return None


def hasFilter(o, ID=None) :
	if utis.TBMajor() > 127 : 
		tp = utis.findParentByID(o,controlTypes.Role.SECTION, "threadPane")
		cnt, inf = utils.getFilterInfos128(tp)
		return True if cnt else False
	
	# TB 115
	if not ID :
		ID = str(utils.getIA2Attr(o))
	if ID.startswith("threadTree-row") :
		o = utis.findParentByID(o,controlTypes.Role.TEXTFRAME, "threadTree")
	# sharedVars.log(o.parent, "parent of threadTree and qfb")
	while o :
		# sharedVars.log(o, "previous ")
		if utils.hasID(o, "quick-filter-bar") : break
		if o.previous : o = o.previous
		else : break
	# 7,        0 of 1, Role.SECTION, IA2ID : quickFilterBarContainer Tag: div, States : , childCount  : 9 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i1, Role-SECTION, , IA2ID : quick-filter-bar | i0, Role-SECTION, , IA2ID : quickFilterBarContainer , IA2Attr : id : quickFilterBarContainer, display : flex, tag : div,  ;
	try :
		o = o.firstChild.getChild(1)
		# sharedVars.log(o, "focusEntered, editabe")
		while o :
			role = o.role
			if role == controlTypes.Role.EDITABLETEXT and o.value : return True
			if role ==  controlTypes.Role.TOGGLEBUTTON and controlTypes.State.PRESSED in o.states : return True
			o = o.next
	except :  pass
	
	return False

def sayFilterRemoved(oCurRow) :
	speech.cancelSpeech()
	infos  =  utils.getMessageStatus128()
	fo = api.getFocusObject()
	role = fo.role
	if role in (controlTypes.Role.TABLE, controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) :
		cc = fo.childCount
		if cc == 0 :
			beep(120, 40)
			infos = _("No messages displayed") + ", " + infos
	name = ""
	if oCurRow :
		name = " " + oCurRow.name
	message(_("Filter removed") + infos+ name)

def activateMenuItem(o, ID) :
	# called after press on delete key in the message list
	# o is role.popupmenu
	try : # finally
		o = o.firstChild 
		while o :
			if o.role == controlTypes.Role.MENUITEM and utils.hasID(o, ID) :
				o.doAction()
				return
			o = o.next
	finally :
		speech.setSpeechMode(speech.speech.SpeechMode.talk)
