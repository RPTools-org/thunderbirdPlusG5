# thunderbirdPlusG5/appModules/shared/checkListMenu.py.

import wx
# from gui import guiHelper, nvdaControls
from tones import beep

import addonHandler
addonHandler.initTranslation()

import utis

class StartupDialog(wx.Dialog):

	def __init__(self, parent, title,options):
		super().__init__(parent, title=title)
		# (self)
		self.options = options
		panel = wx.Panel(self)
		
		self.focusLbl  = wx.StaticText(panel, label=getFirstLabel())
		
		self.defaultRadio = wx.RadioButton(panel, label=_("Default (do nothing)"), style=wx.RB_GROUP)
		self.lastMsgRadio = wx.RadioButton(panel, label=_("Last message in message list"))
		self.firstMsgRadio = wx.RadioButton(panel, label=_("First message"))
		self.firstUnreadMsgRadio = wx.RadioButton(panel, label=_("First unread message"))
		self.folderTreeRadio = wx.RadioButton(panel, label=_("Folder tree"))
		
		# check box
		self.focusOnStartupChk = wx.CheckBox(panel, wx.ID_ANY, _("Use this mode when starting Thunderbird"))
		# ok_button = wx.Button(panel, label=_("OK"))
		okButton = wx.Button(panel, id=wx.ID_OK, label="OK")
		okButton.Bind(wx.EVT_BUTTON, self.onOK)

		# Escape Key
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

		# Check the appropriate radio button
		mode = int(self.options.options["messengerWindow"]["focusMode"])
		if mode == 0 :self.defaultRadio.SetValue(True)
		elif mode == 1 :self.lastMsgRadio.SetValue(True)
		elif mode == 2 :self.firstMsgRadio.SetValue(True)
		elif mode == 3 :self.firstUnreadMsgRadio.SetValue(True)
		elif mode == 4 :self.folderTreeRadio.SetValue(True)

		self.focusOnStartupChk.SetValue(self.options.options["messengerWindow"]["focusOnStartup"])


		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.focusLbl, 0, wx.EXPAND | wx.ALL, 5)
		self.sizer.Add(self.defaultRadio, 0, wx.ALL, 5)
		self.sizer.Add(self.lastMsgRadio, 0, wx.ALL, 5)
		self.sizer.Add(self.firstMsgRadio, 0, wx.ALL, 5)
		self.sizer.Add(self.firstUnreadMsgRadio, 0, wx.ALL, 5)
		self.sizer.Add(self.folderTreeRadio, 0, wx.ALL, 5)
		self.sizer.Add(self.focusOnStartupChk, 0, wx.ALL, 5)
		self.sizer.Add(okButton, 0, wx.ALL | wx.CENTER, 5)
		
		panel.SetSizer(self.sizer)
		panel.SetSizer(self.sizer)
		self.sizer.Fit(self)
		
	def onOK(self, event):
		if self.defaultRadio.GetValue() : mode = "0"
		elif self.lastMsgRadio.GetValue() : mode = "1"
		elif self.firstMsgRadio.GetValue() : mode = "2"
		elif self.firstUnreadMsgRadio.GetValue() : mode = "3"
		elif self.folderTreeRadio.GetValue() : mode = "4"
		self.options.options["messengerWindow"]["focusMode"] = int(mode)
		self.options.options["messengerWindow"]["focusOnStartup"] = self.focusOnStartupChk.GetValue()
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
	lbl = _("With the {} key in the main window or Space in the folder tree, bring the &focus to:") 
	return lbl.format(key)
	
