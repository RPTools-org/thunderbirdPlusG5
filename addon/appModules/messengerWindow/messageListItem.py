#-*- coding:utf-8 -*
# thunderbirdPlusG5 forr Thunderbird 115

from tones  import beep
import speech 
from scriptHandler import getLastScriptRepeatCount
import api, globalVars
import winUser
from api import copyToClip
import controlTypes
from keyboardHandler import KeyboardInputGesture
from NVDAObjects.IAccessible import IAccessible # , getNVDAObjectFromPoint
import wx
from wx import CallAfter, CallLater
from gui import messageBox
from core import callLater
from ui import  browseableMessage
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, utils115 as utils, sharedVars
from utils115 import message
# from . import foldersMessages
del sys.path[-1]

from time import time, sleep
addonHandler.initTranslation()

# postMessage =windll.user32.PostMessageA
# optimization : the dict below is initialized on add-on initialization
TTIDefGestures = {
	"kb:1" : "readTTICell",
	"kb:2" : "readTTICell",
	"kb:3" : "readTTICell",
	"kb:4" : "readTTICell",
	"kb:5" : "readTTICell",
	"kb:6" : "readTTICell",
	"kb:7" : "readTTICell",
	"kb:8" : "readTTICell",
	"kb:9" : "readTTICell",
	"kb:0" : "readTTICell",
	# "kb:upArrow" : "selectLine",
	# "kb:downArrow" : "selectLine",
	"kb:space" : "readPreview",
	"kb:shift+space" : "readPreview",
	"kb:enter" : "openMessage",
	"kb:nvda+upArrow" : "sayLine",
	"kb(laptop):nvda+l" : "sayLine",
	"kb:control+leftArrow" : "goGroupedFirst", 	
	"kb:control+rightArrow" : "goGroupedLast", 	
	"kb:a" : "sayShortcut",
	"kb:f" : "showFilterBar",
	# "kb:delete" : "deleteMsg",
	# "kb:home" : "gotoFirstMsg",
	# "kb:end" : "gotoMsg",
	# "kb:n" : "gotoMsg",
	# "kb:shift+delete" : "deleteMsg",
	# "kb:shift+c" : "sayShortcut",
	# "kb:j" : "toggleJunk",
	# "kb:shift+j" : "toggleJunk",
	"kb:m" : "toggleUnread"
} 

TTITagGestures = {
	"kb:shift+1" : "sayMessageTags",
	"kb:shift+2" : "sayMessageTags",
	"kb:shift+3" : "sayMessageTags",
	"kb:shift+4" : "sayMessageTags",
	"kb:shift+5" : "sayMessageTags",
	"kb:shift+6" : "sayMessageTags",
	"kb:shift+7" : "sayMessageTags",
	"kb:shift+8" : "sayMessageTags",
	"kb:shift+9" : "sayMessageTags",
	"kb:shift+0" : "removeMessageTags",
	"kb:alt+0" : "sayMessageTags"
}

gSaying = False
def gSayShortcut(row) :
	global gSaying
	message(row)
	gSaying = False
# gTimer = None
# def gInitTimer() :
	# global gTimer
	# if gTimer is not None:
		# gTimer.Stop()
		# gTimer = None
# def saySelection(row, oParent) :
	# global gTimer
	# o = api.getFocusObject()
	# if o.role not in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM) :
		# KeyboardInputGesture.fromName("space").send()
		
		# # oParent.setFocus()
		# sleep(.3)
		# message(str(o.role))
		# sleep(3)
		# # beep(700, 10)
		# gTimer = callLater(100, saySelection, row, oParent)
		# return
	# nm = o.name
	# message(row + o.name)

class MessageListItem(IAccessible):
	timer = None
	timerCount = 0
	def initOverlayClass (self):
		if  controlTypes.State.SELECTED not in self.states : return
		if  sharedVars.TTClean : 
			self.name = self.customizeRow()
		# cause issue if controlTypes.State.SELECTED not in self.states : self.doAction()
		self.bindGestures(TTIDefGestures)
		if not sharedVars.TTnoTags :
			self.bindGestures(TTITagGestures)
		if sharedVars.TTClean and not sharedVars.delContextMenu:
			self.bindGesture("kb:delete", "deleteMsg")
			self.bindGesture("kb:numpaddelete", "deleteMsg")
		elif sharedVars.TTClean and sharedVars.delContextMenu :
			self.bindGesture("kb:delete", "deleteWithMenu")
			self.bindGesture("kb:numpadDelete", "deleteWithMenu")

	
	def customizeRow(self, oRow=None) :
		dbg = False
		if dbg : sharedVars.logte("Customize row begin")
		if not oRow :
			oRow = self
		colSepar = ", " 
		if dbg : sharedVars.logte("Original rowName:" + oRow.name)
		# l is the line we are going to build
		if controlTypes.State.COLLAPSED in oRow.states : l = _("Collapsed") + ", "
		else : l = ""

		try : # finally
			sharedVars.objLooping = True
			oCell = oRow.firstChild
			while oCell :
				s = "" ; t = ""
				longID = str(utils.getIA2Attr(oCell, False, "class"))
				p = longID.find("-column")
				ID = longID[:p]
				p = ID.find(" ")
				if p == -1 : p = 0
				ID = ID[p:].strip()
				# if dbg : sharedVars.logte("Cell Name : " + str(oCell.name))
				for c in oCell.recursiveDescendants : 
					if  hasattr(c, "name")  and c.name :
						t = str(c.name).strip()
				if dbg : sharedVars.logte("ColID {} : {}".format(ID, t))
				if ID == "statuscol" :
					if not t :
						s = _("Unread")
					elif t == _("Read") :
						s = ""
					else :
						s= t
				elif ID == "flaggedcol" : 
					if _("Starred") + ", " in oRow.name : s = _("Starred")
				elif ID == "subjectcol" :
					s = t.replace("*** SPAM ***", "") 
					s=self.removeResponseMention (s,1).strip (" -_*#").replace(" - "," ")
					if  sharedVars.listGroupName :
						s= sharedVars.regExp_nameListGroup.sub (" ",s)
					# # # sharedVars.curSubject = s
				elif ID in ("correspondentcol","sendercol","recipientcol") :  # clean
					if not sharedVars.namesCleaned : # corresp name : 
						s = t
					else :
						s = sharedVars.regExp_mailAddr.sub("", t)
						s = sharedVars.regExp_removeSymDigits.sub(" ", s)
				elif ID == "attachmentcol" :
					if t :
						s = _("attachment") 
				elif ID =="junkstatuscol" :
					if not t or _(" not marked as") in t :
						s = ""
					else :
						s = "Spam"
				elif ID == "threadcol" : # This is a threaded message
					s = ""
				elif ID == "unreadbuttoncolheader" : 
					# TB 145
					if _("unread") in t :
						s = _("unread")
				else : 
					s = t
				if s : l += s + colSepar
				oCell = oCell.next
				
				# end of loop
			# positon info
			# posInfo = oRow.positionInfo
			# # example : PosInfo={'level': 1, 'similarItemsInGroup': 973, 'indexInGroup': 971}posInfo = oRow.positionInfo 
			# # Remarhs :  the level info  and oRow.childcount are both erroneous.
			# l += " " + str(posInfo['indexInGroup']) + _(" of ") + str(posInfo['similarItemsInGroup'])
			# # for testing, duration
			# ms = time () - t
			# ms = int(ms *1000)
			# l += ", duration : " + str(ms) 
			if not l :
				return "Card, " + str(oRow.name)
			return sharedVars.regExp_removeMultiBlank.sub(" ", l) 
		finally :
			sharedVars.objLooping = False
		
	def removeResponseMention (self,s,mode):
		mode = sharedVars.oSettings.responseMode
		if not mode : return s
		s = s.replace(" ", " ") # 2023-04-23 unbrekable space
		s , n= sharedVars.regExp_AnnotationResponse.subn(" ",s)
		if  mode == 1 : # "responseMentionGroup"
			s=(str (n) if n>1 else "")+(_("Re ") if n else "")+s
		elif   mode == 3 : # "messengerWindow", "responseMentionDelColon" 
			s="Re"*n+" "+s
		return s 

	def script_sayLine(self, gesture):
		rc =  int(getLastScriptRepeatCount ())
		if rc > 0 :
			browseableMessage (message= self.name.replace(", ", "\n"), title = _("Line details") + " - ThunderbirdPlus", isHtml = False)
		else : # 1 press
			message(self.name)
	
	script_sayLine.__doc__ = _("Message list : One press announces the current line, two presses displays the line text in a window.")
	script_sayLine.category=sharedVars.scriptCategory

	def script_selectLine(self, gesture) :
		# if gesture.mainKeyName == "upArrow" : CallAfter(KeyboardInputGesture.fromName("b").send)
		# elif gesture.mainKeyName == "downArrow" : CallAfter(KeyboardInputGesture.fromName("f").send)
		try :
			if gesture.mainKeyName == "upArrow" : o = self.previous
			else : o = self.next
		except :
			self.doAction()
			return
		if not o : 
			beep(120, 10)
			message(self.name)
			return
		o.doAction()

	# read threadTree item  cells  
	# def script_readTTICell(self,gesture):
		# rc = getLastScriptRepeatCount()
		# idx = int(gesture.mainKeyName)
		# idx = 9 if idx == 0   else idx-1


		# if idx >= len (self.appModule.columnID) : return beep(100, 10)
		# left = self.appModule.columnID[idx][0]
		# ID = self.appModule.columnID[idx][1]
		# label = self.appModule.columnID[idx][2] 
		# oCell = self.getCellObj(left)
		# if not oCell : return beep(100, 10)
		
		# name = ""
		# if oCell.name : name = oCell.name
		# else : 
			# try : name = oCell.firstChild.name
			# except : pass  
		# if not name :
			# if "attachment" in ID : label = "" ; name = _("No Attachement.")
			# else : name = _("Blank")
		# if rc == 0 :
			# message(label + name)
		# elif rc == 1 :
			# speech.speakSpelling(name)
		# else :
			# message(_("{columnText} copied to clipboard").format (columnText = "")+ " : "+ name)
			# api.copyToClip (name)

	def script_readTTICell(self,gesture):
		rc = getLastScriptRepeatCount()
		idx = int(gesture.mainKeyName)
		idx = 9 if idx == 0 else idx-1
		oCell = self.getChild(idx)
		if not oCell : return message(_("No column ") + str(idx+1)) 
		lbl = oCell.name
		# oCell = oCell.firstChild
		c = GetDescObject(controlTypes.Role.STATICTEXT, controlTypes.Role.GRAPHIC)
		c.run(oCell)
		name = ""
		if c.mainObj and c.mainObj.name : 
			name  =  str(c.mainObj.name)
		if c.secondObj and c.secondObj.name : 
			name += str(c.secondObj.name)
		if not name :
			return message(_("No") + " " + lbl)
		
		if rc == 0 :
			message(lbl + " : " + name)
		elif rc == 1 :
			speech.speakSpelling(name)
		else :
			message(_("{columnText} copied to clipboard").format (columnText = "")+ " : "+ name)
			api.copyToClip (name)



	def getCellObj(self, iLeft) :
		# self is a threadTree item or row
		o = self.firstChild
		while o :
			ID = str(utils.getIA2Attr(o,False, "class"))
			left = int(o.location[0])
			msg = "cell, left:{}, iLeft:{}, ID:{}".format(left, iLeft, ID) 
			# sharedVars.logte(msg)
			if left == iLeft :
				return o
			o = o.next
		return None
		

	# read headers scritps with alt+n
	# see  thunderbird.py script_sharedAltN

	# begin tags 
	def getTagName(self, tagNo="1") :
		if tagNo > "6" :
			return tagNo
		#tagNo = str(tagNo)
		if tagNo < "1" or tagNo > "9" : return None
		# 0 of  1, name : Étiquette, role.POPUPMENU=12, IA2ID : mailContext-tagpopup Tag: menupopup, états : , COLLAPSED, INVISIBLE, OFFSCREEN, childCount  : 11 Chemin : role FRAME=34| i2, role-POPUPMENU=12, , IA2ID : mailContext | i11, role-MENUITEM=11, , IA2ID : mailContext-tags | i0, role-POPUPMENU=12, , IA2ID : mailContext-tagpopup , IA2Attr : explicit-name : true, id : mailContext-tagpopup, display : -moz-popup, tag : menupopup, , Actions : click ancestor,  ;
		o = sharedVars.oCurFrame # globalVars.foregroundObject
		# sharedVars.debugLog = ""
		# if sharedVars.debug : sharedVars.log(o, "frame   ", False)
		# | i2, role-POPUPMENU=12, , IA2ID : mailContext | i11, role-MENUITEM=11, , IA2ID : mailContext-tags | i0, role-POPUPMENU=12, , IA2ID : mailContext-tagpopup 
		o = utis.findChildByID(o,  "mailContext")
		# if sharedVars.debug : sharedVars.log(o, " child ", False)
		o = utis.findChildByID(o,  "mailContext-tags")
		# if sharedVars.debug : sharedVars.log(o, " child ", False)
		o = utis.findChildByID(o,  "mailContext-tagpopup")
		# if sharedVars.debug : sharedVars.log(o, " child ", False)
		#      5 of 10, name : 1 Important	1, role.CHECKMENUITEM=60 Tag: menuitem, états : , CHECKED, INVISIBLE, SELECTABLE, FOCUSABLE, CHECKABLE Chemin : role FRAME=34| i2, role-POPUPMENU=12, , IA2ID : mailContext | i11, role-MENUITEM=11, , IA2ID : mailContext-tags | i0, role-POPUPMENU=12, , IA2ID : mailContext-tagpopup | i5, role-CHECKMENUITEM=60,  , IA2Attr : explicit-name : true, checkable : true, display : -moz-box, tag : menuitem, , Actions : click,  ;
		try :
			sharedVars.objLooping = True
			o = o.getChild(5)
			while o :
				# if sharedVars.debug : sharedVars.log(o, " menu item  ", False)
				if o.name.startswith(tagNo) : 
					nm = o.name.split("\t")
					nm = nm[0]
					return nm[2:]
				o = o.next
			return None
		finally :
			sharedVars.objLooping = False

	def getMessageTagSet(self) :
		tagSet =set ()
		o =  utils.getMessageHeaders(msgPane=None)
		if not o : return tagSet
		#| i3, role-SECTION=86, , IA2ID : expandedtagsRow  
		o = utis.findChildByID(o, "expandedtagsRow")
		if not o : return tagSet
		# modifié 102.b4
		#| i1, role-SECTION=86, , IA2ID : expandedtagsBox 
		o = utis.findChildByID(o, "expandedtagsBox")
		# | i0, role-LIST=14,  
		o = o.firstChild
		# | i0, role-LISTITEM=15,  , IA2Attr : setsize : 2, display : list-item, class : tag, tag : li, posinset : 1, formatting : block, , Actions : click ancestor,  ;
		o = o.firstChild
		while o :
			tagSet.add(o.name)
			o = o.next
		return tagSet

	def getMessageTagStr(self) :
		TagSet =  self.getMessageTagSet() 
		return setToStr(TagSet, _("Tags"), _("No tag."))

	def script_sayMessageTags(self,gesture):
		if controlTypes.State.COLLAPSED in self.states :
			return message(_("No tag on a collapsed discussion"))
		lblTags = _("Tags")
		#Translators: Tags feature
		lblNoTags = _("No tag.")
		if gesture.mainKeyName == "0" :
			msgTags = setToStr(self.getMessageTagSet(), lblTags, lblNoTags)
			return message(msgTags)
		#translators
		lblNoMore = _("No More tag.")
		lblAdded = _("added")
		lblRemoved = _(" removed")
		prevTagSet = self.getMessageTagSet() 
		# 2022-1215 : explicit key name send necessary
		KeyboardInputGesture.fromName(gesture.mainKeyName).send()
		sleep(0.2)
		api.processPendingEvents()
		newTagSet =  self.getMessageTagSet() 
		tagChanged =newTagSet.difference(prevTagSet)
		if not tagChanged  :tagChanged = prevTagSet.difference(newTagSet)
		# return message("tagChanged" + str(tagChanged))
		msg  = list(tagChanged)[0]+" "+(lblAdded,lblRemoved)[len(prevTagSet)>len(newTagSet)]
		msg ="{0}, {1}".format(msg, setToStr(newTagSet, lblTags, lblNoMore))
		message(msg)
		#message(u"Changé" + str(tagChanged))
		#message(u"étiquettes : " + str(newTagSet))
		return
		# translator 
		lblTag = _("tag")
		lblNoMore = _("No more tag.")
		lblAdded = _("added")
		lblRemoved  = _("removed")
		msgTags = self.getMessageTags()
		if not msgTags : 
			msgTags =  lblNoMore
		newState = (lblAdded if tagName in msgTags else lblRemoved)
		message("{0} : {1} {2}, {3}".format(lblTag, tagName, newState, msgTags))
	script_sayMessageTags.__doc__ = _("Shift + 1 to 8: announces the additions or removals of tags, Shift+0 announces the tags of the message")
	script_sayMessageTags.category=sharedVars.scriptCategory

	def script_removeMessageTags(self,gesture):
		# translator
		lblNoTag = _("No tag to remove.")
		msgTags = self.getMessageTagSet()
		if not msgTags :  
			return message(lblNoTag)
		rc =  getLastScriptRepeatCount ()
		if rc == 0 :
			# translator 
			lblPressTwice = _("Press this command twice quickly to delete the") 
			msgTags = setToStr(msgTags, lblPressTwice) 
			return message(msgTags)
		elif rc   == 1:
			KeyboardInputGesture.fromName("0").send()
			# translator
			lblNoTag = _("All tags have been removed from this message.")
		return callLater(40, message, lblNoTag)
	script_removeMessageTags.__doc__ = _("Removes all tags from the selected message.")
	script_removeMessageTags.category=sharedVars.scriptCategory
	# end of Message tags

	# read preview panel for spaceBar
	def script_readPreview(self, gesture) :
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		sharedVars.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		utils.setMLIState(self)
		o = None
		if   utils.hasID(self, "threadTree-row") :
			for i in range(0, 20) :
				o2, retryNeeded = utils.getPreviewDoc()
				if o2 : 
					o = o2
					break
				if not  retryNeeded : break
				sleep(0.1)
				api.processPendingEvents()
			if not o : return # 2023-09-12 gesture.send()
			else : return sharedVars.oQuoteNav.readMail(self, o, ("shift" in gesture.modifierNames))
		else : return gesture.send()
	script_readPreview.__doc__ = _("Filtered reading of the message preview pane without leaving the list.")
	script_readPreview.category=sharedVars.scriptCategory

	def script_openMessage(self, gesture) :
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav()
		utils.setMLIState(self) # select and expand
		if sharedVars.oSettings.getOption("deactiv", "SWRnoRead") :
			sharedVars.msgOpened = "noRead"
		else :
			# msgOpened will no longer contain the current brailleMode
			sharedVars.msgOpened = "read" # utils.setBrailleMode("speechOutput")
		return gesture.send()
		
	def isUnifiedRow(self, oRow) :
		self.unifiedNextRow = False
		if not oRow : return
		for c in oRow.children :
			if utils.hasIA2Class(c, "location") :
				self.unifiedNextRow = True
				break
	# def focusNewRow(self) :
		# if self.unifiedNextRow : # if  sharedVars.delContextMenu :
			# KeyboardInputGesture.fromName("control+space").send()
			# speech.setSpeechMode(speech.SpeechMode.talk)
			# sharedVars.rowAfterDelete = None
			# CallLater(50, KeyboardInputGesture.fromName("control+space").send)
			# return

		# speech.setSpeechMode(speech.SpeechMode.talk)
		# if not sharedVars.rowAfterDelete : 
			# msg = _("No message selected, press Escape or Shift+Tab")
		# else :
			# msg =  str(sharedVars.rowAfterDelete.name)
		# message(msg)
		# sharedVars.rowAfterDelete = None
		
	def script_deleteMsg(self,gesture):
		if controlTypes.State.COLLAPSED in self.states :
			return gesture.send()
		# version 2512.10
		# below, the module utils is  in shared\utils115.py
		oPrevious = self.previous
		if oPrevious and controlTypes.State.SELECTED in oPrevious.states :
			return self.script_deleteWithMenu(gesture)
		oNext = self.next
		if oNext and controlTypes.State.SELECTED in oNext.states :
			return self.script_deleteWithMenu(gesture)
		if not oNext  and oPrevious :
			rowName =  self.customizeRow(oPrevious)
		elif  oNext : 				
			rowName = self.customizeRow(oNext)
		else :
			rowName = _("blank")
		parent = self.parent
		self.name = ""
		gesture.send() # sends delete to thunderbird
		utils.brailleClear()
		message(rowName, speech=False, braillePersists=True)
		CallAfter(speech.speakMessage, rowName)
		if parent.childCount == 0 :
			speech.cancelSpeech()
		# end 2512.10		

	def script_deleteWithMenu(self,gesture):
		if controlTypes.State.COLLAPSED in self.states :
			return gesture.send()
		speech.setSpeechMode(speech.speech.SpeechMode.off)  # onDemand)
		sharedVars.delPressed = True
		KeyboardInputGesture.fromName("applications").send()
		
	# def script_gotoMsg(self, gesture) :
		# sharedVars.nPressed = True
		# gesture.send()

	def script_gotoFirstMsg(self, gesture) :
		gesture.send()
		CallLater(50, 
		KeyboardInputGesture.fromName("upArrow").send)

		sharedVars.nPressed = True
		gesture.send()

	def script_sayShortcut (self,gesture):
		global gSaying
		rc = getLastScriptRepeatCount() 
		if gSaying  or rc : return beep(100, 20)
		gSaying = True
		sel = utils.getMessageStatus(infoIdx=2)
		mk = gesture.mainKeyName  
		if mk == "a" :
			sharedVars.lastJkey = mk
			lblAction = str(_("Deleted") if mk == "delete" else _("Archived")) + ", "
			lblCurrent = str(_("Current row")) + " : "
			if sel == "" :  # 1 message selected
				if self.name : sel = self.name[:30] 
				sel = lblAction + str(sel) + lblCurrent
				CallAfter(gSayShortcut, sel)
			else : # sevral selected
				message(lblAction + sel + lblCurrent)
				sleep(3.0)
				gSaying = False
			return gesture.send()
		elif mk == "c"  and"shift" in gesture.modifierNames :
			gSaying = False
			folder = self.windowText.split (" - ")[0]
			if rc == 0 : return message(_("Press this command twice to mark all messages as read in the folder:" + folder))
			else :
				gesture.send()
				return message(_("the {name} folder no longer contains unread messages.").format (name = folder))
		elif mk  == "j" : #   junk mail
			newState = (_("not junk") if "shift" in gesture.modifierNames else _("junk"))
			sel = utils.getMessageStatus(infoIdx=2)
			if sel  :
				message(_("{} applied. ").format(newState) + ", " + sel) 
			else :
				message(_("{} applied to: ").format(newState) + str(self.name))
			gSaying = False
			return			 gesture.send()

	def script_showFilterBar(self, gesture) :
		if utils.hasID(self, "threadTree") :
			return  KeyboardInputGesture.fromName ("control+shift+k").send()
		gesture.send()
	script_showFilterBar.__doc__ = _("Shows the quick filter bar from the message list.")
	script_showFilterBar.category=sharedVars.scriptCategory

	# def script_toggleUnread(self,gesture):
		# sharedVars.lastKey = "Del"
		# gesture.send ()
		# # callLater(600, sayTTi)
		
		# # sel = utils.getMessageStatus(infoIdx=2)
		# # if sel  :
			# # message(_("{} applied. ").format(_("read or unread")) + ", " + sel) 
		# # else :
			# # sleep(.1)
			# # s = getStatus(self, "read")
			# # if not s : 
				# # s  = _("Status column not found. Read or Unread applied.")
			# # else :
				# # s += " " + _("Applied to: ") + self.name 
			# # message(s)
			# # # causes the line to be reread at the wrong time > self.name =  self.appModule.buildColumnNames(self)
			# # sharedVars.curTTRow = self.appModule.buildColumnNames(self)
	# script_toggleUnread.__doc__ = _("Reverses the read and unread status of the selected message")
	# script_toggleUnread.category=sharedVars.scriptCategory
	def script_toggleUnread(self, gesture) :
		gesture.send()
		if not sharedVars.TTClean :
			return
		sleep(.2)
		message(self.customizeRow())
	script_toggleUnread.__doc__ = _("Reverses the read and unread status of the selected message")
	script_toggleUnread.category=sharedVars.scriptCategory

	# script_toggleUnread.__doc__ = _("Reverses the read and unread status of the selected message")
	# script_toggleUnread.category=sharedVars.scriptCategory
	
	# def script_toggleJunk(self, gesture) :
		# gesture.send()
		# # callLater(200, reportFocusedLine) 
		# sleep(.3)
		# value = utils.getColValue(self, "tree-view-row-spam junkstatuscol-")
		# if not value :
			# value = _("The junk or acceptable status  has been changed.")
		# elif value.endswith(" : ") : 
			# value += _("acceptable")
		# message(value)
	# script_toggleJunk.__doc__ = _("Reverses the junk and acceptable status of the selected message")
	# script_toggleJunk.category=sharedVars.scriptCategory

	def script_goGroupedFirst(self, gesture) :
		colIndex = getTotalCol(self)
		if  colIndex == -1 :
			return gesture.send()
		n =getThreadMsgCount(self, colIndex)
		if n == 1 : return gesture.send()
		# if  n > 1 and  controlTypes.State.COLLAPSED in self.states :
			# self.doAction() # expand
			# sleep(0.3)
		o = self
		oFound = None
		while o  :
			if getThreadMsgCount(o, colIndex) > 1 :
				oFound = o
				break
			o = o.previous
		# end while
		if oFound :
			oFound.setFocus()
			oFound.doAction()

	def script_goGroupedLast(self, gesture) :
		colIndex = getTotalCol(self)
		if  colIndex == -1 :
			return gesture.send()
		n =getThreadMsgCount(self, colIndex)
		sharedVars.logInit("* go first grouped ")
		sharedVars.logte("returned by getThreadMsgCount ={}".format(n))
		if n == 1 : return gesture.send()
		if  n > 1 and controlTypes.State.COLLAPSED in self.states :
			KeyboardInputGesture.fromName("rightArrow").send()
		callLater(50, self.selectLastMsgInGroup, colIndex)
			
	def selectLastMsgInGroup(self, colIdx) :
		if controlTypes.State.COLLAPSED in self.states :
			return callLater(100, self.selectLastMsgInGroup, colIdx) 
		try : o = self.next
		except : return  beep(100, 40)
		oFound = None
		while o  :
			if getThreadMsgCount(o, colIdx) > 0 :
				oFound = o.previous
				break
			oFound = o
			o = o.next
		# end while
		if not oFound :
			return
			# sharedVars.log(oFound, "oFound=")
		oFound .setFocus()
		oFound.doAction()

def getThreadMsgCount(o, totalColIdx) :
	try :
		return int(o.getChild(totalColIdx).firstChild.name)
	except :
		return 0
	return 0
	# sharedVars.log(o, "getThreadMsgCount, totalColIdx: " + str(totalColIdx))
	o =o.getChild(totalColIdx)
	# sharedVars.log(o, "getThreadMsgCount, row name : " + str(o.name))
	if o.childCount  == 0 :
		return 0
	# o = o.firstChild
	# nm = o.name
	# sharedVars.logte("value to return : {}".format(nm))
	return int(o.firstChild.name.strip())

# function helpers

def getToolbarButtons() :
	# ble, role.BUTTON=9, IA2ID : hdrJunkButton Tag: toolbarbutton, états :  Chemin : role FRAME=34| i34, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i7, role-BUTTON=9, , IA2ID : hdrJunkButton , IA2Attr : tag : toolbarbutton, explicit-name : true, class : toolbarbutton-1 msgHeaderView-button hdrJunkButton, display : -moz-box, id : hdrJunkButton, setsize : 19, posinset : 8, , Actions : press,  ;
	o = utis.getPropertyPageFromFG()
	if not o : return beep(150, 20)
	o = o.firstChild
	while o and o.role != controlTypes.Role.BUTTON : o = o.next
	if not o : return beep(150, 20)
	# sharedVars.debugLog = ""
	while o and  o.role == controlTypes.Role.BUTTON :
		if sharedVars.debug : sharedVars.log(o, " Bouton barre outils : ", False)
		o = o.next
		
def getToolbarButtonByID(btnID) :
	# ble, role.BUTTON=9, IA2ID : hdrJunkButton Tag: toolbarbutton, états :  Chemin : role FRAME=34| i34, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i7, role-BUTTON=9, , IA2ID : hdrJunkButton , IA2Attr : tag : toolbarbutton, explicit-name : true, class : toolbarbutton-1 msgHeaderView-button hdrJunkButton, display : -moz-box, id : hdrJunkButton, setsize : 19, posinset : 8, , Actions : press,  ;
	o = utis.getPropertyPageFromFG()
	if not o : return beep(150, 20)
	o = o.firstChild
	while o and o.role != controlTypes.Role.BUTTON : o = o.next
	if not o : return beep(150, 20)
	# sharedVars.debugLog = ""
	while o and  o.role == controlTypes.Role.BUTTON :
		if sharedVars.debug : sharedVars.log(o, " Bouton barre outils : ", False)
		if str(utis.getIA2Attribute(o)) == btnID :
			return o
		o = o.next
	return None


def setToStr(aSet, aLabel="", msgEmpty="") :
	if len(aSet) == 0 : return msgEmpty
	result = ""
	for e  in aSet :
		result += str(e) + ", " 
	return aLabel + " : " + result[:-2]

def chichiLinks(rc) :
	callLater(20, utis.sendKey, "space", rc, 0.02)
	callLater(100, speech.cancelSpeech) # message, "Liste de liens : ")
	return

def getStatus(oRow, which="read") :
	# sharedVars.debugLog +="* Columns properties\n"
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
		if ID == "statuscol" and which=="read" :
			o = oCell.firstChild
			if not o : return _("unread")
			else : 
				try : return o.Name
				except : return _("Read")

		# if ID == "junkStatusCol" and which = ""junk :
			# s =  _("Spam")
			# if   s not in sharedVars.curTTRow :
				# s =""
		oCell = oCell.next
	return ""

def  fSayTTi() :
	# sharedVars.logte("After delete sharedVars.curTTRow: " + sharedVars.curTTRow) 
	o = api.getFocusObject()
	# sharedVars.logte("After delete o.name: " + str(o.name)) 

def differMsg(ini=False) :
	if ini :
		sharedVars.gTimer = callLater(500, differMsg, False)
	else : 
		sharedVars.gTimer = None

def sayTTi() :
	# api.processPendingEvents()
	# o = api.getFocusObject()
	# message(str(o.name))
	sharedVars.nameChanging = False

class GetDescObject() :
	def __init__(self, mainRole, secondRole=None, ID="") :
		self.mainRole = mainRole
		self.secondRole = secondRole
		self.ID = ID
		self.mainObj = self.secondObj = None # object found after the run methode
		self.unifiedNextRow = False
	def run(self, obj) :
		if not obj : return
		obj = obj.firstChild
		if not obj : return 
		while obj :
			ID_OK = True
			if self.ID : 
				ID =  str(getIA2Attr(obj))
				if not ID.startswith(self.IDObj) : ID_OK = False
			if obj.role == self.secondRole   and ID_OK: self.secondObj = obj
			elif obj.role == self.mainRole   and ID_OK:self.mainObj = obj
			if self.mainObj and self.secondObj :return
			if obj.childCount > 0 :
				self.run(obj)
			obj = obj.next
def closeMenu(startTime) :
	# if time() - startTime > 2.0 : return beep(100, 40)
	# if  api.getFocusObject() .role != controlTypes.Role.MENUITEM :
		# beep(120, 10)
		# return CallLater(100, closeMenu, startTime)
	if sharedVars.debug : beep(440, 40)
	KeyboardInputGesture.fromName("tab").send()
	speech.setSpeechMode(speech.SpeechMode.talk)
# def reportFocusedLine() :
	# #speech.cancelSpeech()
	# fo = api.getFocusObject()
	# if fo.name :
		# message(fo.name)
		
def selLine(gest) :
	api.processPendingEvents()
	fo = api.getFocusObject()
	if controlTypes.State.SELECTED not in fo.states :
		fo.doAction()
		message(fo.name)
		beep(100, 40)

def nextRow(oRow) :
	if oRow.next :
		return oRow.next
	if oRow.previous :
		return oRow.previous
	beep(100, 40)
	return None
	# if oRow.next : 
		# o = oRow.next
		# if o.next : # and o.next.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) :
			# return o
		# if oRow.previous :
			# return o.previous
	# return None

# def focusNewRow2(nextRow, prevRow, posInfo) :
	# delay1 = sharedVars.deleteDelays[0] /1000 
	# delay2 = sharedVars.deleteDelays[1] /1000 
	# prevTTClean = sharedVars.TTClean
	# speech.setSpeechMode(speech.speech.SpeechMode.off)  # onDemand)
	# name = ""
	# index = posInfo['indexInGroup']
	# if nextRow : 
		# try : total = nextRow.positionInfo['similarItemsInGroup']
		# except : total = posInfo['similarItemsInGroup']
		# # total  = "Total= " + utils.getMessageStatus115()
		# name = str(nextRow.name) + " " + str(index) + _(" of ") + str(total)
		# # name = "NextRow=" + str(nextRow.name) +  str(posInfo)
		# sleep(delay1)
		# KeyboardInputGesture.fromName("downArrow").send()
		# sleep(delay2)
		# KeyboardInputGesture.fromName("upArrow").send()
	# elif  prevRow : 
		# if not sharedVars.TTClean :
			# try : total = prevRow.positionInfo['similarItemsInGroup']
			# except : total = posInfo['similarItemsInGroup']
			# # total = "Total= " + utils.getMessageStatus115()
			# name = str(prevRow.name) + " " + str(index - 1) + _(" of ") + str(total)
			# # name = str(prevRow.name) + str(posInfo)
		# sleep(delay1)
		# KeyboardInputGesture.fromName("upArrow").send()
		# sleep(delay2)
		# KeyboardInputGesture.fromName("downArrow").send()
	# else :
		# name = "No new row"
	# sharedVars.TTClean = prevTTClean
	# CallLater(50, sayNewRow, name) 
	
def sayNewRow(msg, later) :
	speech.setSpeechMode(speech.SpeechMode.talk)
	if msg :
		if later : CallLater(200, message, msg)
		else : message(msg)
		
# def saySmartNewRow128(nextRow, prevRow) :
	# delay1 = sharedVars.deleteDelays[0] /1000 
	# delay2 = sharedVars.deleteDelays[1] /1000 
	# sleep(delay1)
	# name = ""
	# if not prevRow and nextRow :
		# # sharedVars.log(nextRow, "no preVrow but NextRow")
		# if nextRow.role == controlTypes.Role.UNKNOWN :
			# KeyboardInputGesture.fromName("downArrow").send()
			# sleep(delay2)
			# speech.setSpeechMode(speech.SpeechMode.talk)

			# KeyboardInputGesture.fromName("upArrow").send()
	# if not nextRow and prevRow :
		# # sharedVars.log(nextRow, "no preVrow but NextRow")
		# name = prevRow.name
		# if prevRow.role == controlTypes.Role.UNKNOWN :
			# KeyboardInputGesture.fromName("upArrow").send()
			# sleep(delay2)
			# speech.setSpeechMode(speech.SpeechMode.talk)
			# KeyboardInputGesture.fromName("downArrow").send()
	# elif nextRow :
		# sharedVars.log(nextRow, "NextRow")
		# if nextRow.role == controlTypes.Role.UNKNOWN :
			# KeyboardInputGesture.fromName("upArrow").send()
			# sleep(delay2)
			# speech.setSpeechMode(speech.SpeechMode.talk)
			# KeyboardInputGesture.fromName("downArrow").send()
		# name = nextRow.name
	# elif prevRow :
		# # sharedVars.log(prevRow, "NextRow")
		# if prevRow.role == controlTypes.Role.UNKNOWN :
			# KeyboardInputGesture.fromName("upArrow").send()
			# sleep(delay2)
			# speech.setSpeechMode(speech.SpeechMode.talk)
			# KeyboardInputGesture.fromName("downArrow").send()
		# name = prevRow.name
	# # sayNewRow(name, later=False)
	# speech.setSpeechMode(speech.SpeechMode.talk)d

def saySmartNewRow128(nextRow, prevRow) :
	delay1 = sharedVars.deleteDelays[0] /1000 
	delay2 = sharedVars.deleteDelays[1] /1000 
	
	name = ""
	if nextRow : 
		name = nextRow.name
		sleep(delay1)
		KeyboardInputGesture.fromName("downArrow").send()
		sleep(delay2)
		KeyboardInputGesture.fromName("upArrow").send()
	elif  prevRow : 
		name = prevRow.name
		sleep(delay1)
		KeyboardInputGesture.fromName("upArrow").send()
		sleep(delay2)
		KeyboardInputGesture.fromName("downArrow").send()
	speech.setSpeechMode(speech.SpeechMode.talk)
	message(name)


def saySmartNewRow138(nextRow, prevRow) :
	delay1 = sharedVars.deleteDelays[0] /1000 
	delay2 = sharedVars.deleteDelays[1] /1000 
	sleep(delay1)
	if not prevRow and nextRow :
		# sharedVars.log(nextRow, "no preVrow but NextRow")
		if nextRow.role == controlTypes.Role.UNKNOWN :
			KeyboardInputGesture.fromName("downArrow").send()
			sleep(delay2)
			KeyboardInputGesture.fromName("upArrow").send()
	elif nextRow :
		# sharedVars.log(nextRow, "NextRow")
		if nextRow.role == controlTypes.Role.UNKNOWN :
			KeyboardInputGesture.fromName("upArrow").send()
			sleep(delay2)
			KeyboardInputGesture.fromName("downArrow").send()
	elif prevRow :
		# sharedVars.log(prevRow, "NextRow")
		if prevRow.role == controlTypes.Role.UNKNOWN :
			KeyboardInputGesture.fromName("upArrow").send()
			sleep(delay2)
			KeyboardInputGesture.fromName("downArrow").send()
	speech.setSpeechMode(speech.SpeechMode.talk)


def getPositionString(oRow, add) :
	index = oRow.positionInfo['indexInGroup'] + add
	try : total = oRow.positionInfo['similarItemsInGroup']
	except : total = "" 
	return " " + str(index) + _(" of ") + str(total)

def getTotalCol(oCurRow) :
	if oCurRow.role != controlTypes.Role.TREEVIEWITEM :
		return -1
	if not globalVars.TBThreadTree :
		return -1
	oRows = None
	o = globalVars.TBThreadTree .firstChild
	while o :
		# sharedVars.log(o, "getTotalCol first child=")
		if o.role == controlTypes.Role.TABLEROW :
			oRows = o
			break
		o = o.firstChild
	if not oRows : return -1
	o = oRows.firstChild
	i = 0
	while o :
		# sharedVars.log(o, "getTotalCol tableRow child=")
		if utils.hasID(o, "totalCol") : 
			return i
		o = o.next
		i += 1

	return -1
	