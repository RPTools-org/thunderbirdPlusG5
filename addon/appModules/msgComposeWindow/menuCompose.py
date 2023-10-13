#-*- coding:utf-8 -*
# Thunderbird+ 4.x

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
from utis import getIA2Attribute, showNVDAMenu , versionTB,  getElementWalker
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
from wx import CallAfter, CallLater,Menu,MenuItem,ITEM_CHECK,EVT_MENU
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


class ComposeMenu() :
	kbd =(u"Ctrl+Maj+G,Ctrl+Maj+J,Ctrl+Maj+U,Ctrl+Maj+S,Ctrl+Alt+P,Ctrl+Alt+P,Ctrl+Maj+Alt+P,Ctrl+Maj+D,Ctrl+Maj+"+_("lower than")+",Ctrl+"+_("lower than")+",Ctrl+B,Ctrl+I,Ctrl+U,Ctrl+Maj+"+_("semicolon")+",Ctrl+Maj+"+_("colon")+",Ctrl+Maj+"+_("equal")+",Ctrl+"+_("equal")+",Ctrl+Maj+T,Ctrl+Maj+B,Ctrl+Maj+M,Ctrl+Maj+E").split (",")
	kbd_replace=[]
	state_msg_activated=(_("Disabled"),_("Enabled"))
	obj_toolBar = {}

	def __init__(self, appMod) :
		self.appMod= appMod

	def showMenu(self) : 
		o, mainMenu =clientObject.ElementFromHandle (api.getForegroundObject ().windowHandle).FindAll (TreeScope_Children,clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_ToolBarControlTypeId )),Menu ()
		for e in range (1,o.Length):
			element = o.GetElement (e)
			role=utis.getElementWalker (element,7).GetCurrentPropertyValue (UIA_ControlTypePropertyId) 
			if role ==UIA_ButtonControlTypeId :mainMenu.AppendSubMenu (self.getSubMenuForToolBar1(element),_("TB Mail Toolbar"))
			elif role == UIA_ComboBoxControlTypeId  : mainMenu.AppendSubMenu (self.getSubMenuForToolBar2 (element),_("Text formatting"))
			else:continue
			self.obj_toolBar[role]=element
		mainMenu.Bind (EVT_MENU,self.onMenuForToolBar )
		#if gesture :showNVDAMenu (mainMenu)
		showNVDAMenu (mainMenu)

	def script_execute (self,gesture):  ## ??
		#ci dessous on fait appel au script script_showMenu  afin qu'il crée l'objet obj_toolBAr
		if not self.obj_toolBar:self.script_showMenu(gesture=False)
		kbd= gesture.identifiers[1]
		index =self.kbd_replace.index (kbd[kbd.find (":")+1:])
		if index >5 :index-=1
		self.onMenuForToolBar (index+1,type="scriptKey")

	def onMenuForToolBar (self,evt,type=None):
		evtId =(evt if type =="scriptKey" else (evt.Id))
		if evtId <=5:
			pass
		if  evtId ==100 :return self.onMenu_otherOption  (evt)
		#barre d'outilTB 
		isFirstToolBar =(True if evtId <=5 else False)
		toolBar =self.obj_toolBar[(UIA_ButtonControlTypeId if isFirstToolBar  else UIA_ComboBoxControlTypeId)]
		element = toolBar.FindAll (TreeScope_Children, clientObject.CreateNotCondition (clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_SeparatorControlTypeId ,)))
		#on vérifie la présence de l'addon mark down , et on gère l'ajout d'émoticône
		if element.length ==15 and type =="scriptKey":
			if evtId ==20 : return b() #message( _("l'addon mark down est absent"))
			elif evtId ==21 :evtId =20
		#fin 
		element = element.GetElement ((evtId-1 if isFirstToolBar else evtId-6))
		if bool (element.GetCurrentPropertyValue (UIA_LegacyIAccessibleStatePropertyId )&STATE_SYSTEM_UNAVAILABLE ):
			return message (_("%s unavailable") % element.CurrentName)
		CallAfter (element.GetCurrentPattern (10018 ).QueryInterface (IUIAutomationLegacyIAccessiblePattern).DoDefaultAction )
		if type != "scriptKey" or element.GetCurrentPropertyValue (UIA_ControlTypePropertyId, )!=UIA_ButtonControlTypeId  or utis.getElementWalker (element,7): return 
		#partie appelée par une touche de raccourci 
		name =element.CurrentName
		if evtId in range (11,14):
			name+=_(" Activated, Déactivated").split (",")[bool (element.GetCurrentPropertyValue (UIA_LegacyIAccessibleStatePropertyId )&STATE_SYSTEM_PRESSED)]
		CallAfter (message ,name)

	def getSubMenuForToolBar1 (self,obj):
		menu=Menu ()
		oList= obj.FindAll (TreeScope_Children, clientObject.CreateNotCondition (clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_SeparatorControlTypeId ,)))
		for e in range (oList.Length):
			element =oList.GetElement (e)
			item =MenuItem (menu,e+1,element.CurrentName)  #+"\t%s" % self.kbd[e]
			item.Enable (not element.GetCurrentPropertyValue(UIA_LegacyIAccessibleStatePropertyId )&STATE_SYSTEM_UNAVAILABLE )
			menu.AppendItem (item)
		return  menu

	def getSubMenuForToolBar2 (self,obj):
		menu=Menu ()
		o= obj.FindAll (TreeScope_Children, clientObject.CreateNotCondition (clientObject.CreatePropertyCondition (UIA_ControlTypePropertyId, UIA_SeparatorControlTypeId ,)))
		ran  =range (o.Length)
		ranCount =len (ran)
		for e in ran:
			element =o.GetElement (e)
			name =element.CurrentName
			if not name :name = _("Paragraph,&font").split(",")[e]
			kbd =self.kbd[e+5]
			if ranCount == 15 and e==14 :kbd ="Ctrl+Maj+E"
			item =MenuItem (menu, e+6,name,kind=ITEM_CHECK ) #+"\t%s" % kbd
			item.Enable (not element.GetCurrentPropertyValue(UIA_LegacyIAccessibleStatePropertyId )&STATE_SYSTEM_UNAVAILABLE )
			menu.AppendItem (item)
			#  Rem v 4 : the check() method works only after tehe menu item is appended
			item.Check (element.GetCurrentPropertyValue(UIA_LegacyIAccessibleStatePropertyId )&STATE_SYSTEM_PRESSED )
		return menu
