# thunderbirdPlusG5/appModules/shared/checkListMenu.py.
# Written by Abdelkrimt  ALIAS  Abdel
import wx
from gui import guiHelper, nvdaControls
from tones import beep

import addonHandler
addonHandler.initTranslation()

class CheckListMenu(wx.Dialog):

	def __init__(self, parent, title, frame, options, fakeRadioGroups=None, postFunction=None):
		super().__init__(parent, title=title)
		self.frame = frame
		self.options = options
		self.fakeRadioGroups = fakeRadioGroups 
		self.postFunc = postFunction
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)
		# Voici les éléments qui feront partie des cases à cocher.
		self._elements = list(getattr(options, "option_%s" % frame).values())
		self.choicesBox = sHelper.addLabeledControl(
			_("List of choices"),
			nvdaControls.CustomCheckListBox,
			choices = self._elements
		)
		# On défini quels seront les items qui seront cochés par défaut.
		checkedItems = []
		self.keys = list(getattr(options, "option_%s" % frame).keys())
		for key in self.keys:
			if key in options.options[frame] and options.options[frame].as_bool(key):
				checkedItems.append(self.keys.index(key))

		self.choicesBox.Checked = [
			index for index in range(len(self._elements)) if index in checkedItems
		]
		# On sélectionne par défaut le premier élément de la liste de cases à cocher.
		self.choicesBox.Select(0)
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		# Événement du clic sur le bouton OK.
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.choicesBox.SetFocus()

	def onOk(self, evt):
		#  self.frame is the section name in the ini file
		choices = self.choicesBox.CheckedItems
		if self.fakeRadioGroups : # list of tuples with indexes 
			for tuple in self.fakeRadioGroups : 
				lChecked = []
				for t in tuple :
					if t in choices : lChecked.append(t)
					if len(lChecked) > 1 : 
						self.choicesBox.Select(t)
						self.choicesBox.SetFocus()
						return self.displayError(lChecked)

		items = list(range(len(self.keys)))
		for i in items:
			key = self.keys[i]
			if i in choices:
				self.options.options[self.frame][key] = True
			else:
				self.options.options[self.frame][key] = False
		self.options.options.write()
		if self.postFunc :
			self.postFunc(self.frame)
		self.Close()

	def displayError(self, lstOptions) :
		from ui import  browseableMessage
		msg = _("The options below cannot be checked at the same time :\n")
		for e in lstOptions :
			msg += self._elements[e] + " ; \n"
		msg += _("Press escape to return to the option list")
		return browseableMessage (message=msg, title=_("Error in two  options - Thunderbird+G5"), isHtml = False)
		