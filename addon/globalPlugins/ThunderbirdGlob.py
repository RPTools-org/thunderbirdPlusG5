# -*- coding: utf-8 -*-
# globalPlugins/Thunderbird.py
# Thunderbird+ 4.x

import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"_roleLabels": controlTypes.roleLabels}))
# End of compatibility fixes
import globalPluginHandler, addonHandler
from scriptHandler import getLastScriptRepeatCount

addonHandler.initTranslation()
import api
import ui
import speech
import wx
from .shared import updateLite
from .shared import notif
from time import time
import winUser
from winUser import getKeyNameText 
from tones import beep
import winKernel, globalVars
import os, sys

def gestureFromScanCode(sc, prefix) :
	# sc stands for the scanCode  of the key
	# prefix is "kb:modifiers"
	k = getKeyNameText(sc, 0)
	return prefix + k

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	focusNothing = False
	timer = None
	timerStartedAt = 0

	def __init__(self, *args, **kwargs):
		# beep(150, 60)
		# self.loadCfg()
		super (GlobalPlugin, self).__init__(*args, **kwargs)
		# if  getProcessIDFromExe("thunderbird.exe") == 0 : # TB is not  running
			# globalVars.TBStep = 0
		# else : globalVars.TBStep = 5
		hTaskBar = ctypes.windll.user32.FindWindowExA(None, None, b"Shell_TrayWnd", None)
		if not hTaskBar or  globalVars.appArgs.launcher : 
			return
		if notif.	checkNotif() :
			beep(440, 30)
			wx.CallLater(200, notif.showNotif)
		else :
			wx.CallLater(3000, updateLite.checkUpdate, True) # auto

	def initTimer(self):
		if self.timer is not None:
			self.timer.Stop()
			self.timer = None


	# def event_foreground(self, obj, nextHandler) :
		# beep(200, 2)
		# # print("Event_foreground " + str(obj.role))
		# if obj.role == controlTypes.Role.WINDOW : 
			# if "Thunderbird" not in obj.name and getProcessIDFromExe("thunderbird.exe")== 0 :
				# # beep(200, 2)
				# globalVars.TBStep=0
		# nextHandler()

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
		# beep(440, 30)
		if getProcessIDFromExe("thunderbird.exe") != 0 :
			ui.message(_("Thunderbird is already in use."))
			return
		#wx.CallLater(50, speech.speakMessage , "Hello everyone !", priority = speech.priorities.Spri.NOW)		
		focusTaskButton()
		ui.message(_("Starting Thunderbird."))
		tbPaths = ("C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe", "C:\\Program Files (x86)\\Mozilla Thunderbird\\thunderbird.exe")
		idx = -1
		if  os.path.exists(tbPaths[0]) :
			idx = 0 
		elif   os.path.exists(tbPaths[1]) :
			idx = 1
		else :
			#messageBox("Thunderbird.exe non trouvé dans C:\Program files", "Lanceur de Thunderbird", wx.CLOSE|wx.ICON_WARNING)
			ui.message(_("Thunderbird.exe not found in C:\\Program files"))
			return
		startProgramMaximized(tbPaths[idx])
		return
	script_startTB.__doc__ = _("Starts Thunderbird")
	script_startTB.category=_("Thunderbird+, launcher and update")

	def  script_searchUpdate(self, gesture) :
		repeat = getLastScriptRepeatCount()
		self.initTimer ()
		if repeat == 0: # 1 press : search new update 
			self.timer = wx.CallLater(300, updateLite.checkUpdate, False)
		elif repeat == 2 : # 3 press, force update
			self.timer = wx.CallLater(300, updateLite.forceUpdate)
	script_searchUpdate.__doc__ = _("Check for Thunderbird+ update")
	script_searchUpdate.category=_("Thunderbird+, launcher and update")

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


class processEntry32W(ctypes.Structure):
	_fields_ = [
		("dwSize",ctypes.wintypes.DWORD),
		("cntUsage", ctypes.wintypes.DWORD),
		("th32ProcessID", ctypes.wintypes.DWORD),
		("th32DefaultHeapID", ctypes.wintypes.DWORD),
		("th32ModuleID",ctypes.wintypes.DWORD),
		("cntThreads",ctypes.wintypes.DWORD),
		("th32ParentProcessID",ctypes.wintypes.DWORD),
		("pcPriClassBase",ctypes.c_long),
		("dwFlags",ctypes.wintypes.DWORD),
		("szExeFile", ctypes.c_wchar * 260)
	]

def getProcessIDFromExe(exeName):
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = processEntry32W()
	FProcessEntry32.dwSize = ctypes.sizeof(processEntry32W)
	ContinueLoop = winKernel.kernel32.Process32FirstW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	pID = 0
	while ContinueLoop:
		if exeName == FProcessEntry32.szExeFile :
			pID = FProcessEntry32.th32ProcessID
			break
		ContinueLoop = winKernel.kernel32.Process32NextW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	winKernel.kernel32.CloseHandle(FSnapshotHandle)
	return pID
