#-*- coding:utf-8 -*
# Thunderbird+ 4.x
import sys
import addonHandler
addonHandler.initTranslation()
import api
import speech 
# from winsound import MessageBeep 
from tones import beep
import os
# _curAddon=addonHandler.getCodeAddon()
# sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
# sys.path.append(sharedPath)
import  utis, sharedVars, utils115 as utils
from utis import getIA2Attribute, showNVDAMenu , TBMajor # ,  getElementWalker
from utils115 import message
# del sys.path[-1]
from time import sleep
from keyboardHandler import KeyboardInputGesture, passNextKeyThrough
import controlTypes,wx
from gui import mainFrame
from wx import CallAfter, CallLater,Menu,MenuItem,ITEM_CHECK,EVT_MENU
# from NVDAObjects.IAccessible import IAccessible
import winUser

class ComposeMenu():
	def __init__(self, appModule=None):
		self.oToolbar = None
		self.formatMenu = None
		self.pointers =[] 
		self.lastIndex = -1

	def showMenu(self): 
		self.buildFormatMenu()

	def buildFormatMenu(self):
		if not self.oToolbar:
			# level 2,   1 of 3, Role.TOOLBAR, IA2ID: FormatToolbar Tag: toolbar, States: , childCount: 20
			# IA2ID = composeContentBox in , Role.SECTION
			fg =  api.getForegroundObject()
			o = utils.getChildByRoleIDName(fg, controlTypes.Role.SECTION, ID="composeContentBox", name="", idx=11)
			# IA2ID = FormatToolbar in , Role.TOOLBAR
			if o is not None: self.oToolbar = utils.getChildByRoleIDName(o, controlTypes.Role.TOOLBAR, ID="FormatToolbar", name="", idx=1)
			if not self.oToolbar:
				return beep(100, 30)
		# buttons and comboboxes in the toolbar
		o =  self.oToolbar.firstChild
		if o is None: 
			return

		self.		formatMenu = wx.Menu()
		self.pointers = []
		idx = 0 # index
		while o is not None:
			role = o.role
			if o.keyboardShortcut:
				shortcut = ", " + str(o.keyboardShortcut)
			else:
				shortcut = ""
			itemName = ""
			if role == controlTypes.Role.BUTTON:
				itemName = "{0}, {1} {2}".format(o.name, role.displayString, shortcut)
			elif  role == controlTypes.Role.TOGGLEBUTTON:
				state = controlTypes.State.PRESSED.displayString if controlTypes.State.PRESSED in o.states else ""
				itemName = "{0}, {1} {2}{3}".format(o.name, role.displayString, state, shortcut)
			elif  role == controlTypes.Role.COMBOBOX:
				itemName = "{0}, {1} {2}{3}".format(o.name, role.displayString, o.value, shortcut)
			if itemName:
				self.formatMenu.Append(idx, itemName)
				self.pointers.append(o) 
				idx += 1
			o = o.next
		# end of while
		self.formatMenu.Bind(wx.EVT_MENU, self.onFormatMenu)
		# if self.lastIndex > 0:
		utis.showNVDAMenu  (self.formatMenu)

	def onFormatMenu(self, evt):
		o = self.pointers[evt.Id]
		if o is None:
			return
		self.lastIndex = evt.Id  # for future preselection
		role = o.role
		if role == controlTypes.Role.BUTTON:
			CallLater(50, self.activateControl, o)
		elif  role == controlTypes.Role.TOGGLEBUTTON:
			CallLater(50, self.activateControl, o, redisplayMenu=True)
		elif  role == controlTypes.Role.COMBOBOX:
			CallLater(50, self.activateControl, o)
			
		# CallAfter(o.doAction)
		# self.showMenu()

	def activateControl(self, obj, redisplayMenu=False): 
		# speech.cancelSpeech()
		obj.doAction()