#-*- coding:utf-8 -*
# ThunderbirdPlusG5

import sys
import speech 
from winsound import MessageBeep 
try:
	from UIAUtils import createUIAMultiPropertyCondition
except ImportError:
	from UIAHandler.utils import createUIAMultiPropertyCondition
from oleacc import STATE_SYSTEM_UNAVAILABLE,STATE_SYSTEM_PRESSED
from tones import beep
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, sharedVars
from utis import getIA2Attribute, showNVDAMenu , TBMajor,  getElementWalker
del sys.path[-1]
addonHandler.initTranslation()
from time import sleep
from oleacc import STATE_SYSTEM_PRESSED, ROLE_SYSTEM_PUSHBUTTON
from keyboardHandler import KeyboardInputGesture, passNextKeyThrough
import controlTypes,wx
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
from gui import mainFrame
from wx import CallAfter, CallLater # ,Menu,MenuItem,ITEM_CHECK,EVT_MENU
from NVDAObjects.IAccessible import IAccessible
from ui import message
from UIAHandler import handler,TreeScope_Children,  TreeScope_Descendants, UIA_ControlTypePropertyId, UIA_TableControlTypeId, UIA_EditControlTypeId, UIA_ListControlTypeId  ,UIA_ListItemControlTypeId ,UIA_ButtonControlTypeId, UIA_LegacyIAccessibleStatePropertyId,UIA_ToolBarControlTypeId, UIA_ComboBoxControlTypeId ,UIA_LegacyIAccessibleStatePropertyId , UIA_SeparatorControlTypeId , IUIAutomationLegacyIAccessiblePattern, UIA_LegacyIAccessibleValuePropertyId ,UIA_LegacyIAccessibleNamePropertyId,IUIAutomationInvokePattern
clientObject =handler.clientObject
GetFirstChildElement, GetNextSiblingElement, GetParentElement, GetLastChildElement    = clientObject.RawViewWalker.GetFirstChildElement, clientObject.RawViewWalker.GetNextSiblingElement, clientObject.RawViewWalker.GetParentElement, clientObject.RawViewWalker.GetLastChildElement
CPC=clientObject.CreatePropertyCondition 
import winUser
from winUser import *
import UIAHandler
import globalVars
import api
#pas de vocalisation de control+b,u,i 
#objEntetes = ["", _("De"), _("Sujet"), _(""), _("Pour"), _("Copie à"), _("Copie cachée à")] #,"Réponse à"
# dbg = sharedVars.log


class MsgComposeWindow():
	frame = None	
	def __init__(self) : # obj = focused object in msgComposeWindow
		self.headersToolbar = None
		self.labelsID = ["", "identityLabel", "toAddrLabel", "attach", "ccAddrLabel", "bccAddrLabel", "subjectLabel", "replyAddrLabel"] 
		self.fieldGestures = ["", "Alt+e", "toAddrLabel", "attach", "control+shift+c", "control+shift+b", "alt+s", "replyAddrLabel"] 
		#translators: compose field labels : "none, From, To, Attachement, CC, BCC, Subject, Reply to"
		self.fieldLabels = _("void, From, To, Attachement, CC, BCC, Subject, Reply to")

	def update(self) :
		if self.frame==  globalVars.foregroundObject : return
		# v5 Niveau 3,    3 sur 8, name : Pour, role.LABEL=73, IA2ID : toAddrLabel Tag: label, états : , READONLY, childCount  : 1 
		#Chemin : role FRAME=34| i13, role-SECTION=86, , IA2ID : composeContentBox | i0, role-TOOLBAR=35, , IA2ID : MsgHeadersToolbar | i3, role-LABEL=73, , IA2ID : toAddrLabel 
		self.frame = globalVars.foregroundObject
		# i13, role-SECTION=86, , IA2ID : composeContentBox
		obj = utis.findChildByID(self.frame, "composeContentBox") 
		# search toolbar
		obj = utis.findChildByID(obj, "MsgHeadersToolbar") 
		self.headersToolbar = obj
		return

	def getMsgHeader(self, oToolbar, idx, noText) :
		findID = self.labelsID[idx]
		sharedVars.debugLog = ""
		lbl = ""
		o = oToolbar.firstChild 
		# sharedVars.log(o, "toolbar firstChild, ID a trouver : " + findID) 
		while o :
			if o.role == controlTypes.Role.LABEL :
				if str(utis.getIA2Attribute(o)) == findID :
					# sharedVars.log(o, "Label") 
					lbl = o.name + " : "
					oFocus = o
					o = o.next
					if not o : return None, "no obj"
					if o.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.COMBOBOX) :
						return o, lbl + (" vide"if not o.value else o.value)
					elif o.role in (controlTypes.Role.UNKNOWN, controlTypes.Role.PANE) :  # TB115, TB128
						oFocus = o
						loopRole = o.role
						val = ""
						while o and o.role == loopRole :
							# sharedVars.log(o, "objet inconnu") 
							val +=  o.name.split(">")[0] + ">, "
							o = o.next
						return oFocus, lbl + val
			o = o.next # caution : 3 tabs 
		return None, _("No header.")

	def readField(self, mainKeyName, repeats) :
		mainKeyName = int(mainKeyName)
		if mainKeyName == 3 : # appeler fonction getAttachment
			CallAfter(self.readAttachments, repeats)
			return
		lastIdx = len(self.labelsID) - 1
		if mainKeyName > lastIdx : mainKeyName = lastIdx - 1 # subject
		oField, fieldText = self.getMsgHeader(self.headersToolbar, mainKeyName, (repeats > 0))
		# sharedVars.log(oField, fieldText)
		if not oField : 
			if repeats == 0 : message(_("The field {0} is missing, type this command twice quickly to show it.").format(self.fieldLabels.split(",")[mainKeyName]))
			elif repeats > 0 : 
				try : KeyboardInputGesture.fromName(self.fieldGestures[mainKeyName]).send()
				except : message(_("You will find this field by pressing the button: Other addressing fields to show"))
			return
		if not repeats :
			message(fieldText)
		else :
			if not oField.hasFocus :
				oField.setFocus()
				if mainKeyName == 1 : # 2025-01-10 open from combo box
					CallLater(100, KeyboardInputGesture.fromName("alt+downArrow").send)				
				
	# attachments
	def getAttachments(self) :
		# 0 sur 0, name : update-settings .ini 155 octet, role.LISTITEM=15 Tag: richlistitem, états : , FOCUSED, SELECTED, SELECTABLE, FOCUSABLE, childCount  : 4 
		# path  : role FRAME=34| i13, role-SECTION=86, , IA2ID : composeContentBox 
		o = utis.findChildByID(self.frame, "composeContentBox") 
		if not o : 
			return None, "Error retrieving composeContentBox"
		# | i4, role-GROUPING=56, , IA2ID : attachmentArea 
		o = utis.findChildByID(o, "attachmentArea")
		if not o : 
			# translator
			return None, _("The attachments area is missing. Press Control+Shift+A to add attachements.")
		#0 sur 1, name : 1 pièce jointe 155 octets, role.BUTTON=9 Tag: summary, états : , EXPANDED, FOCUSABLE, childCount  : 3 
		# path : role FRAME=34| i13, role-SECTION=86, , IA2ID : composeContentBox | i4, role-GROUPING=56, , IA2ID : attachmentArea | i0, role-BUTTON=9,  , IA2Attr : display : flex, tag : summary, , Actions : collapse,  ;
		o = o.firstChild
		msgAttach = o.name + " : " 
		# | i1, role-LIST=14, , IA2ID : attachmentBucket 
		o = o.next
		# attachment list
		o = o.firstChild
		oFocus = o
		i = 1
		while o   :
			msgAttach += str(i) + " : " + o.name + ", "
			i += 1
			o = o.next
		return oFocus,  msgAttach

	def readAttachments(self, repeats) :
		oAttach, textAttach = self.getAttachments()
		if not repeats  :
			message(textAttach)
		else :
			if oAttach : oAttach.setFocus()
# normal functions
def focusDoc() :
	utis.sendKey("shift+tab", 2)
	d = getComposeDoc()
	if d and d.role == controlTypes.Role.DOCUMENT : 
		message("Corps du message.")
		CallLater(100, api.setFocusObject, d) # d.setFocus() does not work
			
# Niveau 2,   0 sur 0, name : Corps du message, role.DOCUMENT=52 Tag: body, états : , FOCUSED, FOCUSABLE, EDITABLE, childCount  : 5 Chemin : role FRAME=34| i23, role-INTERNALFRAME=115, , IA2ID : content-frame | i0, role-DOCUMENT=52,  , IA2Attr : explicit-name : true, display : block, tag : body, line-number : 1,  ;
def getComposeDoc() :
	sharedVars.objLooping = True
	o = globalVars.foregroundObject
	# recent version of TB > 102.10
	# level 4,     0 of 0, name : Corps du message, Role.DOCUMENT Tag: body, States : , FOCUSED, FOCUSABLE, EDITABLE, childCount  : 5 Path : Role-FRAME
	# search child  i13, Role-SECTION, , IA2ID : composeContentBox 
	o = utis.findChildByRoleID(o, "composeContentBox", controlTypes.Role.SECTION, 10)
	# search i5, Role-SECTION, , IA2ID : messageArea 
	o = utis.findChildByRoleID(o, "messageArea", controlTypes.Role.SECTION)
	if o :
		# select  i0, Role-INTERNALFRAME, , IA2ID : messageEditor | i0, Role-DOCUMENT,  , IA2Attr : display : block, explicit-name : true, tag : body, line-number : 1,  ;
		o = o.firstChild.firstChild
		if o : return o
	# below, old versions of TB
	#beep(120, 20)
	#if sharedVars.debug : sharedVars.log(o, "cadre ?")
	o = utis.findChildByIDRev(o, "content-frame")
	#if sharedVars.debug : sharedVars.log(o, "section 115 ?")
	if not o : return None 
	#beep(440, 20)
	o = o.firstChild
	#if sharedVars.debug : sharedVars.log(o, "Document ?")
	sharedVars.objLooping = False
	return o
	
def getComposeHeader(o, key, repeats=0) :
	oCompose = MsgComposeWindow()
	oCompose.update()
	oCompose.readField(key, repeats)

