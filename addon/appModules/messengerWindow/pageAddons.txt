#-*- coding:utf-8 -*

from api import processPendingEvents
import winUser
from time import sleep
from speech import cancelSpeech
from NVDAObjects.IAccessible import IAccessible
from ui import message
import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import globalVars
from wx import CallLater
import addonHandler,  os, sys
from keyboardHandler import KeyboardInputGesture
from tones import  beep
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, sharedVars
del sys.path[-1]
addonHandler.initTranslation()


class AddonsPage(IAccessible):

	def initOverlayClass (self):
		try : role =self.role
		except : return
		# implémenter sur role=8 dont le nom est Rechercher sur addons.thunderbird : touche ebtrée   pour activer nouvel onglet résultats de recherche.
		if role == controlTypes.Role.EDITABLETEXT :
			if "addons.thunderbird" in str(self.name) :
				self.bindGestures({"kb:enter":"goTabAddons"})

	def script_goTabAddons(self, gesture) :
		sharedVars.objLooping = True  # reset to False in trackResults()
		# beep(440, 20)
		# message(u"Recherche de module pour  : " + self.value + ", Patientez ...") 
		# gesture.send()
		# TB 91 : CallLater(100, trackResult, str(self.value) + " :: Recherche") # tracks the fralme which the name contains the expression. 
		# translator : in TB 102, tab name   that will open is  : Recherche :: Modules
		trackText = _("Search :: Add-ons")
		# if sharedVars.debug : sharedVars.log(None, "avant appel trackResult")
		CallLater(20, trackResult, trackText) 
		gesture.send()

	# __gestures={
	# "kb:f12":"goTop",
	# }


# normal functions
oFound = None

def trackResult(name) :
	global oFound

	hwFG = winUser.getForegroundWindow()
	title = winUser.getWindowText(hwFG)
	if name not in str(title) :
		return CallLater(100, trackResult, name)
	# beep(440, 60)
	utis.sendKey("tab", 5, 0.5) 
	processPendingEvents()
	try : # finally
		sharedVars.objLooping = True
		oFound = None
		fo = globalVars.focusObject
		while fo :
			if fo.role == controlTypes.Role.DOCUMENT :
				oFound = fo
				break
			fo = fo.parent
		if not oFound : return
		if oFound.role == controlTypes.Role.DOCUMENT :
			fo = oFound
			oFound = None
			sharedVars.debugLog = ""
			if sharedVars.debug : sharedVars.log(fo, "avant recurserfindID", False)
			recurseFindID(fo, "pjax-results") # "page")
			if sharedVars.debug : sharedVars.log(fo, "P jax Result ? ", False)
			#  after i0, role-SECTION=86, , IA2ID : pjax-results :  i1, role-SECTION=86,  | i0, role-SECTION=86,  | i0, role-HEADING=40,  , 
			fo = oFound
			oFound =  None
			recurseFindTag(fo, "h3"), 
			if sharedVars.debug : sharedVars.log(oFound, " apres recurseFindTag ", False)
			if u"Trier par" in oFound.name :
				fo = oFound.parent.next
				oFound = None
				recurseFindTag(fo, "h3"), 
				if sharedVars.debug : sharedVars.log(oFound, " Apres Second recurseFindTag ", False)
			if oFound :
				oFound.firstChild.setFocus()
				cancelSpeech()
				message(oFound.name)
	finally :
		sharedVars.objLooping = False

def recurseFindID(o, searchID) :
	global oFound
	#beep(740, 2)
	o = o.firstChild
	while o :
		ID = utis.getIA2Attribute(o)
		#if ID :
			#sharedVars.debugLog += "ID={0}, role={1}".format(ID, o.role) + "\n"
		if ID and str(ID) == searchID :
			oFound = o
			break
		if hasChildren(o)  :
			oFound = recurseFindID(o, searchID)
			if oFound : return oFound
		o = o.next
	if oFound :   return oFound
	return None

def recurseFindTag(oParent, searchTag) :
	global oFound
	#beep(740, 2)
	o = oParent.firstChild
	while o :
		tag = utis.getIA2Attribute(o, False, "tag")
		#if tag :
			#sharedVars.debugLog += "tag={0}, role={1}".format(tag, o.role) + "\n"
		if str(tag) == searchTag :
			oFound = o
			break
		if hasChildren(o)  :
			recurseFindTag(o, searchTag)
			if oFound : return oFound
		o = o.next
	if oFound : return oFound
	return None

def hasChildren(obj) :
	try :
		obj = obj.firstChild
		return (True if obj else False)
	except :
		return False

def findObjectByRole(o, role) :
	if not hasChildren(o) : return None
	o = o.firstChild
	while o :
		if o.role ==role :
			return o
		o = o.next
	return None

def getChild(o, idx) :
	if sharedVars.debug : sharedVars.log(o, u" entrée ", False)
	if not hasChildren(o) : return None
	o = o.getChild(idx)
	if sharedVars.debug : sharedVars.log(o, u" sortie ", False)
	return o
