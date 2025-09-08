# thunderbirdPlusG5/appModules/shared/checkListMenu.py.

import wx
# from gui import guiHelper, nvdaControls
from tones import beep

import addonHandler

import utis

addonHandler.initTranslation()

class StartupDialog(wx.Dialog):

	def __init__(self, parent, title,options):
		super().__init__(parent, title=title)
		# (self)
		self.options = options
		panel = wx.Panel(self)

		startupActions = [
			_("Do not change focus"),
			_("Apply options below"),
			_("Show All inboxes menu"),
			_("Show all unread inboxes menu"),
_("Show All unread folders menu"),
			_("Show all folders menu"),		]
		self.onStartupLbl  = wx.StaticText(panel, label=_("On Thunderbird startup"))
		self.onStartupChoice = wx.Choice(panel, choices=startupActions)
		vSizer1 = wx.BoxSizer(wx.VERTICAL)
		vSizer1.Add(self.onStartupLbl, 0, wx.EXPAND | wx.ALL, 5)
		vSizer1.Add(self.onStartupChoice, 0, wx.EXPAND | wx.ALL, 5)
		# focus modes
		focusModes = [		
			_("Default (do nothing)"),
			_("Last message in message list"),
			_("First message"),
			_("First unread message"),
			_("Folder tree"),
		]
		self.focusModesLbl  = wx.StaticText(panel, label=getFirstLabel())
		self.focusModesChoice = wx.Choice(panel, choices=focusModes)
		vSizer2 = wx.BoxSizer(wx.VERTICAL)
		vSizer2.Add(self.focusModesLbl, 0, wx.EXPAND | wx.ALL, 5)
		vSizer2.Add(self.focusModesChoice, 0, wx.EXPAND | wx.ALL, 5)

		# ok_button = wx.Button(panel, label=_("OK"))
		okButton = wx.Button(panel, id=wx.ID_OK, label="OK")
		okButton.Bind(wx.EVT_BUTTON, self.onOK)

		# Escape Key
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
		# preselect actio in the list
		action =  int(self.options.options["messengerWindow"]["onStartupAction"])
		self.onStartupChoice.SetSelection(action)

		mode = int(self.options.options["messengerWindow"]["focusMode"])
		self.focusModesChoice.SetSelection(mode)
		# Main Sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		# onStartup choice
		self.sizer.Add(vSizer1, 0, wx.EXPAND | wx.ALL, 10)
		self.sizer.Add(vSizer2, 0, wx.EXPAND | wx.ALL, 10)
		self.sizer.Add(okButton, 0, wx.ALL | wx.CENTER, 5)

		panel.SetSizer(self.sizer)
		panel.SetSizer(self.sizer)
		self.sizer.Fit(self)

		self.onStartupChoice.SetFocus()
		
	def onOK(self, event):
		self.options.options["messengerWindow"]["onStartupAction"] = self.onStartupChoice.GetSelection()
		self.options.options["messengerWindow"]["focusMode"] = self.focusModesChoice.GetSelection()
		self.options.options.write()
		# self.Close()
		return self.Destroy()


	def onKey(self, event):
		kc =  event.GetKeyCode()
		if kc == wx.WXK_RETURN :
			obj = str(event.GetEventObject())
			if ".RadioButton " in obj :
				wx.CallAfter(self.onOK, event)
		elif kc == wx.WXK_ESCAPE:
			self.Destroy()
		else : 
			event.Skip()

def getFirstLabel() :
	key = utis.gestureFromScanCode(41, "") 
	key = '"' + key + '"'
	lbl = _("On startup or   With the {} key in the main window, bring the &focus to:") 
	return lbl.format(key)
	
