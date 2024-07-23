#-*- coding:utf-8 
# THUNDERBIRDpLUSg5

from scriptHandler import getLastScriptRepeatCount
import speech 
from speech import speak, speakSpelling
from tones  import beep
from NVDAObjects.IAccessible import IAccessible
import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
from keyboardHandler import KeyboardInputGesture
from ui import message
from api import copyToClip, getForegroundObject,   processPendingEvents
from wx import CallAfter, CallLater
import addonHandler,  os, sys
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, sharedVars 
del sys.path[-1]
addonHandler.initTranslation()

lastWord=None
newWord=None

class SpellCheckDlg (IAccessible):
	def initOverlayClass (self):
		role =self.role
		id =(self.IA2Attributes["id"] if hasattr (self,"IA2Attributes") and "id" in self.IA2Attributes else None)
		if role == controlTypes.Role.EDITABLETEXT :
			#beep(150, 30)
			# if _("None") in self.parent.getChild (1).name :
				# message(_("No misspelled words were found"))
			#self.name = ""

			self.bindGestures ({"kb:nvda+tab":"reportFocus","kb:ALT+UPARROW":"reportFocus", "kb:enter":"enterFromEdit", "kb:shift+enter":"enterFromEdit", "kb:control+enter":"enterFromEdit", "kb:control+shift+enter":"enterFromEdit", "kb:alt+enter":"enterFromEdit", "kb:alt+i":"altLetter", "kb:alt+n":"altLetter", "kb:alt+r":"altLetter", "kb:alt+t":"altLetter", "kb:alt+a":"altLetter"})
		""" elif role == (controlTypes.Role.LISTITEM if hasattr(controlTypes, "Role") else controlTypes.ROLE_LISTITEM) and not self.previous :self.keyboardShortcut =self.container.keyboardShortcut """

	def event_gainFocus (self):
		if self.role == controlTypes.Role.EDITABLETEXT :
			self.sayWords()
		super (SpellCheckDlg,self).event_gainFocus ()

	def script_enterFromEdit (self,gesture):
		# self is the editable text field 
		speech.cancelSpeech()
		if "control" in gesture.modifierNames : # Ignore orAll or Ignore 
			if "shift" in gesture.modifierNames : # Ignore orAll or Ignore 
				self.pressButton ("ignoreAll")
			else :
				self.pressButton ("ignore")
		elif "alt" in gesture.modifierNames :
			self.pressButton("addtodictionary")
		else : # no modifiers replaceAll or replace			
			if "shift" in  gesture.modifierNames : 
				self.pressButton ("replaceAll")
			else :
				self.pressButton ("replace")
		self.sayWords()
	script_enterFromEdit.__doc__ = u"gère différentes combinaisons autour de Enter pour simuler les boutons de correction"

	def sayWords(self) :
		#global lastWord, newWord
		#newWord=self.parent.getChild (1).name
		misp = self.parent.getChild (1).name
		if _("Check Spelling ") in misp : return message(_("Spell check complete."))
		spell = sharedVars.oSettings.getOption("msgcomposeWindow", "spellWords")
		replace= self.value
		if replace :
			#if lastWord != newWord : message ("Mispelled word : %s" % misp)
			message (_("Misspelled word: %s") % misp)
			if spell: speakSpelling (misp)
			#if  lastWord != newWord : message ("Remplacer par : %s" % replace)
			message(_("Replace with: %s") % replace)
			if spell : speakSpelling (replace)
		else :
			message(_("Misspelled word : %s, no suggestion.") % misp)
		#lastWord = newWord

	def script_altLetter (self, gesture) :
		# beep (500, 50)
		mk = gesture.mainKeyName
		# mk letters : language dependant
		if mk == _("i") : btn = "ignore"
		elif mk  == _("l") : btn = "ignoreAll"
		elif mk == _("d") : btn = "addtodictionary"
		elif mk == _("a") : btn = "replaceAll"
		elif mk == _("r") : btn = "replace"
		self.pressButton (btn, sayMisp=True)
		# v3 & v2.1.1 announcement of the following mispelled word if not None
		#self.sayWords1 ()

	def pressButton (self, btnID, sayMisp=False) :
		oDlg = self.parent # v3 TB 91
		#oDlg.parent.name = ""
		#message ("oDlg role :" + str(oDlg.role) + ", name : "+ str(oDlg.name))
		o = oDlg.firstChild
		btnID = btnID.lower()
		obj = None
		while o :
			if o.role == controlTypes.Role.BUTTON : # button
				ID = (o.IA2Attributes["id"] if hasattr (o,"IA2Attributes") and "id" in o.IA2Attributes else False)
				if  ID :
					ID = ID.lower ()
					if ID == btnID :
						obj = o
						break
			o = o.next
		if not obj : return False
		#cmdVol = #speech.VolumeCommand
		#cmdVol(0.4)
		message (obj.name)
		#cmdVol(1)
		obj.doAction ()
			# added 2022-08-09
		if sayMisp  : # 2022-08-09
			# self.script_reportFocus(None)
			self.sayWords()

	def script_reportFocus (self,gesture):
		c = getLastScriptRepeatCount () 
		misp = self.parent.getChild (1).name
		message(misp)
		if c == 2 :
			#speak ([u"Mot mal orthographié : " + misp])
			speak ([(_("replaced, {0} . by . {1}")).format((" . ").join (list (self.parent.getChild(1).name)), (" . ").join (list (self.value)))],symbolLevel  =0)
		elif c == 0 :
			a = _("Replace : ") + misp + " : "
			message  (a)
			speakSpelling (misp)
			a = _(" with : ") + self.value + " : "
			message  (a)
			speakSpelling (self.value)
		elif c == 1 :
			if not sharedVars.oQuoteNav : sharedVars.initQuoteNav()
			sharedVars.oQuoteNav.setDoc(sharedVars.oEditing, nav=True, fromSpellCheck=True)
			sharedVars.oQuoteNav.setText(0) # speakMode=0 silent
			sharedVars.oQuoteNav.findItem(misp)
		# else :
			# copyToClip (misp)
			# message(misp + _(", copied to clipboard"))
	script_reportFocus.__doc__ = u"Lire ou épeler le mot mal orthographié et le mot proposé par NVDA+Tab"

