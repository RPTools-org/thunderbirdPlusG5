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
from tones import beep
from re import compile
from datetime import datetime
from ui import message, browseableMessage
from gui import mainFrame  
from keyboardHandler import KeyboardInputGesture
import globalVars
from time import sleep, mktime, time
from winsound import PlaySound,SND_MEMORY, SND_PURGE, MessageBeep,MB_ICONASTERISK
import threading
objSoundFiles = {}
import speech
from wx import CallAfter, Menu, MessageBox
from core import callLater
from winUser import setCursorPos, getKeyNameText 
import addonHandler,  os, sys
addonHandler.initTranslation()

import api
from api import copyToClip
from UIAHandler import handler,UIA_LegacyIAccessibleRolePropertyId, UIA_LegacyIAccessibleStatePropertyId, TreeScope_Children, UIA_ButtonControlTypeId, UIA_ControlTypePropertyId, IUIAutomationInvokePattern, UIA_LegacyIAccessibleKeyboardShortcutPropertyId, TreeScope_Descendants, UIA_SeparatorControlTypeId, UIA_TabItemControlTypeId,UIA_LegacyIAccessibleDescriptionPropertyId 
clientObject =handler.clientObject
GetPreviousSiblingElement = clientObject.RawViewWalker.GetPreviousSiblingElement
GetFirstChildElement  = clientObject.RawViewWalker.GetFirstChildElement
GetNextSiblingElement =clientObject.RawViewWalker.GetNextSiblingElement
import sharedVars
import globalVars


def _unicode(s) : return str(s)
def isChichi() :
	if sharedVars.chichi is not None : return sharedVars.chichi
	# level 4,     6 of 7, name : chichi, Role.BUTTON, IA2ID : chichi_free_fr-browserAction-toolbarbutton Tag: toolbarbutton, States :  Path : Role-FRAME| i46, Role-GROUPING, , IA2ID : tabpanelcontainer | i0, Role-PROPERTYPAGE, , IA2ID : mailContent | i0, Role-TOOLBAR, , IA2ID : mail-bar3 | i6, Role-BUTTON, , IA2ID : chichi_free_fr-browserAction-toolbarbutton , IA2Attr : tag : toolbarbutton, id : chichi_free_fr-browserAction-toolbarbutton, class : toolbarbutton-1 webextension-action, explicit-name : true, setsize : 2, display : -moz-box, posinset : 1, , Actions : press,  ;
	o = getPropertyPageFromFG()
	# sharedVars.log(o, "prop page : ")
	if not o or not hasattr(o, "role") : return False
	if o.role != controlTypes.Role.PROPERTYPAGE : return False
	# i0, Role-TOOLBAR, , IA2ID : mail-bar3 | i6, Role-BUTTON, , IA2ID : chichi_free_fr-browserAction-toolbarbutton
	o =  findChildByID(o, "mail-bar3")
	# sharedVars.log(o, "Toolbar : ")
	if not o : return False
	o = findChildByRoleID(o, "chichi_free_fr-browserAction-toolbarbutton", controlTypes.Role.BUTTON)
	# sharedVars.log(o, "Bouton  : ")
	sharedVars.chichi = (True if o else False)
	# sharedVars.log(o, "Chichi : " + str(sharedVars.chichi))
	return sharedVars.chichi

def beepRepeat(freq, dur, repeats=1) :
	for i in range(0, repeats) :
		beep(freq,  dur)
		sleep(.3)
def noSpeechMessage(msg) :
	speech.cancelSpeech()
	message(msg)

def playSound (soundFile): 
	try :
		threading.Thread (None, PlaySound, None, (objSoundFiles[(soundFile if soundFile.endswith (".wav") else soundFile+".wav")],SND_MEMORY|SND_PURGE)).start ()
	except : 
		# deactivated for those who don't like sound -> beep(440, 80)
		pass #son non trouvé

def versionTB() :   
	return int(globalVars.foregroundObject.appModule.productVersion.split(".") [0])

def TBVersion(asInt=False) : # full version string
	pv = globalVars.foregroundObject.appModule.productVersion
	if not asInt : return pv
	tv = pv.split(".")
	tv[1] = str(tv[1]).rjust(2, "0") # minor version
	tv[2]= "0" if not tv[2] else tv[2] # build
	tv[2] = str(tv[2]).rjust(2, "0")
	v = tv[0] +  tv[1] + tv[2]	
	return int(v)

def addonVersion(sp="%20") :
	_curAddon = addonHandler.getCodeAddon()
	name = _curAddon.manifest["name"]
	ver = _curAddon.manifest["version"]
	return  name + sp + ver.split(" ")[0]

# new speechMode functions by Paulber19 for NVDA 2021.1+ ander previous 
def getSpeechMode():
	try:
		# for nvda version >= 2021.1
		return speech.getState().speechMode
	except AttributeError:
		return speech.speechMode

def setSpeechMode(mode):
	global prevSpeechMode
	try:
		# for nvda version >= 2021.1
		speech.setSpeechMode(mode)
	except AttributeError:
		speech.speechMode = mode

def setSpeechMode_off():
	global prevSpeechMode
	#print(u"Fonction setSpeechMode_off")
	try:
		# for nvda version >= 2021.1
		speech.setSpeechMode(speech.SpeechMode.off)
	except AttributeError:
		speech.speechMode = speech.speechMode_off

def setSpeech(enable) :
	global  prevSpeechMode
	if enable and prevSpeechMode :
		setSpeechMode(prevSpeechMode)
		prevSpeechMode = None
	elif not enable :
		prevSpeechMode = getSpeechMode()
		setSpeechMode_off()

def enableSpeechAndSay(msg, focusName=False) :
	if focusName :
		o = api.getFocusObject()
		msg = str(o.name) + ", " + o.role.displayString + ", " + msg 
		speech.setSpeechMode(speech.SpeechMode.talk)
	message(msg)


def getIA2Attribute (obj,attribute_value=False,attribute_name ="id"):
	r= hasattr (obj,"IA2Attributes") and attribute_name in obj.IA2Attributes.keys ()
	if not r :return False
	r =obj.IA2Attributes[attribute_name]
	return r if not attribute_value  else r ==attribute_value

def disableOvl(mode) :
		sharedVars.objLooping = mode

def findChildByRoleID(obj,ID, role, startIdx=0) : # attention : valeurs role de controlTypes.pyelse :

	if obj  is None : return None

	try : 
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
				if  str(getIA2Attribute(o)) ==  ID:
					# sharedVars.log(o, "toolbar found ")
					return o
			o = o.next
		return None
	finally :
		sharedVars.objLooping = prevLooping


def findChildByID(obj,id) : # attention : valeurs role de controlTypes.py
	# 2023-07-31 : added folowin line
	if obj  is None : return None
	try : 
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		try:
			o = obj.firstChild
		except :
			return None
		while o:
			ia2ID = str(getIA2Attribute(o))  # get_ia2Id(o)	
			if  ia2ID ==  id:
				return o
			try:
				o= o.next
			except:
				o = None
		return None	
	finally :
		sharedVars.objLooping = prevLooping

def findChildByIDRev(obj,id) : # attention : valeurs role de controlTypes.py
	# 2023-07-31 : added folowin line
	if obj  is None : return None

	try : 
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		try:
			o = obj.lastChild
		except :
			return None
		while o:
			ia2ID = str(getIA2Attribute(o)) # get_ia2Id(o)	
			if  ia2ID ==  id:
				return o
			try:
				o= o.previous
			except:
				o = None
		return None	
	finally :
		sharedVars.objLooping = prevLooping

def findParentByID(o, role, ID) :
	if str(getIA2Attribute(o)) == ID :
		return o
	try : 
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		while o :
			if sharedVars.debug : sharedVars.log(o, " parent ", False)
			if o.role == role :
				if str(getIA2Attribute(o)) == ID :
					return o
			o = o.parent

		return None
	finally :
		sharedVars.objLooping = prevLooping

def formatDateTime (d):
	return d
	"""if not d.count (":"):return d
	elif d and not d.count("/"):return u" aujourdhui à" +formatTime (d.split (":"))
	date =d.split (" ")
	date_original =date[0]
	date, time = date[0].split ("/"), date[1].split (":")
	date =datetime (int (date[2]), int (date[1]), int (date[0]))
	return weekDay[date.weekday ()]+" "+date_original+u" à " +formatTime (time)"""
def wordsMatchWord(words, word) :
	lst = words.split("|")
	for e in lst:
		if e in word : return True
	return False

def hasTabPanel(frame=None) :
	try :
		sharedVars.objLooping = True
		if not frame :
			frame = globalVars.foregroundObject
		o = frame.lastChild
		while o :
			#beep(100, 2)
			#if sharedVars.debug : sharedVars.log(o, " frame child " + str(i))
			if o.role  == controlTypes.Role.GROUPING :
				if str(getIA2Attribute(o)) == "tabpanelcontainer" : 
					return True
			if o.previous : o = o.previous
			else : o = None
		return False
	finally :
		sharedVars.objLoping = False

def getObjFirstGrouping (self): 
	#if not api.getForegroundObject():return getObjFirstGrouping2 (self) # modif PL
	try :
		o = clientObject.ElementFromHandle (api.getForegroundObject().windowHandle)
		o=o.FindFirst(TreeScope_Children,clientObject.CreatePropertyCondition (UIA_LegacyIAccessibleRolePropertyId  , 22)) #barre d'outilTB
		if o and GetNextSiblingElement(o):
			o=GetNextSiblingElement(o)
			if o.GetCurrentPropertyValue(30095)==22 : o=GetNextSiblingElement(o)
			o= GetFirstChildElement(o)
		else :
			oo=api.getForegroundObject()
			oo= findChildByID(oo,"tabpanelcontainer") 
			oo= findChildByID(oo,"mailContent") 
			oo=oo.firstChild
			(x,y,l,h)=oo.location
			from ctypes.wintypes import POINT, RECT
			o=clientObject.ElementFromPoint(POINT(int(x)+40,int(y)+8)) # bouton relever
			while o and  o.GetCurrentPropertyValue (30095)!=38:
				o=clientObject.ControlViewWalker.GetParentElement(o)
		if o and o.GetCurrentPropertyValue (30095)==38 : return o
		else : return False
	except :
		MessageBeep
		return False

def getObjFirstGrouping2 (self): 
	try :
		o = clientObject.ElementFromHandle (api.getFocusObject().windowHandle).FindFirst(TreeScope_Children,clientObject.CreateAndCondition (clientObject.CreatePropertyCondition (30095,38),clientObject.CreatePropertyCondition (30011,"mailContent" )))
		return o
	except :
		try :
			oo=api.getForegroundObject()
			oo= findChildByID(oo,"tabpanelcontainer") 
			oo= findChildByID(oo,"mailContent") 
			oo=oo.firstChild
			(x,y,l,h)=oo.location
			from ctypes.wintypes import POINT, RECT
			o=clientObject.ElementFromPoint(POINT(int(x)+40,int(y)+8)) # bouton relever
			while o and not o.GetCurrentPropertyValue(30095)==38 : #page propriétés
				o=clientObject.RawViewWalker.getParentElement(o)
			if o and clientObject.RawViewWalker.GetParentElement(o).GetCurrentPropertyValue(30095)==20 :
				return o
		except :	
			# print (u" !!! problème firstGrouping 2  !!!")	
			return  False		

def getElementWalker(o,n):
	walker = clientObject.createTreeWalker(clientObject.CreateTrueCondition ())
	if n==4 :o=walker.getParentElement(o)
	elif n==5 :o=walker.getNextSiblingElement(o)
	elif n==6 :o=walker.getPreviousSiblingElement(o)
	elif n==7 :o=walker.getFirstChildElement(o)
	elif n==8 :o=walker.getLastChildElement(o)
	return o

# Pour  TB91 :   l'ID "messengerWindow" a disparu du frame de la fenêtre principale
# ID=compose-toolbar-menubar2, role TOOLBAR=35  

def getExpandedHeadersFromFO(o, num="") :
	try :
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True

		ID =     "expandedHeaders" + num 
		if o.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.TABLEROW) : # liste messages 
			o2 = o.parent.parent # role-PROPERTYPAGE=57, , IA2ID : mailContent 
		elif controlTypes.Role.DOCUMENT : 
			o2 = o.parent.parent # role frame  = 34
		elif role in (controlTypes.Role.UNKNOWN, controlTypes.Role.BUTTON) :
			while  o :
				if o.role == controlTypes.Role.TABLE : return o
				if o.role in (controlTypes.Role.FRAME, controlTypes.Role.PROPERTYPAGE) : return -1
				o = o.parent
			return -1
			return -1 # retry
		o2 = o2.lastChild 
		# cherche : Niveau 3,    11 sur 19, role.TABLE=28, IA2ID : expandedHeaders Tag: table, états : , childCount  : 2 Chemin : role FRAME=34| i37, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i11, role-TABLE=28, , IA2ID : expandedHeaders , IA2Attr : id : expandedHeaders, layout-guess : true, tag : table, display : inline-grid,  ;
		while o2 :
			if o2.role == controlTypes.Role.TABLE :
				if str(getIA2Attribute(o2)) == ID  :
					return o2
			o2 = o2.previous
	finally :
		sharedVars.objLooping = prevLooping

def getIAPropertyPage (o=None) :
	# retturns the propertypage obj if found otherwise an obj of an upper level, ie. role frame = 34
	r = None
	if not o :
		o = api.getFocusObject()
		# search role frame=34
	while o :
		if o.role ==controlTypes.Role.FRAME :
			r = o
			break
		o = o.parent
	if not o : return None
	#   niveau 2, 47 sur 50, ID=tabpanelcontainer, role GROUPING=56, childCount=2, sans nom, Chemin : role WINDOW=1|, role FRAME=34 messengerWindow|, role GROUPING=56 tabpanelcontainer ;
	# search role GROUPING=56 tabpanelcontainer
	o = o.lastChild 
	while o :
		if o.role == controlTypes.Role.GROUPING : # 56
			if getIA2Attribute(o)  == "tabpanelcontainer" : 
				r = o
				break
		o = o.previous
	if not o : return r
	# search role 57 property page , ID in  ("mailContent", "messengerWindow") :
	o = o.firstChild
	while o :
		if o.role == controlTypes.Role.PROPERTYPAGE :
			if  getIA2Attribute(o) ==  "mailContent" :
				return o
	return r
def setGroupingIndex() :
	# by default in TB 115, sharedVars.groupingIdx = 32 # index of child object of role grouping in the foregroundObject children   
	try : 
		sharedVars.objLooping = True
		try : o = api.getForegroundObject()
		except : 
			sharedVars.groupingIdx = 27
			return
		if not o : sharedVars.groupingIdx = 28 ; return
		if o.role != controlTypes.Role.FRAME : return
		i = min(30, o.childCount ) # changed on 2023.12.29 for TB 115.6.0
		try : o = o.getChild(i)
		except : sharedVars.groupingIdx = i ; return
		while o :
			if o.role == controlTypes.Role.GROUPING :  
				sharedVars.groupingIdx = i
				return			
			i += 1
			o=o.next
	finally :
		sharedVars.objLooping = False
		
	
def getPropertyPageFromFG() :
	# 2023-01-03 this version is 2 times faster than the old one
	try :
		sharedVars.objLooping = True
		# t = time()
		if sharedVars.curFrame == "1messageWindow" :
			return sharedVars.oCurFrame
		# search for grouping : level 1,  46 of 49, Role.GROUPING, IA2ID : tabpanelcontainer Tag: tabpanels, States : , childCount  : 3 Path : Role-FRAME| i46, Role-GROUPING, , IA2ID : tabpanelcontainer , IA2Attr : display : -moz-deck, class : plain, tag : tabpanels, id : tabpanelcontainer, , Actions : click ancestor,  ;
		if sharedVars.groupingIdx < 26 :
			i = 30 # for TB 115
			try : o = sharedVars.oCurFrame.getChild(i)
			except : return None # globalVars.foregroundObject # sharedVars.oCurFrame # for separate message window.
			while o :
				if o.role == controlTypes.Role.GROUPING :
					sharedVars.groupingIdx = i
					break
				o = o.next
				i += 1
		else :
			o = sharedVars.oCurFrame.getChild(sharedVars.groupingIdx)
		if not o : return None
		# search  level 2,   0 of 3, Role.PROPERTYPAGE, IA2ID : mailContent Tag: box, States : , OFFSCREEN, childCount  : 5 Path : Role-FRAME| i46, Role-GROUPING, , IA2ID : tabpanelcontainer | i0, Role-PROPERTYPAGE, , IA2ID : mailContent , IA2Attr : display : -moz-box, id : mailContent, tag : box, , Actions : click ancestor,  ;
		#  on the main Tab if property page  is not offscreen
		try :
			o = o.firstChild # propertypage
		except : return None, 2
		# if controlTypes.State.OFFSCREEN in o.states : return None
		return o
	finally :
		# ms = time() - t
		# sharedVars.log(None, "getPropertyPage duration : {0}".format(ms * 1000))
		sharedVars.objLooping = False

# def getPropertyPageFromFG() :
	# try :
		# sharedVars.objLooping = True
		# t = time()
		# fg =  globalVars.foregroundObject
		# # 0 sur 3, role.PROPERTYPAGE=57, IA2ID : mailContent Tag: box, états : , childCount  : 3 Chemin : role FRAME=34| i37, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent , IA2Attr : id : mailContent, display : -moz-box, tag : box,  ;
		# o = fg.lastChild
		# while o : 
			# if o.role  == controlTypes.Role.GROUPING :
				# break
			# if o.previous :
				# o = o.previous
			# else : o = None
		# if not o :  # no grouping, search other frame
			# #  role FRAME=34| i23, role-INTERNALFRAME=115, , IA2ID : content-frame | 
			# o = fg.lastChild.previous
		# #ID =  getIA2Attribute(o)
		# # search propertypage
		# o = o.firstChild
		# if not o : return fg
		# if o.role == controlTypes.Role.PROPERTYPAGE :
			# return o
		# else :
			# return fg
	# finally :
		# ms = time() - t
		# sharedVars.log(None, "getPropertyPage duration : {0}".format(ms * 1000))
		# sharedVars.objLooping = False

# with collapsed brnach : level 1,  3 of 3, Role.INTERNALFRAME, IA2ID : multimessage Tag: browser, States : , FOCUSABLE, childCount  : 1 Path : Role-PROPERTYPAGE| i3, Role-INTERNALFRAME, , IA2ID : multimessage , IA2Attr : id : multimessage, display : inline, tag : browser, , Actions : click,  ;
# with expanded branch : level 1,  4 of 5, Role.LANDMARK, IA2ID : messageHeader Tag: header, States : , FOCUSABLE, childCount  : 7 Path : Role-PROPERTYPAGE| i4, Role-LANDMARK, , IA2ID : messageHeader , IA2Attr : xml-roles : banner, display : grid, class : message-header-container scrollable, tag : header, id : messageHeader, , Actions : click ancestor,  ;

def getPreviewPane(oPropPage=None) :
	if not oPropPage  or  (oPropPage and oPropPage.role != controlTypes.Role.PROPERTYPAGE ) :
		oPropPage = getPropertyPageFromFG() 
		# 2023-05-18 bug fix, added is None
		if oPropPage is None or oPropPage.role != controlTypes.Role.PROPERTYPAGE : return None, -1
	o = oPropPage.lastChild
	while o :
		role =o.role 
		if role  ==controlTypes.Role.INTERNALFRAME  : break 
		elif role == controlTypes.Role.EDITABLETEXT: o = None
		else : o=o.previous
	return o

def getMessageHeadersFromFG(reportNotOpen=True) :
	# look for in main window : 7 sur 8, role.LANDMARK = 149, IA2ID : messageHeader Tag: header, états : , childCount  : 5 Chemin : role FRAME=34| i47, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i7, role-LANDMARK = 149, , IA2ID : messageHeader , IA2Attr : display : grid, id : messageHeader, tag : header, xml-roles : banner, class : message-header-container, , Actions : click ancestor,  ;
	# in separate msg window : 19 sur 21, role.LANDMARK = 149, IA2ID : messageHeader Tag: header, états : , childCount  : 5 Chemin : role FRAME=34| i19, role-LANDMARK = 149, , IA2ID : messageHeader , IA2Attr : display : grid, id : messageHeader, tag : header, xml-roles : banner, class : message-header-container, , Actions : click ancestor,  ; 
	o = getPropertyPageFromFG() # returns  a property  page object if found otherwise a frame object
	# sepWnd = (True if o.role == controlTypes.Role.FRAME else False)
	o = o.lastChild
	while o :
		if o.role == controlTypes.Role.LANDMARK : # table ID= expandedHeaders
			if str(getIA2Attribute(o)) == "messageHeader" : 
				return o # , sepWnd
		o = o.previous
	return None # , sepWnd

def strBetween(txt, sep1, sep2) :
	pos1 = txt.find(sep1) 
	if pos1 < 0 : return ""
	pos2 = txt.find(sep2, pos1)
	if  pos2 < 0 : return ""
	return txt[pos1+1:pos2]

def truncateBefore(text, subStr) :
	p = text.find(subStr)
	if p == -1 : return text
	return text[p:]


def truncateAfter(text, subStr) :
	p = text.find(subStr)
	if p == -1 : return text
	return text[0:p]
	
def getStatusBarText() :
	o = globalVars.foregroundObject # frame
	t = ""
	o = o.lastChild
	while o :
		if o.role == controlTypes.Role.STATUSBAR :
			break
		o = o.previous
	if not o : return _("The status bar is not displayed.")
	o = o.firstChild
	while o :
		if o.role != controlTypes.Role.BUTTON :
			if hasattr(o, "name") :
				if o.name : t += str(o.name ) + ", "
		o = o.next
	return t

def sendKey(keyName, num=1, delay=0.01) :
	i = 1
	while i <= num :
		# sharedVars.log(None, "sendKey, i " + str(i) + ", num " + str(num))
		KeyboardInputGesture.fromName(keyName).send()
		if i < num : sleep(delay)
		i += 1

# 2022-12-09 : 2 scancode functions
def gestureFromScanCode(sc, prefix="") :
	# sc stands for the scanCode  of the key
	# prefix is "kb:modifiers"
	k = getKeyNameText(sc, 0)
	return prefix + k

def listGestFromScanCodes() :
	txt = "Scancode : Key name\n"
	for i in range(0, 102) :
		k = getKeyNameText(i, 0)
		txt += "{0} : {1}".format(i, k) + "\n"
	CallAfter(browseableMessage, message =txt, title = "List of keys from scancodes", 	isHtml = False)

def showNVDAMenu (menu):
	setCursorPos(100,100)
	sleep(0.03)
	CallAfter (displayMenu,menu)
def displayMenu (menu):
	mainFrame.prePopup ()
	mainFrame.PopupMenu (menu)
	mainFrame.postPopup ()

def toolBarClickButton (toolBar, buttonIndex): toolBar.FindAll (TreeScope_Children, clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId,  UIA_ButtonControlTypeId)).GetElement (buttonIndex).GetCurrentPattern (10000 ).QueryInterface (IUIAutomationInvokePattern).Invoke ()
def alertClickButton(objStart, evt):
	hk =evt.GetEventObject ().GetLabelText (evt.Id).split (" ")[-1]
	if not hk.count ("+"):
		o= GetNextSiblingElement ( objStart.FindFirst (TreeScope_Descendants , clientObject.CreateAndCondition (clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_ButtonControlTypeId),clientObject.CreatePropertyCondition (UIA_LegacyIAccessibleKeyboardShortcutPropertyId, evt.GetEventObject().GetLabelText (evt.Id-1).split (" ")[-1]))))
	else:
		o= objStart.FindFirst (TreeScope_Descendants , clientObject.CreateAndCondition (clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_ButtonControlTypeId),clientObject.CreatePropertyCondition (UIA_LegacyIAccessibleKeyboardShortcutPropertyId, evt.GetEventObject().GetLabelText (evt.Id).split (" ")[-1])))
	CallAfter (o.GetCurrentPattern (10000 ).QueryInterface (IUIAutomationInvokePattern).Invoke)

def formatTime (time):
	"""h, m=int (time[0]), int (time[1])
	#>>h =("minuit" if not h else h)
	#h>>=("midi" if h ==12 else h )
	m=(" " if not m else m)
	if m :
		time =("{h} heure {m}".format (h=h, m=m) if str (h).isdigit () else str (h)+" "+str (m))
	else:
		time =h"""
	return time

def  getTimeStamp  (t):
	if t.count ("/"):
		t =t.replace ("/"," ").replace (":"," ").split (" ")
		day,month, year, hour, minute =[int (e) for e in t]
	else:
		t, now =[int (e) for e in t.split (":")], datetime.now ()
		day, month, year, hour, minute = now.day, now.month, now.year, t[0], t[1]
	return  float (mktime (datetime  (year =year,month =month, day =day, hour =hour, minute=minute).timetuple ()))

def showTextFile(pth, titl) :
	# import unicodedata
	try :
		with open(pth, 'r', encoding="utf-8", errors="surrogateescape") as f:
			text = f.read()	
	except OSError :
		text = "File not found\n" + pth
		pass
		
	# text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
	browseableMessage (message = text, title = titl, isHtml = False)
	

def inputBox (label, title, postFunction, startValue=""):
	import gui
	import wx
	d = wx.TextEntryDialog(
		gui.mainFrame,
		label,
		title,
		style = wx.OK | wx.CANCEL)
	d.Value = str(startValue)

	def callback(result):
		if result == wx.ID_OK:
			# On a validé sur OK, d.Value récupère le contenu de la saisie, on peut l'analyser ici.
			if postFunction :
				wx.CallAfter(postFunction, d.Value)
			else : 
				copyToClip(d.Value)
				message(_("Copied"))
				sleep(0.4)
		else :
			if postFunction : wx.CallAfter(postFunction, "ibCancel")
	gui.runScriptModalDialog(d, callback)
	#CallAfter(KeyboardInputGesture.fromName ("control+a").send) 

import inspect
def getStack(msg, min=1) :
	t = msg 
	stk =  inspect.stack()
	max = len(stk)
	if min < 0 : min = max + min
	for i in range(min, max) :
		t = t + " fonction  : {0}, {1}, {2}, {3}".format(stk[i][0], stk[i][1], stk[i][2], stk[i][3])
	return t

def openListAttachment2 (fo, repeat ):
	oPP = getPropertyPageFromFG() # return pp if main window else frame if separate message window
	if not oPP : return
	#cherche les objets d'ID attachmentCount 
	# 8 sur 12, name : 1 pièce jointe :, role.LABEL=73, IA2ID : attachmentCount    Chemin : role FRAME=34| i46, role-GROUPING=56, , IA2ID : tabpanelcontainer | i0, role-PROPERTYPAGE=57, , IA2ID : mailContent | i8, role-LABEL=73, , IA2ID : attachmentCount , IA2Attr : explicit-name : true, id : attachmentCount, tag : label, display : inline-block, , Actions : click,  ;
	o = findChildByIDRev(oPP, "attachmentCount")	
	if not o :
		message (_("No Attachement."))
		return False
	# il y a 1 ou plusieurs  PJ
	message(o.name)
	if repeat == 0 : return True
	# on doit activer le bouton toggle attachments si pas enfoncé
	o=o.previous.previous # bouton 
	if (controlTypes.State.PRESSED if hasattr(controlTypes, "State") else controlTypes.STATE_PRESSED) not in o.states:
		#message(u"bouton non enfoncé, on l'active")
		o.doAction() # place aussi le focus dans la liste
		return True
	else :
		while o and not o.role==14:  #list
			o=o.next
		o=o.firstChild 
		if (controlTypes.State.SELECTED if hasattr(controlTypes, "State") else controlTypes.STATE_SELECTED) not in o.states:
			o.doAction()
		o.setFocus()	
		message (o.name)
		return True
	# else :
		# message(u"Le bouton toggle attachment est enfoncé, on le relâche")
		# o.doAction()

	# bouton déjà enfoncé, on doit trouver la liste des PJ
	o = oPP # property page ou frame
	x = (e for e in range (o.childCount, o.childCount-10,-1)) # -5,-1
	pj=False
	for e in x:
		if getIA2Attribute (o.getChild (e), "attachmentList") : # "attachmentSize"): 
			#message (u"attachment_ trouvé")
			o =  o.getChild(e)
			pj=True
			break

	# if o.childCount == 1 :
		# message(u"Une pièce jointe.")
	# else  :
		# message( str(o.childCount) + u" pièces jointes.")
	o.setFocus()
	return True

def getLang() :
	from languageHandler import getLanguage
	l = getLanguage() 
	if "pt" in l : return l # pt_PT
	return l.split("_")[0]


def showHelp() :
	# 2022-12-09 localized
	lang = getLang()
	# message("langue : " + str(lang)) 
	curAddon=addonHandler.getCodeAddon()
	if "pt_BR" in lang :
		lang = "pt_PT"
	helpPath=os.path.join(curAddon.path,"doc", lang, "readme.html")
	if  os.path.exists(helpPath) :
		helpPath = "file:///" + helpPath.replace("\\", "/") # does not work > + "#navpanels"
	else :
		helpPath  = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/thunderbirdPlusG5_en.html?_x_tr_sl=en&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		helpPath = helpPath.replace("@lg", lang)
	# message(_("Ouverture de  l'aide dans votre navigateur"))
	try :  os.startfile (helpPath)
	except : message(_("File not found") + helpPath)
	
def toSupport(tbVersion) :
	a = "ma" + "il" + "to:"
	a += "plr.listes"
	a += "@"
	a += "rptools.org"
	a +=  "?subject=Support%20" + addonVersion() + "%20Thunderbird%20" + tbVersion
	os.startfile (a)
import winUser
def getWinTitle() :
	hwFG = winUser.getForegroundWindow()
	title = winUser.getWindowText(hwFG)
	return title

def cleanedWinTitle(appMod) :
	s = getWinTitle()
	s = s.replace("Mozilla Thunderbird", "TB")
	# listgroup name repeats
	grp = strBetween(s, "[", "]")
	if grp == "" : return s
	# api.copyToClip("groupe " + grp)
	s= grp + ", " + appMod.regExp_nameListGroup.sub (" ",s)
	# beep(700, 50)
	# api.copyToClip(s)
	return s

