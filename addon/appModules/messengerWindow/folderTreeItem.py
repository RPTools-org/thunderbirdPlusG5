#-*- coding:utf-8 -*
# Thunderbird+ G5

import api
from time import sleep
from NVDAObjects.IAccessible import IAccessible
from ui import message, browseableMessage
import speech
import controlTypes
from wx import CallAfter, CallLater, Menu, EVT_MENU
import winUser
import addonHandler,  os, sys
from keyboardHandler import KeyboardInputGesture
from tones import  beep
_curAddon=addonHandler.getCodeAddon()
sharedPath=os.path.join(_curAddon.path,"AppModules", "shared")
sys.path.append(sharedPath)
import  utis, sharedVars, utils115 as utils
del sys.path[-1]
addonHandler.initTranslation()

from re import  compile,IGNORECASE
gRegExcludeFolders =compile (_("Drafts|Deleted") + "|\-, \d")
gRegUnread = compile (", \d+")

lastSearch = ""


class FolderTreeItem (IAccessible):
	oLastNav = None
	spacePressed = False

	def initOverlayClass (self):
		# if not sharedVars.FTnoSpace : 
		self.bindGestures({"kb:space":"ftiNextUnread", "kb:control+enter":"menuUnread", "kb:enter":"menuSiblings"})
		self.bindGesture ("kb:nvda+upArrow", "sayFolderName") 
	# version g5
	def script_sayFolderName(self, gesture):
		speech.speakText(self.name)

	def script_ftiNextUnread(self, gesture) :
		# CallAfter(KeyboardInputGesture.fromName ("n").send )
		utils.getThreadTreeFromFG(focus=True, nextGesture="n")
	script_ftiNextUnread.__doc__ = _("selects the first unread message in the list from the folder tree.")
	script_ftiNextUnread.category = sharedVars.scriptCategory
	# version g5
	def script_menuSiblings(self, gesture) :
		menuFolders(self, unread=False)
	script_menuSiblings.__doc__ = _("Folders : displays a menu allowing you to reach a subfolder of your choice.")
	script_menuSiblings.category = sharedVars.scriptCategory
	
	def script_menuUnread(self, gesture) :
		menuFolders(self, unread=True)
	script_menuUnread.__doc__ = _("Folders : displays a menu allowing you to reach an unread subfolder of your choice.")
	script_menuUnread.category = sharedVars.scriptCategory

# functions version 5
def menuFolders(o, unread=False) :
	# msg = "Subfolders"
	# CallAfter(message, msg)
	if not utils.hasID(o, "all-") : return speech.speakText(_("The folder tree is not in All folders mode"))
	m = FolderMenu(o)
	m.showMenu(unread)
	
from utis import showNVDAMenu
class FolderMenu() :
	def __init__(self, startFTI) :
		self.fti = startFTI
		self.ptrs = []

	def showMenu(self, unread = False) :
		folderMenu = Menu()
		i = 0
		# parent of self.fti
		o = self.fti.parent.parent
		parName = ""
		if o.name :
			parName = str(o.name)
			nm = _("1: Go back to") + " : " + parName
			folderMenu.Append (0, nm)
			self.ptrs.append(o)
			i += 1
		# siblings of fti
		o = self.fti.parent.firstChild
		while o :
			nm = o.name
			Excluded = gRegExcludeFolders.findall(nm)
			sharedVars.tlog("excluded=" + str(Excluded) + ", " + nm)
			included = (len(gRegExcludeFolders.findall(nm)) == 0)
			if not unread or (unread and gRegUnread.findall(nm) and included) :
				folderMenu.Append (i, nm)
				self.ptrs.append(o)
				i += 1
			o = o.next 
		if len(self.ptrs) :
			folderMenu.Bind (EVT_MENU,self.onMenu)
			CallLater(50, self.sayMenuTitle, unread, parName)
			utis.showNVDAMenu  (folderMenu)
		else : message(_("No unread folders at this level."))
	
	def onMenu(self, evt):
		# idx = evt.Id
		o = self.ptrs[evt.Id]
		o.doAction()
		o.scrollIntoView()
		o.setFocus()
		
	def sayMenuTitle(self, unread, name) :
		speech.cancelSpeech()
		if not name :
			return speech.speakText(_("Accounts, menu"))
		
		if unread :
			msg = _("Menu, Unread subfolders of") + name
		else :			
			msg = _("Menu, Subfolders of ") + name
		speech.speakText(msg)
		
def menuAccounts() :
	o = utils.getFolderTreeFromFG()
	if not o : return beep(100, 30)
	# get the first item
	# level 6,       1 of 1, Role.TREEVIEW, IA2ID : folderTree 
	# level 7,        0 of 0, Role.TREEVIEWITEM Tag: li, 
	# level 8,         0 of 0, Role.GROUPING Tag: ul, 
	# level 9,          0 of 10, name : RPTools, Role.TREEVIEWITEM, IA2ID : all-bWFpbGJveDovL3Bsci5saXN0ZXMlNDBycHRvb2xzLm9yZ0Bwb3AzLnJwdG9vbHMub3Jn Tag: li
	try : o = o.firstChild.firstChild.firstChild
	except : return beep(100, 30)
	if not utils.hasID(o, "all-") : return speech.speakText(_("The folder tree is not in All folders mode"))
	m = FolderMenu(o)
	m.showMenu(False)
