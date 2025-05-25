# -*- coding: utf-8 -*-
# globalPlugins/ThunderbirdGlob.py
# Thunderbird+G5

import controlTypes
import globalPluginHandler, addonHandler
from scriptHandler import getLastScriptRepeatCount

addonHandler.initTranslation()
ADDON_NAME = addonHandler.getCodeAddon().manifest["name"]
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
ADDON_VERSION = addonHandler.getCodeAddon().manifest["version"]
import api
import ui
import speech
import wx
# from .shared import notif
from .shared import winUtils
from time import time, sleep
import winUser
from winUser import getKeyNameText, setCursorPos 
from tones import beep
import globalVars
import os, sys

def gestureFromScanCode(sc, prefix) :
	# sc stands for the scanCode  of the key
	# prefix is "kb:modifiers"
	k = getKeyNameText(sc, 0)
	return prefix + k

# def setTBOnTop() :
	# hWindow = winUtils.findWindowFromExeName("thunderbird.exe")
	# if hWindow and winUser.getForegroundWindow() != hWindow :
		# winUser.setForegroundWindow(hWindow)
	# else :
		# # beep(250, 5)
		# wx.CallLater(500, setTBOnTop) 


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = ADDON_SUMMARY

	focusNothing = False
	timer = None
	timerStartedAt = 0

	def __init__(self, *args, **kwargs):
		super (GlobalPlugin, self).__init__(*args, **kwargs)
		globalVars.TBPropertyPage = None
		hTaskBar = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
		if not hTaskBar or  globalVars.appArgs.launcher : 
			return
		# if notif.	checkNotif() :
			# beep(440, 30)
			# wx.CallLater(200, notif.showNotif)
		# # else :
			# # wx.CallLater(3000, updateLite.checkUpdate, True) # auto
		scriptDir  = os.path.dirname(os.path.abspath(__file__))
		iniFile =  scriptDir + f"\showChangelog.ini"
		if os.path.exists(iniFile) :
			wx.CallLater(5000, showChangelog) 
			try:
				os.remove(iniFile)
			except FileNotFoundError:
				ui.message("The followingficherd could not be deleted because not found:\n" + iniFile)

	def RestoreSpeechAndSay(msg, focusName=False) :
		if focusName :
			o = api.getFocusObject()
			msg = str(o.name) + ", " + o.role.displayString + ", " + msg 
		if self.prevSpeechMode :
			speech.setSpeechMode(self.TprevSpeechMode)
			self.prevSpeechMode = None
		ui.message(msg)
		
	def initTimer(self):
		if self.timer is not None:
			self.timer.Stop()
			self.timer = None


	def event_foreground(self, obj, nextHandler) :
		if obj.role not in (controlTypes.Role.PANE, controlTypes.Role.FRAME, controlTypes.Role.WINDOW) :
			return nextHandler()
		if globalVars.TBPropertyPage  and not winUtils.findWindowByPartialTitle(" - Mozilla Thunderbird") :
			# wx.CallLater(1000, ui.message, "Reset of globalVars, Eventt foreground role={}, class={}, name={}".format(obj.role.name, obj.windowClassName, "" if not obj.name else obj.name))
			globalVars.TBPropertyPage = None
			globalVars.TBFolderTree = None
			globalVars.TBThreadTree = None
			globalVars.TBThreadPane = None
		nextHandler()
		

	# def notifyAppmodule(self):
		# obj=api.getForegroundObject()
		# globalVars.TBExited=True
		# ui.message("fglobalVars.TBExited" + str(globalVars.TBExited))
		# appMod =  obj.appModule
		# if appMod and hasattr(appMod, "TBExited") :
			# # beep(200, 20)
			# appMod.TBExited() 
			# return True
		# return  False
		# if time() - self.timerStartedAt < 30.0 : # secondes
			# self.timer.Start()
			
	def script_startTB(self, gesture) :
		forced = False if getLastScriptRepeatCount() == 0 else True
		if not forced :
			hWindowList = winUtils.findWindowByPartialTitle(" - Mozilla Thunderbird")
			if hWindowList :
				hWindowList.sort(reverse=False)				
				winUser.setForegroundWindow(hWindowList[0])
				# ui.message("Title : {}, hWindow : {}".format(winUser.getWindowText(hWindow), hWindow))
				return
			# focusTaskButton()
		tbPaths = ("C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe", "C:\\Program Files (x86)\\Mozilla Thunderbird\\thunderbird.exe")
		idx = -1
		if os.path.exists(tbPaths[0]) :
			idx = 0 
		elif   os.path.exists(tbPaths[1]) :
			idx = 1
		else :
			#messageBox("Thunderbird.exe non trouvé dans C:\Program files", "Lanceur de Thunderbird", wx.CLOSE|wx.ICON_WARNING)
			ui.message(_("Thunderbird.exe not found in C:\\Program files"))
			return
		startProgramMaximized(tbPaths[idx])
		# wx.CallLater(300, setTBOnTop)
		return
	script_startTB.__doc__ = _("Starts Thunderbird")
	script_startTB.category= ADDON_SUMMARY

	def  script_searchUpdate(self, gesture) :
		self.updateMenu = wx.Menu()
		# self.updateMenu.Append(0, _("Check for an update"))
		# self.updateMenu.Append(1, getUpdateLabel())
		lbl =  _("Install version {}")
		lbl = lbl.format(updateLite.getLatestVersion())
		self.updateMenu.Append(2, lbl)
		self.updateMenu.Bind (wx.EVT_MENU,self.onMenu)
		wx.CallLater(20, ui.message, ADDON_NAME +" " + ADDON_VERSION)
		showNVDAMenu  (self.updateMenu)

	def onMenu(self, evt):
		if evt.Id == 0 :
			# wx.CallLater(20, updateLite.checkUpdate, False)
			updateLite.checkUpdate(False)
		elif evt.Id == 1 :
			toggleUpdateState()
		elif evt.Id == 2 :
			wx.CallLater(20, updateLite.forceUpdate)
	script_searchUpdate.__doc__ = _("Update : shows an update menu")
	script_searchUpdate.category=ADDON_SUMMARY

	__gestures={
		gestureFromScanCode(41, "kb:control+alt+"): "startTB",
		gestureFromScanCode(41, "kb:control+alt+shift+"): "searchUpdate",
	}
	
def startProgramMaximized(exePath):
	import subprocess
	SW_MAXIMIZE = 3
	info = subprocess.STARTUPINFO()
	info.dwFlags = subprocess.STARTF_USESHOWWINDOW
	info.wShowWindow = SW_MAXIMIZE
	subprocess.Popen(exePath, startupinfo=info)
	return
import ctypes
from oleacc import AccessibleObjectFromWindow
def focusTaskButton():
	""" set focus on  weather button or startbutton """
	hTask = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
	if not hTask : return False
	#print("winver : " + str(sys.getwindowsversion()))
	if sys.getwindowsversion().major < 10 :
		cn = (b"start", b"DynamicContent2", b"DynamicContent1")
	else :
		cn = (b"DynamicContent2", b"DynamicContent1", b"start")
	for c in cn :
		hButton = ctypes.windll.user32.FindWindowExA(hTask, 0, c, 0)
		if hButton : break
	if not hButton : return False
	oAttribs = AccessibleObjectFromWindow(hButton, winUser.OBJID_WINDOW) # winUser.OBJID_WINDOW ou   winUser.OBJID_CLIENT) = -4
	oAttribs.accSelect(1) # set focus
	return True

# new speechMode functions by Paulber19 for NVDA 2021.1+ ander previous 
def getSpeechMode():
	try:
		# for nvda version >= 2021.1
		return speech.getState().speechMode
	except AttributeError:
		return speech.speechMode

def setSpeechMode(mode):
	try:
		# for nvda version >= 2021.1
		speech.setSpeechMode(mode)
	except AttributeError:
		speech.speechMode = mode

def setSpeechMode_off():
	#print(u"Fonction setSpeechMode_off")
	try:
		# for nvda version >= 2021.1
		speech.setSpeechMode(speech.SpeechMode.off)
	except AttributeError:
		speech.speechMode = speech.speechMode_off


# class processEntry32W(ctypes.Structure):
	# _fields_ = [
		# ("dwSize",ctypes.wintypes.DWORD),
		# ("cntUsage", ctypes.wintypes.DWORD),
		# ("th32ProcessID", ctypes.wintypes.DWORD),
		# ("th32DefaultHeapID", ctypes.wintypes.DWORD),
		# ("th32ModuleID",ctypes.wintypes.DWORD),
		# ("cntThreads",ctypes.wintypes.DWORD),
		# ("th32ParentProcessID",ctypes.wintypes.DWORD),
		# ("pcPriClassBase",ctypes.c_long),
		# ("dwFlags",ctypes.wintypes.DWORD),
		# ("szExeFile", ctypes.c_wchar * 260)
	# ]

import psutil

def getPidByName(process_name):
	# Search for the PID of an application from its executable name.
	# Args:
		# process_name (str): The name of the application executable (for example, "notepad.exe").
	# Returns:List: A PID list corresponding to the application.
	# Return an empty list if no application is found.
	pids = []
	for proc in psutil.process_iter(['pid', 'name']):
		try:
			if proc.info['name'].lower() == process_name.lower():
				pids.append(proc.info['pid'])
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			# Gérer les erreurs potentielles (processus disparu, accès refusé, etc.)
			pass
	return pids

def showNVDAMenu (menu):
	setCursorPos(100,100)
	sleep(0.03)
	wx.CallAfter (displayMenu,menu)
from gui import mainFrame  
def displayMenu (menu):
	mainFrame.prePopup ()
	mainFrame.PopupMenu (menu)
	mainFrame.postPopup ()


def getUpdateLabel() :
	global ADDON_NAME
	nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  ADDON_NAME + "-nextUpdate.pickle"
	exists =  (True if  os.path.exists(nextUpdateFile) else False)
	if exists and  os.path.getsize(nextUpdateFile) < 5 : # mise à jour désactivée # maj désactivée
		return  _("Enable automatic update")
	return _("Disable automatic update")

def toggleUpdateState() :
	global ADDON_NAME
	nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  ADDON_NAME + "-nextUpdate.pickle"
	if  os.path.exists(nextUpdateFile) and   os.path.getsize(nextUpdateFile) < 5 : 
		os.remove(nextUpdateFile) # réactive la maj
		speech.cancelSpeech()
		wx.CallAfter(ui.message, _("Automatic update has been enabled. You can restart NVDA to check for an update."))
		return 1
	# désactivation maj : écrit le fichier de longueur < 5 et contenant 0
	speech.cancelSpeech()
	try :
		ut = "0"
		with open(nextUpdateFile, mode="w") as fileObj :
			#pickle.dump(ut, fileObj)  #, protocol=0
			fileObj.write(ut)
	except :
		return wx.CallAfter(ui.message, _("Error saving update settings file."))
	wx.CallAfter(ui.message, _("Automatic update has been disabled."))

def showChangelog() :
	pageName = "TB+G5-history.html"
	from languageHandler import getLanguage
	lang = getLanguage()
	if "fr" in lang :
		url = "https://www.rptools.org/NVDA-Thunderbird/" + pageName
	else :
		url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/" + pageName + "?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		url = url.replace("@lg", lang)
	#  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	os.startfile (url)
