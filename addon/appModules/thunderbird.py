 # ThunderbirdPlusG5 for Thunderbird >= 115
import sys
import addonHandler
addonHandler.initTranslation()
from nvdaBuiltin.appModules import thunderbird
from time import time, sleep
from datetime import datetime
from NVDAObjects.IAccessible import IAccessible
from tones import beep
import controlTypes
import api
import ui
import scriptHandler
from scriptHandler import script
import winUser
import speech
import gui
import wx
from core import callLater
import globalCommands
import config
from re import compile,IGNORECASE

import os
# code for importing commonVars which is in the root of the add-on
_curAddon=addonHandler.getCodeAddon()
sys.path.append(_curAddon.path)
import commonVars
del sys.path[-1]
# shutils logger import
sharedPath=os.path.join(_curAddon.path,"shutils")
sys.path.append(sharedPath)
import tbLogger
del sys.path[-1]
# modules in appModules\shared
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import utis, sharedVars, utils115 as utils # , sendInput
from utils115 import message
import  langUtils
import textDialog
del sys.path[-1]
sharedPath = ""

sharedVars.scriptCategory = _curAddon.manifest['summary']
# keys from scancodes
# kBS1 = utis.gestureFromScanCode(13) # first key at the left of backspace
# kBS2 = utis.gestureFromScanCode(12) # second key at the left of backspace
kGrave			= utis.gestureFromScanCode(41) # the key above tab key

# Extension modules import
from . import messengerWindow, msgComposeWindow # , addressbookWindow
from scriptHandler import getLastScriptRepeatCount


# def sayTreeItem(fo=None):
	# try: # finally 
		# done = False
		# if not fo:
			# fo = api.getFocusObject()
		# ID = str(utils.getIA2Attr(fo))
		# if ID.startswith("threadTree-"):
			# roleName = controlTypes.Role.TABLE.displayString
		# elif utils.isFolderTreeItem(fo, ID):
			# roleName = controlTypes.Role.TREEVIEW.displayString
		# else:
			# roleName = fo.role.displayString
		# utis.setSpeech(True)
		# done = True
		# message("{}, {}, {}".format(utis.getWinTitle(appName=False), roleName, fo.name))
	# finally:
		# sharedVars.mainTabInit = True
		# sharedVars.starting = False
		# if not done:
			# utis.setSpeech(True)

def sayTreeItem(fo=None):
	try: # finally 
		done = False
		utis.setSpeech(True)
		done = True
		# message (utis.getWinTitle(appName=False))
	finally:
		sharedVars.mainTabInit = True
		sharedVars.starting = False
		if not done:
			utis.setSpeech(True)

def sayWinTitle():
	prevSpeechMode =  utis.getSpeechMode()
	speech.setSpeechMode(commonVars.cv.defaultSpeechMode)
	speech.cancelSpeech()
	message(utis.getWinTitle(appName=False))
	sleep(1.5)
	speech.setSpeechMode(prevSpeechMode)

def applyFocusModeFromThreadTree(focusMode):
			# we are on role = textFrame and id=threadTree
	if focusMode == 1: # last message
		gest = "end"
	elif focusMode == 2: # first  message
		gest = "home"			
	elif focusMode == 3: # first  unread message
		gest = "n"
	else:
		return utis.setSpeech(True)
	KeyboardInputGesture.fromName("f6").send()
	sleep(0.1)
	KeyboardInputGesture.fromName(gest).send()
	callLater(100, sayTreeItem)

def applyFocusMode():
	# from script_Grave
	try: # finally
		focusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
		if focusMode == 0: return
		if focusMode == 4: # folderTree
			oTree = utils.getFolderTreeFromFG()
			if oTree: oTree.setFocus()
			return
		# else threadTree
		oTree = utils.getThreadTreeFromFG()
		if not oTree: 
			return
		oTree = utils.getThreadTreeListOrTable(oTree)
		oTree.setFocus()

		if focusMode == 1: # last message
			gest = "end"
		elif focusMode == 2: # first  message
			gest = "home"
		elif focusMode == 3: # first  unread message
				gest = "n"
		callLater(50, KeyboardInputGesture.fromName(gest).send)
	finally:
		# speech.setSpeechMode(commonVars.cv.defaultSpeechMode)
		utis.setSpeech(True) # 2026-07-19

# def handleFirstFocus(oTreeItem, focusMode):
	# ID = str(utils.getIA2Attr(oTreeItem))
	# if ID.startswith("threadTree-"):
		# applyFocusModeFromThreadTree(focusMode)
	# elif utils.isFolderTreeItem(oTreeItem, ID):
		# role = controlTypes.Role.TREEVIEW
		# applyFocusModeFromFolderTree(focusMode)

# def processTrees(oFolders, oThreads):
	# if sharedVars.mainTabInit: return
	# sharedVars.mainTabInit= True
	# sharedVars.starting = False
	# fo = api.getFocusObject()
	# sharedVars.log(fo, "ProcessTree begin")
	# if utils.hasID(fo, "threadTree-row") or utils.isFolderTree(fo):
		# return
	# onStartupAction  = sharedVars.oSettings.getOption("messengerWindow","onStartupAction", kind="i")
	# match onStartupAction:
		# case 0: # do nothing
			# return
		# case 1: # apply option below
			# focusMode  = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
		# case 2: # Show All inboxes menu
			# callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=False)
		# case 3: # Show all unread inboxes menu
			# callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=True)
		# case 4: # Show All unread folders menu
			# wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)
		# case 5: # Show all folders menu 
			# wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)

class ListTreeView(IAccessible):
	def initOverlayClass (self):
		self.bindGesture ("kb:f", "goFilterBar")
	@script(
		gesture="kb:f",
		description=_("Focus the quick filter bar"),
		category=sharedVars.scriptCategory
	)
	def script_goFilterBar(self, gesture):
		if sharedVars.curTab != "main": return gesture.send() 
		KeyboardInputGesture.fromName ("shift+control+k").send() 

class QuickFilterBar(IAccessible):
	def initOverlayClass (self):
		self.bindGesture ("kb:downArrow", "goMessageList")
	def script_goMessageList(self, gesture):
		if sharedVars.curTab != "main": return gesture.send() 
		KeyboardInputGesture.fromName ("f6").send() 


class TabAddons(IAccessible):
	def initOverlayClass (self):
		self.bindGesture ("kb:enter", "validateEdit")

	@script(
		gesture="kb:enter",
		description=_("Validate edit in addon search"),
		category=sharedVars.scriptCategory
	)
	def script_validateEdit(self, gesture):
		gesture.send()
		ParentPP  = utils.findParentByRole(self, controlTypes.Role.PROPERTYPAGE)
		callLater(200, self.waitForAddonSearchFrame, self.value + ":: ", ppStart=parentPP) 

	def waitForAddonSearchFrame(self, titleStart, ppStart):
		# we are on an editabletext
		title = utis.getWinTitle()
		if title.startswith(titleStart):
			sharedVars.curTab = "sp:addonsearch"
			pp =  utils.getActivePropertyPage(oFrame=None, ppExcluded=ppStart,   debug=False)
			wx.CallAfter(messengerWindow.tabs.setFocusTo, frame=None, propertyPage=pp, curTab=sharedVars.curTab)
		else:
			callLater(200, self.waitForAddonSearchFrame, titleStart, ppStart)

class AppModule(thunderbird.AppModule):
	timer = None
	counter = 0

	def __init__(self, *args, **kwargs):
		super(thunderbird.AppModule, self).__init__(*args, **kwargs)
		# note : api.getForegroundObject returns  the window that is actually in the foreground right now
		processName =  utis.getProcessName(api.getForegroundObject().windowHandle)
		# sharedVars.logte("processName=" + str(processName))

		if processName != "thunderbird.exe":	
			# beep(600, 50)
			sharedVars.logEvents = False
			if sharedVars.logEvents: sharedVars.logte("Thunderbird+G5 _init")
			utis.disableOvl(True) # set objLooping = True
			commonVars.cv.defaultSpeechMode = utis.getSpeechMode()
			sharedVars.initSettingsMenu(self) # then use  sharedVars.oSettings.*
			commonVars.cv.reset() # grouping, folderTree, threadTree, etc.
			sharedVars.curFrame = "unknown"
			sharedVars.curTab = "unknown"
			self.startupAction = sharedVars.oSettings.getOption("messengerWindow","onStartupAction", kind="i") 
			self.startupFocusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i") 
			if sharedVars.logEvents: 
				sharedVars.logte("Call of self.tbStartup")
				sleep(0.2)
			callLater(1500, self.tbStartup)

	def waitForTree(self, oFrame):
		dbg = False if commonVars.cv.logger is None else True
		if dbg: commonVars.cv.logger.add("waitForTree pass=" + str(sharedVars.loopCount))
		if sharedVars.loopCount == 10: 
			sharedVars.loopCount = 0
			if dbg: commonVars.cv.logger.add("waitForTree, max of 10 passes were reached")
			return self.endStartup()
		frame = api.getForegroundObject()
		if sharedVars.loopCount == 1: 
			# select first tab, only  if it is not already selected
			if messengerWindow.tabs.selectTab(oFrame, 0):
				# tab has changed
				callLater(100, sayWinTitle)
			else:
				sayWinTitle()
			if dbg: commonVars.cv.logger.add("waitForTree, first tab selected curTab=" + sharedVars.curTab)
		elif sharedVars.loopCount > 1 and sharedVars.curTab == "main": 
			if dbg: commonVars.cv.logger.addobj(frame, "waitForTree oFrame")
			pp = folderTree = threadTree = None
			oGrouping = utils.getMainGrouping(frame, True)
			if oGrouping: 
				pp = utils.getPropertyPage(frame, debug=dbg)
			if pp: 
				folderTree = utils.getFolderTreeFromPP(oPP=pp, debug=dbg)
				if dbg: commonVars.cv.logger.addobj(folderTree, "waitForTree after getFolderTreeFromPP")  
				threadTree = utils.getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, oPP=pp, debug=dbg)
				if dbg: commonVars.cv.logger.addobj(threadTree, "waitForTree, after getThreadTree")
			# else: # pp is None
				# dbg = True
			if dbg: commonVars.cv.logger.add("\nwaitForTree loppCount".format(sharedVars.loopCount))

			if folderTree and threadTree:
				return self.processTrees(oFrame, folderTree, threadTree, dbg)
		sharedVars.loopCount += 1	
		callLater(200, self.waitForTree, oFrame)	

	def processTrees(self, oFrame, oFolders, oThreads, dbg=False):
		if dbg:
			commonVars.cv.logger.addobj(oFrame, "processTrees, Frame")
			commonVars.cv.logger.addobj(oFolders, "processTrees, FolderTree")
			commonVars.cv.logger.addobj(oThreads, "processTrees, ThreadTree")

		fo = api.getFocusObject()
		# sharedVars.log(fo, "ProcessTree begin")
		if utils.hasID(fo, "threadTree-row") or utils.isFolderTreeItem(fo):
			self.endStartup()
			utils.message(fo.name)
			return

		match self.startupAction:
			case 0: # do nothing
				return self.endStartup()
			case 1: # apply option below
				focusMode = self.startupFocusMode
				if focusMode in (1, 2): #skip to last message in threadTree or firstMessage
					oThreads.setFocus()
					if dbg: commonVars.cv.logger.addobj(oThreads, "processTrees, ThreadTree after setFocus") 
					# applyFocusModeFromThreadTree restores speech
					applyFocusModeFromThreadTree(focusMode)
				elif focusMode == 3: # skip to next unread message
					callLater(100, KeyboardInputGesture.fromName("n").send)
				elif focusMode == 4: # skip to folderTree
					self.endStartup()
					oFolders.setFocus()
					return
			case 2: # Show All inboxes menu
				callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=False)
			case 3: # Show all unread inboxes menu
				callLater(100, messengerWindow.folderTreeItem.fMenuInboxes, unread=True)
			case 4: # Show All unread folders menu
				wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)
			case 5: # Show all folders menu 
				wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)
		self.endStartup()

	def endStartup(self):
		sharedVars.starting = False
		sharedVars.mainTabInit = True 
		sharedVars.objLooping = False
		utis.setSpeechMode(commonVars.cv.defaultSpeechMode) # defaultSpeechMode saved in __init__()

	def tbStartup(self):
		dbg = False
		oFrame = api.getForegroundObject()
		oFocused = None
		sharedVars.startFromPasswordDlg = False
		if str(oFrame.parent.windowClassName) == "MozillaDialogClass":
			sharedVars.curFrame = "firstDlg"
			sharedVars.curTab = "firstDlg"
			for c in oFrame.recursiveDescendants: 
				if c.role == controlTypes.Role.EDITABLETEXT:
					c.setFocus()
					oFocused = c
					break
			if oFocused and oFocused.role == controlTypes.Role.EDITABLETEXT and utils.hasID(oFocused, "password1Textbox"):
				sharedVars.startFromPasswordDlg = True
				sharedVars.curFrame = "passwordDlg"
				sharedVars.curTab = "passwordDlg"
				sharedVars.log(oFocused, "Dialog before main window, focusObject")
				# wx.CallAfter(utils.message, oFocused.role.displayString)
				return
		# normal window
		oFocused = api.getFocusObject()
		if sharedVars.logEvents: 
			sharedVars.log(oFocused, "tbStartup oFocused, curTab=" + sharedVars.curTab) 
			if dbg: sharedVars.log(api.getForegroundObject().parent, "tbStartup foreground.parent, curTab=" + sharedVars.curTab) 
		# utis.setSpeech(False)
		if dbg: sharedVars.debugLog = "Start of Thunderbird+G5\n"
		
		# sharedVars.logte("Before first waitForTree")
		sharedVars.starting = True
		sharedVars.loopCount = 1
		oFrame = api.getForegroundObject()
		callLater(300, self.waitForTree, oFrame)  

	def initTimer(self):
		if self.timer is not None and self.timer.IsRunning():
			self.timer.Stop()
			self.timer = None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if sharedVars.objLooping  or sharedVars.disabMode == 1: return
		role = obj.role
		ID = str(utils.getIA2Attr(obj))
		# write or spellCheck dialog
		if ID.startswith("ReplaceWordInput") or (role == controlTypes.Role.LISTITEM and utils.hasID(obj.parent, "SuggestedList")):
			clsList.insert (0,msgComposeWindow.spellCheckDlg.SpellCheckDlg)
			return
		if sharedVars.curTab == "comp": # compose Window
			return 


		# reduce verbosity
		if role == controlTypes.Role.GROUPING: obj.name = "" ; return 
		
		if role == controlTypes.Role.FRAME: 
			sharedVars.curWinTitle = obj.name
			return # deactivated since  2025.08.27 > m essengerWindow.tabs.setCurFrameTab(obj)
		# if role == controlTypes.Role.PROPERTYPAGE:
			# sharedVars.logte("Overlay, curTab:{}, curFrame: {}, title: {}".format(sharedVars.curTab, sharedVars.curFrame, obj.name))
		
		if role == controlTypes.Role.DOCUMENT and sharedVars.curTab in ("main", "message"):
			if obj.name: sharedVars.curWinTitle = obj.name
			obj.name = ""
			return
		# List of messages
		if role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM):
			if ID.startswith("threadTree-row"):
				# sharedVars.logte(" Overlay:" + obj.name)
				sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "main"
				clsList.insert(0, ListTreeView)
				clsList.insert(0, messengerWindow.messageListItem.MessageListItem)
				return

			if role == controlTypes.Role.TREEVIEWITEM and utils.isFolderTreeItem(obj, ID):
				clsList.insert(0, ListTreeView)
				clsList.insert(0, messengerWindow.folderTreeItem.FolderTreeItem)
				sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "main"
				return
		# quick filter bar
		if role ==  controlTypes.Role.TOGGLEBUTTON and ID.startswith("qfb-"):
			clsList.insert (0, QuickFilterBar); return
		# special tabs documents 
		if sharedVars.curTab == "sp:addressbook":
			if not sharedVars.noAddressBook:
				clsList.insert(0, messengerWindow.tabAddressBook.AddressBook)

		if sharedVars.curTab == "sp:addons":
			if role == controlTypes.Role.EDITABLETEXT:
				clsList.insert (0, TabAddons)

	def event_foreground(self, obj,nextHandler):
		if sharedVars.startFromPasswordDlg:
			# beep(300, 40)
			speech.cancelSpeech()
			# utils.message("Thunderbird") # utis.getWinTitle(appName=True))
			# utis.setSpeech(False)
			callLater(500, self.tbStartup)
			return nextHandler()

		role = obj.role
		if sharedVars.logEvents: sharedVars.log(obj, "* Event foreground start:" )
		if role == controlTypes.Role.FRAME and  sharedVars.replyTo:
			# for smartReply
			sharedVars.replyTo = False
			# speech.setSpeechMode(commonVars.cv.defaultSpeechMode)			
			utis.setSpeech(True)
			msgComposeWindow.msgComposeWindow.sayAllRecipients(obj)
			return # nextHandler()
		# set context  
		if role == controlTypes.Role.FRAME:
			if obj.windowClassName == "MozillaDialogClass":
				ID = str(utils.getIA2Attr(obj.firstChild))
				# 1: dialog  spellcheck
				if ID == "MisspelledWordLabel":
					sharedVars.curFrame = sharedVars.curTab = "spellcheckDlg"
				# 2: dialog filterRules
				elif utils.hasID(obj.firstChild, "filterNameBox"):
					sharedVars.curFrame = sharedVars.curTab = "filterRules"
				return nextHandler()
			ID = str(utils.getIA2Attr(obj))
			childCount = obj.childCount
			# sharedVars.log(obj, "event_foreground, childCount=" + str(childCount))
			if childCount == 0:
				return nextHandler()
			elif childCount < 2:
				# activities
				if utils.hasID(obj.firstChild, "activityContainer"):
					sharedVars.curFrame = sharedVars.curTab = "activity"
				return nextHandler()
			# separate message reading window: 6 children
			elif childCount < 7:
				o = utils.findChildByRoleID(obj, controlTypes.Role.INTERNALFRAME, "messageBrowser", 3)
				if o is not None:
					sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab =  "message" 
				return nextHandler()
			# compose window: 14 childrenbefore, 23 in 2026
			# elif childCount < 15: # obsolete
				# o = utils.findChildByRoleID(obj,controlTypes.Role.POPUPMENU, ID="msgComposeContext", startIdx=1)
				# if o is not None:
					# sharedVars.curTab = "comp" ; sharedVars.curFrame="msgcomposeWindow" 
				# return nextHandler()
			# filterList
			elif childCount < 20: 
				if utils.hasID(obj.getChild(1), "serverMenu"):
					sharedVars.curFrame = sharedVars.curTab = "filterlist"
				return nextHandler()
			# sharedVars.logte("event_foreground, First Grouping and descendants\n")
			oGrouping = utils.getMainGrouping(obj, False)
			if not oGrouping:  # we are not in main window
				utils.setFontextFromFirstID(obj)
				return nextHandler()
			# sharedVars.log(oGrouping, "event_foreground, After call of getFirstGrouping")
			# sharedVars.logte("* List of in Screen property pages")
			curPPID = ""
			curPP = None
			for c in oGrouping.children:
				if c.role == controlTypes.Role.PROPERTYPAGE:
					ppID = str(utils.getIA2Attr(c))
					if controlTypes.State.OFFSCREEN not in c.states:
						curPPID = ppID
						curPP = c
						# sharedVars.log(c, "_foreground current ppID" + ppID) 
					if ppID == "mail3PaneTab":
						commonVars.cv.propertyPage = c
						# sharedVars.log(c, "stored in commonVars.cv.propertyPage")
						# sharedVars.log(c, "pp")
						# sharedVars.log(c.firstChild, "pp.firstChild")

			folderTree = utils.getFolderTreeFromPP(commonVars.cv.propertyPage, debug=False)
			# sharedVars.log(commonVars.cv.folderTree, "commonVars.cv.folderTree")
			threadTree = utils.getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, oPP=commonVars.cv.propertyPage, debug=False)
			# sharedVars.log(commonVars.cv.threadTree, "commonVars.cv.threadTree")
			sharedVars.curFrame = "messengerWindow"
			messengerWindow.tabs.getTabFromPropertyPage(curPPID, curPP)
			return
		if role == controlTypes.Role.DIALOG:
			if "|dlg" not in sharedVars.curFrame: sharedVars.curFrame += "|dlg"
			# sharedVars.log(obj, "Dialog, curframe = " +  sharedVars.curFrame) 
		elif role == controlTypes.Role.FRAME:
			sharedVars.curFrame = sharedVars.curFrame.replace("|dlg", "")
			# sharedVars.log(obj, "FRAME, curframe = " +  sharedVars.curFrame) 
		nextHandler()

	def event_gainFocus (self,obj,nextHandler):
		if sharedVars.logEvents: sharedVars.log(obj, "Event gainFocus start: ")
		# if sharedVars.speechOff:
			# speech.setSpeechMode(commonVars.cv.defaultSpeechMode)
			# sharedVars.speechOff = False
		if sharedVars.curTab == "comp":
			# the try except is needed when NVDA is restarted on th writ window
			try : return nextHandler()
			except : pass
		role = obj.role
		if sharedVars.delPressed and role == controlTypes.Role.POPUPMENU and  utils.hasID(obj, "mailContext"):
			sharedVars.delPressed = False
			wx.CallAfter(activateMenuItem, obj, "navContext-delete")
			return nextHandler()

		# if sharedVars.nPressed: 
			# sharedVars.nPressed = False
			# if role == controlTypes.Role.TABLE:
				# callLater(100, self.focusMessageItem, "gainFocus", time(), obj)
			# return nextHandler()
		# if sharedVars.disabMode == 3: return nextHandler()
		# api.setNavigatorObject(obj) # 2311.12.08
		if sharedVars.menuClosing and role == controlTypes.Role.TREEVIEWITEM:
			sharedVars.menuClosing = False
			utis.setSpeech(True)
		# if sharedVars.TBMajor > 135 and sharedVars.curTab == "main" and role in  (controlTypes.Role.LIST, controlTypes.Role.TABLE):
			# callLater(100, self.focusMessageItem, "gainFocus", time())
			# return nextHandler()

		if role == controlTypes.Role.UNKNOWN:
			if obj.parent and obj.parent.role in(controlTypes.Role.LIST, controlTypes.Role.TREEVIEW):
				# beep(100, 10)
				self.initTimer()
				self.timer = callLater(300, KeyboardInputGesture.fromName("control+space").send)
			return nextHandler()
		elif sharedVars.msgOpened and role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in obj.states:
			speech.cancelSpeech()
			sharedVars.msgOpened = False
			sharedVars.curTab = "message"
			if not sharedVars.oQuoteNav.translate:
				return nextHandler()
			else:
				return wx.CallAfter(sharedVars.oQuoteNav.readMail, obj, obj, rev=False, spkMode=1) # spkMode=1: with utils.sayLongText,  =10 with ui.message
		# column headers  on top of message list
		if sharedVars.curTab == "main" :
			if role == controlTypes.Role.BUTTON :
				ID = str(utils.getIA2Attr(obj))
				if "Col" in ID :
					wx.CallAfter(sayColumnOrder, obj, ID)
					return nextHandler()
		if sharedVars.curTab == "sp:addressbook" and sharedVars.TBMajor > 127:
			messengerWindow.tabAddressBook.abGainFocus(obj)

		nextHandler()
		
	def event_focusEntered (self,obj,nextHandler):
		if sharedVars.logEvents: sharedVars.log(obj, "Event focusEntered start: ")
		role, ID  = obj.role, str(utils.getIA2Attr(obj))
		if role == controlTypes.Role.SECTION and  ID == "composeContentBox": 
			sharedVars.curFrame = "msgcomposeWindow"
			sharedVars.curTab = "comp"
			sharedVars.msgComposeBox = obj
			return nextHandler()
		if sharedVars.curFrame == "msgcomposeWindow" and ID == "msgIdentity":
			return #  No nextHandler()
			
		# sharedVars.log(obj, "focusEntered")
		if role == controlTypes.Role.GROUPING and ID == "tabpanelcontainer":
			commonVars.cv.grouping = obj
			return nextHandler()
		if role == controlTypes.Role.SECTION and ID == "threadPane":
			commonVars.cv.threadPane = obj
			return nextHandler()
		if role == controlTypes.Role.TREEVIEW and ID == "folderTree": 
			commonVars.cv.folderTree = obj
			if sharedVars.TTnoFolderName: obj.name = "" ; api.getForegroundObject().name  = "" # 2026.07.24: api.getForegroundObject 
			return nextHandler()		
		if role == controlTypes.Role.TEXTFRAME and ID == "threadTree":
			commonVars.cv.threadTree = obj
		#   silencify threadTree list or table
		if sharedVars.curTab == "main"  and role in  (controlTypes.Role.LIST, controlTypes.Role.TABLE, controlTypes.Role.TREEVIEW):
			speech.cancelSpeech()
			if sharedVars.TTnoFolderName  and hasattr(obj, "name"): 
				obj.name = ""
		if not sharedVars.oSettings.getOption("deactiv", "TTnoFilterSnd") and ID == "threadTree": 
			if hasFilter(obj, ID): 
				# beep(440, 10)
				utis.playSound("filter")
		nextHandler()

	def focusMessageItem(self, context, startTime, oFocus=None):
		# beep(700, 100)
		return
		if not oFocus:
			o =  api.getFocusObject()
		else:
			o = oFocus
		if o.role in   (controlTypes.Role.LIST, controlTypes.Role.TABLE):
			# beep(700, 40)
			# sharedVars.logte(context  + ": " + now.strftime("%H:%M:%S.%f")[:-4])
			# prevSpeak = config.conf["keyboard"]["speakTypedCharacters"]
			# config.conf["keyboard"]["speakTypedCharacters"] = False
			speech.cancelSpeech()
			prevSpeechMode =  utis.getSpeechMode()
			speech.setSpeechMode(speech.SpeechMode.off)
			KeyboardInputGesture.fromName("control+space").send()
			# sleep(0.02)
			api.processPendingEvents()
			o = api.getFocusObject()
			KeyboardInputGesture.fromName("control+space").send()
			speech.setSpeechMode(prevSpeechMode)
			message(o.name)
			# config.conf["keyboard"]["speakTypedCharacters"] = prevSpeak
			
	
	# G5: buildColumnID(): used in messageListItem.
	# def buildColumnID(self, oTT):
		# try:
			# # oTT must be the threadTree
			# oTT = utis.findParentByID(oTT, controlTypes.Role.TEXTFRAME, "threadTree")
			# sharedVars.objLooping = True
				# # flat list mode: path Role-TEXTFRAME, , IA2ID: threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
			# o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
			# self.columnID =[]
			# while o and o.role == controlTypes.Role.TABLECOLUMNHEADER:
				# if int(o.location[2]) > 0: # width
					# # append couple (location, IA2ID)
					# ID = utils.getIA2Attr(o)
					# if ID and str(ID) not in "flaggedCol,junkStatusCol,	threadCol,unreadButtonColHeader":
					# # left must be int for correct sorting
						# left = int(o.location[0])
						# name = str(o.name).replace(_("Sort by "), "")
						# self.columnID.append((left, ID, name))
				# o = o.next
			# self.columnID.sort()
			# # self.columnID =[e[1] for e in self.columnID]
			# # debug test
			# # for e in self.columnID:
				# # sharedVars.logte("header left:{}, ID:{}, name:{}".format( str(e[0]), e[1], e[2]))
		# finally:
			# # self.lenColID = len(self.columnID)
			# sharedVars.objLooping = False

	# def buildColumnNames(self, oRow):
		# colSepar = ", " 
		# # sharedVars.logte("Option junkStatusCol:" + str(junkStatusCol))
		# # playSound_unread = False #options.as_bool ("playsound_unread")
		# # sharedVars.logte("Original rowName:" + sharedVars.curTTRow)
		# # l is the line we are going to build
		# if controlTypes.State.COLLAPSED in oRow.states: l = _("Collapsed") + ", "
		# else: l = ""

		# # sharedVars.debugLog +="* Columns properties\n"
		# try: # finally
			# sharedVars.objLooping = True
			# oCell = oRow.firstChild
			# while oCell:
				# s = ""
				# longID = str(utils.getIA2Attr(oCell, False, "class"))
				# sharedVars.logte("Col longID: " + longID)
				# ID = longID.split(" ")
				# ID = str(ID[len(ID)-1])
				# ID = ID.split("-")[0]
				# # begin test
				# # nm = ", name:" +  str(oCell.name)
				# # testChild =", no children" 
				# # if oCell.firstChild:
					# # testChild = ", firstChild role:" + str(oCell.firstChild.role)
					# # if oCell.firstChild.name: testChild += ", cname:" +  oCell.firstChild.name
				# # sharedVars.logte(str(oCell.location.left) + ", short ID:" + ID + ", longID:" + longID + nm + testChild)
				# # end of test 
				# # if "unread" in longID == "statuscol":
					# # s = oCell.FirstChild
					# # s = "col non lu, "
				# if ID == "statuscol":
					# o = oCell.firstChild
					# if o is None:
						# s =  sharedVars.unread if sharedVars.unread not in l else "" # 2023.11.15 
					# else:
						# s = o.name
						# if s == _("Read"): s = ""
				# elif "unreadbuttoncolheader" in longID:
					# if sharedVars.unread  + ", " in oRow.name: s = sharedVars.unread
					# else: s = ""
				# elif "flaggedcol" in longID:
					# if _("Starred") + ", " in oRow.name: s = _("Starred")
				# elif ID == "subjectcol":
					# o = oCell.firstChild.firstChild.firstChild
					# s= ""
					# while o is not None:
						# if o.role == controlTypes.Role.STATICTEXT:
							# s = o.name
							# break
						# o = o.next
					# s=removeResponseMention (self, s,1).strip (" -_*#").replace(" - "," ")
					# if sharedVars.oSettings.regex_removeInSubject is not None: 
						# s =sharedVars.oSettings.regex_removeInSubject.sub ("", s)

					# # listgroup name repeats
					# grp = utis.strBetween(s, "[", "]")
					# # api.copyToClip("groupe " + grp)
					# if grp:
						# s= self.regExp_nameListGroup.sub (" ",s)
						# if not sharedVars.listGroupName:
							# s = "[" + grp + "] " +  s 
					# # sharedVars.curSubject = s
				# elif ID in ("correspondentcol","sendercol","recipientcol"):  # clean
					# if oCell.firstChild:
						# s= oCell.firstChild.name
						# if sharedVars.namesCleaned: # corresp name 
							# s = self.regExp_removeSymDigits.sub (" ", s)
						# else: 
							# s = self.regExp_removeSymbols.sub (" ", s)
						# s = utis.truncateAfter(s, "<")
				# elif "attachmentcol" in longID:
					# if oCell.firstChild:
						# s = _("attachment") 
				# elif ID =="junkstatuscol":
					# # Translators: junk mail column in the list of messages: You dshould write here exactly what  Thunderbird says in your language.
					# if sharedVars.junkStatusCol:
						# s =  _("Spam")
						# if s not in sharedVars.curTTRow:
							# s =""

				# else: #  elif ID in ("datecol, ","receivedcol, "tagscol", "sizecol", "accountcol", "totalcol", "locationcol", "idcol"):
					# try: s = oCell.firstChild.name
					# except: pass
				# if s: l += s + colSepar
				# oCell = oCell.next
				
			# # positon info
			# # posInfo = oRow.positionInfo
			# # # example: PosInfo={'level': 1, 'similarItemsInGroup': 973, 'indexInGroup': 971}posInfo = oRow.positionInfo 
			# # # Remarhs:  the level info  and oRow.childcount are both erroneous.
			# # l += " " + str(posInfo['indexInGroup']) + _(" of ") + str(posInfo['similarItemsInGroup'])
			# # # for testing, duration
			# # ms = time () - t
			# # ms = int(ms *1000)
			# # l += ", duration: " + str(ms) 
			# if not l:
				# return "Card, " + str(oRow.name)
			# return l  # + ", Original: " + oRow.name
		# finally:
			# sharedVars.objLooping = False
			
	def event_stateChange(self,obj,nextHandler):
		if sharedVars.logEvents: sharedVars.log(obj, "Event stateChange start: ")
		if obj.role == controlTypes.Role.TAB and controlTypes.State.SELECTED in obj.states:
			# sharedVars.log(api.getFocusObject(), "event_stateChange")
			if utils.hasID(obj.parent, "tabmail-tabs"):
				wx.CallAfter(messengerWindow.tabs.onTabSelect, obj) 
		elif obj.role == controlTypes.Role.PROPERTYPAGE and controlTypes.State.OFFSCREEN not in obj.states:
			ID = str(utils.getIA2Attr(obj))
			messengerWindow.tabs.getTabFromPropertyPage(ID, obj)
			callLater(100, messengerWindow.tabs.onPropertyPageChange, obj)
			if sharedVars.curTab == "main":
				commonVars.cv.propertyPage = obj
		nextHandler()

# # detects content change in the current row of the message liste. When m or s are  pressed for example
		# if obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and  utils.hasID(obj, "threadTree-row"):
			# # sharedVars.logte("nameChange" + str(obj.name))
			# sharedVars.curTTRow = obj.name
			# if sharedVars.TTClean:
				# try:  # 2023 11 05 necessary when quick deletions
					# sharedVars.curTTRowCleaned = self.buildColumnNames(obj)
				# except: 
					# beep(100, 15)
					# sharedVars.curTTRowCleaned = sharedVars.curTTRow
					# pass
		# nextHandler()
		
	# def event_alert (self,obj,nextHandler):
		# # fo = api.getFocusObject()
		# # isThreadTree = utils.hasID(fo, "threadTree") 
		
		# role = obj.role
		# if role != controlTypes.Role.ALERT: return # nextHandler()
		# try:
			# o = obj.getChild(1).firstChild
		# except:
			# return nextHandler()
		# msg = str(o.name)
		# msg = msg.replace("bird Beta", "bird") 
		# #Translators: alert: this is a draft
		# if _("draft") in msg:
			# return
		# #Translators: alert: Thunderbird thinks this message is fraudulent
		# elif _("bird thinks this message is Junk") in msg: # indésirable
			# beep (200, 2)
			# return
		# #Translators: alert: remote content 
		# elif _("remote content") in msg:
			# # beep(250, 70)
			# return
		# #Translators: 2022-12-12 alert X @gmail.com has asked to be notified when you read this message.
		# elif _("notified when you") in msg:  # demande accusé réception
			# if sharedVars.oSettings.getOption("mainWindow", "withoutReceipt"):
				# return
			# #Translators:  Ignore button in alert in TB
			# oBtn = findButtonByName(obj, _("Ignore"))
			# if oBtn:
				# wx.CallLater (30, focusAlert, "", oBtn)
			# return
		# nextHandler

	# def event_NVDAObject_init(self, obj):
		
	def event_alert (self,obj,nextHandler):
		label = ""
		lButtons = []
		# log = "Alert dialog\n"
		for child in obj.recursiveDescendants:
			role = child.role
			ID = str(utils.getIA2Attr(child))
			if role in (controlTypes.Role.LABEL, controlTypes.Role.STATICTEXT):
				lbl = str(child.name)
				if lbl not in label:
					label += ID + "|" + lbl
				else:
					child.name = ""
				# log += label + "\n"
			elif role == controlTypes.Role.BUTTON:
				lButtons.append(child)
				IA2Class = utils.getIA2Attr(child, False, "class") # for addon adding
				if not	 IA2Class: IA2Class = ""
				if "popup-notification-primary" in IA2Class:
					speech.cancelSpeech()
					# sharedVars.logte("button prmary message = " + label)
					child.setFocus()
					# beep(600, 30)
					return # nextHandler()
				# log += "Button Id=" + ID + ", " + str(IA2Class) + " " + str(child.name) + "\n"
		# log += "end alert\n"
		# sharedVars.logte(log)
		#Translators: alert: this is a draft
		if _("draft") in label:
			return
		#Translators: alert: Thunderbird thinks this message is fraudulent
		elif _("bird thinks this message is Junk") in label: # indésirable
			beep (200, 2)
			return
		#Translators: alert: remote content 
		elif _("remote content") in label:
			return
		#Translators: 2022-12-12 alert X @gmail.com has asked to be notified when you read this message.
		elif _("notified when you") in label:  # demande accusé réception
			if sharedVars.oSettings.getOption("mainWindow", "withoutReceipt"):
				return
			else:
				speech.cancelSpeech()
				lButtons[1].setFocus()

		# nextHandler()
		
	# gesture scripts
	@script(
		gesture="kb:tab",
	)
	def script_sharedTab(self, gesture):
		o=api.getFocusObject() 
		ID = str(utils.getIA2Attr(o))
		if ID.startswith("threadTree-row"):
			rc = int(getLastScriptRepeatCount())
			self.initTimer()
			if rc > 0:
				self.timer = wx.CallLater(25, utis.sendKey, keyName="tab", num=2, delay=0.01)
			else:
				self.timer = wx.CallLater(200, specialSendKey, "f6")
			return
		elif utils.isFolderTreeItem(o, ID): 
			return wx.CallAfter(specialSendKey, "f6")
		elif o.role == controlTypes.Role.LISTITEM and utils.hasID(o.parent, "attachmentList"):
			o.parent.previous.doAction()
			return
		elif sharedVars.curTab == "sp:addressbook":
			if utis.TBMajor() > 127:
				nextGesture = messengerWindow.tabAddressBook.getNextControl(o, ID)
				return KeyboardInputGesture.fromName(nextGesture).send()
			# tb 115
			if ID.startswith("searchInput"):
				return KeyboardInputGesture.fromName ("f6").send () 
		return gesture.send()

	@script(
		gesture="kb:escape",
	)
	def script_sharedEscape(self, gesture):
		if sharedVars.curTab == "msgPreview":
			# sharedVars.logte("sharedEscape, curTab = msgPreview, send shift+f6")
			return KeyboardInputGesture.fromName ("shift+f6").send()  
		o=api.getFocusObject()
		role = o.role
		curTreeType = utils.currentTree(o, role)
		if curTreeType == "f":
			if not sharedVars.oSettings.getOption("mainWindow", "ftNoEscape"):
				return KeyboardInputGesture.fromName ("f6").send()  
			else:
				message(o.name + ", " + str(messengerWindow.folderTreeItem.fGetAccountNode(o).name))
		if role == controlTypes.Role.FRAME:
			return KeyboardInputGesture.fromName ("shift+f6").send()
		ID = str(utils.getIA2Attr(o))
		if curTreeType == "t": # threadTree
			if hasFilter(o, ID):
				gesture.send()
				if hasFilter(o, ID):
					gesture.send()
				wx.CallAfter(sayFilterRemoved, o)
			else:
				if not sharedVars.oSettings.getOption("mainWindow", "ttNoEscape"):
					return KeyboardInputGesture.fromName ("shift+f6").send() # utils.getFolderTreeFromFG(True)
				else:
					message(o.name)
		if sharedVars.curTab == "message":
			if role == controlTypes.Role.LISTITEM and utils.hasID(o.parent, "attachmentList"):
				return  KeyboardInputGesture.fromName("shift+f6").send()
		elif  "Recipient" in ID  or "expandedsubjectBox" in ID or "Recipient" in str(utils.getIA2Attr(o.parent)): # header pane
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role ==  controlTypes.Role.TOGGLEBUTTON  and ID.startswith("attachment"):
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role == controlTypes.Role.LISTITEM and utils.hasID(o.parent, "attachmentList"):
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif sharedVars.curTab == "sp:addressbook"   and role !=  controlTypes.Role.MENUITEM:
			if utis.TBMajor() > 127:
				messengerWindow.tabAddressBook.getPreviousControl(o, ID)
			else: # TB 115
				if ID.startswith("cards-row") or ID.startswith("searchInput") or ID.startswith("cards"):
					return KeyboardInputGesture.fromName ("shift+f6").send () 
				elif role == controlTypes.Role.TREEVIEWITEM and (ID.startswith("list") or utils.hasID(o.parent, "books")):
					return KeyboardInputGesture.fromName ("f6").send () 
				elif role == controlTypes.Role.BUTTON:
					return KeyboardInputGesture.fromName ("shift+tab").send () 
				else: return gesture.send()
		elif role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in o.states:
			#sharedVars.debugLog = "sharedEscape document readonly\n"
			context, oFound = utils.whichMessagePane(o, landMark=False)
			# sharedVars.log(oFound, "sharedEscape, context: " + str(context))
			if not oFound:
				#  beep(100, 40)
				return gesture.send()
			elif context == "preview":
					return KeyboardInputGesture.fromName ("shift+f6").send ()
			elif context == "msgWindow":
					# return KeyboardInputGesture.fromName ("alt+f4").send ()
					return KeyboardInputGesture.fromName ("escape").send ()
		elif role ==  controlTypes.Role.LINK: # in preview Pane document or accountCentral doc
			# before 135 Role.INTERNALFRAME, IA2ID: messagepane Tag: browser, States: , FOCUSABLE, childCount: 1 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID: messagepane , 
			# tb 135: level -6: TEXTFRAME, ID: messagePane, class: MozillaWindowClass, childCount: 1
			if utis.TBMajor() < 135:
				if utis.findParentByID(o, controlTypes.Role.SECTION, "messagePane"): return KeyboardInputGesture.fromName("shift+f6").send()
			else: # >= 135
				if utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "messagePane") or utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser"): return KeyboardInputGesture.fromName("shift+f6").send()
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser"): return KeyboardInputGesture.fromName("shift+f6").send()
		if str(utils.getIA2Attr(o.parent)) in "messageEditor,MsgHeadersToolbar":
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape"):
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "quickFilterBarContainer"):
			# if o.value is not None: message(_("Keyword removed."))
			# return gesture.send()
		elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "MsgHeadersToolbar"): # write window
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape"):
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif  role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW, controlTypes.Role.TABLE) and utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "threadTree"):  # modified 2025-01-09
		elif o.parent.role == controlTypes.Role.INTERNALFRAME and  utils.hasID(o.parent, "accountCentralBrowser"):
			return KeyboardInputGesture.fromName ("shift+f6").send () 
		elif role == controlTypes.Role.BUTTON:
			# preview Pane or separate message window:
			context, oFound = utils.whichMessagePane(o, landMark=True)
			# sharedVars.log(oFound, "sharedEscape, context: " + str(context))
			if not oFound:
				#  beep(100, 40)
				pass
			elif context == "preview":
					return KeyboardInputGesture.fromName ("shift+f6").send ()
			elif context == "msgWindow":
					return KeyboardInputGesture.fromName ("escape").send () # was alt+f4
			# level 1,  40 of 51, name: Aller au jour précédent, Role.BUTTON, IA2ID: previous-day-button
			if ID == "previous-day-button": return KeyboardInputGesture.fromName ("shift+f6").send ()
			# spaces button
			if ID in "spacesPinnedButton|folderPaneMoreButton":
				return self.script_sharedGrave(gesture)
			# accountCentral
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser"):
				return KeyboardInputGesture.fromName ("shift+f6").send ()
		return gesture.send()
		
	@script(
		description=_("Announces abbreviated status line and message filtering information if applicable"),
		category=sharedVars.scriptCategory,
		gestures=["kb:alt+end", utis.gestureFromScanCode(12, "kb:alt+")]
	)
	def script_sharedAltEnd(self, gesture):
		# o = api.getFocusObject()
		# if utils.currentTree(o, o.role) == "t"  or utils.hasID(o.parent, "quickFilterBarContainer"):
		if sharedVars.curTab == "main":
			msg = utils.getMessageStatus()
			if not msg: msg = _("Blank")
			message(msg)
			return
		msg = utis.getStatusBarText()
		if not msg: msg = _("Status line without data")
		return message(msg)

	# def script_sharedCtrlTab(self, gesture):
		# # for test
		# return gesture.send()
		# fo = api.getFocusObject()
		# speech.cancelSpeech()
		# # beep(440, 5)
		# direct = (-1 if "shift" in gesture.modifierNames else 1)
		# if not messengerWindow.tabs.changeTab(self, fo, direct):
			# return gesture.send()


	@script(
		gesture="kb:control+t",
		description=_("Smart reply: replies to the sender or to the  group"),
		category=sharedVars.scriptCategory
	)
	def 	script_smartReplyToSender(self, gesture):
		wx.CallLater(25, utils.smartReplyV4,False, 0)

	@script(
		gesture="kb:shift+control+t",
		description=_("Smart reply: with Shift,  replies to all or to the sender in a group"),
		category=sharedVars.scriptCategory
	)
	def script_smartReplyToAll(self, gesture):
		wx.CallLater(25, utils.smartReplyV4, True, 0)
	

	@script(
		gesture=utis.gestureFromScanCode(13, "kb:alt+"),
		description=_("Tabs: Displays the context menu of the selected tab in the main window."),
		category=sharedVars.scriptCategory
	)
	def  script_sharedAltEqual(self, gesture): # native context menu of active tab
		if sharedVars.curFrame == "messengerWindow":
			messengerWindow.tabs.tabContextMenu(self, sharedVars.oCurFrame)
		if sharedVars.curFrame == "msgcomposeWindow":
			msgComposeWindow.msgComposeWindow.sayAllRecipients()

	@script(
		gesture="kb:f5",
		description=_("Write: displays the spell check dialog with the ability to listen to the phrase containing the misspelled word."),
		category=sharedVars.scriptCategory
	)
	def  script_sharedF5(self, gesture): # show tabs menu
		# for  F5   to call spellCheck dialog
		if sharedVars.curFrame != "msgcomposeWindow": return gesture.send()
		oDoc, msg = getComposingDoc() 
		if not oDoc:
			utils.message(msg)
			return KeyboardInputGesture.fromName("f7").send()
		# if not sharedVars.oQuoteNav: 
		sharedVars.initQuoteNav()
		sharedVars.oQuoteNav.setDoc(oDoc, nav=True, fromSpellCheck=True)
		sharedVars.oQuoteNav.setText(0) # speakMode=0 silent
		KeyboardInputGesture.fromName("f7").send()
	
	@script(
		description=_("Tabs: Displays the open tabs menu in the main window."),
		category=sharedVars.scriptCategory,
		gestures=["kb:control+f8", utis.gestureFromScanCode(13, "kb:control+")]
	)
	def  script_sharedCtrlF8(self, gesture): # show tabs menu
		if sharedVars.curFrame != "messengerWindow": return gesture.send()
		speech.cancelSpeech()
		messengerWindow.tabs.showTabMenu(self, api.getFocusObject())

	@script(
		gesture="kb:alt+=",
		description=_("Sends Control+F4 to the current window."),
		category=sharedVars.scriptCategory
	)
	def script_sendCtrlF4(self, gesture):
		if "shift"  in gesture.modifierNames:  return gesture.send()
		fo = api.getFocusObject()
		if gesture.mainKeyName == "backspace":
			if fo.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT) and controlTypes.State.READONLY  not in fo.states:
				return gesture.send()
		KeyboardInputGesture.fromName("control+f4").send()

	@script(
		description= _("In the main window, 1 press: Alt+1 to 8: reads the message header, 2 presses: displays the header in an edit box, 3 presses: reaches the header in the headers area. In the Write window, Alt1 to 4, reads the headers, 2 presses reaches the header."),
		category=sharedVars.scriptCategory,
		gestures=["kb:alt+1", "kb:alt+2", "kb:alt+3", "kb:alt+4", "kb:alt+5", "kb:alt+6", "kb:alt+7", "kb:alt+8"]
	)
	def script_sharedAltN(self, gesture):
		fo = api.getFocusObject()
		if fo and fo.role == controlTypes.Role.MENU: return
		self.initTimer () # cancels running timer
		rc = int(getLastScriptRepeatCount())
		ID = str(utils.getIA2Attr(fo))
		parID = str(utils.getIA2Attr(fo.parent))
		# sharedVars.logte("SharedAltN parentID=" + parID)
		mk = int(gesture.mainKeyName)
		# compose window
		if parID in ("MsgHeadersToolbar", "messageEditor"):
			# self.initTimer ()
			if rc > 0:
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, mk, rc)
			else:
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, mk, rc)
			return
		elif ID.startswith("threadTree") or parID == "messagepane":
			# message list
			if ID.startswith("threadTree") and controlTypes.State.SELECTED not in fo.states: # for TB 128
				fo.doAction()
				sleep(0.1)
			delay = 10 if rc == 0 else 300
			self.timer = wx.CallLater(delay, utils.getHeader, fo, mk, rc)

	@script(
		description= _("Thunderbird+G5: alt arrow gestures, do not change"),
		gestures=["kb:alt+downArrow", "kb:alt+upArrow", "kb:alt+leftArrow", "kb:alt+rightArrow", "kb:alt+shift+downArrow"]
	)
	def script_sharedAltArrow(self, gesture):
		mainKey = gesture.mainKeyName
		fo = o =   api.getFocusObject()
		role = o.role
		# Optimization for write window
		if role == controlTypes.Role.DOCUMENT and mainKey in ("leftArrow", "rightArrow"): return gesture.send() 
		if mainKey in ("downArrow", "upArrow"): 
			if not sharedVars.oQuoteNav: sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
			if role == controlTypes.Role.DOCUMENT:
				return sharedVars.oQuoteNav.readMail(fo , o,(mainKey == "upArrow")) # with quote list
			ID = str(utils.getIA2Attr(o))
			if ID.startswith("threadTree-row"):
				if controlTypes.State.COLLAPSED in o.states: 
					# sending right arrow after  a alt+downArrow does not work
					return message(_("Press right arrow and retry, please."))
				utils.setMLIState(o) # select or expand
				for i in range(0, 20):
					o2, retryNeeded = utils.getPreviewDoc()
					if o2 is not None: 
						o = o2
						break
					if not retryNeeded: break
					sleep(0.1)
					api.processPendingEvents()
				if o is None: 
					beep(110, 10)
					return 
				return sharedVars.oQuoteNav.readMail(fo, o,(mainKey == "upArrow")) # with quote list
			elif utils.isFolderTreeItem(o, ID):
				# sharedVars.log(o, "folderTreeItem before call of fmenuFolder")
				return messengerWindow.folderTreeItem.fMenuFolders(o, (mainKey == "downArrow"))
			elif  ID.startswith("ReplaceWordInput"): 
				# spellCheckDialog
				if mainKey == "upArrow":
					return fo.script_reportFocus(gesture)
				elif mainKey == "downArrow":
					return o.script_focusSuggested(gesture)
			elif  utils.hasID(o.parent, "SuggestedList"):
				# spellCheckDialog
				return o.script_focusEdit(gesture)
		return gesture.send()

	@script(
		gesture="kb:f4",
		description=_("Filtered reading of the document in the preview pane, reading tab, reading or Write window, from the list of messages or the document."),
		category=sharedVars.scriptCategory
	)
	def script_sharedF4(self, gesture):
		# document or preview reading
		if not sharedVars.oQuoteNav: sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		o = api.getFocusObject()
		role = o.role
		if role in  (controlTypes.Role.DOCUMENT, controlTypes.Role.LINK):
			return sharedVars.oQuoteNav.readMail(o, o, ("shift" in gesture.modifierNames))
		elif   utils.hasID(o, "threadTree-row"):
			fo = o
			utils.setMLIState(o)
			for i in range(0, 20):
				o2, retryNeeded = utils.getPreviewDoc()
				if o2 is not None: 
					o = o2
					break
				if not retryNeeded: break
				sleep(0.1)
				api.processPendingEvents()
			if o is None: 
				beep(110, 40)
				return gesture.send()
			else: return sharedVars.oQuoteNav.readMail(fo, o, ("shift" in gesture.modifierNames))
		else: return gesture.send()

	# @script(
		# gesture="kb:nvda+s",
		# description=_("Toggles NVDA speech modes and notifies Thunderbird+G5"),
		# category = sharedVars.scriptCategory
	# )
	# def script_toggSpeechMode(self, gesture):
		# globalCommands.commands.script_speechMode(gesture)
		# commonVars.cv.defaultSpeechMode =  utis.getSpeechMode()
		# beep(440, 40)

	@script(
		gesture="kb:scrolllock",
		description=_("Enables or disables  the translation mode of a message."),
		category = sharedVars.scriptCategory
	)
	def script_toggleTranslation(self, gesture):
		if not sharedVars.oQuoteNav: sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		sharedVars.oQuoteNav.toggleTranslation()

	@script(
		gesture="kb:shift+scrolllock",
		description=_("Enables or disables the display of the cleaned or translated   message in a window."),
		category = sharedVars.scriptCategory
	)
	def script_toggleBrowseMessage(self, gesture):
		if not sharedVars.oQuoteNav: sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		sharedVars.oQuoteNav.toggleBrowseMessage()

	@script(
		gesture="kb:alt+c",
		description=_("Folders: displays the accounts menu then  the folders menu for the chosen account."),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltC(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		# type 1: read and unread
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAccounts, 1)


	@script(
		gesture="kb:alt+x",
		description=_("Folders: displays the menu of all inbox folders"),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltX(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuInboxes, False)

	@script(
		gesture="kb:alt+v",
		description= _("Folders: displays the menu of unread inbox folders"),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltV(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuInboxes, True)

	@script(
		gesture="kb:alt+b",
		description=_("Folders:, displays the menu of all folders"),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltB(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=False)

	@script(
		gesture="kb:alt+w",
		description=_("Folders:, displays the menu of all unread folders"),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltW(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAllFolders, unRead=True)


	@script(
		gesture="kb:alt+control+c",
		description=_("Folders: displays the accounts menu then the unread folders menu for the chosen account."),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltCtrlC(self, gesture):
		if sharedVars.curTab !=  "main": return gesture.send()
		# type 2: unread only
		wx.CallLater(50, messengerWindow.folderTreeItem.fMenuAccounts, 2)

	@script(
		gesture="kb:alt+home",
		description=_("Focus: 1 press select the current folder in the folder tree, 2 presesses display a menu  allowings to choose an mail account to reach in the folder tree"),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltHome(self, gesture):
		# if sharedVars.curTab != "main": return gesture.send()
		rc = int(getLastScriptRepeatCount())
		d = 100
		self.initTimer ()
		if rc == 0: # 1 press: search new update 
			self.timer = wx.CallLater(d, utils.getFolderTreeFromFG, True)
		elif rc == 1: # 1 press: search new update 
			tp = 2 if "control" in gesture.modifierNames else 1
			self.timer = wx.CallLater(d, messengerWindow.folderTreeItem.fMenuAccounts, tp)

	@script(
		gesture="kb:" + kGrave, 
		description="Thunderbird+G5: various usages of the key above Tab",
	)
	def script_sharedGrave(self, gesture):
		fo = api.getFocusObject()
		if fo.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT) and controlTypes.State.READONLY not in fo.states:
			return gesture.send()
		if sharedVars.curTab == "main":
			speech.setSpeechMode(speech.SpeechMode.off)
			return callLater(50, applyFocusMode)
		elif sharedVars.curTab == "sp:addressbook":
			return self.script_showContextMenu(None)
		elif  sharedVars.curFrame == "messengerWindow":
			speech.setSpeechMode(speech.SpeechMode.off)
			messengerWindow.tabs.selectTab(None, 0)
			return callLater(50, applyFocusMode)
		return gesture.send()
		fo = api.getFocusObject()
		if not commonVars.cv.propertyPage and fo.role == controlTypes.Role.FRAME:
				return KeyboardInputGesture.fromName("shift+f6").send()
		# determine curFrame and curTab
		utils.setCurFrameTabFromFO(fo)
		# msg = "curTab: {}, curFrame: {}".format(sharedVars.curTab, sharedVars.curFrame)
		# message(msg)
		# return
		if sharedVars.curFrame != "messengerWindow"  or getLastScriptRepeatCount() > 0: return gesture.send()
		if sharedVars.curTab == "main" and utils.hasID(fo, "threadTree-"):
			# focus modes: 0 nothing, 1: last msg, 2: first msg, 3: first unread, 4: folderTree
			gestList = ["", "end", "home", "n", "shift+f6"] 
			focusMode = 4 # sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
			if focusMode > 0:
				wx.CallAfter(KeyboardInputGesture.fromName(gestList[focusMode]).send)
			
			# # we are not in folderTree nor in threadTree
			# wx.CallAfter(utils.getFolderTreeFromFG, focus=True)
		# elif sharedVars.curTab == "sp:addressbook":
			# return self.script_showContextMenu(None)
		# else: # other active tab, we activate the first tab 
			# if not messengerWindow.tabs.activateTab(self, api.getFocusObject(), 0):
				# return gesture.send()

	@script(
		gestures=["kb:alt+pageDown", "kb:alt+9"],
		description=_("Attachments: announces or displays the attachment pane."),
		category =sharedVars.scriptCategory
	)
	def script_sharedAltPageDown(self, gesture):
		fo = api.getFocusObject()
		ID = str(utils.getIA2Attr(fo))
		parID = str(utils.getIA2Attr(fo.parent))
		rc = int(getLastScriptRepeatCount())
		if parID in ("MsgHeadersToolbar", "messageEditor"): # write window 
			self.initTimer ()
			if rc > 0:
				self.timer = wx.CallLater(10, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, 3, rc)
			else:
				self.timer = wx.CallLater(20, msgComposeWindow.msgComposeWindow.getComposeHeader, fo, 3, rc)
			return
		elif ID.startswith("threadTree") or parID == "messagepane"  or fo.role == controlTypes.Role.LINK:
			if ID.startswith("threadTree") and not utils.getMessagePane():
				return message(_("The headers pane is not displayed. Please press F8 then try again"))
			if ID.startswith("threadTree") and controlTypes.State.COLLAPSED in fo.states:
				# beep(432, 2)
				self.counter += 1
				utis.sendKey("rightArrow", num=1, delay=0.05)
				return wx.CallLater(100, self.script_sharedAltPageDown, gesture)
			self.counter = 0
			# sharedVars.log(fo,"altPageDown focus")
			self.initTimer ()
			if rc> 0: 
				# beep(440, 40)
				self.timer = wx.CallLater(10, utils.getAttachment, fo, rc)
				return
			elif rc == 0: 
				self.timer = wx.CallLater(200, utils.getAttachment, fo, rc)
				return
		return gesture.send()

	@script(
		description= _("Navigates through quotes in a message"),
		category=sharedVars.scriptCategory,
		gestures=["kb:control+windows+downArrow", "kb:control+windows+upArrow", "kb:control+windows+leftArrow", "kb:control+windows+rightArrow"]
	)
	def script_sharedWinArrow(self, gesture):
		# quote navigator
		beep(440, 5)
		mainKey = gesture.mainKeyName
		if not sharedVars.oQuoteNav:
			return message(_("Press alt+upArrow before navigating through quotes in a message."))
		if mainKey == "upArrow":
			sharedVars.oQuoteNav.skipLine(-1)
		elif mainKey == "downArrow":
			sharedVars.oQuoteNav.skipLine()
		if mainKey == "leftArrow":
			sharedVars.oQuoteNav.skipQuote(-1)
		elif mainKey == "rightArrow":
			sharedVars.oQuoteNav.skipQuote()

	@script(
		gesture="kb:control+" + kGrave,
		description=_("Shows the context menu of actions available in the various Thunderbird windows."),
		category=sharedVars.scriptCategory
	)
	def script_showContextMenu(self, gesture):
		if getLastScriptRepeatCount () > 0: return gesture.send()
		if sharedVars.curTab == "sp:addressbook":
			o = api.getFocusObject()
			if hasattr(o, "script_menuAB"):
				o.script_menuAB(gesture)
		elif sharedVars.curFrame == "messengerWindow":
			oMenu = messengerWindow.menuMain.MainMenu(self)
			oMenu.showMenu(api.getFocusObject())
		elif sharedVars.curFrame == "msgcomposeWindow":
			if api.getFocusObject().role != controlTypes.Role.DOCUMENT: return
			oMenu = msgComposeWindow.menuCompose.ComposeMenu(self)
			oMenu.showMenu()

	@script(
		gesture="kb:shift+" + kGrave,
		description=_("Shows the Options context menu of Thunderbird+"),
		category=sharedVars.scriptCategory
	)
	def script_showOptionMenu(self, gesture):
		repeats = getLastScriptRepeatCount ()
		if sharedVars.curFrame != "msgcomposeWindow":
			sharedVars.oSettings.showOptionsMenu(sharedVars.curFrame) # menu dépendant du frame actif
		else:  # msgcomposeWindow
			self.initTimer()
			if not sharedVars.oSettings.getOption("msgcomposeWindow", "onePress"): # not onePress to showMenu
				if repeats > 0:
					self.timer = wx.CallLater(10, sharedVars.oSettings.showOptionsMenu, sharedVars.curFrame)
				elif repeats == 0: 
					self.timer = wx.CallLater(200, gesture.send)
			else: # menu with onePress
				if repeats > 0:
					self.timer = wx.CallLater(10, gesture.send)
				elif repeats == 0: # (dblPress and repeats== 0) or (not dblPress and repeats == 1): 
					self.timer = wx.CallLater(200, sharedVars.oSettings.showOptionsMenu, sharedVars.curFrame) # menu dépendant du frame acti
			return

	@script(
		# gesture="kb:alt+d",
		description="\u9fff" + "Reserved, edit a timeout to tests",
		category = sharedVars.scriptCategory
	)
	def script_sharedAltD(self,gesture):
		# Remark: this script cannot be renamed because this will deactivate all other scripts.
		desc = _("Shows the dialog for editing the delay before reading the message of the separate reading window.")
		if sharedVars.curFrame == "messengerWindow":
			wx.CallLater(10, sharedVars.oSettings.editDelay)
			return
		return gesture.send()

	@script(
		gesture="kb:alt+delete",
		description=_("Shows the dialog for editing the two delays used for focusing after deleting a message."),
		category=sharedVars.scriptCategory
	)
	def script_sharedAltDelete(self,gesture):
		if sharedVars.curFrame == "messengerWindow":
			wx.CallLater(20, sharedVars.oSettings.editDeleteDelays)
			return
		return gesture.send()

	@script(
		gesture="kb:f8",
		description=_("Turn on or off the preview messages panel"),
		category = sharedVars.scriptCategory
	)
	def script_previewPane(self, gesture):
		if api.getFocusObject().role not in (controlTypes.Role.TREEVIEWITEM , controlTypes.Role.LISTITEM): 
			return gesture.send()
		KeyboardInputGesture.fromName ("f8").send()
		if sharedVars.debug: sharedVars.debugLog = "Search for previewPane\n"
		o =  utils.getMessagePane()
		if o is not None:
			message(_("Present: Headers and message pane."))
		else:
			message(_("Missing: headers and message pane."))

	@script(
		gesture="kb:control+f1",
		description = _("Shows the add-on help in a web page"),
		category = sharedVars.scriptCategory
	)
	def script_showHelp(self, gesture):
		utis.showHelp()

	@script(
		gesture="kb:alt+f12",
		description ="Thunderbird+G5, displays debug dialog",
	)
	def script_displayDebug(self, gesture):
		debugShow(self, False)

	@script(
		gesture="kb:control+windows+f12",
		description ="Thunderbird+G5, displays ascendants and descendants of the focused control",
	)
	def script_listObjects(self, gesture):
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


	@script(
		gesture="kb:windows+f12",
		description ="Thunderbird+G5, initialize debug",
	)
	def script_initDebug(self, gesture):
		if not sharedVars.oQuoteNav: sharedVars.initQuoteNav()
		if sharedVars.oQuoteNav.debug:
			sharedVars.oQuoteNav.debug = False
			message("Debug Microsoft Headers    is disabled")
		else:
			sharedVars.oQuoteNav.debug = True
			message("Debug Microsoft Headers    is  enabled")


		# if sharedVars.logEvents:
			# sharedVars.logEvents = False
			# message("logEvents mode is disabled")
		# else:
			# sharedVars.logEvents = True
			# message("logEvents mode is enabled")

	__gestures = {
		# utis.gestureFromScanCode(41, "kb:"):"showContextMenu", # 41 is the scancode of the key above Tab
		# utis.gestureFromScanCode(41, "kb:shift+"):"showOptionMenu", 
		#"kb(desktop):NVDA+End": "statusBar",
		"kb:tab": "sharedTab",
		"kb:escape": "sharedEscape",
		"kb:alt+1": "sharedAltN",
		"kb:alt+2": "sharedAltN",	
		# utis.gestureFromScanCode(3, "kb:alt+"):"sharedAltN", # 41 is the scancode of the key above Tab
		"kb:alt+3": "sharedAltN",	
		# utis.gestureFromScanCode(4, "kb:alt+"):"sharedAltN", # 41 is the scancode of the key above Tab
		"kb:alt+4": "sharedAltN",
		"kb:alt+5": "sharedAltN",
		"kb:alt+6": "sharedAltN",
		"kb:alt+7": "sharedAltN",
		"kb:alt+8": "sharedAltN",
		"kb:alt+9": "sharedAltPageDown", # attachments
		"kb:alt+home": "sharedAltHome",
		"kb:alt+control+home": "sharedAltHome",
		"kb:shift+f4": "sharedF4",
		"kb:alt+End": "sharedAltEnd",
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
		# "kb:alt+pageup": "smartReplyToSender", # smart reply
		# "kb:control+w": "sendCtrlF4",
		# _("kb:shift+control+²"):"showOptionMenu",
		# _("kb:control+²"):"showContextMenu",
		"kb:alt+d":"sharedAltD",
		"kb:alt+delete":"sharedAltDelete",
		"kb:f8":"previewPane",
		"kb:control+f1": "showHelp",
		"kb:windows+f12": "initDebug",
		"kb:windows+control+f12": "listObjects"
	}

def debugShow(appMod, auto):
	# sharedVars.debugLog += "Debug mode: {}, TB branch: {}".format(str(sharedVars.debug), utis.TBMajor()) + "\n" + "\n" + "\n" + sharedVars.debugLog
	# utils.setBrailleMode()
	# sharedVars.logte("Braille Mode after setBrailleMode: " + str(utils.getBrailleParam("mode")))
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
	# if no.role == controlTypes.Role.GRAPHIC:
		# utils.listAscendants(-6, no, "Nav Object * Ascendents")
		# utils.listDescendants(no, 0, "* Nav object   descendants")
		# textDialog.showText(title="Log", text=sharedVars.debugLog)
		# return

	# textDialog.showText(title="Log", text=sharedVars.debugLog)
	# sharedVars.test(no, "Nav object")
	# if utils.hasID(fo, "threadTree-row"	):
		# sharedVars.logte("Current row original name:\n" + sharedVars.curTTRow)
		# utils.listAscendants(-6)
		# utils.listDescendants(fo, 0, "* List of descendants")
		# utils.listColumnNames(fo) 
	# else:
		# utils.listAscendants(-6)
		# utils.listDescendants(fo, 0, "* List of descendants")
	#sharedVars.debugLog += "\ncurFrame: {0}, curTab: {1},".format(appMod.curFrame, sharedVars.curTab) + "\n"
	sharedVars.debugLog += "\ncurTab: {0}, curFrame: {1},".format(sharedVars.curTab, sharedVars.curFrame) + "\n"
	# sharedVars.test(None, "sharedVars.curSubject:" + sharedVars.curSubject)
	# if sharedVars.oQuoteNav:
		# sharedVars.test(None, "oQuoteNav.subject: " + sharedVars.oQuoteNav.subject)
	# sharedVars.test(None, "GroupingIdx = " + str(sharedVars.groupingIdx))
	# ui.browseableMessage (message = sharedVars.debugLog, title = "TB+G5 log", isHtml = False)
	textDialog.showText(title="Log", text=sharedVars.debugLog)
	if not auto: 
		sharedVars.debugLog = ""

from keyboardHandler import KeyboardInputGesture


# normal function
def specialSendKey(key):
	KeyboardInputGesture.fromName (key).send() 
	sleep(.05)
	api.processPendingEvents()

# functions for event alert
def focusAlert (message, oButton):
	speech.cancelSpeech()
	speech.speak ([message])
	if oButton:
		oButton.setFocus()

def findButtonByName(o, nm):
	o = o.firstChild
	while o is not None:
		r = (o.role if hasattr(o, "role") else 0)
		if r == 9:
			if nm in str(o.name): return o
		o = o.next
	return None


def hasFilter(o, ID=None):
	if utis.TBMajor() > 127: 
		tp = utis.findParentByID(o,controlTypes.Role.SECTION, "threadPane")
		cnt, inf = utils.getFilterInfos128(tp)
		return True if cnt else False
	
	# TB 115
	if not ID:
		ID = str(utils.getIA2Attr(o))
	if ID.startswith("threadTree-row"):
		o = utis.findParentByID(o,controlTypes.Role.TEXTFRAME, "threadTree")
	# sharedVars.log(o.parent, "parent of threadTree and qfb")
	while o is not None:
		# sharedVars.log(o, "previous ")
		if utils.hasID(o, "quick-filter-bar"): break
		if o.previous: o = o.previous
		else: break
	# 7,        0 of 1, Role.SECTION, IA2ID: quickFilterBarContainer Tag: div, States: , childCount: 9 Path: Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i1, Role-SECTION, , IA2ID: quick-filter-bar | i0, Role-SECTION, , IA2ID: quickFilterBarContainer , IA2Attr: id: quickFilterBarContainer, display: flex, tag: div,  ;
	try:
		o = o.firstChild.getChild(1)
		# sharedVars.log(o, "focusEntered, editabe")
		while o is not None:
			role = o.role
			if role == controlTypes.Role.EDITABLETEXT and o.value: return True
			if role ==  controlTypes.Role.TOGGLEBUTTON and controlTypes.State.PRESSED in o.states: return True
			o = o.next
	except:  pass
	
	return False

def sayFilterRemoved(oCurRow):
	speech.cancelSpeech()
	infos  =  utils.getMessageStatus128()
	fo = api.getFocusObject()
	role = fo.role
	if role in (controlTypes.Role.TABLE, controlTypes.Role.LIST, controlTypes.Role.TREEVIEW):
		cc = fo.childCount
		if cc == 0:
			beep(120, 40)
			infos = _("No messages displayed") + ", " + infos
	name = ""
	if oCurRow is not None and hasattr(oCurRow, "name"):
		name = " " + oCurRow.name
	message(_("Filter removed") + infos+ name)

def activateMenuItem(o, ID):
	# called after press on delete key in the message list
	# o is role.popupmenu
	try: # finally
		o = o.firstChild 
		while o is not None:
			if o.role == controlTypes.Role.MENUITEM and utils.hasID(o, ID):
				o.doAction()
				return
			o = o.next
	finally:
		# speech.setSpeechMode(commonVars.cv.defaultSpeechMode)
		utis.setSpeech(True)

def getComposingDoc():
	errMsg = _("NVDA Object  not found:")
	if not sharedVars.msgComposeBox:
		beep(100, 30)
		return None, errMsg + " Compose box."

	# IA2ID = messageArea in , Role.SECTION
	o = utils.getChildByRoleIDName(sharedVars.msgComposeBox, controlTypes.Role.SECTION, ID="messageArea", name="", idx=3)
	if o is None: return None, errMsg + " section message area."
	# IA2ID = messageEditor in , Role.INTERNALFRAME
	o = utils.getChildByRoleIDName(o, controlTypes.Role.INTERNALFRAME, ID="messageEditor", name="", idx=0)
	if o is None: return None, errMsg + " internal frame message editor."
	# Translators: Corps du message
	o = utils.getChildByRoleIDName(o, controlTypes.Role.DOCUMENT, ID="", name="", idx=0)
	if o is None: return None, errMsg + " document."
	return o, "document found"

def sayColumnOrder(oCol, colID) :
	if oCol is None : return
	# Different roles between old and new version of TB :
	# TB < 155 :  level -1 TABLECOLUMNHEADER, ID: statusCol, States:   In screen   , childCount: 2MozillaWindowClass,  TB < 155 :  level -1 TABLECOLUMNHEADER, ID: statusCol, States:   In screen   , childCount: 2MozillaWindowClass, name: Statut
	# TB 155: level -1 TEXTFRAME, ID: statusCol, States:   In screen   , childCount: 2MozillaWindowClass, name: Statut
	# in old versions, the index of moved col is announced, not from versions 15x
	if  oCol.parent.role == controlTypes.Role.TABLECOLUMNHEADER : return
	# TB 155 : level -2 TOOLBAR, ID: None, States:   In screen   , childCount: 8MozillaWindowClass,  class: ,
	oTextFrame = oCol.parent.parent.firstChild
	i = 1
	while oTextFrame is not None:
		tfID = str(utils.getIA2Attr(oTextFrame))
		if tfID in colID :
			message(str(i))
			return
		i += 1
		oTextFrame = oTextFrame.next
	# end for