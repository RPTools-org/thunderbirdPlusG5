# -*- coding: utf-8 -*-
# globalPlugins/ThunderbirdGlob.py
# 2026.05.23 :  cleaned version of this file. The notification feature is in previous versions.
# Thunderbird+G5
import sys
import addonHandler
addonHandler.initTranslation()
import os
addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)
import commonVars

# Get the path of the root directory of the extension (monExtension)
addonDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addonDir not in sys.path:
	sys.path.insert(0, addonDir)
# Now the import will work properly
from shutils import tbLogger
import controlTypes
import globalPluginHandler
from scriptHandler import script, getLastScriptRepeatCount
from shutils import tbLogger

ADDON_NAME = addonHandler.getCodeAddon().manifest["name"]
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
ADDON_VERSION = addonHandler.getCodeAddon().manifest["version"]
import api
import ui
import speech
# import wx
from .shared import winUtils
# from .shared import utilGlob  as ut
from time import time, sleep
import winUser
from winUser import getKeyNameText, setCursorPos 
from tones import beep
import globalVars
import globalCommands
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

	# timer = None
	# timerStartedAt = 0

	def __init__(self, *args, **kwargs):
		super (GlobalPlugin, self).__init__(*args, **kwargs)
		hTaskBar = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
		if not hTaskBar or  globalVars.appArgs.launcher : 
			return
		
	# def initTimer(self):
		# if self.timer is not None:
			# self.timer.Stop()
			# self.timer = None


	def event_foreground(self, obj, nextHandler) :
		if obj.role != controlTypes.Role.FRAME : # not in (controlTypes.Role.PANE, controlTypes.Role.FRAME, controlTypes.Role.WINDOW) :
			return nextHandler()

		if commonVars.cv.propertyPage  and not winUtils.findWindowByPartialTitle(" - Mozilla Thunderbird") : # Thunderbird was closed
			commonVars.cv.reset()
		nextHandler()
	

	@script(
		gesture="kb:alt+windows+f12",
		description="z Starts or stops the internal logger",
		category = "thunderbirdPlusG51, global plugin"
	)
	def script_toggleLogger(self, gesture) :
		if commonVars.cv.logger 	is not None:
			ui.message("disabled : log startup")
			commonVars.cv.logger.terminate()
			commonVars.cv.logger = None
		else :
			commonVars.cv.logger = tbLogger.createLogger(show=True)
			if commonVars.cv.logger :
				commonVars.cv.logger.add("TB logger started from globalPlugin")
				commonVars.cv.logger.add("commonVars.cv.defaultSpeechMode = " + str(commonVars.cv.defaultSpeechMode.displayString))
				ui.message("enabled : log Thunderbird startup.")
			else :
				ui.message("TB logger creation failed")

		



	@script(
		gesture="kb:nvda+s",
		description=_("Toggles NVDA speech modes and notifies Thunderbird+G5"),
		category = "thunderbirdPlusG51, do not change"
	)
	def script_toggleSpeechMode(self, gesture) :
		globalCommands.commands.script_speechMode(gesture)
		commonVars.cV.defaultSpeechMode =  speech.getState().speechMode

	@script(
		gesture=gestureFromScanCode(41, "kb:control+alt+"),
		description=_("Starts Thunderbird"),
		category=ADDON_SUMMARY
	)
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

# def showChangelog() :
	# pageName = "TB+G5-history.html"
	# from languageHandler import getLanguage
	# lang = getLanguage()
	# if "fr" in lang :
		# url = "https://www.rptools.org/NVDA-Thunderbird/" + pageName
	# else :
		# url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/" + pageName + "?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		# url = url.replace("@lg", lang)
	# #  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	# os.startfile (url)
