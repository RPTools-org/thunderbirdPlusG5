#-*- coding:utf-8 -*
# Thunderbird+ G5 tabAddressBook

import api
from time import sleep
from NVDAObjects.IAccessible import IAccessible, getNVDAObjectFromPoint
from ui import message, browseableMessage
import speech
import controlTypes
from wx import CallAfter, Menu, EVT_MENU
from core import  callLater
import winUser
import 	addonHandler,  os, sys
from keyboardHandler import KeyboardInputGesture
from tones import  beep
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, sharedVars, utils115 as utils
del sys.path[-1]
addonHandler.initTranslation()

oDragDropper = oContactLine = None
lastBook = ""

class AddressBook(IAccessible):
	ABMenu = None
	ABMenuPointers = None
	idx = 0
	def initOverlayClass (self):
		global oContactLine
		self.bindGestures({"kb:control+applications" :"menuAB"})
		if self.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM) and utils.hasID(self, "cards-row") :
			self.bindGestures({"kb:a" :"addContactTo", "kb:d" :"setDest"})		
			if not oContactLine : oContactLine = ContactLine()
			oContactLine.line = ""

	def __del__(self) :
		global oContactLine
		oContactLine = None
		# destructor
		
	def event_gainFocus (self):
		global oDragDropper, oContactLine
		role = self.role
		ID = str(utils.getIA2Attr(self))
		name2 = ""

		if role == controlTypes.Role.TREEVIEWITEM and ID.startswith("cards-row") : # element of contact table
			# normal view, mail address path : i1, Role-TREEVIEWITEM, , IA2ID : cards-row1 | i0, Role-TEXTFRAME,  | i0, Role-TEXTFRAME,  | i1, Role-TEXTFRAME,  | i1, Role-TEXTFRAME,  | i0, Role-STATICTEXT
			o =  self.firstChild.firstChild
			if o.role == controlTypes.Role.TEXTFRAME :
				try : 
					o = o.getChild(1).getChild(1).firstChild
					return message(self.name + ", " + o.name + + ", " + str(self.positionInfo['indexInGroup']) + _(" of ") + str(self.positionInfo['similarItemsInGroup']))
				except : message(self.name+ ", " + str(self.positionInfo['indexInGroup']) + _(" of ") + str(self.positionInfo['similarItemsInGroup'])) ; return
			# table view
			try : 
				oContactLine.buildLine(self)
				message(oContactLine.line + ", " + str(self.positionInfo['indexInGroup']) + _(" of ") + str(self.positionInfo['similarItemsInGroup']))
				return
			except : return message(self.name)
		elif role == controlTypes.Role.TREEVIEWITEM : # books tree
			if oDragDropper : oDragDropper = None
			if ID.startswith("book-") : name2 = ", " + _("Address book")
			if ID.startswith("list-") : name2 = getParentBook(self)
		elif role == controlTypes.Role.EDITABLETEXT :
			if self.value : name2 = ", " + self.value
			else :  name2 = ", " + _("blank")
		elif  role == controlTypes.Role.BUTTON :
			name2 = ", " + controlTypes.Role.BUTTON.displayString
			if ID.startswith("toolbarCreateBook") : name2 += ", " + _("Press Alt + down arrow to open the context menu.")  
		elif  role == controlTypes.Role.POPUPMENU :
			name2 = ", " + controlTypes.Role.POPUPMENU.displayString
		message(self.name + name2)
		

	def getContactTable(self, oDoc) :
		# default view : | i0, Role-DOCUMENT,  | i3, Role-SECTION, , IA2ID : cardsPane | i1, Role-TEXTFRAME, , IA2ID : cards | i0, Role-TABLE,  | i1, Role-TREEVIEW, , IA2ID : cardsBody , IA2Attr : id : 
		# table view : | i0, Role-DOCUMENT,  | i3, Role-SECTION, , IA2ID : cardsPane | i1, Role-TEXTFRAME, , IA2ID : cards | i0, Role-TABLE,  | i2, Role-TREEVIEW, , IA2ID : cardsBody 
		o = utils.findChildByRoleID(oDoc, controlTypes.Role.SECTION, "cardsPane")
		o = utils.findChildByRoleID(o, controlTypes.Role.TEXTFRAME, "cards")
		o = o.firstChild
		o = utils.findChildByRoleID(o, controlTypes.Role.TREEVIEW, "cardsBody")
		return o

	def menuToolbar(self) :
		# self is any control in the address book document
		oDoc =  utils.findParentByRole(self, controlTypes.Role.DOCUMENT)
		if not oDoc :  return
		self.ABMenu = Menu()
		self.ABMenuPointers = []
		idx = 0
		
		# Book and list tree
		try : 
			o = oDoc.getChild(1).firstChild # treeview of books
			self.ABMenu.Append(idx, _("Go to &address books and mailing lists tree"))
			self.ABMenuPointers.append(o)
			idx += 1
		except : pass
		# sharedVars.log(o, "AB Treeview")
		# Contact table
		o = self.getContactTable(oDoc)
		if o :
			self.ABMenu.Append(idx, _("Go to &contact table"))
			self.ABMenuPointers.append(o)
			idx += 1

		
		# toolbar buttons
		try : o = oDoc.firstChild.firstChild  # toolbar first button
		except : return
		while o and o.role == controlTypes.Role.BUTTON:
			self.ABMenu.Append(idx, o.name)
			self.ABMenuPointers.append(o)
			idx += 1
			o = o.next			
		self.ABMenu.Bind (EVT_MENU,self.onMenu)
		utis.showNVDAMenu  (self.ABMenu)

	def onMenu(self, evt):
		utis.setSpeech(False)
		o = self.ABMenuPointers[evt.Id]
		# name = o.name + ", " if o.name else ""
		# name += o.role.displayString
		msg = ""
		if utils.hasID(o, "toolbarCreateBook") : msg = _("Press Alt + down arrow to open the popup menu")  
		callLater(100, utis.enableSpeechAndSay, msg, True)
		o.doAction()
		self.ABMenu = self.ABMenuPointers = None

	def script_menuAB(self, gesture) :
		self.menuToolbar()

	def script_addContactTo(self, gesture) :
		global oDragDropper
		if winUser.getKeyState(winUser.VK_LBUTTON)&32768:		
			# release left button
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
			return beep(440, 50)
		# contact source
		o = self
		o.scrollIntoView()
		if not utils.hasID(o, "cards-row") or controlTypes.State.SELECTED not in o.states :
			return beep(100, 30)
		# sharedVars.log(o, "Contact")
		# sharedVars.logte("Contact location : " + str(o.location))
		# beep(200, 40)
		if not oDragDropper :
			oDragDropper = DragDropper()
		oDragDropper.setObject(obj=o, target=False)
		if oDragDropper.objTarget :
			oDragDropper.doDragAndDrop()
		else :
			#message("Destination book or list not defined, press D.")
			if not oDragDropper :
				oDragDropper = DragDropper()
			oDragDropper.autoDragDrop = True
			self.script_setDest(gesture)

	def script_setDest(self, gesture) :
		global oDragDropper
		if not oDragDropper :
			oDragDropper = DragDropper()
		#  target   books and lists
		
		o =  utils.findParentByRole(self, controlTypes.Role.DOCUMENT)
		if not o :  return beep(110, 15)
		try : o = o.getChild(1).firstChild # treeview of books
		except : return beep(200, 40)
		# sharedVars.log(o, "AB Treeview")
		oDragDropper.setTarget(o)

class DragDropper() :
	def __init__(self, autoDrag=False) :
		self.dbg = False # debug mode of this class
		self.autoDragDrop = autoDrag 
		self.objSource = self.objTarget = self.ABMenu = self.ABPointers = None
		self.idx = 0
		self.curBook = ""

	def  setObject(self, obj, target=False) :
		obj.scrollIntoView()
		if target :
			self.objTarget = obj
			t ="t"
		else : 
			self.objSource = obj
			t = "s"
		x, y = self.getObjLocation(obj, t)
		winUser.setCursorPos(x, y)
		self.logObjUnderCursor(0, 0, "setObject " + t)
		if target and self.autoDragDrop :
			self.autoDragDrop = False
			self.doDragAndDrop()
			
	def setTarget(self, oABTree) :
		self.ABMenu = Menu()
		self.ABPointers = []
		self.idx = 0
		self.buildBooksMenu(oABTree)
		self.ABMenu.Bind (EVT_MENU,self.onABMenu)
		callLater(50,message, _("Destinations from ") +self.curBook)
		utis.showNVDAMenu  (self.ABMenu)

	def buildBooksMenu(self, o) :
		global lastBook
		o = o.firstChild
		while o :
			ID = str(utils.getIA2Attr(o)) 
			role = o.role
			if role == controlTypes.Role.TREEVIEWITEM and controlTypes.State.SELECTED in o.states : 
				self.curBook = o.name
			if o.role == controlTypes.Role.TREEVIEWITEM and not ID.startswith("allAddressBooks")  and controlTypes.State.SELECTED not in o.states and controlTypes.State.INVISIBLE not in o.states and controlTypes.State.OFFSCREEN not in o.states :
				include = True ; parName = ""
				if ID.startswith("list-") :
					include, parName = self.includeList(o)
				if include :
					if  o.name == lastBook :
						nm =  "& " + o.name + parName
					else : nm = o.name + parName
					self.ABMenu.Append(self.idx, nm)
					self.ABPointers.append(o)
					self.idx += 1
			if o.childCount : 
				self.buildBooksMenu(o)
			o = o.next			
			
	def includeList(self, obj) :
		if self.dbg :  sharedVars.log(obj, "include list list")
		obj = obj.parent
		while obj :
			if obj.role == controlTypes.Role.TREEVIEWITEM and utils.hasID(obj, "book-") :
				# if self.dbg : return True, _("list in ") + obj.name
				if controlTypes.State.SELECTED in obj.states : return True, _("list in ") + obj.name
			obj = obj.parent
		return False, ""
		if self.dbg :  sharedVars.log(o, "include list parent")
		if o and  controlTypes.State.SELECTED in o.states : return True
		return False
	def onABMenu(self, evt):
		global lastBook
		o = self.ABPointers[evt.Id]
		if not o : return beep(100, 30) 
		lastBook = o.name
		self.setObject(o, True) # target


	def getObjLocation(self, obj, type) :
			# location : RectLTWH(left=201, top=170, width=1522, height=22)
		loc = obj.location
		# sharedVars.logte("location : left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height))
		x =  loc.left + 8 # int(loc.left + loc.width / 2)
		y = loc.top + 8 # int(loc.top + loc.height / 2)
		if self.dbg : sharedVars.logte("getObjLocation {}, Name {}, x {}, y {}".format(type, str(obj.name), x, y))
		return x, y

	def doDragAndDrop(self) :
		speech.setSpeechMode(speech.SpeechMode.off)
		self.ABMenu = self.ABPointers = None
		if self.dbg :  
			# sharedVars.debugLog = "dragDropper.doDragDrop\n"
			self.logInfos("Begin function")
		xSource, ySource  = self.getObjLocation(self.objSource, "Source")
		xTarget, yTarget  = self.getObjLocation(self.objTarget, "Target")
		wait = 0.002
		winUser.setCursorPos (xSource, ySource)
		sleep (wait)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
		sleep(0.1)
		if self.dbg : self.logInfos("Begin drag up")			
		# sleep (wait)
		winUser.setCursorPos (xSource, ySource+30)
		sleep(wait)
		winUser.setCursorPos (xTarget, yTarget)
		if self.dbg : beep(440, 40) ; return
		api.processPendingEvents()
		sleep(.05)
		if self.dbg: self.logInfos("End Drag drop")
		beep(440, 40)
		callLater(100, speech.setSpeechMode, speech.SpeechMode.talk)
		callLater(150, KeyboardInputGesture.fromName("shift+f6").send)
		callLater(200, KeyboardInputGesture.fromName("control+a").send)
		# release left button
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)

		# click source			# winUser.setCursorPos (xSource, ySource)
		# sleep (wait)
		# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
		# sleep (wait)
		# winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		
	def logObjUnderCursor(self, x, y, label) :
		if x+y == 0 :
			pos = winUser.getCursorPos()
			x = pos[0]
			y = pos[1]
		
		o = getNVDAObjectFromPoint(x, y)
		# # if o.role == controlTypes.Role.TEXTFRAME : o = o.parent
		# while o :
			# if o.name :
				# break
			# o = o.parent
		ID = "ID : " + str(utils.getIA2Attr(o))
		sharedVars.logte("* {} object under cursor x : {} y{}, {}, {}".format(label, x, y, self.getObjectProps(o), ID))

	def logLeftButtonState(self, label) :
		sharedVars.logte(label)
		
	def getObjectProps(self, o) :
		s = ""
		if o.name : s += "name : " + str(o.name)
		s += ", " + str(o.role) 
		loc = o.location
		s+= "location : left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height)
		return s
	def logInfos(self, msg="") :
		sharedVars.logte("\n" + msg + " : ")
		self.logObjUnderCursor(0, 0, "")
		if winUser.getKeyState(winUser.VK_LBUTTON)&32768:
			label = "* left button is Down"
		else :
			label = "* left button is Up"
		sharedVars.logte(label)
		hwFG = winUser.getForegroundWindow()
		title = winUser.getWindowText(hwFG)
		sharedVars.logte("* Foreground window : " + str(title))
		sharedVars.logte("* Focus Object : " + self.getObjectProps(api.getFocusObject()))

def getParentBook(obj) :
		obj = obj.parent
		while obj :
			if obj.role == controlTypes.Role.TREEVIEWITEM and utils.hasID(obj, "book-") :
				return ", " + _("list in ") + obj.name
			obj = obj.parent
		return ""

class ContactLine() :
	def __init__(self) :
		# self.obj = None
		self.line = ""
	
	def buildLine(self, obj) :
		# recursive function
		obj = obj.firstChild
		while obj :
			if obj.role == controlTypes.Role.STATICTEXT :
				self.line +=  obj.name + ", "
				sharedVars.logte("contact line : " + self.line)
			if obj.childCount :
				self.buildLine(obj)
			obj = obj.next
