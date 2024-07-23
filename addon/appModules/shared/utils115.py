#-*- coding:utf-8 -*
import addonHandler
addonHandler.initTranslation()
import controlTypes, api
from speech import  speakSpelling, cancelSpeech, setSpeechMode, SpeechMode
from ui import message
from time import time
from tones import beep
from wx  import  CallLater, CallAfter
import sharedVars
import utis
# from utis import utis.findParentByID, utis.inputBox, utis.wordsMatchWord, utis.getSpeechMode
from keyboardHandler import KeyboardInputGesture
import re
gRegFTI = re.compile("all-|unread-|smart-|favorite-|recent-|tags-")
prevSpeechMode = ""
def hasID(obj, IA2ID) :
	# IA2ID can be the n first chars of the ID
	r= hasattr (obj,"IA2Attributes") and "id" in obj.IA2Attributes.keys()
	if not r :return False
	r =str(obj.IA2Attributes["id"])
	return True if r.startswith(IA2ID) else False 

def getIA2Attr(obj,attribute_value=False,attribute_name ="id"):
	r= hasattr (obj,"IA2Attributes") and attribute_name in obj.IA2Attributes.keys ()
	if not r :return False
	r =obj.IA2Attributes[attribute_name]
	return r if not attribute_value  else r ==attribute_value

def isFolderTreeItem(fti, ID="") :
	if fti.role != controlTypes.Role.TREEVIEWITEM : return False 
	if not ID :
		ID = str(getIA2Attr(fti))
	if  gRegFTI.findall(ID) : return True
	return False

def isQuickfilterBar(o) :
	try : o = o.parent
	except : return False
	# Role.SECTION, ID : quickFilterBarContainer, 
	if o.role == controlTypes.Role.SECTION :
		if str(getIA2Attr(o)) == "quickFilterBarContainer" : return True
	return False

def checkObj(o, context="", oPrevious=None) :
	if o : 
		# sharedVars.log(o, "Passed "+ context)
		return True
	# message("Internal Error : object  is None  : " + context) 
	if sharedVars.debug : sharedVars.log(o, "Not passed : " + context) 
	# if oPrevious :
		# sharedVars.log(oPrevious, "Previous : ") 
	return  False


def findChildByRoleID(obj,role, ID, startIdx=0) : # attention : controlTypes roles
	if obj  is None : return None
	# ID can be the n first chars of the searched 
	try :  # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		try:
			if startIdx : o = obj.getChild(startIdx)
			else : o = obj.firstChild
		except :
			o = obj.firstChild
			pass
		while o:
			if o.role == role :
				if  hasID(o, ID) :
					# sharedVars.log(o, "toolbar found ")
					return o
			o = o.next
		return None
	finally :
		sharedVars.objLooping = prevLooping

def findParentByRole(o, role) :
	if o.role == role : return o 
	try :  # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		while o :
			# if sharedVars.debug : sharedVars.log(o, " parent ", False)
			if o.role == role :
					return o
			o = o.parent
		return None
	finally :
		sharedVars.objLooping = prevLooping

class FindDescendantTimer() :
	timer = None
	startTime = 0 
	foundObj = None
	logT = ""

	def __init__(self, role, ID="", name="", interval=20, maxElapsed=500) :
		self.role = role
		self.ID = ID
		self.name = name
		self.interval = interval
		self.maxElapsed = maxElapsed
		self.doAction = False
		
	def log(self, obj, lbl) :
		if not obj : return beep(80, 3)
		if obj.role != self.role : return beep(250, 3)
		# r = "No role" if not hasattr(obj, "role") else obj.role
		# nm = "No name" if not hasattr(obj, "name") else obj.name
		# self.logT += "{} : role={}, ID={}, name={}".format(str(lbl), r, str(getIA2Attr(obj)), nm) + "\n"
		if sharedVars.debug : sharedVars.log(obj, lbl)
		beep(600, 10)
		
	def run(self,obj, doAction=False) :
		if doAction : self.doAction = True
		self.startTime = time()
		self.timer = CallLater(self.interval, self.getSearchedObject, obj) 

	def getSearchedObject(self, o) : 
		if self.foundObj : 
			self.log(self.foundObj, "foundObj at beginning of getSearchedObj ")
			if self.doAction : self.foundObj.doAction()
			return
		self.log(o, "getSearchedObj begin")
		if time() - self.startTime >= self.maxElapsed : 
			self.timer.Stop()
			return

		try :
			o  = o.firstChild
			self.log(o, "startObj.firstChild found")
			if not o :return
		except :
			self.log(o, "Exception sur")
			return
		while o  :
			if  o.role == self.role :
				self.log(o, "Button Child")
				if self.name :
					if  o.name.find(self.name) > -1 : self.foundObj = o
				if not self.foundObj and self.ID  :
					if  hasID(o, self.ID) : self.foundObj = o
			if self.foundObj :
				self.timer.Stop()
				self.log(self.foundObj, "foundObj")
				if self.doAction : self.foundObj.doAction()
				break
			if time() - self.startTime >= self.maxElapsed : 
				self.timer.Stop()
				returbreak
			if o.childCount :
				self.timer = CallLater(self.interval, self.getSearchedObject, o)
			o = o.next
			
def getPropertyPage(oFrame=None) :
	# 24.06.02 : level 2,   2 of 2, role.PROPERTYPAGE, IA2ID : mail3PaneTab1 Tag: vbox, States : , childCount  : 1 Path : r-FRAME, | i31, r-GROUPING, , IA2ID : tabpanelcontainer | i2, r-PROPERTYPAGE, , IA2ID : mail3PaneTab1 , IA2Attr : id : mail3PaneTab1,
	if oFrame : o = oFrame
	else :o = api.getForegroundObject()
	# Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer 
	o = findChildByRoleID(o,controlTypes.Role.GROUPING, "tabpanelcontainer", 30)
	if not checkObj(o, "PropertyPage from  fg") : return None 
	# sharedVars.log(o, "grouping")
	# propPage in tab1, offscreen :  level 2,   2 of 4, Role.PROPERTYPAGE, IA2ID : mail3PaneTab1 Tag: vbox, States : , OFFSCREEN, childCount  : 1 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 , 
	# propPage in tab 3 :level 2,   4 of 4, Role.PROPERTYPAGE, IA2ID : mail3PaneTab3 Tag: vbox, States : , childCount  : 1 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i4, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab3 , IA2Attr : tag : vbox, class : deck-selected, id : mail3PaneTab3, display : flex, , Actions : click ancestor,  ;
	o = o.firstChild
	if not checkObj(o, "PropertyPage firstChild") : return None 
	while o :
		if o.role == controlTypes.Role.PROPERTYPAGE and  controlTypes.State.OFFSCREEN  not in o.states :
			# ID =  str(getIA2Attr(o))
			# if "mail3PaneTab" in ID :
			if hasID(o, "mail3PaneTab") : # partial ID
				checkObj(o, "getPropPage ")
				return o
		o = o.next
	checkObj(o, "getPropPage end")
	return None

def getFolderTreeFromFG(focus=False, pp=None) :
	# utis.beepRepeat(440, 10, 3) 
	if pp : o = pp
	else : o = getPropertyPage()
	if not checkObj(o, "getFT property page") : return None
	# with toolbar Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1| i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i0, Role-SECTION, , IA2ID : folderPane | i1, Role-TREEVIEW, , IA2ID : folderTree 
	# without toolbar Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 
	# wo : | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1  === | i0, Role-GROUPING,  | i0, Role-SECTION, , IA2ID : folderPane __ | i0, Role-TREEVIEW, , IA2ID : folderTree | i0, Role-TREEVIEWITEM,  ,
	# with : | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1  === | i0, Role-GROUPING,  ::: | i0, Role-SECTION, , IA2ID : folderPane __ | i1, Role-TREEVIEW, , IA2ID : folderTree
	try :
		# o = o.firstChild.firstChild.firstChild   .getChild(1)
		o = o.firstChild.firstChild.firstChild
		# sharedVars.log(o, "Retour de getFolderTree")
	except :
		checkObj(o, "getFT folderPane"	)
		return None
	o =   findChildByRoleID(o, controlTypes.Role.TREEVIEW, "folderTree") 
	if not checkObj(o, "getFT folderTree") : return None
	if  o and focus : o.setFocus()
	return o


class RecurseTree() :
	def	 __init__(self, role, IDObj="") :
		self.role = role
		self.ID = IDObj
		self.outObj = None
	def run(self,obj) : 
		if not obj : return
		obj = obj.firstChild
		if not obj : return 
		while obj :
			if obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) : 
				# 		if not self.ID or   hasID(obj, self.ID) :
				self.outObj = obj 
				return
			if obj.firstChild :
				self.run(obj)
			obj = obj.next
		return

# focus ThreadTree from FolderTree
def focusTTFromFT(oFocused, mode) :
	utis.disableOvl(False)
	# utis.beepRepeat(440, 20, 2)
	utis.setSpeechMode_off()
	sharedVars.speechOff = True # speech restored in see event_gainFocus
	KeyboardInputGesture.fromName("f6").send()
	sleep(.2)
	if  mode == 1 : # last message
		KeyboardInputGesture.fromName("end").send()
	elif mode == 2 : # first message 
		KeyboardInputGesture.fromName("home").send()
	elif	 mode > 2 : # first unread message 
		KeyboardInputGesture.fromName("n").send()
	# CallAfter(utis.speech.setSpeechMode, SpeechMode.talk)

def focusThreadTree(focus=False, fromFolderTree=False) :
	# disabled because speech is not always restored in event_gainFocus -> utis.setSpeechMode_off()
	focusMode = sharedVars.oSettings.getOption("messengerWindow", "focusMode", kind="i")
	if focusMode == 0 : focusMode = 1
	fo = api.getFocusObject() 
	role = fo.role
	if hasID(fo, "threadTree-") :
		if focusMode == 1 : k = "end"
		elif focusMode == 2 : k = "home"
		elif focusMode == 3 : k = "n"
		# sharedVars.speechOff = True # talk reactivated in event_gainFocus
		return CallAfter(KeyboardInputGesture.fromName(k).send)
	elif role == controlTypes.Role.TREEVIEWITEM : # we are in folder tree
		return CallAfter(focusTTFromFT, fo, focusMode)
	elif role != controlTypes.Role.FRAME :
		fo = api.getForegroundObject()
		fo.setFocus()
		fo = getFolderTreeFromFG(focus=False)
		if not fo :
			CallAfter(utis.speech.setSpeechMode, SpeechMode.talk)
			return
		fo.setFocus()
		oTimer = GetFocusObjTimer(roleList=[controlTypes.Role.TREEVIEWITEM], stateSelected=True, interval=500, maxElapsed=4000, callBack=focusTTFromFT, cbParam=focusMode)
		oTimer.run()

class GetFocusObjTimer() :
	timer = None
	callCount = 0
	def __init__(self, roleList, stateSelected,  interval, maxElapsed, callBack, cbParam) :
		self.roles = roleList
		self.stateSelected = stateSelected
		self.interval = interval
		self.maxElapsed = maxElapsed
		self.callBack = callBack
		self.cbParam = cbParam
		
	def run(self) :
			self.timer = CallLater(self.interval, self.getFocused) 

	def getFocused(self) : 
		self.callCount += 1
		if self.callCount * self.interval >= self.maxElapsed : 
			self.timer.Stop()
			self.timer = None
			return
		api.processPendingEvents()
		fo = api.getFocusObject()
		if  fo.role in self.roles :
			if self.stateSelected : selected  = True if controlTypes.State.SELECTED in fo.states else False
			else : selected = True
			if selected :
				self.timer.Stop()
				self.timer = None
				if self.callBack : 
					CallAfter(self.callBack, fo, self.cbParam)
				return
		else  :
			self.timer.Start() 

def getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, pp=None ) :
	global prevSpeechMode
	# Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 
	if pp : 
		o = pp
	else :
		o = getPropertyPage()
	if not checkObj(o, "property page") : return None
	# | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  
	try : o = o.firstChild.firstChild
	except :
		checkObj(o, "second grouping")
		return None
	
	# ancien  | i2or i4 , Role-SECTION, , IA2ID : threadPane 
	# 2024 06 : role.SECTION, IA2ID : threadPane Tag: div, States : , childCount  : 4 Path : r-FRAME, | i31, r-GROUPING, , IA2ID : tabpanelcontainer | i2, r-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, r-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, r-GROUPING,  | i2, r-SECTION, , IA2ID : threadPane
	prevO = o
	o = findChildByRoleID(o, controlTypes.Role.SECTION, "threadPane")
	if not checkObj(o, "section threadPane", prevO) : return None
	if getThreadPane and o : return o
	# | i2, Role-TEXTFRAME, , IA2ID : threadTree , 
	o = findChildByRoleID(o, controlTypes.Role.TEXTFRAME, "threadTree")
	if not checkObj(o, "threadTree") : return None
	
	# | i0, Role-TABLE,  | i2, Role-TREEVIEW
	o = o.firstChild.firstChild
	if not checkObj(o, "role treeview") : return None
	while o :
		# if not checkObj(o) : return None
		if o.role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW) :
			break
		o = o.next
	if  o and focus : o.setFocus()
	if nextGesture :
		prevSpeechMode = utis.getSpeechMode()
		setSpeechMode(SpeechMode.off)
		CallLater(50, silentSendKey, nextGesture)
	return  o
		

# def sayQFBInfos(o=None) :
	# try : # finally
		# prevLooping = sharedVars.objLooping
		# sharedVars.objLooping = True
		# if hasID(o, "threadTree")  : # threadTree item
			# # Path : | i2, Role-SECTION, , IA2ID : threadPane | i3, Role-TEXTFRAME, , IA2ID : threadTree | i0, Role-TABLE,  | i2, Role-TREEVIEW,  | i0, Role-TREEVIEWITEM, , IA2ID : threadTree-row0 
			# o = utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "threadTree")
			# while o :
				# if hasID(o, "quick-filter-bar") : break
				# if o.previous : o = o.previous
				# else : break	
			# if not o : return
			# oContainer = o.firstChild # quickFilterBarContainer  
		# elif  hasID(o.parent, "quickFilterBarContainer") :
			# oContainer = o.parent
		# #  sharedVars.log(oContainer, "sayQFBInfos begin")
		# # 1. retrieve number of messages
		# o = oContainer.lastChild.firstChild # qfbResultLabel firstChild
		# # sharedVars.log(o, "oContainer.lastChild")
		# t =""
		# while o :
			# if o.name : t += str(o.name) + ", "
			# o = o.next
		# if not t : t = _("No message informations")

		# # 2. retrieve filter infos
		# word = options = ""
		# # keyword edit 
		# o = oContainer.getChild(1)
		# if o.role == controlTypes.Role.EDITABLETEXT and o.value :
			# word = str(o.value)
		# o = o.next
		# while o :
			# if o.role ==  controlTypes.Role.TOGGLEBUTTON and controlTypes.State.PRESSED in o.states : options += o.name + ", "
			# # sharedVars.log(o, "child")
			# o = o.next
		# # sharedVars.logte(infos)	
		# if word or options : t += _("Expression input: %s") %word
		# message(t)
		# if word : speakSpelling(word)
		# if options : message(options)
	# finally :
		# sharedVars.objLooping = prevLooping

def getMessageStatus(infoIdx=-1)  :
	try : # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# level 8,         1 of 1, Role.SECTION, IA2ID : threadPaneFolderCountContainer, left:272 Tag: div, States : , childCount  : 4 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer 
		# level 9,          0 of 3, name : 13 messages, Role.STATICTEXT, left:281, States :  Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer | i0, Role-STATICTEXT,  
		# level 9,          1 of 3, Role.STATICTEXT, left:347, States :  Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer | i1, Role-STATICTEXT,  
		# level 9,          2 of 3, name : 11 messages sélectionnés, Role.STATICTEXT, left:359, States :  Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer | i2, Role-STATICTEXT,  
		# level 9,          3 of 3, Role.STATICTEXT, left:493, States :  Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID : threadPane | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer | i3, Role-STATICTEXT,  
		# get threadPane
		o = getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=True)
		# get | i0, Role-SECTION, , IA2ID : threadPaneHeaderBar | i0, Role-SECTION,  
		o = o.firstChild.firstChild
		# get | i1, Role-SECTION, , IA2ID : threadPaneFolderCountContainer 
		o = findChildByRoleID(o, controlTypes.Role.SECTION, "threadPaneFolderCountContainer")
		# return "examine le journal tbp	"
		if not o : return ""
		if infoIdx > -1 and infoIdx < 4 : 
			try : return o.getChild(infoIdx).name
			except : return ""
		# all fields
		t = ""
		o = o.firstChild
		while o :
			if o.name :
				t += o.name + ", "
			o = o.next
		if t : t = t[:-2]
		return t
	finally :
		sharedVars.objLooping = prevLooping

def silentSendKey(key) :
	KeyboardInputGesture.fromName (key).send()
	setSpeechMode(prevSpeechMode)
def getMessagePane() : # in the main window
	# level 8,         15 of 15, Role.INTERNALFRAME, IA2ID : messagepane Tag: browser, States : , FOCUSABLE, childCount  : 1 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 
	o = getPropertyPage()
	if not o : return None
	# | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  
	try : o = o.firstChild.firstChild
	except : return None
	# | i4, Role-SECTION, , IA2ID : messagePane 
	o = findChildByRoleID(o, controlTypes.Role.SECTION, "messagePane") 
	return o

def getMessageHeaders(msgPane=None) :
	if msgPane : 
		o = msgPane
	else :
		o = getMessagePane()
	if not o : return None
	# | i0, Role-INTERNALFRAME, IA2ID : messageBrowser | i0, Role-GROUPING,  
	if o.childCount :
		o = o.firstChild
	else  :
		print("getHeaders, Has no firstChild" + sharedVars.getObjAttrs(o))
		return None
	
	if o.childCount :
		o = o.firstChild
	else  :
		print("getHeaders, Has no firstChild" + sharedVars.getObjAttrs(o))
		return None
	# | i13 of 22, Role-LANDMARK, IA2ID : messageHeader 
	o = findChildByRoleID(o, controlTypes.Role.LANDMARK, "messageHeader", 12)
	return o

def getPreviewDoc() :
	o = getMessagePane()
	# checkObj(o, "get previwDoc, get messagePane")
	if not o :
		message(_("The preview pane is not displayed. Press F8 and try again please"))
		return None, False
	# parent of document :| i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  
	#|  child i15, Role-INTERNALFRAME, , IA2ID : messagepane 	
	# 2023-09-12 :try except added
	try : o = o.firstChild.firstChild
	except : return None, False 
	if not o : return None, True # retry needed 
	o = findChildByRoleID(o, controlTypes.Role.INTERNALFRAME, "messagepane", 14)  
	if not o : return None, True # retry needed 
	# checkObj(o, "getPreviewDoc, expected internal frame, messagepane")
	# level 9,          0 of 0, name : [nvda-fr] , Role.DOCUMENT , States : , FOCUSED, READONLY, FOCUSABLE, childCount  : 34 Path : Role-FRAME| i32, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID : messagepane | i0, Role-DOCUMENT
	o = o.firstChild
	# checkObj(o, "get previwDoc, document expected")
	if not o : return None, True # ask retry
	if o.role == controlTypes.Role.DOCUMENT :
		return o, False
	return None, False
	
def isSeparMsgWnd() :
	o =api.getForegroundObject()
	# Path : Role-FRAME| i4, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID : messagepane | i0, Role-DOCUMENT,  , 
	o = findChildByRoleID(o,controlTypes.Role.INTERNALFRAME, "messageBrowser")
	if not o :  return False
	sharedVars.curFrame = sharedVars.curTab= "1messageWnd"
	return True

def getOneMessageGrouping() :
	o =api.getForegroundObject()
	# Path : Role-FRAME| i4, Role-INTERNALFRAME, IA2ID : messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID : messagepane | i0, Role-DOCUMENT,  , 
	o = findChildByRoleID(o,controlTypes.Role.INTERNALFRAME, "messageBrowser")
	if not o :  return None
	sharedVars.curFrame = sharedVars.curTab= "1messageWnd"
	return o.firstChild

	# for message list item
from time import sleep
from keyboardHandler import KeyboardInputGesture
import winUser

def moveMouseToObject(o, moveCursor=True) :
	# location : RectLTWH(left=201, top=170, width=1522, height=22)
	loc = o.location
	# sharedVars.logte("location : left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height))
	x =  int(loc.left + loc.width / 2)
	y = int(loc.top + loc.height / 2)
	# sharedVars.logte("x {}, y {}".format(x, y))
	if moveCursor : winUser.setCursorPos (x, y)
	return x, y

def dragAndDrop(objSource,objTarget, objFocusAfter) :
	xS, yS = moveMouseToObject(objSource)
	# sharedVars.log(objSource, "dragDrop, Source x {}, y {}".format(xS, yS))
	sleep (0.2)
	winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
	x, y = moveMouseToObject(objTarget)
	# sharedVars.log(objTarget, "dragDrop, Target x {}, y {}".format(x, y))
	sleep (0.2)
	winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
	sleep (0.2)
	# api.processPendingEvents()
	# objFocusAfter.setFocus()
	# sharedVars.log(objFocusAfter, "DragDrop focus after")
	# click source
	# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,xS,yS,None,None)	
	# winUser.setCursorPos (xS, yS)
	# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,xS,yS,None,None)
	# sleep(0.005) 
	# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,xS,yS,None,None)


# def dragAndDrop(objSource,objTarget) :
	# xS, yS = moveMouseToObject(objSource, False)
	# xT, yT = moveMouseToObject(objTarget, False)

	# sharedVars.log(objSource, "dragDrop, Source x {}, y {}".format(xS, yS))
	# sharedVars.log(objTarget, "dragDrop, Target x {}, y {}".format(xT, yT))
	# winUser.setCursorPos (xS, yS)
	# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,xS,yS,None,None)
	# # sleep (0.2)

	# winUser.setCursorPos (xT, yT)
	# sleep (0.2)
	# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,xT,yT,None,None)
	# sleep (0.2)



def clickObject(o, left=True) :
	# location : RectLTWH(left=201, top=170, width=1522, height=22)
	api.setNavigatorObject(o)
	loc = o.location
	# sharedVars.logte("location : left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height))
	x =  int(loc.left + loc.width / 2)
	y = int(loc.top + loc.height / 2)
	# sharedVars.logte("x {}, y {}".format(x, y))
	winUser.setCursorPos (x, y)
	if left :
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
		sleep(0.005) 
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,1,None,None)
	else :
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,1,None,None)
		sleep(0.005) 
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,1,None,None)

def setState(o, newState) :
	if newState in o.states : 
		return
	if newState == controlTypes.State.SELECTED :
		# # clickObject(o)
		# KeyboardInputGesture.fromName ("control+space").send()
		o.doAction()
	elif newState == controlTypes.State.EXPANDED :
		if controlTypes.State.COLLAPSED   in o.states :  # necessary double precaution
			# clickObject(o) # necessary  in TB 115 
			o.doAction()
			KeyboardInputGesture.fromName ("control+righTArrow").send()
		else : return
	for i in range(0, 20):
		if newState  in o.states :
			# beep(440, 20)
			break
		api.processPendingEvents()
		sleep(0.1)

	# sharedVars.log(o, "setState,")
	# return

def setMLIState(obj) :
	role = obj.role
	if controlTypes.State.SELECTED not in obj.states : 
		setState(obj, controlTypes.State.SELECTED)
	if role == controlTypes.Role.TREEVIEWITEM   and controlTypes.State.EXPANDED not in obj.states :
		setState(obj, controlTypes.State.EXPANDED)
# Headers pane utils
class RecurseHeaders() :
	def	 __init__(self,IDObj, IDLabel, IDName) :
		self.IDObj = IDObj
		self.IDLabel = IDLabel
		self.IDName = IDName
		self.outObj = None
		self.outLabel = self.outName = ""
	def run(self,obj) : 
		if not obj : return
		obj = obj.firstChild
		if not obj : return 
		while obj :
			ID =  str(getIA2Attr(obj))
			if ID.startswith(self.IDObj) :
				if obj.role == controlTypes.Role.LISTITEM : 
					self.outObj = obj # .parent
					self.outLabel =  obj.parent.name
					o = obj
					while o:
						n =  self.cleanAddr(o.name)
						if n : self.outName += n + ";"
						o = o.next
					self.outName = self.outName[:-1]
					return
				else : # not listitem 
					self.outObj = obj
			if ID.startswith(self.IDLabel) :
				self.outLabel = obj.name  
			if ID.startswith(self.IDName) :
				self.outName = str(obj.name)
			self.run(obj)
			obj = obj.next
		return
	def cleanAddr(self, nm) :
		sep = " "
		if "<" in nm and ">" in nm :
			sep = ">"
		return  nm.split(sep)[0] + ">"				

def getHeader(o, key, repeats=0, say=True) :
	if not o : return"", ""
	# checkObj(o, "focus obj")
	if hasID(o, "threadTree") : 
		if controlTypes.State.COLLAPSED   in o.states :
			# does not work because Alt was pressed before :KeyboardInputGesture.fromName ("righTArrow").send()
			message(_("Press right arrow and retry, please."))
			return "", ""
		o = getMessagePane()
		# checkObj(o, "messagePane depuis liste")
		# if not o :
			# message("F8")
			# KeyboardInputGesture.fromName ("f8").send()
			# sleep(0.15)
			# o = getMessagePane()
			# # checkObj(o, "messagePane after  f8")
			# if not o : return
		if not o :  
			message(_("The headers pane is not displayed. Please press F8 then try again"))
			return "", ""
		o = getMessageHeaders(o)
	elif hasattr(o, "role") and  o.role == controlTypes.Role.DOCUMENT :
		o = findChildByRoleID(o.parent.parent, controlTypes.Role.LANDMARK, "messageHeader", 12)
	else : return "", ""
	# checkObj(o, "messageHeaders")
	if not o :  
		message(_("The headers are not available"))
		return "", ""
	role = controlTypes.Role.SECTION
	ran = False
	if key == 1 : #  from
		# level 1, idx 0 of 2 : Role.SECTION, ID : headerSenderToolbarContainer, childCount : 2
		o = findChildByRoleID(o, role, "headerSenderToolbarContainer", 0) 
		# level 2, idx 1 of 8 : Role.SECTION, ID : expandedfromRow, childCount : 2
		# level 3, idx 0 of 1 : Role.LABEL, ID : expandedfromLabel, childCount : 1
		# name : From
		# level 3, idx 1 of 1 : Role.SECTION, ID : expandedfromBox, childCount : 1
		# level 4, idx 0 of 1 : Role.LIST, ID : None, childCount : 1
		# name : From
		# level 5, idx 0 of 2 : Role.LISTITEM, ID : fromRecipient0, childCount : 2
		# name : Lav <progliste@framalistes.org> Not in the Address Book
		oHeader = RecurseHeaders("fromRecipient0", "dummy", "dummy")
	elif key == 3 : # date 
		o = findChildByRoleID(o, role, "expandedtoRow", 1) 

		oHeader = RecurseHeaders("dateLabel", "dummy", "dummy")
		oHeader.run(o)
		oHeader.outName =str(oHeader.outObj.firstChild.name) 
		return message(oHeader.outName)
	elif key == 4 : # to
		o = findChildByRoleID(o, role, "expandedtoRow", 1) 
		oHeader = RecurseHeaders("toRecipient0", "expandedtoLabel", "dummy")
		# level 1, idx 1 of 2 : Role.SECTION, ID : expandedtoRow, childCount : 3
		# level 2, idx 0 of 1 : Role.LABEL, ID : expandedtoLabel, childCount : 1
		# name : To
		# level 3, idx 0 of 0 : Role.STATICTEXT, ID : None, childCount : 0
		# name : To
		# level 2, idx 1 of 1 : Role.SECTION, ID : expandedtoBox, childCount : 1
		# level 3, idx 0 of 1 : Role.LIST, ID : None, childCount : 1
		# name : To
		# level 4, idx 0 of 2 : Role.LISTITEM, ID : toRecipient0, childCount : 2
		# name : Yannick  <progliste@framalistes.org> Not in the Address Book
	elif key == 5 : # CC:
		o = findChildByRoleID(o, role, "expandedccRow", 2) 
		oHeader = RecurseHeaders("ccRecipient0", "expandedccLabel", "dummy")
		# level 1, idx 2 of 2 : Role.SECTION, ID : expandedccRow, childCount : 2
		# level 2, idx 0 of 1 : Role.LABEL, ID : expandedccLabel, childCount : 1
		# name : Cc
		# level 3, idx 0 of 0 : Role.STATICTEXT, ID : None, childCount : 0
		# name : Cc
		# level 2, idx 1 of 1 : Role.SECTION, ID : expandedccBox, childCount : 1
		# level 3, idx 0 of 2 : Role.LIST, ID : None, childCount : 2
		# name : Cc
		# level 4, idx 0 of 3 : Role.LISTITEM, ID : ccRecipient0, childCount : 3
		# name : Vincent  <vincent@xx> In the Address Book
	elif key == 6 : # BCC:
		o = findChildByRoleID(o, role, "expandedbccRow", 2) 
		oHeader = RecurseHeaders("bccRecipient0", "expandedbccLabel", "dummy")
	elif key == 2 : # subject
		o = findChildByRoleID(o, role, "headerSubjectSecurityContainer", 0) 
		if not o :
			beep(100, 20)
			return None
		oHeader = RecurseHeaders("expandedsubjectBox", "expandedsubjectLabel", "dummy")
		oHeader.run(o)
		oHeader.outName =str(oHeader.outObj.name) # .replace(oHeader.outLabel + ": ", "")
		ran =  True
		# level 1, idx 2 of 2 : Role.SECTION, ID : headerSubjectSecurityContainer, childCount : 1
		# level 2, idx 0 of 2 : Role.SECTION, ID : expandedsubjectRow, childCount : 2
		# level 3, idx 0 of 1 : Role.LABEL, ID : expandedsubjectLabel, childCount : 1
		# name : Subject
		# level 4, idx 0 of 0 : Role.STATICTEXT, ID : None, childCount : 0
		# name : Subject
		# level 3, idx 1 of 1 : Role.SECTION, ID : expandedsubjectBox, childCount : 1
		# name : Subject: Re: [progliste] application trop complexe dès le départ
		# level 4, idx 0 of 0 : Role.STATICTEXT, ID : None, childCount : 0
		# name : Re: [progliste] application trop complexe dès le départ
	# elif key == 9 : # attachments
	elif key == 0 : # tags
		# level 9,          4 of 10, Role.SECTION, IA2ID : expandedtagsRow, left:232 Tag: div, States : , childCount  : 1 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID : messageHeader | i4, Role-SECTION, , IA2ID : expandedtagsRow , IA2Attr : id : expandedtagsRow, display : flex, class : message-header-row, tag : div,  ;
		o = findChildByRoleID(o,controlTypes.Role.SECTION, "expandedtagsRow")
		# level 10,           0 of 0, Role.SECTION, IA2ID : expandedtagsBox, left:232 Tag: div, States : , childCount  : 1 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID : messageHeader | i4, Role-SECTION, , IA2ID : expandedtagsRow | i0, Role-SECTION, , IA2ID : expandedtagsBox , IA2Attr : id : expandedtagsBox, display : block, class : header-tags-row, tag : div, formatting : block,  ;
		# level 11,            0 of 0, name : Étiquettes, Role.LIST, left:230 Tag: ol, States : , READONLY, childCount  : 1 Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID : messageHeader | i4, Role-SECTION, , IA2ID : expandedtagsRow | i0, Role-SECTION, , IA2ID : expandedtagsBox | i0, Role-LIST,  , IA2Attr : class : tags-list, explicit-name : true, child-item-count : 1, display : flex, tag : ol,  ;
		o = o.firstChild.firstChild
		t = o.name + " : "
		o = o.firstChild
		while  o :
			if o.name : t += o.name + ", "
			o = o.next
		return message(t)
	else : # extra headers
		return message(u"entête non encore implémenté")
		# level 1, idx 3 of 2 : Role.SECTION, ID : extraHeadersArea, childCount : 0
		# End of Header list
	# execution
	if not ran :
		oHeader.run(o)
	if not oHeader.outObj : 
		headerLabels = _("void,From,Subject: ,Date,To,CC,BCC,Reply to") 
		headerNotFound = _("The {0} header is missing from this message.")
		if say : message(headerNotFound.format(headerLabels.split(",")[key]))
		try : return  oHeader.outLabel, oHeader.outName
		except : return "", ""
	if repeats == 0 :
		if say :
			oHeader.outLabel += ("" if not oHeader.outLabel else " : ") 
			message(oHeader.outLabel + oHeader.outName)
		else :
			return oHeader.outLabel, oHeader.outName
	elif repeats == 1 :
		CallLater(100, utis.inputBox , label=oHeader.outLabel, title= oHeader.outLabel + ": " + _("Copy to clipboard"), postFunction=None, startValue=oHeader.outName)
	else :
		try : oHeader.outObj.doAction()
		except : clickObject(oHeader.outObj, False) # right click
	return  ""

def getAttachment(oFocus=None, repeats=0) :
	# in  main window :name : doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID : attachmentName Path : Role-FRAME| i31, Role-GROUPING, , IA2ID : tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID : mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID : mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID : messagePane | i0, Role-INTERNALFRAME, , IA2ID : messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID : attachmentName , IA2Attr : id : attachmentName, display : flex, xml-roles : button, tag : label, , Actions : click,  ;
	# In separate window : 18 of 20, name : doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID : attachmentName, Path : Role-FRAME| i4, Role-INTERNALFRAME, IA2ID : messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID : attachmentName
	# sharedVars.debugLog = "getAttachment, repeats : " + str(repeats) + "\n"
	if not oFocus : oFocus = api.getFocusObject()
	if oFocus.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.LINK)  : 
		# if repeats > 0 and oFocus.role == controlTypes.Role.LINK : beep(700, 40)
		o = findParentByRole(oFocus, controlTypes.Role.GROUPING)
		# sharedVars.log(o, "is Grouping from doc ? ")
		if repeats > 0 and o.role != controlTypes.Role.GROUPING : return beep(100, 10)
	elif hasID(oFocus, "threadTree") :
		o = getMessagePane()
		# sharedVars.log(o, "in mainWindow , is messagePane ?")
		o = o.firstChild.firstChild
		# sharedVars.log(o, "in mainWindow , is Grouping ?")
	else : return beep(100, 30)
	
	# common to list and separate reading window
	oStart = o.getChild(14) # cannot be 15 which ID is messagePane
	oLast = o.lastChild
	# sharedVars.log(oStart, "oStart, repeats : " + str(repeats))
	# sharedVars.log(oLast, "oLast, repeats : " + str(repeats))		

	oList = None
	ID = str(getIA2Attr(oLast))
	if ID in ("messagepane", "content") :
		return message(_("No attachment."))
	elif ID.startswith("attachmentSaveAll") :  # hidden attachment list
		o = oStart
		# search  :   Role.TOGGLEBUTTON, ID : attachmentToggle, childCount : 0
		while o :
			ID = str(getIA2Attr(o))
			if o.role == controlTypes.Role.TOGGLEBUTTON and ID == "attachmentToggle" :
				if controlTypes.State.PRESSED not in o.states : 
					# beep(440, 10)
					CallAfter(o.doAction)
					return
			o = o.next
	elif ID == "attachmentList" : 
		oList = oLast

	text =  ""
	o = oStart
	while o :
		# sharedVars.log(o, "getAttachmment, in loop : ")
		ID = str(getIA2Attr(o))
		if ID == "attachmentCount" :
			text +=  str(o.name)
		elif ID == "attachmentSize" :
			text +=  o.name
		o = o.next
	# sharedVars.logte(text)
	if repeats == 0 :
		text += ", "
		o = oList.firstChild
		while o : 
			text += str(o.name) + ", "
			o = o.next
		message(text + ", " + _("Two presses to reach the list."))
	elif repeats > 0 : 
		if  oList.childCount  > 1 : oList.setFocus()
		else : CallAfter(clickObject, oList, False) # right click

def smartReply(repeats=0) :
	o = api.getFocusObject()
	if o.role == controlTypes.Role.DOCUMENT and controlTypes.State.READONLY not in o.states :
		return
	toLabel =  toNames = ""
	try : # 2024.06.26
		toLabel, toNames = getHeader(o, 4, 0, False) # key repeats say
	except :
		return CallLater(25, KeyboardInputGesture.fromName("control+r").send)
	if not toNames :
		toNames = str(getHeader(5, 0, False)) # key repeats say
	isList = (repeats== 0 and utis.wordsMatchWord("@googlegroups|@framalist|@freelist", toNames))
	if isList : 
		message(_("To the group, "))
		# display a menu -> return CallLater(150, replyTo, msgHeader, 1)
		# beep(100, 40)
		return CallLater(25, KeyboardInputGesture.fromName("control+shift+l").send)
	else : # not alist
		# delay = 25
		# if "groups.io" in toNames :
			# if ";" not in str(toNames) : message(_("To the list, "))
			# else : 
				# delay = 250
				# message(toLabel + " 2 addresses") #  + toNames
			# return CallLater(delay, KeyboardInputGesture.fromName("control+r").send)
			# ordinary correspondent
			# beep(440, 10)
			KeyboardInputGesture.fromName("control+r").send()
def getTotalColIdx(oTT):
	try : # finally
		# oTT must be the threadTree
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
			# flat list mode : path Role-TEXTFRAME, , IA2ID : threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
		o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
		i = 0
		while o   :
			if hasID(o, "totalCol") :
				# sharedVars.logte("index of total col : " + str(i))
				return i
			i += 1
			o = o.next
		return -1
	finally :
		sharedVars.objLooping = prevLooping

def cleanWinTitle(title) :
	i =  title.rfind(" - ")
	if i > -1 :
		title =  title[0:i]
	return title.strip((" ,;:?!+"))
# test funcions
def listColumnID(oTT):
	try :
		# oTT must be the threadTree
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# sharedVars.logte("Begin Column ID list")
			# flat list mode : path Role-TEXTFRAME, , IA2ID : threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
		o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
		i = 0
		while o   :
			role = str(o.role)
			ID = str(getIA2Attr(o))
			left =  str(o.location.left) 
			name = "" if not hasattr(o, "name") else o.name
			cName = ""
			if o.firstChild :
				cName = "" if not hasattr(o.firstChild, "name") else o.firstChild.name
			# sharedVars.logte("idx : {},ID {}, left : {}, name : {}, cName : {}, {}".format(i, ID, left, name, cName, role))
			i += 1
			o = o.next
	finally :
		# sharedVars.logte("End of  Column ID list")
		sharedVars.objLooping = prevLooping
def listColumnNames(oRow) :
	if sharedVars.debug : sharedVars.logte("* Begin of columnNames ")
	o = oRow.firstChild
	while o :
		left =  str(o.location.left) 
		clsFull = str(getIA2Attr(o, False, "class"))
		cls = clsFull.split(" ")
		cls = str(cls[len(cls)-1])
		cls = cls.split("-")[0]
		name = "" if not o.name else ", name:" + str(o.name)
		value = "" if not o.value else ", value:" + str(o.value)
		cName = cValue = ""
		if o.firstChild :
			oc = o.firstChild
			cName = "" if not oc.name else ", cName:" + str(oc.name)
			cValue = "" if not oc.value else ", cValue:" + str(oc.value)
		if sharedVars.debug : sharedVars.logte(left + ", " +  cls + ", " + clsFull + str(name) + str(value) + str(cName) + str(cValue))
		o = o.next
	# sharedVars.logte("* End of columnNames ")
	

def getColValue(oRow, colID) :
	o = oRow.firstChild
	idx = 0
	iFound = -1
	while o :
		cls = str(getIA2Attr(o, False, "class"))
		if cls.startswith(colID) :
			iFound = idx
			break
		idx += 1
		o=o.next

	if iFound == -1 : return "" # colID + " column not found"
	cName = ""	
	oc = oRow.getChild(iFound)
	while oc :
		if hasattr(oc, "name") : cName +=str(oc.name)
		try : oc = oc.firstChild
		except : break

	# result = "cls={}, index={}, cName={}".format(cls, iFound, cName)
	return cName
		
def recurseObjects(o, level): 
	if not o : return None
	o = o.firstChild
	if not o : return None
	cCount = " of " + str(o.childCount)
	level += 1
	i = 0
	while o :
		# sharedVars.log(o, "# level " + str(level) + ", idx " + str(i) + cCount)
		if o.childCount > 0 :
			recurseObjects(o, level)
		o = o.next
		i += 1
	return o
def listAscendants(last=-4, o=None, title="** List of ascendants") :
	last = (last if last <= 0 else 0 - last)
	if not o :
		o = api.getFocusObject()
	if sharedVars.debug : sharedVars.logte(title)
	lev = 0
	while o  and lev >= last :
		if sharedVars.debug : sharedVars.log(o, "level " + str(lev))
		lev -= 1
		o = o.parent

def listDescendants(o=None, lev=0, tit=None) :
	if not o :
		o = api.getFocusObject()
	if tit :
		if sharedVars.debug : sharedVars.logte(tit)
	lev += 1
	o = o.firstChild
	i = 1
	while o :
		if sharedVars.debug : sharedVars.log(o, "level " + str(lev) + " " + str(i))
		if o.childCount :
			listDescendants(o, lev) 
		i +=1
		o = o.next


