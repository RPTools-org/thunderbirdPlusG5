#-*- coding:utf-8 -*
# Thunderbird+ G5

import api
from time import sleep
from NVDAObjects.IAccessible import IAccessible
from ui import message, browseableMessage
import speech
import controlTypes
from wx import CallAfter, Menu, EVT_MENU
from core import  callLater
import winUser
import 	addonHandler,  os, sys
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
		self.bindGestures({"kb:space":"ftiNextUnread", "kb:control+enter":"menuUnread", "kb:enter":"menuFolders", "kb:shift+enter":"menuAllFolders", "kb:shift+control+enter":"menuAllUnread"})
		self.bindGesture ("kb:nvda+upArrow", "sayFolderName") 
	# version g5
	# def showAccountMenu(self, ty=1) :
		# o = fGetAccountNode(self)
		# if not o : beep(100, 15) ; return
		# # __init__(self, startNode, unread=False, recurs=True, type=0, allFolders=False) :
		# m = FolderMenu(o.parent, unread=False, recurs=False, type=ty)
		# callLater(10, m.showMenu, title="")

		
	def script_sayFolderName(self, gesture):
		nm = self.name
		o = fGetAccountNode(self)
		if o :
			nm += ", " + o.name 
		message(nm)

	def script_ftiNextUnread(self, gesture) :
		# CallAfter(KeyboardInputGesture.fromName ("n").send )
		utils.getThreadTreeFromFG(focus=True, nextGesture="n")
	script_ftiNextUnread.__doc__ = _("selects the first unread message in the list from the folder tree.")
	script_ftiNextUnread.category = sharedVars.scriptCategory
	# version g5
	def script_menuFolders(self, gesture) :
		fMenuFolders(self, unread=False)
	script_menuFolders.__doc__ = _("Folders : displays a menu allowing you to reach a subfolder of your choice.")
	script_menuFolders.category = sharedVars.scriptCategory
	
	def script_menuUnread(self, gesture) :
		fMenuFolders(self, unread=True)
	script_menuUnread.__doc__ = _("Folders : displays a menu allowing you to reach an unread folder of the current account.")
	script_menuUnread.category = sharedVars.scriptCategory

	def script_menuAllFolders(self, gesture) :
		o = fGetAccountNode(self)
		if not o : beep(100, 15) ; return
		m = FolderMenu(o.parent, unread=False, recurs=True, allFolders=True)
		callLater(10, m.showMenu,title="All Folders, menu")
	script_menuAllFolders.__doc__ = _("Folders : display a menu  of all accounts and folders.")
	script_menuAllFolders.category = sharedVars.scriptCategory

	def script_menuAllUnread(self, gesture) :
		o = fGetAccountNode(self)
		if not o : return
		m = FolderMenu(o.parent, unread=True, recurs=True, allFolders=True)
		callLater(10, m.showMenu,title="All Folders, menu")
	script_menuAllUnread.__doc__ = _("Folders : display a menu of all unread accounts and folders.")
	script_menuAllUnread.category = sharedVars.scriptCategory


# functions version 5
def fMenuFolders(o, unread=False) :
	if not utils.hasID(o, "all-") : return message(_("The folder tree is not in All folders mode"))
	o = fGetAccountNode(o)
	nm = str(o.name) 
	m = FolderMenu(o, unread)
	callLater(10, m.showMenu, title=nm)
def fGetAccountNode(oNode) :
	o = oNode
	lvl = ""
	while o :
		if o.role == controlTypes.Role.TREEVIEWITEM :
			lvl = str(utils.getIA2Attr(o, False, "level"))
			if lvl == "2" :
				return o
		o = o.parent
	return None
	

def showAccountMenu(oNode, ty=1) :
	o = fGetAccountNode(oNode)
	if not o : beep(100, 15) ; return
	# __init__(self, startNode, unread=False, recurs=True, type=0, allFolders=False) :
	m = FolderMenu(o.parent, unread=False, recurs=False, type=ty)
	callLater(10, m.showMenu, title="")

from utis import showNVDAMenu
class FolderMenu() :
	def __init__(self, startNode, unread=False, recurs=True, type=0, allFolders=False) :
		self.fti = startNode
		self.unread = unread
		self.recurs = recurs
		self.all = allFolders
		self.type = type # 0=normal, 1=accounts, 2= accounts that will display unread folders 
		self.idx = 0
		self.account = ""
		# self.excluded = str(_("Drafts|Deleted") + "|-, ").split("|")
		self.fMenu = None

	def buildMenu(self, o) :
		o = o.firstChild
		if o.role == controlTypes.Role.TEXTFRAME : 
			o = o.next.firstChild
			# sharedVars.log(o, "Is TreeviewItem? ")

		
		while o :
			hasChildren = (int(o.childCount) > 0)
			coll = ""
			if o.role == controlTypes.Role.TREEVIEWITEM :
				nm = o.name
				if self.all :  
					lvl = str(utils.getIA2Attr(o, False, "level"))
					if lvl == "2" : 
						if self.unread and nm.endswith("-") : o = o.next ; continue 
						self.account = " (" + nm + ") "
						beep(357, 3)
				OK = True 
				if controlTypes.State.COLLAPSED  in o.states : coll = ", " + _("Collapsed")
				if self.unread :
					if not gRegUnread.search(nm) or gRegExcludeFolders.search(nm) or nm.endswith("-") : OK = False
				if OK and o.name :
					self.fMenu.Append (self.idx, o.name + self.account + coll)
					self.nodes.append(o)
					# sharedVars.logte(str(self.idx) + ", " + o.name + ", node ptr" + str(self.nodes[self.idx]))
					self.idx +=1
			if self.recurs and hasChildren and not coll :
				self.buildMenu(o)
			o = o.next
		return

	def debugMenu(self) :
		beep(600, 50)
		# sharedVars.debugLog = ""
		sharedVars.logte("menu items count {}, nodes count {}".format(self.fMenu.MenuItemCount, len(self.nodes))) 
		litems = self.fMenu.GetMenuItems()
		for i in  range(0, self.fMenu.MenuItemCount) :
			sharedVars.logte(str(i) + ": " + str(self.fMenu.GetLabel(i)) + ", ptr=" + str(self.nodes[i])[:10])

	
	def showMenu(self, title="") :
		self.fMenu = Menu()
		self.nodes = []
		sharedVars.objLooping = True
		# sharedVars.debugLog ="buildMenu\n"
		# sharedVars.log(self.fti, "Before Buildmenu, startNode")
		# sharedVars.log(self.fti.firstChild, "FirstChild of startNode")
		# sharedVars.log(self.fti.getChild(1), "Second Child of startNode")
		
		# if startNode  is collapsed, we must expande it
		if controlTypes.State.COLLAPSED in self.fti.states :
			self.fti.doAction()
			KeyboardInputGesture.fromName("rightArrow").send()
			sleep(.1)
		self.buildMenu(self.fti)
		# sharedVars.log(self.fti, "len self.nodes=" + str(len(self.nodes)))
		sharedVars.objLooping = False
		# Add special menu item in normal menu 
		if self.type == 0 :
			if self.unread : 
				self.fMenu.Append (self.idx, "& > " + _("Choose an account with unread"))
				self.nodes.append(2)
			else : 
				self.fMenu.Append (self.idx, "& > " +  _("Choose an account"))
				self.nodes.append(1)
		# if len(self.nodes) :
		self.fMenu.Bind (EVT_MENU,self.onMenu)
		# self.debugMenu()
		callLater(50, self.sayMenuTitle, self.unread, title)
		utis.showNVDAMenu  (self.fMenu)
		# else : message(_("No unread folders for this account."))
	
	def onMenu(self, evt):
		if str(self.nodes[evt.Id]).startswith("<NVDAObject") :   # pointer, not accounts menu
			o = self.nodes[evt.Id]
			if self.type == 0 : # regular menu item
				# beep(100, 30)
				o.doAction()
				o.scrollIntoView()
				o.setFocus()
				if controlTypes.State.COLLAPSED  in o.states :
					CallAfter(KeyboardInputGesture.fromName("rightArrow").send)
			elif self.type == 1 : # request to display folders of the choosed  account 
				# beep(250, 40)
				fMenuFolderFromAccount(o , False)
			elif self.type == 2 : # request to display unread folders of the choosed  account 
				# beep(440, 40)
				fMenuFolderFromAccount(o , True)
		else : # request to display the mail accounts menu
			# t = 1 if self.nodes[evt.Id] == 9997 else 2
			# sharedVars.log(self.fti, "self.fti=")
			showAccountMenu(self.fti, self.nodes[evt.Id])

			
	def sayMenuTitle(self, unread, accountName) :
		speech.cancelSpeech()
		if self.type == 1 :
			return message(_("Accounts, menu"))
		elif self.type == 2 :
			return message(_("Accounts with unread, menu"))
		# folder menu
		if unread :
			msg = _("Menu, Unread folders of") + accountName
		else :			
			msg = _("Menu, folders of ") + accountName
		message(msg)
		
def fMenuAccounts(type=1) :
	o = utils.getFolderTreeFromFG()
	if not o : return beep(100, 30)
	# get the first item
	# level 6,       1 of 1, Role.TREEVIEW, IA2ID : folderTree 
	# level 7,        0 of 0, Role.TREEVIEWITEM Tag: li, 
	# level 8,         0 of 0, Role.GROUPING Tag: ul, 
	# level 9,          0 of 10, name : RPTools, Role.TREEVIEWITEM, IA2ID : all-bWFpbGJveDovL3Bsci5saXN0ZXMlNDBycHRvb2xzLm9yZ0Bwb3AzLnJwdG9vbHMub3Jn Tag: li
	try : o = o.firstChild.firstChild.firstChild
	except : return beep(100, 30)
	if not utils.hasID(o, "all-") : return message(_("The folder tree is not in All folders mode"))
	# __init__(self, startNode, unread=False, recurs=True, type=0, allFolders=False) :
	# type = 1 : read and unread, type = 2 : unread only
	m = FolderMenu(o.parent, False,  False, type, False)
	callLater(10, m.showMenu)

def fMenuFolderFromAccount(accountNode, unrd=False) :
	speech.cancelSpeech()
	# __init__(self, startNode, unread=False, recurs=True, type=0, allFolders=False) 
	m = FolderMenu(startNode=accountNode, unread=unrd,recurs=True, type=0)
	callLater(10, m.showMenu, title=accountNode.name)
