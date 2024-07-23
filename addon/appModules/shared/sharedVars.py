#-*- coding:utf-8 -*
debug = False
TBMajor = 0
objLooping = False
speechOff = False
gTimer = None
lastKey = ""
oCurFrame = None
groupingIdx = 25 # index of child object of role grouping in the foregroundObject children  
curFrame = curWinTitle = ""
curTab = "init2"
curTTRow = ""  # current thread tree row
oQuoteNav = None
oEditing = None
msgOpened = False
prevObj = ""
chichi = None
menuCommands = {} # parallel to some menu items
# FTnoNavLetter =FTnoSpace = TTnoSpace = TTnoFilterBar = False
lockEditMenu = None
scriptCategory = "Thunderbird+G5"
virtualSpellChk = False
delayFocusDoc = 20
testMode = False
debugLog = ""

import quoteNav
def initQuoteNav() :
	global oQuoteNav
	oQuoteNav = quoteNav.QuoteNav()
import inspect
oSettings = None # options menu
import menuSettings
import controlTypes
import globalVars
from ui import message

def initSettingsMenu(appMod) :
	global oSettings
	oSettings = menuSettings.Settings(appMod)

def setLooping(value) :
	global objLooping, debug, debugLog
	objLooping = value
	if not debug : return
	lastFunction = inspect.stack()[1][3]
	debugLog = debugLog + "setLooping fonction :{0}, valeur : {1}".format(lastFunction, str(value)) + "\n"

def logte(msg) :
	global debugLog
	debugLog += msg + "\n" 
def getObjAttrs(o) :
	states = " Busy, " if controlTypes.State.BUSY in o.states else " "
	states +=  (" focused, " if hasattr(o, "hasFocus") and o.hasFocus else " ")
	states += (", selected" if controlTypes.State.SELECTED in o.states else "")
	if o.role == controlTypes.Role.TREEVIEWITEM :
		states += (",Collapsed" if controlTypes.State.COLLAPSED in o.states else ", Expanded")

	nm = (o.name if hasattr(o, "name") else "")
	if  not nm : nm =""
	else : nm = "\n  name : " + str(nm )
	val = (o.value if hasattr(o, "value") else "")
	if  not val  : val =""
	else : val = "\n value : " + str(val)
	if hasattr(o, "IA2Attributes") :
		ID = str(o.IA2Attributes.get("id"))
	else : ID = ""
	t =  states + " : {}, ID : {}, class : {}, childCount : {}{}".format(o.role.name, ID, str(o.windowClassName), o.childCount, nm + val)
	return t


def log(o, msg="Objet", withStep=False):
	global debugLog
	if withStep :
		step = "step " + str(globalVars.TBStep) + " "
		curFunc = inspect.stack()[1][3] 
		prevFunc = inspect.stack()[2][3]
		lastFunction = " fonk {0}, {1} : ".format(curFunc, prevFunc)
	else :
		step = lastFunction = ""
	if not o : 
		debugLog = debugLog + step + msg + " : objet None, " + lastFunction + "\n"
		return
	t = getObjAttrs(o)
	debugLog = debugLog + step + lastFunction + msg + t + "\n"

def debugMess(o, msg="Objet") :
	lastFunc = inspect.stack()[1][3]
	foc =  ("focused, " if o.hasFocus else "")
	sel = u"Etat sélectionné" # (", selected" if controlTypes.State.SELECTED in o.states else "non selected")
	# if o.role == controlTypes.TREEVIEWITEM :
	sel += (",Collapsed" if controlTypes.State.COLLAPSED in o.states else ", Expanded")
	nm = str(o.name)
	ID = str(o.IA2Attributes.get("id"))
	t =  foc + sel + " : role : {0}, ID : {1}, childCount : {2}name : {3}".format(o.role.name, ID, o.childCount, nm[:15])
	message(lastFunc + msg + t )
