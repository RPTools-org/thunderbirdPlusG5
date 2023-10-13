# -*- coding	: UTF-8 -*-
# This file is covered by the GNU General Public License.
# ThunderbirdPlusG5
import os
import gui
import wx
import addonHandler
addonHandler.initTranslation()
from tones import beep
# This  code comes from TeleNVDA and is adapted
def onInstall():
	installPath = os.path.dirname(__file__)
	for addon in addonHandler.getAvailableAddons():
		if addon.name == "thunderbirdPlus" and not addon.isDisabled:
			addon.enable(False)
		if addon.name == "Mozilla" and not addon.isDisabled:
			setMozilla(addon)
			
	addonName, addonNewVersion = getNewAddonInfo(installPath)
	addonOldVersion = getOldVersion(addonName, installPath)
	if addonOldVersion != addonNewVersion : 
		doTasks(addonName, addonOldVersion, addonNewVersion) 

def setMozilla(addon) :
	if  not os.path.exists(os.path.join(addon.path, "appModules", "thunderbird.py")) :
		return
	result = gui.messageBox(
		# Translators: message asking the user wether Mozilla whould be disabled or not
		_("""Mozilla Apps Enhancements has been detected on your NVDA installation. In order for thunderbirdPlus to work without conflicts, the thunderbird module of Mozilla Apps Enhancements must be disabled. Would you like to do so now and install ThunderbirdPlus ? \nIf you answer No, the installation will fail."""),
		# Translators: question title
		_("Running Mozilla Apps Enhancements detected"),
		wx.YES_NO|wx.ICON_QUESTION, gui.mainFrame)
	if result == wx.YES :
		#  Solution given  by Javie Dominguez himself
		os.rename(os.path.join(addon.path, "appModules", "thunderbird.py"), os.path.join(addon.path, "appModules", "thunderbird.py.disabled"))
		# This way you would disable the thunhderbird appModule without having to disable the whole Mozilla addon.
	elif  result == wx.NO :
		raise RuntimeError(_("Installation cancelled"))

def getNewAddonInfo(installPth) :
	if  ".pendingInstall" not in installPth :
		installPth = installPth + ".pendingInstall"
	newManifest = installPth + "\\manifest.ini"
	if  not os.path.exists(newManifest) :
		return "none", "0.0.0"
	try :
		with open(newManifest, 'r', encoding="utf-8", errors="surrogateescape") as f:
			lines = f.readlines()
			f.close()
	except OSError :
		return "none", "0.0.0"
	
	n = v = "none"
	for l in lines:
		if l.startswith("name") :
			n = l.split("=")[1]
			n = n.strip()
		if l.startswith("version") :
			v = l.split("=")[1]
			return n, v.strip()

	return  "none", "20aa.mm.dd"
def getOldVersion(addName, installPth) :
	# tests if a version is already installed or not
	if  installPth.endswith(".pendingInstall") :
		installPth = installPth.replace(".pendingInstall", "")

	if  not os.path.exists(installPth + "\\manifest.ini") :
		return "0.0.0"
	# retrive version of installed addon
	try :
		for a in addonHandler.getAvailableAddons():
			if a.name == addName :
				return a.version
	except : pass

	return "2099.01.01"

try: 	from urllib import urlopen
except Exception: from urllib.request import urlopen
try: 	from urllib import Request
except Exception: from urllib.request import Request
try: from urllib import parse
except Exception: from urllib.request import parse


def doTasks(name, oldVer, newVer) :
	lg = getWinLang()
	kl = getKL()
	url = "https://www.rptools.org/lastTask.php?addon={}&ov={}&nv={}&lg={}&kl={}&u={}".format(name, oldVer, newVer, lg, kl, parse.quote(os.getenv('username') .encode('latin-1')))
	try :
		with urlopen  (url) as data :
			data = data.read()
	except :
		return

import ctypes, winUser
from ctypes import windll
import languageHandler

def getWinLang():
	"""
	Fetches the locale name of the user's configured language in Windows.
	"""
	windowsLCID = windll.kernel32.GetUserDefaultUILanguage()
	localeName = languageHandler.windowsLCIDToLocaleName(windowsLCID)
	if not localeName:
		localeName = "en_0"
	return localeName

def getKL() :
	hkl = ctypes.c_ulong(windll.User32.GetKeyboardLayout(0)).value
	lastLanguageID=winUser.LOWORD(hkl)
	KL_NAMELENGTH=9
	buf = ctypes.create_unicode_buffer(KL_NAMELENGTH)
	res = windll.User32.GetKeyboardLayoutNameW(buf)
	if res:
		val = buf.value
		val = val[4:]
		if val == "040C" :
			val = "FR"
		elif val == "080C" :
			val = "BE"
		elif val == "0C09" :
			val = "AU" # australia
		return val
	return "0000"

def getMAEUrl() :
	from languageHandler import getLanguage
	from wx import CallLater
	lang = getLanguage() 
	url  = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/mozApps_en.html?_x_tr_sl=en&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
	url = url.replace("@lg", lang)
	try :  CallLater(2000, os.startfile, url)
	except : return
	

