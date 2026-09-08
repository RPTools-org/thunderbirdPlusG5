#-*- coding:utf-8 -*

import addonHandler
addonHandler.initTranslation()
import controlTypes, api
from speech import  speakMessage, speakText, speakSpelling, cancelSpeech, setSpeechMode, SpeechMode

import braille
import config
from config.configFlags import (
	ShowMessages,
	BrailleMode,
	OutputMode,
)
from time import time, sleep
from tones import beep
import wx
from wx  import  CallLater, CallAfter

import commonVars
import sharedVars
import utis
# from utis import utis.findParentByID # , utis.inputBox, utis.wordsMatchWord, utis.getSpeechMode
import keyboardHandler
from keyboardHandler import KeyboardInputGesture
import re


gRegFTI = re.compile("all-|unread-|smart-|favorite-|recent-|tags-")
gRegTags = re.compile(r'<.*?>')
# gRegConvertLF = re.compile(r'(?<!\r)\n')
prevSpeechMode = ""

def getBrailleParam(param="mode"):
	return config.conf["braille"][param] 
	
def setBrailleMode(value="speechOutput"):
	# the two possible values are: followCursors (default) and  speechOutput
	prevValue = config.conf["braille"]["mode"] 
	if not value or  value == prevValue:
		return prevValue
	config.conf["braille"]["mode"]  = value
	return prevValue

def brailleClear():
		if braille.handler:
			braille.handler._clearAll()
# def brailleShowTex
# t(text_to_display: str):
	# """
	# Affiche le texte spécifié sur l'afficheur Braille.
	# """
	# # 1. Créer un objet BrailleText à partir de la chaîne de caractères
	# braille_text = braille.BrailleText(
		# text=text_to_display,
		# # Vous pouvez spécifier des attributs de texte si nécessaire (ex: sélection)
	# )

	# # 2. Créer un cadre (frame) contenant le texte.
	# # Un cadre permet à NVDA de gérer le panning (défilement) si le texte est trop long.
	# braille_frame = braille.BrailleTextFrame(
		# [braille_text],
		# # Les paramètres suivants définissent ce que NVDA doit annoncer en plus:
		# cursor=None,        # Ne pas afficher de curseur spécifique
		# requestedCursorShape=braille.CURSORSHAPE_BLOCK, # Forme du curseur (non pertinent ici)
		# controlType=controlTypes.CONTROLTYPE_STATUSBAR, # Type de contrôle (aide à la gestion du braille)
	# )

	# # 3. Afficher le cadre sur l'afficheur Braille.
	# # C'est cette méthode qui envoie le contenu à l'afficheur.
	# braille.display(braille_frame)
	
	# # OPTIONNEL: Annoncer le texte vocalement pour les utilisateurs n'utilisant pas le braille

def brailleMessagePersistent(msg, scrollMsg=""):
	# function by André from AccessSolutions France
	# for testing api.copyToClip(scrollMsg+msg)
	region = braille.TextRegion(scrollMsg + msg)
	region.obj = None
	region.update()
	braille.handler.mainBuffer.clear()
	braille.handler.mainBuffer.regions.append(region)
	braille.handler.mainBuffer.update()
	braille.handler.update()

def messageBraille(text):
	# works  even if message in Braille is disabled in Braille options in NVDA
	if text is None:
		return
	if braille.handler.buffer is braille.handler.messageBuffer:
		braille.handler.buffer.clear()
	else:
		braille.handler.buffer = braille.handler.messageBuffer
	region = braille.TextRegion(text)
	region.update()
	braille.handler.buffer.regions.append(region)
	braille.handler.buffer.update()
	braille.handler.update()
	braille.handler._resetMessageTimer()
	braille.handler._keyCountForLastMessage = keyboardHandler.keyCounter



def message(text, speech=True, brailleScrollShort=False):
	"""say a short message and Display a scrollable  message to the user 
	"""
	if text is None:
		return
	if speech:
		speakMessage(text)
	if sharedVars.brailleScrollShort:
		brailleMessagePersistent(text)
	else:
		messageBraille(text)

def sayLongText(text, speech=True):
	"""say a long text and Display a persistant message to the user 
	"""
	if text is None:
		return
		
	text = text.replace(chr(30), "").replace(chr(31), "").replace("\r", "").strip()
	
	if speech:
		speakText(text.strip()) # strip is very important for sapi5 neural voices
	if sharedVars.brailleScrollLong:
		# replace \n by ¶
		text = text.replace("\n", "¶  ")
		# api.copyToClip(text)
		# beep(440, 30)

		brailleMessagePersistent(text, _("[Scrollable]") + " ")
	else:
		messageBraille(text)


# def braillePersistent_old(text): 
	# # function derived from braille.py
	# brHandler =   braille.handler
	# if brHandler.buffer is brHandler.messageBuffer:
		# brHandler.buffer.clear()
	# else:
		# brHandler.buffer = brHandler.messageBuffer
	# region = braille.TextRegion(text)
	# region.update()
	# brHandler.buffer.regions.append(region)
	# brHandler.buffer.update()
	# brHandler.update()

# def brailleMessage(text, speak=False): 
	# if speak: 
		# speakMessage("Braille: ")
	# braille.handler.message(text)


# def clearBrailleDisplay():
	# # Crée une source Braille vide.
	# # The braille.BrailleCellText constructor accepts an empty string.
	# # error: BrailleCellText is not an attribute of Braille.
	# empty_source = braille.BrailleCellText("", name="Empty Source")

	# # Asks the Braille manager to update the display
	# # with the empty source
	# braille.handler.update(empty_source)
	
def messageLater(msg):
	# function called with a wx.CallLater
	cancelSpeech()
	message(msg)
	
def hasID(obj, IA2ID, partialID=True):
	# IA2ID can be the n first chars of the ID
	r= hasattr (obj,"IA2Attributes") and "id" in obj.IA2Attributes.keys()
	if not r:return False
	r =str(obj.IA2Attributes["id"])
	if partialID:
		return True if r.startswith(IA2ID) else False 
	else :
		return True if r == IA2ID else False


def hasIA2Class(obj, IA2Class):
	r= hasattr (obj,"IA2Attributes") and "class" in obj.IA2Attributes.keys()
	if not r:return False
	r =str(obj.IA2Attributes["class"])
	return True if r.startswith(IA2Class) else False 

def getIA2Attr(obj,attribute_value=False,attribute_name ="id"):
	r= hasattr (obj,"IA2Attributes") and attribute_name in obj.IA2Attributes.keys ()
	if not r:return False
	r =obj.IA2Attributes[attribute_name]
	return r if not attribute_value  else r ==attribute_value

def getAllIA2Attrs(obj) :
	if not  hasattr (obj,"IA2Attributes") : return ""
	tAttrs = ""
	for attrKey, attrValue in obj.IA2Attributes.items():
		if "id" not in attrKey and "explicit" not in attrKey and "draggable" not in attrKey and "margin" not in attrKey and "text-" not in attrKey :
			tAttrs = tAttrs + str(attrKey) + " : " + str(attrValue) + ", " 
	if tAttrs : 
		return "\n   AllIA2Attrs : " + tAttrs
	return ""

def setCurFrameTabFromFO(obj):
	sharedVars.curFrame = "" ; sharedVars.curTab = ""
	fg = api.getForegroundObject()
	# messengerWindow:
	o = getChildByRoleIDName(fg, controlTypes.Role.GROUPING, ID="tabpanelcontainer", name="", idx=34)
	if o is not None:
		sharedVars.curFrame = "messengerWindow"
	if not sharedVars.curFrame:
		# separate reading window
		o = getChildByRoleIDName(fg, controlTypes.Role.INTERNALFRAME, ID="messageBrowser", name="", idx=4)
		if o is not None: 			
			sharedVars.curFrame = "messengerWindow" ; sharedVars.curTab = "message" 
			return
	if not sharedVars.curFrame:
		# msgCompose window
		o = getChildByRoleIDName(fg, controlTypes.Role.POPUPMENU, ID="msgComposeContext", name="", idx=0)
		if o is not None: 
			sharedVars.curFrame = "msgcomposeWindow" ; sharedVars.curTab = "comp"
			return
	if not sharedVars.curFrame:
		sharedVars.curFrame = "not found" ; sharedVars.curTab = "Not Found"
		return


	# try: # except
	role = obj.role
	ID = str(getIA2Attr(obj))
	if role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM):
		if ID.startswith("threadTree"):
			sharedVars.curTab = "main" 
			return
		if controlTypes.Role.TREEVIEWITEM and  isFolderTreeItem(obj, ID):
			sharedVars.curTab = "main" 
			return
	if role == controlTypes.Role.DOCUMENT  and controlTypes.State.READONLY in obj.states:
		o = obj.parent
		while o is not None:
			ID = str(getIA2Attr(o))
			if o.role ==  controlTypes.Role.GROUPING and ID.startswith("paneLayout"):
				sharedVars.curTab = "main" 
			o = o.parent
		if sharedVars.curTab: return			
	#  search document 
	oDoc = None
	o = obj.parent
	while o is not None:
		role = o.role
		if role == controlTypes.Role.DOCUMENT:
			oDoc = o
			break
		elif  role == controlTypes.Role.GROUPING or not hasattr(o, "parent"):
			break
		o = o.parent
	if not oDoc: sharedVars.curTab = "main"
	else: sharedVars.curTab = str(getIA2Attr(oDoc.parent))

def getTVItemLevel(obj):
	if obj.role != controlTypes.Role.TREEVIEWITEM: return 0
	return obj.positionInfo['level']
	
def isFolderTreeItem(fti, ID=""):
	if fti.role != controlTypes.Role.TREEVIEWITEM: return False 
	if not ID:
		ID = str(getIA2Attr(fti))
	if gRegFTI.findall(ID): return True
	return False

def currentTree(o, role):
	if role not in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM, controlTypes.Role.TABLE, controlTypes.Role.TREEVIEW, controlTypes.Role.LIST): 
		return ""
	o = o.parent
	while o is not None:
		r = o.role
		if r ==  controlTypes.Role.TEXTFRAME:
			if hasID(o, "threadTree"):
				return "t"
		if r == controlTypes.Role.TREEVIEW:
			if hasID(o, "folderTree"):
				return "f"
		o = o.parent
	return""
			
def isQuickfilterBar(o):
	try: o = o.parent
	except: return False
	# Role.SECTION, ID: quickFilterBarContainer, 
	if o.role == controlTypes.Role.SECTION:
		if str(getIA2Attr(o)) == "quickFilterBarContainer": return True
	return False

def checkObj(o, context="", oPrevious=None):
	if o is not None: 
		if sharedVars.debug: sharedVars.log(o, "Passed "+ context)
		return True
	# message("Internal Error: object  is None: " + context) 
	if sharedVars.debug: sharedVars.log(o, "Not passed: " + context) 
	# if oPrevious:
		# sharedVars.log(oPrevious, "Previous: ") 
	return  False

def findChildByRole(obj, role): 
	if obj is None: return None
	try: # Finally
		obj = obj.firstChild
		while obj is not None:
			if obj.role == role:
				return obj
			obj = obj.next
		return None
	finally:
		if sharedVars.debug: sharedVars.log(obj, "findChildByRole expected " + str(role.displayString))

def findChildByRoleID(obj,role, ID, startIdx=0): # attention: controlTypes roles
	if obj  is None: return None
	# ID can be the n first chars of the searched 
	try:  # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		try:
			if startIdx > 0: o = obj.getChild(startIdx)
			else: o = obj.firstChild
		except:
			o = obj.firstChild
			pass
		while o is not None:
			if o.role == role:
				if hasID(o, ID):
					if ID == "tabpanelcontainer": sharedVars.groupingIdx = startIdx 
					# sharedVars.log(o, "toolbar found ")
					return o
			o = o.next
			startIdx += 1
			
			
		return None
	finally:
		sharedVars.objLooping = prevLooping

def findParentByRole(o, role):
	if o.role == role: return o 
	try:  # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		while o is not None:
			# sharedVars.log(o, "findParentByRole parent ")
			if o.role == role:
					return o
			o = o.parent
		return None
	finally:
		sharedVars.objLooping = prevLooping

class FindDescendantTimer():
	timer = None
	startTime = 0 
	foundObj = None
	logT = ""

	def __init__(self, role, ID="", name="", interval=20, maxElapsed=500):
		self.role = role
		self.ID = ID
		self.name = name
		self.interval = interval
		self.maxElapsed = maxElapsed
		self.doAction = False
		
	def log(self, obj, lbl):
		if obj is None: return beep(80, 3)
		if obj.role != self.role: return beep(250, 3)
		# r = "No role" if not hasattr(obj, "role") else obj.role
		# nm = "No name" if not hasattr(obj, "name") else obj.name
		# self.logT += "{}: role={}, ID={}, name={}".format(str(lbl), r, str(getIA2Attr(obj)), nm) + "\n"
		if sharedVars.debug: sharedVars.log(obj, lbl)
		beep(600, 10)
		
	def run(self,obj, doAction=False):
		if doAction: self.doAction = True
		self.startTime = time()
		self.timer = CallLater(self.interval, self.getSearchedObject, obj) 

	def getSearchedObject(self, o): 
		if self.foundObj: 
			self.log(self.foundObj, "foundObj at beginning of getSearchedObj ")
			if self.doAction: self.foundObj.doAction()
			return
		self.log(o, "getSearchedObj begin")
		if time() - self.startTime >= self.maxElapsed: 
			self.timer.Stop()
			return

		try:
			o  = o.firstChild
			self.log(o, "startObj.firstChild found")
			if o is None:return
		except:
			self.log(o, "Exception sur")
			return
		while o is not None:
			if o.role == self.role:
				self.log(o, "Button Child")
				if self.name:
					if o.name.find(self.name) > -1: self.foundObj = o
				if not self.foundObj and self.ID:
					if hasID(o, self.ID): self.foundObj = o
			if self.foundObj:
				self.timer.Stop()
				self.log(self.foundObj, "foundObj")
				if self.doAction: self.foundObj.doAction()
				break
			if time() - self.startTime >= self.maxElapsed: 
				self.timer.Stop()
				returbreak
			if o.childCount:
				self.timer = CallLater(self.interval, self.getSearchedObject, o)
			o = o.next

def getMainGrouping(oFrame=None, force=False):
	if not force and commonVars.cv.grouping is not None:
		return commonVars.cv.grouping
	# search grouping
	if not oFrame:
		oFrame = api.getForegroundObject()
	o = findChildByRoleID(oFrame, controlTypes.Role.GROUPING, "tabpanelcontainer", 34)
	if o is not None:
		commonVars.cv.grouping = o
	return o

def getPropertyPage(oFrame=None, debug=False, searchID="mail3PaneTab" ):
	try: # finally
		if debug: sharedVars.logte("Entering getPropertyPage")
		if searchID == "mail3PaneTab" and commonVars.cv.propertyPage is not None:
			# the following line is necessary because the finally cmause
			o = commonVars.cv.propertyPage
			if debug: sharedVars.log(commonVars.cv.propertyPage, "getPropertyPage, commonVars.cv.propertyPage")
			return o
		if oFrame: o = oFrame
		else:o = api.getForegroundObject()
		# firstGrouping 
		o = getMainGrouping(oFrame)
		if o is None: 
			sharedVars.error(o, "getPropertyPage, firstGrouping is None")
			return None
		o = o.firstChild
		while o is not None:
			if o.role == controlTypes.Role.PROPERTYPAGE: # and  controlTypes.State.OFFSCREEN  not in o.states:
				# ID =  str(getIA2Attr(o))
				if hasID(o, searchID): # partial ID
					# checkObj(o, "getPropPage , befor return o")
					if searchID == "mail3PaneTab":
						commonVars.cv.propertyPage = o
					if debug: sharedVars.log(o, "getPropertyPage, o=")
					return o
			o = o.next
		checkObj(o, "getPropPage before return None")
		return None
	finally:
		if debug: sharedVars.log(o, "getPropertyPage result")

def getActivePropertyPage(oFrame=None, ppExcluded=None, debug=False ):
	try: # finally
		if debug: sharedVars.logte("getActivePropertyPage")
		if oFrame: o = oFrame
		else:o = api.getForegroundObject()
		# firstGrouping 
		o = getMainGrouping(oFrame)
		if o is None: 
			sharedVars.error(o, "getActivePropertyPage, firstGrouping is None")
			return None
		o = o.firstChild
		while o is not None:
			if o.role == controlTypes.Role.PROPERTYPAGE: 
				# if debug: sharedVars.log(o, "getActivePropertyPage, o=")
				if ppExcluded and o == ppExcluded:
					o = o.next
					continue
				if controlTypes.State.OFFSCREEN  not in o.states:
					return o
			o = o.next
		checkObj(o, "getActivePropPage before return None")
		return None
	finally:
		if debug: sharedVars.log(o, "getActivePropertyPage result")

def setFontextFromFirstID(oParent):
	for o in oParent.recursiveDescendants:
		ID = getIA2Attr(oParent)
		if ID:
				sharedVars.curFrame = sharedVars.curTab = str(ID)
				break

def getThreadPaneFromFG():
	if commonVars.cv.threadPane is not None:
		return commonVars.cv.threadPane
	oFrame = api.getForegroundObject()
	if oFrame: o = getChildByRoleIDName(oFrame, controlTypes.Role.GROUPING, ID="tabpanelcontainer", name="", idx=35)
	# IA2ID = mail3PaneTab1 in , Role.PROPERTYPAGE
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.PROPERTYPAGE, ID="mail3PaneTab1", name="", idx=2)
	# IA2ID = mail3PaneTabBrowser1 in , Role.INTERNALFRAME
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.INTERNALFRAME, ID="mail3PaneTabBrowser1", name="", idx=0)
	# IA2ID = paneLayout in , Role.GROUPING
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="paneLayout", name="", idx=0)
	# IA2ID = threadPane in , Role.SECTION
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.SECTION, ID="threadPane", name="", idx=2)
	if o is not None: commonVars.cv.threadPane = o
	return o

def hasRole(obj, role):
	if obj and obj.role == role:
		return True
	return False

def getThreadTreeFromFG(focus=False, nextGesture="", getThreadPane=False, oPP=None, debug=False):
	global prevSpeechMode
	if debug: 
		import tbLogger
		commonVars.cv.logger.addobj(oPP, "Entering getThreadTreeFromFG, propertyPage")
	if getThreadPane and hasRole(commonVars.cv.threadPane, controlTypes.Role.SECTION): 
		return commonVars.cv.threadPane
	if not getThreadPane and hasRole(commonVars.cv.threadTree, controlTypes.Role.TEXTFRAME):
		# 2025-05-22: focus and  nextGesture   are never used
		if focus: commonVars.cv.threadTree.setFocus()
		if debug: commonVars.cv.logger.addobj(commonVars.cv.threadTree, "getThreadTreeFromFG, commonVars.cv.threadTree was initialized before ")
		return commonVars.cv.threadTree
	# search ThreadTree
	# Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 
	if oPP: 
		o = oPP
	else:
		o = getPropertyPage()
	if not checkObj(o, "property page"): 
		if debug: commonVars.cv.logger.add("getThreadTreeFromFG, Property page not found, return none")
		return None
	# | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  
	try: o = o.firstChild.firstChild
	except:
		checkObj(o, "second grouping")
		if debug: commonVars.cv.logger.add("getThreadTreeFromFG, exception second grouping  not found, return none")
		return None
	
	# ancien  | i2or i4 , Role-SECTION, , IA2ID: threadPane 
	# 2024 06: role.SECTION, IA2ID: threadPane Tag: div, States: , childCount: 4 Path: r-FRAME, | i31, r-GROUPING, , IA2ID: tabpanelcontainer | i2, r-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, r-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, r-GROUPING,  | i2, r-SECTION, , IA2ID: threadPane
	prevO = o
	o = findChildByRoleID(o, controlTypes.Role.SECTION, "threadPane")
	if not checkObj(o, "section threadPane", prevO): 
		if debug: commonVars.cv.logger.add("getThreadTreeFromFG, section threadPane  not found, return none")
		return None
	if getThreadPane and o: 
		commonVars.cv.threadPane = o
		return o
	# | i2, Role-TEXTFRAME, , IA2ID: threadTree , 
	o = findChildByRoleID(o, controlTypes.Role.TEXTFRAME, "threadTree")
	if not checkObj(o, "threadTree"):
		if debug: commonVars.cv.logger.add("getThreadTreeFromFG, threadTree not found, return none")
		return None
	commonVars.cv.threadTree = o
	if debug: commonVars.cv.logger.addobj(o, "getThreadTreeFromFG, threadTree found, returnobj")
	return o
	# | i0, Role-TABLE,  | i2, Role-TREEVIEW
	o = o.firstChild.firstChild
	if not checkObj(o, "role treeview"): return None
	while o is not None:
		# if not checkObj(o): return None
		if o.role in (controlTypes.Role.LIST, controlTypes.Role.TREEVIEW):
			break
		o = o.next
	if o and focus: o.setFocus()
	if nextGesture:
		prevSpeechMode = utis.getSpeechMode()
		setSpeechMode(SpeechMode.off)
		CallLater(50, silentSendKey, nextGesture)
	commonVars.cv.threadTree = o
	return  o
	
def getThreadTreeListOrTable(oThreadTree): 
	if not oThreadTree:
		return None
	oFirstTable = getChildByRoleIDName(oThreadTree, controlTypes.Role.TABLE, ID="", name="", idx=0)
	if not oFirstTable:
		return None
	o = getChildByRoleIDName(oFirstTable, controlTypes.Role.TABLE, ID="", name="", idx=0)
	if o is not None: return o # tree view 
	# list view
	o = getChildByRoleIDName(oFirstTable, controlTypes.Role.LIST, ID="", name="", idx=0)
	if o is not None: return o
	return None


def getFolderTreeFromPP(oPP, debug=False):
	if debug: 
		import tbLogger
		commonVars.cv.logger.add("entering getFolderTreeFromPP.")
	commonVars.cv.folderTree = None
	if not oPP:
		if debug: commonVars.cv.logger.add("getFolderTreeFromPP, propertyPage is none in getFolderTreeFromPP")
		return None
	o = oPP
	# search for section, ID: folderPane 
	fp = None
	for g in range(0, 3):
		o = o.firstChild
		if o is None: return None
		if debug: commonVars.cv.logger.addobj(o, "descendant gen=" + str(g))
		if o.role == controlTypes.Role.SECTION  and hasID(o, "folderPane", partialID=False): # added on 2026-08-22
			fp = o
			break
	# end for
	if debug: commonVars.cv.logger.addobj(fp, "folderPane ? fp=")
	if fp is None : return None
	# search for TREEVIEW id=threadTree
	for c in fp.recursiveDescendants:
		if c and c.role == controlTypes.Role.TREEVIEW:
			if debug: commonVars.cv.logger.addobj(c, "c=")
			commonVars.cv.folderTree = c
			return c
	if debug: commonVars.cv.logger.add("getFolderTreeFromPP, folderTree not found.")
	return None


def getFolderTreeFromFG(focus=False, oPP=None):
	if commonVars.cv.folderTree is not None:
		if focus: commonVars.cv.folderTree.setFocus()
		return commonVars.cv.folderTree
	# utis.beepRepeat(440, 10, 3) 
	if oPP: o = oPP
	else: o = getPropertyPage()
	if not checkObj(o, "getFT property page"): return None
	# with toolbar Path: Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1| i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i0, Role-SECTION, , IA2ID: folderPane | i1, Role-TREEVIEW, , IA2ID: folderTree 
	# without toolbar Path: Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 
	# wo: | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1  === | i0, Role-GROUPING,  | i0, Role-SECTION, , IA2ID: folderPane __ | i0, Role-TREEVIEW, , IA2ID: folderTree | i0, Role-TREEVIEWITEM,  ,
	# with: | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1  === | i0, Role-GROUPING,::: | i0, Role-SECTION, , IA2ID: folderPane __ | i1, Role-TREEVIEW, , IA2ID: folderTree
	for i in range(0, 3): # 0 to 2 = 3 passes   
		o = o.firstChild
		if o is None:
			# sharedVars.logte("firstChild None, pass=" + str(i))
			break
		# sharedVars.log(o, "firstChild pass=" + str(i)) 
	# end for
	if o is None:
		return None
	checkObj(o, "getFT folderPane"	)
	o =   findChildByRoleID(o, controlTypes.Role.TREEVIEW, "folderTree") 
	if not checkObj(o, "getFT folderTree"): return None
	if o and focus: o.setFocus()
	commonVars.cv.folderTree = o
	return o
def isSmartFolderTree():
	o = getFolderTreeFromFG()
	o = o.firstChild.firstChild.firstChild
	# sharedVars.log(o, "First treeview item ? ")
	if hasID(o, "smart-"):
		return True
	return False
 

class RecurseTree():
	def	 __init__(self, role, IDObj=""):
		self.role = role
		self.ID = IDObj
		self.outObj = None
	def run(self,obj): 
		if obj is None: return
		obj = obj.firstChild
		if obj is None: return 
		while obj is not None:
			if obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM): 
				# 		if not self.ID or   hasID(obj, self.ID):
				self.outObj = obj 
				return
			if obj.firstChild:
				self.run(obj)
			obj = obj.next
		return

# focus ThreadTree from FolderTree
def focusTTFromFT(oFocused, mode):
	try: # finally
		utis.disableOvl(True)
		# utis.beepRepeat(440, 20, 2)
		utis.setSpeechMode_off()
		# sharedVars.speechOff = True # speech restored in see event_gainFocus
		# if	 mode > 2: # first unread message 
			# KeyboardInputGesture.fromName("n").send()
			# return True

		# the closest common ancestor of folderTree and ThreadTree is: the rol internal frame  object
		oFocused = oFocused.parent
		o = None
		while oFocused:
			if oFocused.role == controlTypes.Role.INTERNALFRAME:
				if hasID(oFocused, "mail3PaneTabBrowser"):
					o = oFocused
					break
			oFocused =  oFocused.parent
		if o is None: return False
		
		o = o.firstChild # grouping
		# | i2, SECTION, , IA2ID: threadPane | i2, TEXTFRAME, , IA2ID: threadTree , 
		o = findChildByRoleID(o, controlTypes.Role.SECTION, "threadPane")
		o = findChildByRoleID(o, controlTypes.Role.TEXTFRAME, "threadTree")
		o = o.firstChild.firstChild # first level table 
		while o is not None:
			if o.role in (controlTypes.Role.TABLE, controlTypes.Role.LIST):
				break
			o = o.next
		if o is None:
			return False
		o.setFocus()
		# utis.speech.setSpeechMode(SpeechMode.talk)
		setSpeechMode(SpeechMode.talk)
		if mode == 1: # last message
			KeyboardInputGesture.fromName("end").send()
		elif  mode == 2: # first message
			KeyboardInputGesture.fromName("home").send()
		elif	 mode > 2: # first unread message 
			KeyboardInputGesture.fromName("n").send()
		return True
	finally:
		utis.disableOvl(False)
		# utis.speech.setSpeechMode(SpeechMode.talk)
		setSpeechMode(SpeechMode.talk)

def focusThreadTree(focus=False, fromFolderTree=False):
	# disabled because speech is not always restored in event_gainFocus -> utis.setSpeechMode_off()
	focusMode = sharedVars.oSettings.getOption("messengerWindow", "focusMode", kind="i")
	if focusMode == 0: focusMode = 1
	fo = api.getFocusObject() 
	role = fo.role
	if hasID(fo, "threadTree-"):
		if focusMode == 1: k = "end"
		elif focusMode == 2: k = "home"
		elif focusMode == 3: k = "n"
		# sharedVars.speechOff = True # talk reactivated in event_gainFocus
		return CallAfter(KeyboardInputGesture.fromName(k).send)
	elif role == controlTypes.Role.TREEVIEWITEM: # we are in folder tree
		return CallAfter(focusTTFromFT, fo, focusMode)
	elif role != controlTypes.Role.FRAME:
		fo = api.getForegroundObject()
		fo.setFocus()
		fo = getFolderTreeFromFG(focus=False)
		if not fo:
			# CallAfter(utis.speech.setSpeechMode, SpeechMode.talk)
			CallAfter(setSpeechMode, SpeechMode.talk)
			return
		fo.setFocus()
		oTimer = GetFocusObjTimer(roleList=[controlTypes.Role.TREEVIEWITEM], stateSelected=True, interval=500, maxElapsed=4000, callBack=focusTTFromFT, cbParam=focusMode)
		oTimer.run()

class GetFocusObjTimer():
	timer = None
	callCount = 0
	def __init__(self, roleList, stateSelected,  interval, maxElapsed, callBack, cbParam):
		self.roles = roleList
		self.stateSelected = stateSelected
		self.interval = interval
		self.maxElapsed = maxElapsed
		self.callBack = callBack
		self.cbParam = cbParam
		
	def run(self):
			self.timer = CallLater(self.interval, self.getFocused) 

	def getFocused(self): 
		self.callCount += 1
		if self.callCount * self.interval >= self.maxElapsed: 
			self.timer.Stop()
			self.timer = None
			return
		api.processPendingEvents()
		fo = api.getFocusObject()
		if fo.role in self.roles:
			if self.stateSelected: selected  = True if controlTypes.State.SELECTED in fo.states else False
			else: selected = True
			if selected:
				self.timer.Stop()
				self.timer = None
				if self.callBack: 
					CallAfter(self.callBack, fo, self.cbParam)
				return
		else:
			self.timer.Start() 

	

# def sayQFBInfos(o=None):
	# try: # finally
		# prevLooping = sharedVars.objLooping
		# sharedVars.objLooping = True
		# if hasID(o, "threadTree"): # threadTree item
			# # Path: | i2, Role-SECTION, , IA2ID: threadPane | i3, Role-TEXTFRAME, , IA2ID: threadTree | i0, Role-TABLE,  | i2, Role-TREEVIEW,  | i0, Role-TREEVIEWITEM, , IA2ID: threadTree-row0 
			# o = utis.findParentByID(o, controlTypes.Role.TEXTFRAME, "threadTree")
			# while o is not None:
				# if hasID(o, "quick-filter-bar"): break
				# if o.previous: o = o.previous
				# else: break	
			# if o is None: return
			# oContainer = o.firstChild # quickFilterBarContainer  
		# elif  hasID(o.parent, "quickFilterBarContainer"):
			# oContainer = o.parent
		# #  sharedVars.log(oContainer, "sayQFBInfos begin")
		# # 1. retrieve number of messages
		# o = oContainer.lastChild.firstChild # qfbResultLabel firstChild
		# # sharedVars.log(o, "oContainer.lastChild")
		# t =""
		# while o is not None:
			# if o.name: t += str(o.name) + ", "
			# o = o.next
		# if not t: t = _("No message informations")

		# # 2. retrieve filter infos
		# word = options = ""
		# # keyword edit 
		# o = oContainer.getChild(1)
		# if o.role == controlTypes.Role.EDITABLETEXT and o.value:
			# word = str(o.value)
		# o = o.next
		# while o is not None:
			# if o.role ==  controlTypes.Role.TOGGLEBUTTON and controlTypes.State.PRESSED in o.states: options += o.name + ", "
			# # sharedVars.log(o, "child")
			# o = o.next
		# # sharedVars.logte(infos)	
		# if word or options: t += _("Expression input: %s") %word
		# message(t)
		# if word: speakSpelling(word)
		# if options: message(options)
	# finally:
		# sharedVars.objLooping = prevLooping

def getMessageStatus115(infoIdx=-1):
	try: # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# level 8,         1 of 1, Role.SECTION, IA2ID: threadPaneFolderCountContainer, left:272 Tag: div, States: , childCount: 4 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer 
		# level 9,          0 of 3, name: 13 messages, Role.STATICTEXT, left:281, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i0, Role-STATICTEXT,  
		# level 9,          1 of 3, Role.STATICTEXT, left:347, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i1, Role-STATICTEXT,  
		# level 9,          2 of 3, name: 11 messages sélectionnés, Role.STATICTEXT, left:359, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i2, Role-STATICTEXT,  
		# level 9,          3 of 3, Role.STATICTEXT, left:493, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i3, Role-STATICTEXT,  
		# get threadPane
		threadPane = commonVars.cv.threadPane
		# get | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  
		o = threadPane.firstChild.firstChild
		# get | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer 
		# the following line is OK in TB 128.
		o = findChildByRoleID(o, controlTypes.Role.SECTION, "threadPaneFolderCountContainer")
		# sharedVars.log(o, "threadPaneFolderCountContainer") 
		if o is None: return ""

		if infoIdx > -1 and infoIdx < 4: 
			try: return o.getChild(infoIdx).name
			except: return ""
		# all fields
		t = ""
		o = o.firstChild
		while o is not None:
			if o.name:
				t += o.name + ", "
			o = o.next
		if t: t = t[:-2]
		return t
	finally:
		sharedVars.objLooping = prevLooping

def getFilterInfos128(threadPane, infos=False):
	if not threadPane:
		threadPane = commonVars.cv.threadPane
		if not threadPane: beep(100, 30)
		else: beep(440, 30)
	# children of threadPane: | i1, 86, , IA2ID: quick-filter-bar | i0, 86, , IA2ID: quickFilterBarContainer | i7, 91, , IA2ID: qfb-results-label
	o = findChildByRoleID(threadPane, controlTypes.Role.SECTION, ID="quick-filter-bar",startIdx=0)
	if o is None: return "", ""
	o = oContainer  = findChildByRoleID(o, controlTypes.Role.SECTION, ID="quickFilterBarContainer",startIdx=0)
	if o is None: return "", ""
	o = findChildByRoleID(o, controlTypes.Role.TEXTFRAME, ID="qfb-results-label",startIdx=6)
	count = ""
	if o and o.firstChild:
		count = _("Filtered: ") + str(o.firstChild.name) + " / "
	if not infos:
		return count, ""
	# 2. retrieve filter expression
	word = options = ""
	# keyword edit: path = | i0, 86, , IA2ID: quickFilterBarContainer | i1, 91, , IA2ID: qfb-qs-textbox | i0, 39,  | i0, 8,  ,  
	o = oContainer.getChild(1).firstChild.firstChild # new in TB 128
	if o.role == controlTypes.Role.EDITABLETEXT and o.value:
		word = str(o.value)
	# toggle buttons
	o = oContainer.getChild(2) # unread toggle button
	while o is not None:
		if o.role ==  controlTypes.Role.TOGGLEBUTTON and controlTypes.State.PRESSED in o.states:
			options += o.name + ", "
		# # sharedVars.log(o, "child")
		o = o.next
	# # sharedVars.logte(infos)	
	filtExpr = ""
	if word or options: 
		filtExpr = ", " + _("Filter: ")
	if word:
		filtExpr += word + ", "
	if options:
		filtExpr += options
	return count, filtExpr
def getMessageStatus128(infoIdx=-1):
	# returns total messages, filter infos
	try: # finally
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# level 8,         1 of 1, Role.SECTION, IA2ID: threadPaneFolderCountContainer, left:272 Tag: div, States: , childCount: 4 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer 
		# level 9,          0 of 3, name: 13 messages, Role.STATICTEXT, left:281, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i0, Role-STATICTEXT,  
		# level 9,          1 of 3, Role.STATICTEXT, left:347, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i1, Role-STATICTEXT,  
		# level 9,          2 of 3, name: 11 messages sélectionnés, Role.STATICTEXT, left:359, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i2, Role-STATICTEXT,  
		# level 9,          3 of 3, Role.STATICTEXT, left:493, States:  Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i2, Role-SECTION, , IA2ID: threadPane | i0, Role-SECTION, , IA2ID: threadPaneHeaderBar | i0, Role-SECTION,  | i1, Role-SECTION, , IA2ID: threadPaneFolderCountContainer | i3, Role-STATICTEXT,  
		for i in range(0, 2):
			threadPane = getThreadPaneFromFG()	# get threadPane
			if threadPane: 
				o = getChildByRoleIDName(threadPane, controlTypes.Role.SECTION, ID="threadPaneHeaderBar", name="", idx=0)
			else: o = None
			if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.SECTION, ID="", name="", idx=0)
			# IA2ID = threadPaneFolderCountContainer in , Role.SECTION
			if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.SECTION, ID="threadPaneFolderCountContainer", name="", idx=1)
			# sharedVars.log(o, "threadPaneFolderCountContainer") 
			# if o is None:
				# commonVars.cv.threadPane = None # this reference must be searched again
			else:
				break
			# end for
		# 128 specific
		if infoIdx > -1 and infoIdx < 4: 
			try: return o.getChild(infoIdx).name
			except: return ""
		# all fields
		# filtered message count
		t, filterInfos = getFilterInfos128(threadPane, infos=True)
		try: o = o.firstChild
		except: 
			message(_("message list header is hiddend."))
			return ""
		while o is not None:
			# sharedVars.log(o, "Nombre ")
			if o.name:
				t += o.name + ", "
			o = o.next
		if t: t = t[:-2]
		return t + filterInfos 
	finally:
		sharedVars.objLooping = prevLooping

def getMessageStatus(infoIdx=-1):
	if utis.TBMajor() < 128:
		return getMessageStatus115(infoIdx)
	else:
		return getMessageStatus128(infoIdx)
		
def silentSendKey(key):
	KeyboardInputGesture.fromName (key).send()
	setSpeechMode(prevSpeechMode)
def getMessagePane(): # in the main window
	# level 8,         15 of 15, Role.INTERNALFRAME, IA2ID: messagepane Tag: browser, States: , FOCUSABLE, childCount: 1 Path: Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 
	o = getPropertyPage()
	# if sharedVars.debug: sharedVars.log(o, "getPreviewPane, Expected propertyPage")
	if o is None: return None
	# | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  
	o = findChildByRoleID(o, controlTypes.Role.INTERNALFRAME, "mail3PaneTabBrowser") 
	if not checkObj(o, "getPreviewPane, expected INTERNALFRAME mail3PaneTabBrowser1"): 
		return None 
	
	o = findChildByRole(o, controlTypes.Role.GROUPING) 
	if not checkObj(o, "getPreviewPane, expected Grouping"): return None 

	if utis.TBMajor() < 135:
		# | i4, Role-SECTION, , IA2ID: messagePane 
		o = findChildByRoleID(o, controlTypes.Role.SECTION, "messagePane") 
	else:
		# i4, Role-TEXTFRAME, , IA2ID: messagePane 
		o = findChildByRoleID(o, controlTypes.Role.TEXTFRAME, "messagePane") 
	if sharedVars.debug:  sharedVars.log(o, "getMessagePane, expected messagePane")
	return o

def getMessageHeaders(msgPane=None):
	if msgPane: 
		o = msgPane
	else:
		o = getMessagePane()
	if o is None: return None
	# | i0, Role-INTERNALFRAME, IA2ID: messageBrowser | i0, Role-GROUPING,  
	if o.childCount:
		o = o.firstChild
	else:
		print("getHeaders, Has no firstChild" + sharedVars.getObjAttrs(o))
		return None
	
	if o.childCount:
		o = o.firstChild
	else:
		print("getHeaders, Has no firstChild" + sharedVars.getObjAttrs(o))
		return None
	# | i13 of 22, Role-LANDMARK, IA2ID: messageHeader 
	o = findChildByRoleID(o, controlTypes.Role.LANDMARK, "messageHeader", 12)
	return o

def getPreviewDoc():
	o = getMessagePane()
	# checkObj(o, "get previwDoc, get messagePane")
	if o is None:
		message(_("The preview pane is not displayed. Press F8 and try again please"))
		return None, False
	# parent of document:| i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  
	#|  child i15, Role-INTERNALFRAME, , IA2ID: messagepane 	
	# 2023-09-12:try except added
	try: o = o.firstChild.firstChild
	except: return None, False 
	if o is None: return None, True # retry needed 
	o = findChildByRoleID(o, controlTypes.Role.INTERNALFRAME, "messagepane", 14)  
	if o is None: return None, True # retry needed 
	# checkObj(o, "getPreviewDoc, expected internal frame, messagepane")
	# level 9,          0 of 0, name: [nvda-fr] , Role.DOCUMENT , States: , FOCUSED, READONLY, FOCUSABLE, childCount: 34 Path: Role-FRAME| i32, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID: messagepane | i0, Role-DOCUMENT
	o = o.firstChild
	# checkObj(o, "get previwDoc, document expected")
	if o is None: return None, True # ask retry
	if o.role == controlTypes.Role.DOCUMENT:
		return o, False
	return None, False
	
def whichMessagePane(obj, landMark):
	if obj is None:
		beep(110, 40)
		return  "error objFocusNone", None
	# preview, path:  Role-FRAME| i35, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING, , IA2ID: paneLayout | i4, Role-TEXTFRAME, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i14, Role-LANDMARK, , IA2ID: messageHeader | i0, Role-SECTION, , IA2ID: headerSenderToolbarContainer | i0, Role-TOOLBAR, , IA2ID: header-view-toolbox | i0, Role-BUTTON, , IA2ID: hdrReplyButton  
	# separ window,  Path: Role-FRAME| i4, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i14, Role-LANDMARK, , IA2ID: messageHeader | i0, Role-SECTION, , IA2ID: headerSenderToolbarContainer | i0, Role-TOOLBAR, , IA2ID: header-view-toolbox | i0, Role-BUTTON, , IA2ID: hdrReplyButton 
	# search for LANDMARK, ID: messageHeader
	o = obj
	if landMark:
		found = False
		while o is not None: 
			# sharedVars.log(o, "search landMark in messagepane")
			role = o.role
			if role == controlTypes.Role.LANDMARK and hasID(o, "messageHeader"):
				found = True
				break
			if role == controlTypes.Role.INTERNALFRAME and hasID(o, "multiMessageBrowser"):
				return "preview", o
			try: o = o.parent
			except: break
		#end while
		# sharedVars.log(o, "Expected landMark")
		if not found:
			return "not landmark", None
	# preview, path:  Role-FRAME| i35, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING, , IA2ID: paneLayout | i4, Role-TEXTFRAME, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i14, Role-LANDMARK, , IA2ID: messageHeader | i0, Role-SECTION, , IA2ID: headerSenderToolbarContainer | i0, Role-TOOLBAR, , IA2ID: header-view-toolbox | i0, Role-BUTTON, , IA2ID: hdrReplyButton  
	# separ window,  Path: Role-FRAME| i4, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i14, Role-LANDMARK, , IA2ID: messageHeader | i0, Role-SECTION, , IA2ID: headerSenderToolbarContainer | i0, Role-TOOLBAR, , IA2ID: header-view-toolbox | i0, Role-BUTTON, , IA2ID: hdrReplyButton 
	while o is not None:
		role = o.role 
		# sharedVars.log(o, "parent in previewPane")
		if role == controlTypes.Role.GROUPING and hasID(o, "tabpanelcontainer"):
			return "preview", o
		if role == controlTypes.Role.INTERNALFRAME and o.parent.role ==  controlTypes.Role.FRAME:
			return "msgWindow", o
		try: o = o.parent
		except: break

	return "NotFound", None
	
def isSeparMsgWnd():
	o =api.getForegroundObject()
	# sharedVars.log(o, "isSeparMsgWnd fg")
	# Path: Role-FRAME| i4, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID: messagepane | i0, Role-DOCUMENT,  , 
	o = findChildByRoleID(o,controlTypes.Role.INTERNALFRAME, "messageBrowser")
	# sharedVars.log(o, "isSeparMsgWnd, internal frame messageBrowser")
	if o is None:  return False
	sharedVars.curFrame = sharedVars.curTab= "message"
	return True

def getOneMessageGrouping():
	o =api.getForegroundObject()
	# Path: Role-FRAME| i4, Role-INTERNALFRAME, IA2ID: messageBrowser | i0, Role-GROUPING,  | i15, Role-INTERNALFRAME, , IA2ID: messagepane | i0, Role-DOCUMENT,  , 
	o = findChildByRoleID(o,controlTypes.Role.INTERNALFRAME, "messageBrowser")
	if o is None:  return None
	sharedVars.curFrame = sharedVars.curTab= "message"
	return o.firstChild

	# for message list item
from keyboardHandler import KeyboardInputGesture
import winUser

def moveMouseToObject(o, moveCursor=True):
	# location: RectLTWH(left=201, top=170, width=1522, height=22)
	loc = o.location
	# sharedVars.logte("location: left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height))
	x =  int(loc.left + loc.width / 2)
	y = int(loc.top + loc.height / 2)
	# sharedVars.logte("x {}, y {}".format(x, y))
	if moveCursor: winUser.setCursorPos (x, y)
	return x, y

def dragAndDrop(objSource,objTarget, objFocusAfter):
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


# def dragAndDrop(objSource,objTarget):
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



def clickObject(o, left=True):
	# location: RectLTWH(left=201, top=170, width=1522, height=22)
	api.setNavigatorObject(o)
	loc = o.location
	# sharedVars.logte("location: left {} width {} top {} height {}".format(loc.left, loc.width, loc.top, loc.height))
	x =  int(loc.left + loc.width / 2)
	y = int(loc.top + loc.height / 2)
	# sharedVars.logte("x {}, y {}".format(x, y))
	winUser.setCursorPos (x, y)
	if left:
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,1,None,None)
		sleep(0.005) 
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,1,None,None)
	else:
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,1,None,None)
		sleep(0.005) 
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,1,None,None)

def setState(o, newState):
	if newState in o.states: 
		return
	if newState == controlTypes.State.SELECTED:
		# # clickObject(o)
		# KeyboardInputGesture.fromName ("control+space").send()
		o.doAction()
	elif newState == controlTypes.State.EXPANDED:
		if controlTypes.State.COLLAPSED   in o.states:  # necessary double precaution
			# clickObject(o) # necessary  in TB 115 
			o.doAction()
			KeyboardInputGesture.fromName ("control+righTArrow").send()
		else: return
	for i in range(0, 20):
		if newState  in o.states:
			# beep(440, 20)
			break
		api.processPendingEvents()
		sleep(0.1)

	# sharedVars.log(o, "setState,")
	# return

def setMLIState(obj):
	role = obj.role
	if controlTypes.State.SELECTED not in obj.states: 
		setState(obj, controlTypes.State.SELECTED)
	if role == controlTypes.Role.TREEVIEWITEM   and controlTypes.State.EXPANDED not in obj.states:
		setState(obj, controlTypes.State.EXPANDED)
# Headers pane utils
# class RecurseHeaders():
	# def	 __init__(self,IDObj, IDLabel, IDName):
		# self.IDObj = IDObj
		# self.IDLabel = IDLabel
		# self.IDName = IDName
		# self.outObj = None
		# self.outLabel = self.outName = ""
	# def run(self,obj): 
		# if obj is None: return
		# obj = obj.firstChild
		# if obj is None: return 
		# while obj is not None:
			# ID =  str(getIA2Attr(obj))
			# if ID.startswith(self.IDObj):
				# if obj.role == controlTypes.Role.LISTITEM: 
					# self.outObj = obj # .parent
					# self.outLabel =  obj.parent.name
					# o = obj
					# while o is not None:
						# n =  self.cleanAddr(o.name)
						# if n: self.outName += n + ";"
						# o = o.next
					# self.outName = self.outName[:-1]
					# return
				# else: # not listitem 
					# self.outObj = obj
			# if ID.startswith(self.IDLabel):
				# self.outLabel = obj.name  
			# if ID.startswith(self.IDName):
				# self.outName = str(obj.name)
			# self.run(obj)
			# obj = obj.next
		# return
	# def cleanAddr(self, nm):
		# sep = " "
		# if "<" in nm and ">" in nm:
			# sep = ">"
		# return  nm.split(sep)[0] + ">"				

def trimAddr(addr) : # truncate mail address after >
	pos = addr.rfind(">")
	if pos != -1 :
		return addr[:pos+1]
	pos = addr.rfind("@")
	if pos == -1 :
		return addr
	pos = addr.find(" ", pos+1)
	if pos != -1 : 
		return addr[:pos]
	return addr
def getRecipientHeader(oRoot, labelID, objID):
	if oRoot is None :
		return "", "", None
	# attention : objID without de ending digits 
	firstObjID = objID + "0"
	label = ""
	firstObj = None
	for c in oRoot.recursiveDescendants : 
		if label and firstObj is not None: break
		ID = str(getIA2Attr(c))
		if ID == labelID: label = str(c.name) +": "
		elif  ID == firstObjID: firstObj = c
	# end for
	if firstObj is None: return "", "", None
	# sharedVars.logte("Label" + label)
	c = firstObj
	name = ""
	while c is not None :
		if hasID(c, objID) : 
			# sharedVars.log(c, "toRecipient")
			name += trimAddr(str(c.name)) + ";"
		c = c.next
	# end while
	return label, name[:-1], firstObj

def getSimpleHeader(oRoot, labelID, objID):
	if oRoot is None :
		return "", ""
	label = ""
	obj = None
	for c in oRoot.recursiveDescendants : 
		if label and obj is not None: break
		ID = str(getIA2Attr(c))
		if ID == labelID: label = str(c.name) +": "
		elif  ID == objID: obj = c
	# end for
	if obj is None: return "", "", None
	# sharedVars.logte("Label" + label)
	name = ""
	if hasID(obj, objID) : 
		# sharedVars.log(c, "toRecipient")
		name = str(obj.name)
	return label, name, obj

def getHeader(o, key, repeats=0, say=True):
	if o is None: return"", ""
	# checkObj(o, "focus obj")
	if hasID(o, "threadTree"): 
		if controlTypes.State.COLLAPSED   in o.states:
			# does not work because Alt was pressed before:KeyboardInputGesture.fromName ("righTArrow").send()
			message(_("Press right arrow and retry, please."))
			return "", ""
		o = getMessagePane()
		# checkObj(o, "messagePane depuis liste")
		# if o is None:
			# message("F8")
			# KeyboardInputGesture.fromName ("f8").send()
			# sleep(0.15)
			# o = getMessagePane()
			# # checkObj(o, "messagePane after  f8")
			# if o is None: return
		if o is None:  
			message(_("The headers pane is not displayed. Please press F8 then try again"))
			return "", ""
		o = getMessageHeaders(o)
	elif hasattr(o, "role") and  o.role == controlTypes.Role.DOCUMENT:
		o = findChildByRoleID(o.parent.parent, controlTypes.Role.LANDMARK, "messageHeader", 12)
	else: return "", ""
	# checkObj(o, "messageHeaders")
	if o is None:  
		message(_("The headers are not available"))
		return "", ""
	dbg = False if commonVars.cv.logger is None else True
	import tbLogger
	
	role = controlTypes.Role.SECTION
	ran = False
	hdrLabel = "" 
	hdrName = ""
	hdrObj = None
	if key == 1: #  from
		# level 1, idx 0 of 2: Role.SECTION, ID: headerSenderToolbarContainer, childCount: 2
		o = findChildByRoleID(o, role, "headerSenderToolbarContainer", 0) 
		if dbg: commonVars.cv.logger.addobj(o, "getHeader from, headerSenderToolbarContainer") 
		# new version 2026-09-03 
		hdrLabel, hdrName, hdrObj = getRecipientHeader(o, "expandedfromLabel", "fromRecipient")
	elif key == 2: # subject
		o = findChildByRoleID(o, role, "headerSubjectSecurityContainer", 0) 
		hdrLabel, hdrName, hdrObj = getSimpleHeader(o, "expandedsubjectLabel", "expandedsubjectBox")
		# remove "subject:" from the subject
		pos =  hdrName.find(":")
		if pos > -1:  hdrName = hdrName[pos+1:].strip()
		# subject has no doAction attribute
		if repeats == 2:
			hdrObj.setFocus()
			wx.CallAfter(message, hdrName)
			KeyboardInputGesture.fromName("applications").send()
			return ""
	elif key == 3: # date 
		o = findChildByRoleID(o, role, "expandedtoRow", 1) 
		# hdrLabel= ""
		# hdrName = ""
		if  o : 
			for c in o.recursiveDescendants :
				if hdrName : break
				if hasID(c, "dateLabel"): hdrName = str(c.firstChild.name)
			# end for
		return message(hdrLabel + hdrName)
	elif key == 4: # to
		o = findChildByRoleID(o, role, "expandedtoRow", 1) 
		# new version 2026-09-03 
		hdrLabel, hdrName, hdrObj = getRecipientHeader(o, "expandedtoLabel", "toRecipient")
	elif key == 5: # CC:
		o = findChildByRoleID(o, role, "expandedccRow", 2) 
		hdrLabel, hdrName, hdrObj = getRecipientHeader(o, "expandedccLabel", "ccRecipient")
	elif key == 6: # BCC:
		o = findChildByRoleID(o, role, "expandedbccRow", 2) 
		hdrLabel, hdrName, hdrObj = getRecipientHeader(o, "expandedbccLabel", "bccRecipient")
	# elif key == 9: # attachments: not implemented here
	elif key == 0: # tags
		# level 9,          4 of 10, Role.SECTION, IA2ID: expandedtagsRow, left:232 Tag: div, States: , childCount: 1 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID: messageHeader | i4, Role-SECTION, , IA2ID: expandedtagsRow , IA2Attr: id: expandedtagsRow, display: flex, class: message-header-row, tag: div,  ;
		o = findChildByRoleID(o,controlTypes.Role.SECTION, "expandedtagsRow")
		# level 10,           0 of 0, Role.SECTION, IA2ID: expandedtagsBox, left:232 Tag: div, States: , childCount: 1 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID: messageHeader | i4, Role-SECTION, , IA2ID: expandedtagsRow | i0, Role-SECTION, , IA2ID: expandedtagsBox , IA2Attr: id: expandedtagsBox, display: block, class: header-tags-row, tag: div, formatting: block,  ;
		# level 11,            0 of 0, name: Étiquettes, Role.LIST, left:230 Tag: ol, States: , READONLY, childCount: 1 Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i13, Role-LANDMARK, , IA2ID: messageHeader | i4, Role-SECTION, , IA2ID: expandedtagsRow | i0, Role-SECTION, , IA2ID: expandedtagsBox | i0, Role-LIST,  , IA2Attr: class: tags-list, explicit-name: true, child-item-count: 1, display: flex, tag: ol,  ;
		o = o.firstChild.firstChild
		t = o.name + ": "
		o = o.firstChild
		while o is not None:
			if o.name: t += o.name + ", "
			o = o.next
		return message(t)
	else: # extra headers
		return message(_("blank"))
		# End of Header list
	if not hdrName: 
		headerLabels = _("void,From,Subject: ,Date,To,CC,BCC,Reply to") 
		headerNotFound = _("The {0} header is missing from this message.")
		if say: message(headerNotFound.format(headerLabels.split(",")[key]))
		return  hdrLabel, hdrName
	if repeats == 0:
		if say:
			message(hdrLabel + hdrName)
		else:
			return hdrLabel, hdrName, hdrObj
	elif repeats == 1:
		CallLater(100, utis.inputBox , label=hdrLabel, title=hdrLabel + ": " + _("Copy to clipboard"), postFunction=None, startValue=hdrName)
	else:
		try: 
			hdrObj.doAction()
		except: 
			clickObject(hdrObj, False) # right click
	return  ""

def getAttachment(oFocus=None, repeats=0):
	# in  main window:name: doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID: attachmentName Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID: attachmentName , IA2Attr: id: attachmentName, display: flex, xml-roles: button, tag: label, , Actions: click,  ;
	# In separate window: 18 of 20, name: doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID: attachmentName, Path: Role-FRAME| i4, Role-INTERNALFRAME, IA2ID: messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID: attachmentName
	# sharedVars.debugLog = "getAttachment, repeats: " + str(repeats) + "\n"
	if not oFocus: oFocus = api.getFocusObject()
	if oFocus.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.LINK): 
		# if repeats > 0 and oFocus.role == controlTypes.Role.LINK: beep(700, 40)
		o = findParentByRole(oFocus, controlTypes.Role.GROUPING)
		# sharedVars.log(o, "is Grouping from doc ? ")
		if repeats > 0 and o.role != controlTypes.Role.GROUPING: return beep(100, 10)
	elif hasID(oFocus, "threadTree"):
		o = getMessagePane()
		# sharedVars.log(o, "in mainWindow , expected messagePane")
		o = o.firstChild.firstChild
		# sharedVars.log(o, "in mainWindow , expected Grouping")
	else: return beep(100, 30)
	
	# common to list and separate reading window
	# current object is grouping with no IA2ID
	oStart = o.getChild(14) # cannot be 15 which ID is messagePane
	oLast = o.lastChild
	oList = oLast if oLast.role == controlTypes.Role.LIST  else None
	ID = str(getIA2Attr(oLast))
	if ID in ("messagepane", "content"):
		return message(_("No attachment."))
	elif ID.startswith("attachmentSaveAll"):  # hidden attachment list
		o = oStart
		# 1: search:   Role.TOGGLEBUTTON, ID: attachmentToggle, childCount: 0
		while o is not None:
			ID = str(getIA2Attr(o))
			if o.role == controlTypes.Role.TOGGLEBUTTON and ID == "attachmentToggle":
				if controlTypes.State.PRESSED not in o.states: 
					o.doAction()
					sleep(0.1)
					oList = o.parent.lastChild
				break
			o = o.next
		if oList is None :
			# message("No attachment")
			return

	# 2: search again from oStart
	text =  ""
	o = oStart
	while o is not None:
		# sharedVars.log(o, "getAttachmment, in loop: ")
		ID = str(getIA2Attr(o))
		if ID == "attachmentCount":
			text +=  str(o.name)
		elif ID == "attachmentSize":
			text +=  o.name
		o = o.next
	if repeats == 0:
		text += ", "
				
		o = oList.firstChild
		while o is not None: 
			text += str(o.name) + ", "
			o = o.next
		message(text + ", " + _	("Two presses to reach the list."))
		return
	elif repeats > 0: 
		cc =  oList.childCount
		if cc > 0: 
			oList = oList.firstChild
			oList.setFocus()
			if cc == 1:
				cancelSpeech()
				CallLater(500, message, oList.name)
				KeyboardInputGesture.fromName("shift+f10").send()

def getAttachment_notOK(oFocus=None, repeats=0):
	# in  main window:name: doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID: attachmentName Path: Role-FRAME| i31, Role-GROUPING, , IA2ID: tabpanelcontainer | i2, Role-PROPERTYPAGE, , IA2ID: mail3PaneTab1 | i0, Role-INTERNALFRAME, , IA2ID: mail3PaneTabBrowser1 | i0, Role-GROUPING,  | i4, Role-SECTION, , IA2ID: messagePane | i0, Role-INTERNALFRAME, , IA2ID: messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID: attachmentName , IA2Attr: id: attachmentName, display: flex, xml-roles: button, tag: label, , Actions: click,  ;
	# In separate window: 18 of 20, name: doc_thunderbirdPlusG5_fr.md, Role.BUTTON, IA2ID: attachmentName, Path: Role-FRAME| i4, Role-INTERNALFRAME, IA2ID: messageBrowser | i0, Role-GROUPING,  | i18, Role-BUTTON, , IA2ID: attachmentName
	# sharedVars.debugLog = "getAttachment, repeats: " + str(repeats) + "\n"
	if not oFocus: oFocus = api.getFocusObject()
	if oFocus.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.LINK): 
		# if repeats > 0 and oFocus.role == controlTypes.Role.LINK: beep(700, 40)
		o = findParentByRole(oFocus, controlTypes.Role.GROUPING)
		# sharedVars.log(o, "is Grouping from doc ? ")
		if repeats > 0 and o.role != controlTypes.Role.GROUPING: return beep(100, 10)
	elif hasID(oFocus, "threadTree"):
		o = getMessagePane()
		# sharedVars.log(o, "in mainWindow , expected messagePane")
		o = o.firstChild.firstChild
		# sharedVars.log(o, "in mainWindow , expected Grouping")
	else: return beep(100, 30)
	
	# common to list and separate reading window
	oStart = o.getChild(14) # cannot be 15 which ID is messagePane
	oLast = o.lastChild
	# sharedVars.log(oStart, "oStart, repeats: " + str(repeats))
	# sharedVars.log(oLast, "oLast, repeats: " + str(repeats))		

	oList = None
	ID = str(getIA2Attr(oLast))
	if ID in ("messagepane", "content"):
		return message(_("No attachment."))
	# elif ID.startswith("attachmentSaveAll"):  # hidden attachment list
		# o = oStart
		# # search:   Role.TOGGLEBUTTON, ID: attachmentToggle, childCount: 0
		# while o is not None:
			# ID = str(getIA2Attr(o))
			# if o.role == controlTypes.Role.TOGGLEBUTTON and ID == "attachmentToggle":
				# if controlTypes.State.PRESSED not in o.states: 
					# # beep(440, 10)
					# CallAfter(o.doAction)
					# return
			# o = o.next
	elif ID == "attachmentList": 
		oList = oLast

	text =  ""
	o = oStart
	while o is not None:
		# sharedVars.log(o, "getAttachmment, in loop: ")
		ID = str(getIA2Attr(o))
		if ID == "attachmentCount":
			text +=  str(o.name)
		elif ID == "attachmentSize":
			text +=  o.name
		o = o.next
	# sharedVars.logte(text)
	if repeats == 0:
		text += ", "
		o = oList.firstChild
		while o is not None: 
			text += str(o.name) + ", "
			o = o.next
		message(text + ", " + _("Two presses to reach the list."))
	elif repeats > 0: 
		cc = oList.childCount
		if cc >  0: 
			oList = oList.firstChild
			oList.setFocus()
			if cc > 1:
				return
			cancelSpeech()
			CallLater(500, message, oList.name)
			KeyboardInputGesture.fromName("shift+f10").send()

def getChildByRoleIDName(oParent, role, ID, name, idx=0): # attention: controlTypes roles
	if sharedVars.debug: 
		sharedVars.logte("* Start of getChildByRoleIDName search for role: {}, ID: {}, idx: {}, {}".format(role.name, ID, idx, name))
		sharedVars.log(oParent, "Begin getChildByRoleIDName oParent")
	if not oParent: 
		return None
	# ID can be the n first chars of the searched 
	try:  # except
		if idx > 0: o = oParent.getChild(idx)
		else: o = oParent.firstChild
	except:
		if sharedVars.debug: sharedVars.log(o, "getChildByRoleIDName Exception in getChildByRoleIDName")
		o = oParent.firstChild
		pass
	result = None
	while o is not None:
		if sharedVars.debug: sharedVars.log(o, "Loop begin")
		if o.role == role:
			if sharedVars.debug: sharedVars.log(o, "Role matched")
			if ID == "" and name == "": 
				# sharedVars.log(o, "returned o Empty ID and name matched")
				return o
			if ID:
				objID = str(getIA2Attr(o))
				if objID.startswith(ID): 
					if sharedVars.debug: sharedVars.log(o, "returned o  ID matched")
					return o
			elif name and hasattr(o, "name") and o.name.startswith(name):
				# sharedVars.log(o, "Name matched")
				return  o
			else:
				# sharedVars.log(o, "returned o Only Role matched")
				return o
		o = o.next
		idx += 1
		# end while
	if o is None:
		if sharedVars.debug: sharedVars.logte("Not found in getChildByRoleIDName: role={}, ID={}, name={}".format(role.name, ID, name))
	return None

def getReplyToolbarFromMsgWindow():
	# separate reading window
	oMsgHeader = None
	o = api.getForegroundObject() 
	# IA2ID = messageBrowser in , Role.INTERNALFRAME
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.INTERNALFRAME, ID="messageBrowser", name="", idx=4)
	if o is None:
		return None, None
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="", name="", idx=0)
	# IA2ID = messageHeader in , Role.LANDMARK
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.LANDMARK, ID="messageHeader", name="", idx=14)
	oMsgHeader = o
	# IA2ID = headerSenderToolbarContainer in , Role.SECTION
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.SECTION, ID="headerSenderToolbarContainer", name="", idx=0)
	# IA2ID = header-view-toolbox in , Role.TOOLBAR
	return o, oMsgHeader

def getReplyToolbarFromMain(msgPane): 
	oMsgHeader = None
	# o = api.getForegroundObject()
	# # IA2ID = tabpanelcontainer in , Role.GROUPING
	# o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="tabpanelcontainer", name="", idx=36)
	# if o is None:
		# return None, None
	# # IA2ID = mail3PaneTab1 in , Role.PROPERTYPAGE
	# if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.PROPERTYPAGE, ID="mail3PaneTab", name="", idx=2)
	# # IA2ID = mail3PaneTabBrowser1 in , Role.INTERNALFRAME
	# if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.INTERNALFRAME, ID="mail3PaneTabBrowser", name="", idx=0)
	# # IA2ID = paneLayout in , Role.GROUPING
	# if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="paneLayout", name="", idx=0)
	# # IA2ID = messagePane in , Role.TEXTFRAME
	# if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.TEXTFRAME, ID="messagePane", name="", idx=4)
	# IA2ID = messageBrowser in , Role.INTERNALFRAME
	o = getChildByRoleIDName(msgPane, controlTypes.Role.INTERNALFRAME, ID="messageBrowser", name="", idx=0)
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="", name="", idx=0)
	# IA2ID = messageHeader in , Role.LANDMARK
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.LANDMARK, ID="messageHeader", name="", idx=14)
	oMsgHeader = o
	# IA2ID = headerSenderToolbarContainer in , Role.SECTION
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.SECTION, ID="headerSenderToolbarContainer", name="", idx=0)
	# IA2ID = header-view-toolbox in , Role.TOOLBAR
	if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.TOOLBAR, ID="header-view-toolbox", name="", idx=0)
	return o, oMsgHeader

def getSenderNames(obj, ID):
	# sharedVars.log(obj, "Begin of getsenderNames") 
	names = ID + ":"
	for c in obj.recursiveDescendants:
		if c.role in (controlTypes.Role.LISTITEM,controlTypes.Role.SECTION) and  hasattr(c, "name"):
			nm = "" if not hasattr(c, "name") or not c.name else c.name
			sep = "<" if "<" in nm else " "
			pos = nm.find(sep)
			if pos > -1:
				nm = nm[pos+2:-1] if "List-ID" in nm else nm[0:pos]
				if nm:
					names += nm.strip() + "; "
	# sharedVars.logte(names)
	return names

def smartReplyV4(shift, repeats=0):
	debug = False
	o = None
	if sharedVars.curTab == "main":
		oPane = getMessagePane()
		if not oPane:
			return message(_("The preview pane is not displayed. Press F8 and try again please"))
		fo = api.getFocusObject()
		if fo.role == controlTypes.Role.TREEVIEWITEM  and controlTypes.State.COLLAPSED in fo.states:
			KeyboardInputGesture.fromName("rightArrow").send()
			sleep(0.1)
		if fo.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and controlTypes.State.SELECTED not in fo.states:
			fo.doAction()
			sleep(0.1)
		if debug: sharedVars.debugLog = ""
		# IA2ID = messageBrowser in , Role.INTERNALFRAME
		o = getChildByRoleIDName(oPane, controlTypes.Role.INTERNALFRAME, ID="messageBrowser", name="", idx=0)
		# sharedVars.log(o, "Message Browser ? ")
		if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="", name="", idx=0)
		# sharedVars.log(o, "Grouping  ? ")
		# IA2ID = messageHeader in , Role.LANDMARK
		if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.LANDMARK, ID="messageHeader", name="", idx=14)
	elif sharedVars.curTab == "message": # separate reading window 
		# IA2ID = messageBrowser in , Role.INTERNALFRAME
		o = getChildByRoleIDName(api.getForegroundObject(), controlTypes.Role.INTERNALFRAME, ID="messageBrowser", name="", idx=4)
		if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="", name="", idx=0)
		# IA2ID = messageHeader in , Role.LANDMARK
		if o is not None: o = getChildByRoleIDName(o, controlTypes.Role.LANDMARK, ID="messageHeader", name="", idx=14)

	if o is None:
		return
	if debug: sharedVars.log(o, "messageHeader ? ")
	# process reply buttons 
	gest = "control+r"
	# groups = ""
	for child in   o.recursiveDescendants:
		if debug: sharedVars.log(child, "Descendant")	
		role = child.role
		if role == controlTypes.Role.BUTTON: 
			IA2ID = str(getIA2Attr(child))
			match IA2ID: 
				case "hdrReplyListButton":
					if not shift:
						gest = "control+shift+l"
						break
				case "hdrReplyAllButton":
					if shift: 
						gest = "control+shift+r"
						break
				case "hdrArchiveButton":
					# default exit condition 
					break
		# elif role == controlTypes.Role.LISTITEM:
			# if hasID(child, "toRecipient"):
				# name = child.name
				# if "groups"  in name  or "list" in name:
					# groups += name + "," 
					# sharedVars.log(child, "Recipient")	
	if debug: 
		message("gest=" + gest + ", pressez Alt+f12 pour voir les objets descendants")
	else:
		# avoid double announcement  of the write windows title
		setSpeechMode(SpeechMode.off)
		sharedVars.replyTo = True
		return KeyboardInputGesture.fromName(gest).send()

def getTotalColIdx(oTT):
	try: # finally
		# oTT must be the threadTree
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
			# flat list mode: path Role-TEXTFRAME, , IA2ID: threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
		o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
		i = 0
		while o is not None:
			if hasID(o, "totalCol"):
				# sharedVars.logte("index of total col: " + str(i))
				return i
			i += 1
			o = o.next
		return -1
	finally:
		sharedVars.objLooping = prevLooping

def cleanWinTitle(title):
	i =  title.rfind(" - ")
	if i > -1:
		title =  title[0:i]
	return title.strip((" ,;:?!+"))
# test funcions
def listColumnID(oTT):
	try:
		# oTT must be the threadTree
		prevLooping = sharedVars.objLooping
		sharedVars.objLooping = True
		# sharedVars.logte("Begin Column ID list")
			# flat list mode: path Role-TEXTFRAME, , IA2ID: threadTree | i0, Role-TABLE,  | i0, Role-TEXTFRAME,  | i0, Role-TABLEROW,  , 
		o =  oTT.firstChild.firstChild.firstChild.firstChild  # first headers of threadTree
		i = 0
		while o is not None:
			role = str(o.role)
			ID = str(getIA2Attr(o))
			left =  str(o.location.left) 
			name = "" if not hasattr(o, "name") else o.name
			cName = ""
			if o.firstChild:
				cName = "" if not hasattr(o.firstChild, "name") else o.firstChild.name
			# sharedVars.logte("idx: {},ID {}, left: {}, name: {}, cName: {}, {}".format(i, ID, left, name, cName, role))
			i += 1
			o = o.next
	finally:
		# sharedVars.logte("End of  Column ID list")
		sharedVars.objLooping = prevLooping
def listColumnNames(oRow):
	if sharedVars.debug: sharedVars.logte("* Begin of columnNames ")
	o = oRow.firstChild
	while o is not None:
		left =  str(o.location.left) 
		clsFull = str(getIA2Attr(o, False, "class"))
		cls = clsFull.split(" ")
		cls = str(cls[len(cls)-1])
		cls = cls.split("-")[0]
		name = "" if not o.name else ", name:" + str(o.name)
		value = "" if not o.value else ", value:" + str(o.value)
		cName = cValue = ""
		if o.firstChild:
			oc = o.firstChild
			cName = "" if not oc.name else ", cName:" + str(oc.name)
			cValue = "" if not oc.value else ", cValue:" + str(oc.value)
		if sharedVars.debug: sharedVars.logte(left + ", " +  cls + ", " + clsFull + str(name) + str(value) + str(cName) + str(cValue))
		o = o.next
	# sharedVars.logte("* End of columnNames ")
	

def getColValue(oRow, colID):
	o = oRow.firstChild
	idx = 0
	iFound = -1
	while o is not None:
		cls = str(getIA2Attr(o, False, "class"))
		if cls.startswith(colID):
			iFound = idx
			break
		idx += 1
		o=o.next

	if iFound == -1: return "" # colID + " column not found"
	cName = ""	
	oc = oRow.getChild(iFound)
	sep = ": "
	while oc:
		if hasattr(oc, "name"): 
			cName +=str(oc.name) + sep
			sep = ""
		try: oc = oc.firstChild
		except: break

	# result = "cls={}, index={}, cName={}".format(cls, iFound, cName)
	return cName
		
def recurseObjects(o, level): 
	if o is None: return None
	o = o.firstChild
	if o is None: return None
	cCount = " of " + str(o.childCount)
	level += 1
	i = 0
	while o is not None:
		# sharedVars.log(o, "# level " + str(level) + ", idx " + str(i) + cCount)
		if o.childCount > 0:
			recurseObjects(o, level)
		o = o.next
		i += 1
	return o
def listAscendants(last=-4, o=None, title="** List of ascendants"):
	last = (last if last <= 0 else 0 - last)
	if o is None:
		o = api.getFocusObject()
	if sharedVars.debug: sharedVars.logte(title)
	lev = 0
	while o  and lev >= last:
		if sharedVars.debug: sharedVars.log(o, "level " + str(lev))
		if o.role in (controlTypes.Role.FRAME, controlTypes.Role.DIALOG): return
		lev -= 1
		o = o.parent

def listDescendants(o=None, lev=0, tit=None):
	if o is None:
		o = api.getFocusObject()
	if tit:
		if sharedVars.debug: sharedVars.logte(tit)
	lev += 1
	o = o.firstChild
	i = 1
	while o is not None:
		if sharedVars.debug: sharedVars.log(o, "level " + str(lev) + " " + str(i))
		if o.childCount:
			listDescendants(o, lev) 
		i +=1
		o = o.next

class NVDATBMenu(wx.Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def AppendNVDAItem(self, item_id, label, nvda_obj):
		"""Adds an item and links the NVDA object via ClientData."""
		item = self.Append(item_id, label)
		if item:
			item.SetClientData(nvda_obj)
		return item


