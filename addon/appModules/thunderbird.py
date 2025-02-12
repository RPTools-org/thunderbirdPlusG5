# ThunderbirdPlusG5 for Thunderbird 115+

from nvdaBuiltin.appModules import thunderbird
from time import time, sleep
from datetime import datetime
try:
	from NVDAObjects.IAccessible.mozilla import BrokenFocusedState as IAccessible
except ImportError:
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
from re import compile,IGNORECASE

# shared modules import
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import utis, sharedVars, utils115 as utils # , sendInput
import  langUtils
import textDialog
# dbg = sharedVars.log
# from  py3compatibility import *
# from  py3compatibility import utis._unicode
del sys.path[-1]
addonHandler.initTranslation()
import api

sharedVars.scriptCategory = _curAddon.manifest['summary']

# Extension modules import
from . import messengerWindow, msgComposeWindow # , addressbookWindow
from scriptHandler import getLastScriptRepeatCount
def TBStartup() :
	#  sharedVars.objLooping was  set tot  True in __init__
	sharedVars.TBMajor = utis.versionTB()
	o =  api.getFocusObject()
	if o.role != controlTypes.Role.FRAME  or  not utils.hasID(o.getChild(1), "toolbar-context-menu"):
		return utis.disableOvl(False)
	
	# focus modes : 0 nothing, 1 : last msg, 2 : first msg, 3 : first unread, 4 : folderTree
	focusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
	focusOnStartup = sharedVars.oSettings.getOption("messengerWindow","focusOnStartup", kind="b")

	if not focusOnStartup or not focusMode :  
		return utis.disableOvl(False)
		# StartWithInbox preselected the folderTree
	if sharedVars.oSettings.getOption("messengerWindow","focusStartWithInbox", kind="b"):
		utis.disableOvl(False)
		if focusMode == 4 : 
			return # folderTree 
		# for i in range(0, 5) :
			# goodRole = False
			# if hasattr(o, "role") :
				# if o.role == controlTypes.Role.TREEVIEWITEM : goodRole = True
			# if goodRole and utils.focusTTFromFT(fo, focusMode) :
				# break
			# sleep(.5)
			# o = api.getFocusObject()
		# else :
			# beep(150, 60)
		oTimer = utils.GetFocusObjTimer(roleList=[controlTypes.Role.TREEVIEWITEM], stateSelected=True, interval=500, maxElapsed=7000, callBack=utils.focusTTFromFT, cbParam=focusMode)
		oTimer.run()
		return
	fo = activateTB()
	if not fo or fo.role != controlTypes.Role.FRAME :
		return utis.disableOvl(False)
	for i in range(0, 5) :
		oPP = utils.getPropertyPage()
		# sharedVars.log(oPP, "oPP " +str(i) + "=")
		if oPP :
			break
		beep(250, 5)
		sleep(.5)
	if not fo : 
		return utis.disableOvl(False)
	# sharedVars.log(fo, "First startup")
	if  fo.role != controlTypes.Role.FRAME  :  
		return utis.disableOvl(False)
	# we select the first tab
	# sharedVars.logte("Select first tab")
	oTab , idx, lastIdx = messengerWindow.tabs.findCurTab(fo)
	if idx > 0 :
		t = oTab.parent.firstChild
		t.doAction()
		sleep(.1)
		fo.setFocus()

	# startup modes : 1 : last msg, 2 : first msg, 3 : first unread, 4 : folderTree
	# ui.message("focusMode = [{}]".format(focusMode))		# getThreadTree first
	# utis.beepRepeat(440, 10, 3) 
	# sharedVars.logte("Search for folderTree")
	for i in range(0, 5) :
		# sharedVars.logte("Search FolderTree i=" + str(i))
		o = utils.getFolderTreeFromFG(focus=False, pp=oPP)
		if o : break
		oPP = None
		sleep(1.0)	
		
	# sharedVars.log(o,"After getFFolderTree") 
	if not o : 
		# core.callLater
		callLater(1500, utis.sendKey, "f")
		speech.setSpeechMode(speech.SpeechMode.talk)
		return utis.disableOvl(False)
	o.setFocus()
	if focusMode == 4 :  # folder Tree
		return utis.disableOvl(False)
	utis.setSpeechMode_off()
	oTimer = utils.GetFocusObjTimer(roleList=[controlTypes.Role.TREEVIEWITEM], stateSelected=True, interval=500, maxElapsed=7000, callBack=utils.focusTTFromFT, cbParam=focusMode)
	oTimer.run()

class ListTreeView(IAccessible) :
	def initOverlayClass (self):
		self.bindGesture ("kb:f", "goFilterBar")
	def script_goFilterBar(self, gesture) :
		if sharedVars.curTab != "main" : return gesture.send() 
		KeyboardInputGesture.fromName ("shift+control+k").send() 

class AppModule(thunderbird.AppModule):
	timer = None
	counter = 0

	def __init__(self, *args, **kwargs):
		super(thunderbird.AppModule, self).__init__(*args, **kwargs)
		# Thunderbird+G5
		utis.disableOvl(True)
		speech.cancelSpeech()
		self.disabMode = 0
		# self.columnID= []
		#ui.message("TBStep : " + str(globalVars.TBStep))
		sharedVars.initSettingsMenu(self) # then use  sharedVars.oSettings.*
		# initQuotenav  will be run at first use of quote Navigator >sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		self.regExp_nameListGroup, self.regExp_AnnotationResponse, self.regExp_mailAddress  =compile ("\[.*\]|\{.*\}"), compile("re[ ]*:[ ]", IGNORECASE), compile ("\S+?@\S+?\.\S+")
		# self.regExp_listGroupName = compile ("\[(.*)\]") # |\{?*\}") # first occurrence of the list group name
		self.regExp_removeMultiBlank =compile (" {2,}")
		self.regExp_removeSymDigits =compile ("\d+|&|_|@.+|=|\.| via .*")
		self.regExp_removeSymbols =compile (r"&|_|@.+|=|\. | via .*")
		#wx.CallLater(25000, debugShow, self, True)
		k =  utis.gestureFromScanCode(41)
		self.bindGesture("kb:control+" + k, "showContextMenu") # 41 is the scancode of the key above Tab
		self.bindGesture("kb:shift+" + k,  "showOptionMenu") 
		self.bindGesture("kb:" + k, "sharedGrave") # 41 is the scancode of the key above Tab
		callLater(1500, TBStartup)

		
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
			return messengerWindow.tabs.setCurFrameTab(obj)
		
		if sharedVars.curFrame == "messengerWindow"and role == controlTypes.Role.DOCUMENT :
			if obj.name : sharedVars.curWinTitle = obj.name
			obj.name = ""
			# sharedVars.curTab = messengerWindow.tabs.getTabTypeFromName(obj.name, "document")
			# return
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
				# if sharedVars.TTFillRow : self.fillRow(obj)
				clsList.insert(0, messengerWindow.messageListItem.MessageListItem)
				return
			if role == controlTypes.Role.TREEVIEWITEM and utils.isFolderTreeItem(obj, ID) :
				clsList.insert(0, messengerWindow.folderTreeItem.FolderTreeItem)
				sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "main"
				return
		# spellCheck dialog
		if   obj.windowClassName == "MozillaDialogClass" :
			# if ID.startswith("ReplaceWordInput") or  utils.hasIA2Class(obj, "spell-check") : #  or (role == controlTypes.Role.LISTITEM and utils.hasID(obj.parent, ""SuggestedList")) :
			if ID.startswith("ReplaceWordInput") or (role == controlTypes.Role.LISTITEM and utils.hasID(obj.parent, "SuggestedList")) :
				# sharedVars.log(obj, "Spellcheck control")
				sharedVars.curTab = sharedVars.curFrame = "spellcheckDlg"
				clsList.insert (0,msgComposeWindow. spellCheckDlg.SpellCheckDlg); return
		# special tabs documents 
		# if role == controlTypes.Role.DOCUMENT : 
			# parID = str(utils.getIA2Attr(obj.parent))
			# if parID == "messagepane" : sharedVars.curTab = "main" ; return
			# elif  parID.startswith("addressBookTab") : sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "sp:addressbook" ; return
			# else : sharedVars.curTab = messengerWindow.tabs.specialTabType(obj.name, True)

		if sharedVars.curTab == "sp:addressbook" :
			if not  sharedVars.noAddressBook :  # and role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.BUTTON, controlTypes.Role.EDITABLETEXT) :
				if sharedVars.TBMajor < 128 :  clsList.insert(0, messengerWindow.tabAddressBook.AddressBook115)
				else : clsList.insert(0, messengerWindow.tabAddressBook.AddressBook)

	def event_foreground(self, obj,nextHandler):
		# sharedVars.log(obj, "Foreground")
		if obj.role == controlTypes.Role.DIALOG :
			if "|dlg" not  in sharedVars.curFrame : sharedVars.curFrame += "|dlg"
			# sharedVars.log(obj, "Dialog, curframe = " +  sharedVars.curFrame) 
		elif  obj.role == controlTypes.Role.FRAME :
			sharedVars.curFrame = sharedVars.curFrame.replace("|dlg", "")
			# sharedVars.log(obj, "FRAME, curframe = " +  sharedVars.curFrame) 
		nextHandler()

	def event_NVDAObject_init(self, obj):
		if self.disabMode == 2 : return
		
		if sharedVars.curTab != "main" : return
		if obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and  utils.hasID(obj, "threadTree-row") :
			# if controlTypes.State.SELECTED not in obj.states : 
				# obj.doAction()
				# beep(100, 60)
				# ui.message(obj.name)
			if not sharedVars.TTClean : 
				sharedVars.curTTRow = obj.name
				return

			# sharedVars.logte("objectInit TTI:" + sharedVars.curTTRow)
			try :  # 2023 11 05 necessary when quick deletions
				sharedVars.curTTRow = str(obj.name) 
				obj.name = self.buildColumnNames(obj)
				if not sharedVars.curTTRow : sharedVars.curTTRow = obj.name
			except : 
				#beep(100, 15)
				sharedVars.curTTRow = "Error rebuilding row"

	# def fillRow(self, obj) :
			# try :  # 2023 11 05 necessary when quick deletions
				# sharedVars.curTTRowCleaned = self.buildColumnNames(obj)
				# obj.name = sharedVars.curTTRowCleaned 
				# sharedVars.curTTRow = sharedVars.curTTRowCleaned 
			# except : 
				# beep(100, 15)
				# sharedVars.curTTRowCleaned = "Error rebuilding row"
			

	# def customizeRow(self, obj) :
		# sharedVars.curTTRow = str(obj.name)
		# if not sharedVars.TTClean  :
			# sharedVars.curTTRowCleaned = sharedVars.curTTRow 
			# return
		# try :  # 2023 11 05 necessary when quick deletions
			# sharedVars.curTTRowCleaned = self.buildColumnNames(obj)
		# except : 
			# beep(100, 15)
			# sharedVars.curTTRowCleaned = sharedVars.curTTRow


	def event_gainFocus (self,obj,nextHandler):
		if sharedVars.speechOff :
			speech.setSpeechMode(speech.SpeechMode.talk)
			sharedVars.speechOff = False

		if  sharedVars.curFrame == "msgcomposeWindow" :
			# beep(440, 5)
			nextHandler()
			return
		if self.disabMode == 3 : return nextHandler()
		role = obj.role
		# api.setNavigatorObject(obj) # 2311.12.08
		if sharedVars.menuClosing and role == controlTypes.Role.TREEVIEWITEM :
			sharedVars.menuClosing = False
			utis.setSpeech(True)
		
		if  role == controlTypes.Role.UNKNOWN :
			if obj.parent and obj.parent.role in(controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) :
				# beep(100, 10)
				self.initTimer()
				self.timer = callLater(300, KeyboardInputGesture.fromName("control+space").send)
			return nextHandler()
		elif role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in obj.states :
			if not sharedVars.msgOpened :
				sharedVars.curTab = "msgPreview"
			elif  sharedVars.msgOpened :  # separate message window	
				sharedVars.msgOpened = False
				speech.cancelSpeech()
				# below : Separate reading window: do not read the cleaned version of the message when the window is opened.
				if sharedVars.oSettings.getOption("deactiv", "SWRnoRead") :
					return nextHandler()
				return wx.CallAfter(sharedVars.oQuoteNav.readMail, obj, obj, False)
		if sharedVars.curTab == "sp:addressbook" and sharedVars.TBMajor > 127 :
			messengerWindow.tabAddressBook.abGainFocus(obj)

		nextHandler()
		
	def event_focusEntered (self,obj,nextHandler):
		role, ID  = obj.role, str(utils.getIA2Attr(obj))
		# sharedVars.log(obj, "current ")
		# sharedVars.log(obj, "FocusEntered")
		if  sharedVars.curFrame == "msgcomposeWindow" and ID == "msgIdentity" :
			return #  No nextHandler()
		# if sharedVars.menuClosing  and role != controlTypes.Role.TREEVIEWITEM:
			# sharedVars.log(obj, "menuClosing ") 
			# if hasattr(obj, "name") :
				# obj.name = ""
			# # menuClosing is set to False  in event_gainFocus
			# return
		#  Role.TEXTFRAME, IA2ID : threadTree Tag: tree-view, States : , FOCUSABLE, childCount  : 1 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i2, Role-TEXTFRAME, , IA2ID : threadTree , IA2Attr : id : threadTree, display : flex, class : tree-view-scrollable-container, tag : tree-view,  ;
		if sharedVars.TTnoFolderName and role in  (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) and utils.hasID(obj.parent.parent, "threadTree") :
			# beep(440, 5)
			obj.name = ""
			globalVars.foregroundObject.name  = ""
		elif role == controlTypes.Role.TEXTFRAME and ID == "threadTree" :
			if not sharedVars.oSettings.getOption("deactiv", "TTnoFilterSnd") :
				if hasFilter(obj, ID) : utis.playSound("filter") 
			# utils.listColumnID(obj)
			sharedVars.totalColIdx = utils.getTotalColIdx(obj)

		nextHandler()
		
	# G5 : buildColumnID() : used in messageListItem.
	def buildColumnID(self, oTT):
		try :
			# oTT must be the threadTree
			oTT = utis.findParentByID(oTT, controlTypes.Role.TEXTFRAME, "threadTree")
			sharedVars.objLooping = True
				# flat list mode : path Role-TEXTFRAME, , IA2ID : threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
			o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
			self.columnID =[]
			while o and o.role == controlTypes.Role.TABLECOLUMNHEADER :
				if int(o.location[2]) > 0 : # width
					# append couple (location, IA2ID)
					ID = utils.getIA2Attr(o)
					if ID and str(ID) not in "flaggedCol,junkStatusCol,	threadCol,unreadButtonColHeader" :
					# left must be int for correct sorting
						left = int(o.location[0])
						name = str(o.name).replace(_("Sort by "), "")
						self.columnID.append((left, ID, name))
				o = o.next
			self.columnID.sort()
			# self.columnID =[e[1] for e in self.columnID]
			# debug test
			# for e in self.columnID  :
				# sharedVars.logte("header left:{}, ID:{}, name:{}".format( str(e[0]), e[1], e[2]))
		finally :
			# self.lenColID = len(self.columnID)
			sharedVars.objLooping = False

	def buildColumnNames(self, oRow) :
		colSepar = ", " 
		# sharedVars.logte("Option junkStatusCol:" + str(junkStatusCol))
		# playSound_unread = False #options.as_bool ("playsound_unread")
		# sharedVars.logte("Original rowName:" + sharedVars.curTTRow)
		# l is the line we are going to build
		if controlTypes.State.COLLAPSED in oRow.states : l = _("Collapsed") + ", "
		else : l = ""

		# sharedVars.debugLog +="* Columns properties\n"
		try : # finally
			sharedVars.objLooping = True
			oCell = oRow.firstChild
			while oCell :
				s = ""
				longID = str(utils.getIA2Attr(oCell, False, "class"))
				ID = longID.split(" ")
				ID = str(ID[len(ID)-1])
				ID = ID.split("-")[0]
				# begin test
				# nm = ", name:" +  str(oCell.name)
				# testChild =", no children" 
				# if oCell.firstChild :
					# testChild = ", firstChild role:" + str(oCell.firstChild.role)
					# if oCell.firstChild.name : testChild += ", cname:" +  oCell.firstChild.name
				# sharedVars.logte(str(oCell.location.left) + ", short ID:" + ID + ", longID:" + longID + nm + testChild)
				# end of test 
				# if "unread" in longID == "statuscol" :
					# s = oCell.FirstChild
					# s = "col non lu, "
				if ID == "statuscol" :
					o = oCell.firstChild
					if not o :
						s =  sharedVars.unread if sharedVars.unread not in l else "" # 2023.11.15 
					else :
						s = o.name
						if s == _("Read") : s = ""
				elif "unreadbuttoncolheader" in longID :
					if sharedVars.unread  + ", " in oRow.name : s = sharedVars.unread
					else : s = ""
				elif "flaggedcol" in longID :
					if _("Starred") + ", " in oRow.name : s = _("Starred")
				elif ID == "subjectcol" :
					o = oCell.firstChild.firstChild.firstChild
					s= ""
					while  o :
						if o.role == controlTypes.Role.STATICTEXT :
							s = o.name
							break
						o = o.next
					s=removeResponseMention (self, s,1).strip (" -_*#").replace(" - "," ")
					if sharedVars.oSettings.regex_removeInSubject is not None : 
						s =sharedVars.oSettings.regex_removeInSubject.sub ("", s)

					# listgroup name repeats
					grp = utis.strBetween(s, "[", "]")
					# api.copyToClip("groupe " + grp)
					if grp :
						s= self.regExp_nameListGroup.sub (" ",s)
						if  not sharedVars.listGroupName :
							s = "[" + grp + "] " +  s 
					# sharedVars.curSubject = s
				elif ID in ("correspondentcol","sendercol","recipientcol") :  # clean
					if  oCell.firstChild :
						s= oCell.firstChild.name
						if sharedVars.namesCleaned : # corresp name 
							s = self.regExp_removeSymDigits.sub (" ", s)
						else : 
							s = self.regExp_removeSymbols.sub (" ", s)
						s = utis.truncateAfter(s, "<")
				elif "attachmentcol" in longID :
					if oCell.firstChild :
						s = _("attachment") 
				elif ID =="junkstatuscol" :
					# Translators : junk mail column in the list of messages : You dshould write here exactly what  Thunderbird says in your language.
					if sharedVars.junkStatusCol :
						s =  _("Spam")
						if   s not in sharedVars.curTTRow :
							s =""

				else : #  elif ID in ("datecol, ","receivedcol, "tagscol", "sizecol", "accountcol", "totalcol", "locationcol", "idcol") :
					try : s = oCell.firstChild.name
					except : pass
				if s : l += s + colSepar
				oCell = oCell.next
				
			# positon info
			# posInfo = oRow.positionInfo
			# # example : PosInfo={'level': 1, 'similarItemsInGroup': 973, 'indexInGroup': 971}posInfo = oRow.positionInfo 
			# # Remarhs :  the level info  and oRow.childcount are both erroneous.
			# l += " " + str(posInfo['indexInGroup']) + _(" of ") + str(posInfo['similarItemsInGroup'])
			# # for testing, duration
			# ms = time () - t
			# ms = int(ms *1000)
			# l += ", duration : " + str(ms) 
			return l  # + ", Original : " + oRow.name
		finally :
			sharedVars.objLooping = False

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
			if sharedVars.TBMajor > 127 :
				nextGesture = messengerWindow.tabAddressBook.getNextControl(o, ID)
				return KeyboardInputGesture.fromName(nextGesture).send()
			# tb 115
			if ID.startswith("searchInput") :
				return KeyboardInputGesture.fromName ("f6").send () 
		return gesture.send()

	def script_sharedEscape(self, gesture) :
		if sharedVars.curTab == "message" :
			return gesture.send()
		elif sharedVars.curTab == "msgPreview" :
			return KeyboardInputGesture.fromName ("shift+f6").send()  
		o=api.getFocusObject()
		role = o.role
		curTreeType = utils.currentTree(o, role)
		if curTreeType == "f" :
			if not sharedVars.oSettings.getOption("mainWindow", "ftNoEscape") :
				return KeyboardInputGesture.fromName ("f6").send()  
			else :
				ui.message(o.name + ", " + str(messengerWindow.folderTreeItem.fGetAccountNode(o).name))
			
		ID = str(utils.getIA2Attr(o))
		if curTreeType == "t" : # threadTree
			if hasFilter(o, ID) :
				gesture.send()
				if hasFilter(o, ID) :
					gesture.send()
				callLater(50, sayFilterRemoved)
			else :
				if not sharedVars.oSettings.getOption("mainWindow", "ttNoEscape") :
					return KeyboardInputGesture.fromName ("shift+f6").send() # utils.getFolderTreeFromFG(True)
				else :
					ui.message(o.name)
		elif  "Recipient" in ID  or "expandedsubjectBox" in ID or "Recipient" in str(utils.getIA2Attr(o.parent)) : # header pane
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role in  (controlTypes.Role.BUTTON, controlTypes.Role.TOGGLEBUTTON)  and ID.startswith("attachment") :
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif role == controlTypes.Role.LISTITEM and utils.hasID(o.parent, "attachmentList") :
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif  utils.hasID(o.parent, "attachmentBucket") :  # attachment list in write window
			return KeyboardInputGesture.fromName ("shift+f6").send()
		elif sharedVars.curTab == "sp:addressbook"   and role !=  controlTypes.Role.MENUITEM :
			if sharedVars.TBMajor > 127 :
				messengerWindow.tabAddressBook.getPreviousControl(o, ID)
			else : # TB 115
				if ID.startswith("cards-row") or ID.startswith("searchInput") or ID.startswith("cards") :
					return KeyboardInputGesture.fromName ("shift+f6").send () 
				elif role == controlTypes.Role.TREEVIEWITEM and (ID.startswith("list") or utils.hasID(o.parent, "books")) :
					return KeyboardInputGesture.fromName ("f6").send () 
				elif role == controlTypes.Role.BUTTON :
					return KeyboardInputGesture.fromName ("shift+tab").send () 
				else : return gesture.send()
		# elif role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in o.states :
			# if utils.isSeparMsgWnd() :
				# # 2025-02-08 : control+w replaced with escape. works bettter   in some situations
				# return KeyboardInputGesture.fromName ("escape").send () 
			# if o.parent.role == controlTypes.Role.INTERNALFRAME and utils.getIA2Attr(o.parent, "messagepane") :
				# return KeyboardInputGesture.fromName ("shift+f6").send () 
		elif role ==  controlTypes.Role.LINK  : # in preview Pane document or accountCentral doc
			# before 135 Role.INTERNALFRAME, IA2ID : messagepane Tag: browser, States : , FOCUSABLE, childCount  : 1 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID : messagepane , 
			# tb 135 : level -6   : TEXTFRAME, ID : messagePane, class : MozillaWindowClass, childCount : 1
			if sharedVars.TBMajor < 135 :
				if  utis.findParentByID(o, controlTypes.Role.SECTION, "messagePane") : return KeyboardInputGesture.fromName("shift+f6").send()
			else : # >= 135
				if  utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "messagePane") or utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") : return KeyboardInputGesture.fromName("shift+f6").send()
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") : return KeyboardInputGesture.fromName("shift+f6").send()
		if str(utils.getIA2Attr(o.parent)) in "messageEditor,MsgHeadersToolbar" :
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape") :
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "quickFilterBarContainer") :
			# if o.value is not None : ui.message(_("Keyword removed."))
			# return gesture.send()
		elif role == controlTypes.Role.EDITABLETEXT and utils.hasID(o.parent, "MsgHeadersToolbar") : # write window
			if sharedVars.oSettings.getOption("compose", "closeMessageWithEscape") :
				return KeyboardInputGesture.fromName ("control+w").send () 
		# elif  role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW, controlTypes.Role.TABLE) and utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "threadTree") :  # modified 2025-01-09
		elif o.parent.role == controlTypes.Role.INTERNALFRAME and  utils.hasID(o.parent, "accountCentralBrowser") :
			return KeyboardInputGesture.fromName ("shift+f6").send () 
		elif role == controlTypes.Role.BUTTON : 
			# level 1,  40 of 51, name : Aller au jour précédent, Role.BUTTON, IA2ID : previous-day-button
			if ID == "previous-day-button" : return KeyboardInputGesture.fromName ("shift+f6").send ()
			if sharedVars.TBMajor < 135 :
				if  utis.findParentByID(o, controlTypes.Role.SECTION, "messagePane") : return KeyboardInputGesture.fromName("shift+f6").send()
			else : # >= 135
				if  utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "messagePane") : return KeyboardInputGesture.fromName("shift+f6").send()
			if utis.findParentByID(o, controlTypes.Role.INTERNALFRAME, "accountCentralBrowser") :
				return KeyboardInputGesture.fromName ("shift+f6").send ()
		return gesture.send()
		
	def script_sharedAltEnd(self, gesture) :
		o = api.getFocusObject()
		if utils.currentTree(o, o.role) == "t"  or utils.hasID(o.parent, "quickFilterBarContainer") :
			msg = utils.getMessageStatus()
			if not msg  : msg = _("Blank")
			ui.message(msg)
			return
		msg = utis.getStatusBarText()
		if not msg : msg = _("Status line without data")
		return ui.message(msg)
	script_sharedAltEnd.__doc__ = _("Announces abbreviated status line and message filtering information if applicable")
	script_sharedAltEnd.category = sharedVars.scriptCategory

	def script_sharedCtrlTab(self, gesture) :
		fo = globalVars.focusObject # api.getFocusObject()
		speech.cancelSpeech()
		# beep(440, 5)
		direct = (-1 if "shift" in gesture.modifierNames else 1)
		if not messengerWindow.tabs.changeTab(self, fo, direct) :
			return gesture.send()

	def script_sharedCtrlN(self, gesture) :
		speech.cancelSpeech()
		fo = api.getFocusObject()
		mainKey = gesture.mainKeyName
		# 2022-12-09 localized replacement of if mainKey == "=" : mainKey = "0" # for control+=
		if mainKey == utis.gestureFromScanCode(13,"") : mainKey = "0" # for they at the left of backspace
		newTabIdx = int(mainKey) - 1
		if newTabIdx == -1 :  # control+0 - 1
			messengerWindow.tabs.showTabMenu(self, fo)
			return
		# control+1 to control+9
		# beep(100, 30)
		if not messengerWindow.tabs.activateTab(self, fo, newTabIdx) :
			return gesture.send()

	def script_sharedCtrlR(self, gesture) :
		# if not sharedVars.oSettings.getOption("deactiv", "TTnoSmartReply") : return gesture.send()
		rc = int(getLastScriptRepeatCount())
		self.initTimer()
		if rc > 0 :
			self.timer = wx.CallLater(25, utils.smartReply, rc)
		else :
			self.timer = wx.CallLater(200, utils.smartReply, rc)
	script_sharedCtrlR.__doc__ = _("Smart reply to reply to a recipient or mailing list")
	script_sharedCtrlR.category = sharedVars.scriptCategory

	def  script_sharedAltEqual(self, gesture) : # native context menu of active tab
		if sharedVars.curFrame != "messengerWindow" : return
		messengerWindow.tabs.tabContextMenu(self, sharedVars.oCurFrame)

	def script_sendCtrlF4(self, gesture) :
		if "shift"  in gesture.modifierNames :  return gesture.send()
		fo = globalVars.focusObject
		role = fo.role
		if gesture.mainKeyName == "backspace" :
			if role == controlTypes.Role.EDITABLETEXT or (role == controlTypes.Role.DOCUMENT and controlTypes.State.READONLY not in fo.states)  :
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
					return ui.message(_("Press right arrow and retry, please."))
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
					beep(100, 10)
					return 
				return sharedVars.oQuoteNav.readMail(fo, o,(mainKey == "upArrow")) # with quote list
			elif utils.isFolderTreeItem(o, ID) :
				# sharedVars.log(o, "folderTreeItem before call of fmenuFolder")
				return messengerWindow.folderTreeItem.fMenuFolders(o, (mainKey == "downArrow"))
			elif  ID.startswith("ReplaceWordInput") : 
				# spellCheckDialog
				if mainKey == "upArrow" :
					return o.script_reportFocus(gesture)
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
				beep(100, 40)
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
		if sharedVars.curFrame != "messengerWindow"  or getLastScriptRepeatCount() > 0 : return gesture.send()
		if sharedVars.curTab == "main" :
			# focus modes : 0 nothing, 1 : last msg, 2 : first msg, 3 : first unread, 4 : folderTree
			focusMode = sharedVars.oSettings.getOption("messengerWindow","focusMode", kind="i")
			if focusMode >   0 and focusMode < 4 :
				return wx.CallAfter(utils.focusThreadTree, focus=True)
			# focusMode = 4 = folderTree
			fo = api.getFocusObject()
			if utils.isFolderTreeItem(fo) :
				return
			# we are not in folderTree nor in threadTree
			wx.CallAfter(utils.getFolderTreeFromFG, focus=True)
		elif sharedVars.curTab == "sp:addressbook" :
			return self.script_showContextMenu(None)
		else : # other active tab, we activate the first tab 
			if not messengerWindow.tabs.activateTab(self, api.getFocusObject(), 0) :
				return gesture.send()
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
				return ui.message(_("The headers pane is not displayed. Please press F8 then try again"))
			if ID.startswith("threadTree") and controlTypes.State.COLLAPSED in fo.states :
				beep(432, 2)
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
			return ui.message(_("Press alt+upArrow before navigating through quotes in a message."))
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

	def script_previewPane(self, gesture) :
		if globalVars.focusObject.role  not in (controlTypes.Role.TREEVIEWITEM , controlTypes.Role.LISTITEM) : 
			return gesture.send()
		KeyboardInputGesture.fromName ("f8").send()
		o =  utils.getMessagePane()
		if o :
			ui.message(_("Present: Headers and message pane."))
		else :
			ui.message(_("Missing : headers and message pane."))
	script_previewPane.__doc__ = _("Turn on or off the preview messages panel")
	script_previewPane.category = sharedVars.scriptCategory

	def script_showHelp(self, gesture) :
		utis.showHelp()
	script_showHelp.__doc__ = _("Shows the add-on help in a web page")
	script_showHelp.category = sharedVars.scriptCategory

	def script_displayDebug(self, gesture) :
		debugShow(self, False)

	def script_initDebug(self, gesture) :
		if sharedVars.debug :
			sharedVars.debug = False
			ui.message("Debug mode is disabled")
		else :
			sharedVars.debug = True
			ui.message("Debug mode is enabled")

		# # disabModes : 0 nothing, 1 choose overlay, 2 : object init, 3 gainFocus 
		# self.disabMode +=1
		# if self.disabMode > 3 : self.disabMode = 0
		# if self.disabMode == 0 : mode = u"Aucune désactivation"
		# elif self.disabMode == 1 : mode = u"Désactivation de l'intercepteur."
		# elif self.disabMode == 2 : mode = u"Désactivation de l'initialisation des objets NVDA."
		# elif self.disabMode == 3 : mode = u"Désactivation de  gain focus."
		# else : mode = "disabMode = " + str(self.disabMode)

		# ui.message(mode)

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
		"kb:control+tab": "sharedCtrlTab",
		"kb:control+shift+tab": "sharedCtrlTab",
		"kb:control+1": "sharedCtrlN",
		"kb:control+2": "sharedCtrlN",
		"kb:control+3": "sharedCtrlN",	
		"kb:control+4": "sharedCtrlN",
		"kb:control+5": "sharedCtrlN",
		"kb:control+6": "sharedCtrlN",
		"kb:control+7": "sharedCtrlN",
		# "kb:control+8": "sharedCtrlN",
		"kb:control+9": "sharedCtrlN",
		"kb:control+0": "sharedCtrlN",
		utis.gestureFromScanCode(13, "kb:control+") : "sharedCtrlN", # 13 : first hey at the left of backspace
		utis.gestureFromScanCode(13, "kb:alt+") : "sharedAltEqual",
		# "kb:alt+pageup": "sharedCtrlR", # smart reply
		"kb:control+r": "sharedCtrlR", # smart reply
		# "kb:control+f4": "sendCtrlF4",
		# "kb:control+w": "sendCtrlF4",
		"kb:control+backspace": "sendCtrlF4",
		# _("kb:shift+control+²") :"showOptionMenu",
		# _("kb:control+²") :"showContextMenu",
		"kb:alt+d":"sharedAltD",
		"kb:f8":"previewPane",
		"kb:control+f1": "showHelp",
		"kb:alt+f12": "displayDebug",
		"kb:windows+f12": "initDebug"
	}

def debugShow(appMod, auto) :
	sharedVars.debugLog = "Debug mode : {}, TB branch : {}".format(str(sharedVars.debug), sharedVars.TBMajor) + "\n" + "\n" + sharedVars.debugLog
	sharedVars.log(api.getFocusObject(), "* FocusObject")
	sharedVars.log(api.getNavigatorObject(), "* NavigatorObject")
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
	# sharedVars.log(no, "Nav object")
	fo = api.getFocusObject()
	if utils.hasID(fo, "threadTree-row"	) :
		# sharedVars.logte("Current row original name :\n" + sharedVars.curTTRow)
		utils.listAscendants(-6)
		utils.listDescendants(fo, 0, "* List of descendants")
		# utils.listColumnNames(fo) 
	else :
		utils.listAscendants(-6)
		utils.listDescendants(fo, 0, "* List of descendants")
	#sharedVars.debugLog += "\ncurFrame : {0}, curTab : {1},".format(appMod.curFrame, sharedVars.curTab) + "\n"
	sharedVars.debugLog += "\ncurTab : {0}, curFrame : {1},".format(sharedVars.curTab, sharedVars.curFrame) + "\n"
	# sharedVars.logte("sharedVars.curSubject :" + sharedVars.curSubject)
	# if sharedVars.oQuoteNav :
		# sharedVars.logte("oQuoteNav.subject : " + sharedVars.oQuoteNav.subject)
	sharedVars.logte("GroupingIdx = " + str(sharedVars.groupingIdx))
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


def removeResponseMention (appMod,s,mode):
	mode = sharedVars.oSettings.responseMode
	if not mode : return s
	s = s.replace(" ", " ") # 2023-04-23 unbrekable space
	s , n= appMod.regExp_AnnotationResponse.subn(" ",s)
	if  mode == 1 : # "responseMentionGroup"
		s=(str (n) if n>1 else "")+(_("Re ") if n else "")+s
	elif   mode == 3 : # "messengerWindow", "responseMentionDelColon" 
		s="Re"*n+" "+s
	return s 

def hasFilter(o, ID=None) :
	if sharedVars.TBMajor > 127 : 
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

def activateTB() :
	# following line for test
	# focusTaskbar()

	tbTitle = " Thunderbird"
	hwFG = winUser.getForegroundWindow()
	winClass = winUser.getClassName(hwFG) 
	# sharedVars.logte("ActivateTB window class : {}, curFrame : {}, curTab : {}".format(winClass, sharedVars.curFrame, sharedVars.curTab))
	if "Mozilla" not in winClass : return None
	winTitle = winUser.getWindowText(hwFG)
	if "bird Beta" in winTitle :
		tbTitle = "bird Beta"

	isTB = True if winTitle.endswith(tbTitle)else False
	fg =  api.getForegroundObject()
	if isTB and "Mozilla" in fg.windowClassName and fg.childCount < 32 :
		return None

	fo = api.getFocusObject()
	attrs = "Fg=" + sharedVars.getObjAttrs(fg) + "\nFo=" + sharedVars.getObjAttrs(fo)
	print("activateTB begin\n" + attrs)
	if isTB :
		o =  api.getFocusObject()
		wcn =  o.windowClassName
		if  wcn == "MozillaWindowClass" :
			# sharedVars.log(o, "ActivateTB, focus object is of mozilla window class")
			return o 
		elif  wcn == "MozillaDialogClas" :
			return None

	o = api.getDesktopObject()
	o = o.firstChild
	while o :
		print("Desktop child=" + sharedVars.getObjAttrs(o))
		if o.windowClassName == "MozillaDialogClas" :
			print("Mozilla  dialog found")
			# o.firstChild.setFocus()
			return None
		if o.name and o.name.find(tbTitle) > -1 :
			t =  "activateTB, before setFGo : " + sharedVars.getObjAttrs(o) + "\n"
			winUser.setForegroundWindow(o.windowHandle)
			o = api.getForegroundObject()
			o.setFocus()
			t +=  "activateTB, After  setFGo : " + sharedVars.getObjAttrs(o) + "\n"
			print(t) 
			return o
		try : o= o.next
		except : break
	return None
	
def focusTaskbar() :
	o = api.getDesktopObject()
	o = o.firstChild
	while o :
		print("focusTaskbar, fo=" + sharedVars.getObjAttrs(o))
		if "Shell_TrayWnd" in o.windowClassName :
			o.setFocus()
			t = "Found focusTaskbar, fo=" + sharedVars.getObjAttrs(o)
			print(t)
			return
		try : o = o.next
		except : break

def sayFilterRemoved() :
	infos  =  utils.getMessageStatus128()
	fo = api.getFocusObject()
	role = fo.role
	if role in (controlTypes.Role.TABLE, controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) :
		cc = fo.childCount
		if cc == 0 :
			beep(120, 40)
			infos = _("No messages displayed") + ", " + infos
	ui.message(_("Filter removed") + infos)
