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
from wx import CallAfter
from core import callLater
from ui import  browseableMessage, message
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, utils115 as utils, sharedVars
# from . import foldersMessages
del sys.path[-1]
addonHandler.initTranslation()

from time import time, sleep

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
	"kb:space" : "readPreview",
	"kb:shift+space" : "readPreview",
	"kb:enter" : "openMessage",
	"kb:nvda+upArrow" : "sayLine",
	"kb(laptop):nvda+l" : "sayLine", 	
	# "kb:delete" : "deleteMsg",
	"kb:a" : "sayShortcut",
	# "kb:shift+c" : "sayShortcut",
	# "kb:j" : "sayShortcut",
	# "kb:shift+j" : "sayShortcut",
	"kb:f" : "showFilterBar",
	# "kb:m" : "toggleUnread"
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
	#lastScriptName=False
	def initOverlayClass (self):
		self.bindGestures(TTIDefGestures)
		if not sharedVars.TTnoTags :
			self.bindGestures(TTITagGestures)

	def script_sayLine(self, gesture):
		rc =  getLastScriptRepeatCount ()
		nm = self.name
		if rc > 0 :
			browseableMessage (message=nm.replace(", ", "\n"), title = _("Line details") + " - ThunderbirdPlus", isHtml = False)
		else : # 1 press
			if sharedVars.TTClean or sharedVars.TTFillRow : message(sharedVars.curTTRow)
			else :  message(self.name)
	script_sayLine.__doc__ = _("Message list : One press announces the current line, two presses displays the line text in a window.")
	script_sayLine.category=sharedVars.scriptCategory


	# read threadTree item  cells  
	def script_readTTICell(self,gesture):
		rc = getLastScriptRepeatCount()
		idx = int(gesture.mainKeyName)
		idx = 9 if idx == 0   else idx-1

		self.appModule.buildColumnID(self)

		if idx >= len (self.appModule.columnID) : return beep(100, 10)
		left = self.appModule.columnID[idx][0]
		ID = self.appModule.columnID[idx][1]
		label = self.appModule.columnID[idx][2] 
		oCell = self.getCellObj(left)
		if not oCell : return beep(100, 10)
		
		name = ""
		if oCell.name : name = oCell.name
		else : 
			try : name = oCell.firstChild.name
			except : pass  
		if not name :
			if "attachment" in ID : label = "" ; name = _("No Attachement.")
			else : name = _("Blank")
		if rc == 0 :
			message(label + name)
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
		msg ="{0}, {1}".format(msg,setToStr(newTagSet, lblTags, lblNoMore))
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
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
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
			else : return sharedVars.oQuoteNav.readMail(o, ("shift" in gesture.modifierNames))
		else : return gesture.send()
	script_readPreview.__doc__ = _("Filtered reading of the message preview pane without leaving the list.")
	script_readPreview.category=sharedVars.scriptCategory

	def script_openMessage(self, gesture) :
		if not sharedVars.oQuoteNav : sharedVars.initQuoteNav() # then use  sharedVars.oQuoteNav.*		self.regExp_date =compile ("^(\d\d/\d\d/\d{4} \d\d:\d\d|\d\d:\d\d)$")
		utils.setMLIState(self)
		sharedVars.msgOpened = True
		return gesture.send()
		
	def script_deleteMsg(self,gesture):
		# sharedVars.logte("Before delete : " + sharedVars.curTTRow) 
		# gesture.send()
		# sleep(.5)
		# callLater(200, fSayTTi) 
		if sharedVars.gTimer : beep(100, 5) ; return
		gesture.send()
		sharedVars.gTimer = callLater(50,  differMsg, True)
		

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

	def script_toggleUnread(self,gesture):
		sharedVars.lastKey = "Del"
		gesture.send ()
		# callLater(600, sayTTi)
		
		# sel = utils.getMessageStatus(infoIdx=2)
		# if sel  :
			# message(_("{} applied. ").format(_("read or unread")) + ", " + sel) 
		# else :
			# sleep(.1)
			# s = getStatus(self, "read")
			# if not s : 
				# s  = _("Status column not found. Read or Unread applied.")
			# else :
				# s += " " + _("Applied to: ") + self.name 
			# message(s)
			# # causes the line to be reread at the wrong time > self.name =  self.appModule.buildColumnNames(self)
			# sharedVars.curTTRow = self.appModule.buildColumnNames(self)
	script_toggleUnread.__doc__ = _("Reverses the read and unread status of the selected message")
	script_toggleUnread.category=sharedVars.scriptCategory


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
