# -*- coding: utf-8 -*-
# ThunderbirdPlusG5

try: 	from urllib import urlopen
except Exception: from urllib.request import urlopen
try: 	from urllib import Request
except Exception: from urllib.request import Request

import api, globalVars
import os, wx
import  gui
from ui import  message, browseableMessage
import addonHandler
import core
from speech import cancelSpeech
addonHandler.initTranslation()
import api
import time, winUser
import config
from tones import beep
import pickle


class availableUpdateDialog(wx.Dialog):

	def __init__(self, parent, title, msg, releaseNoteURL=None):  #, message, auto, releaseNoteURL=None , releaseNoteURL
		super(availableUpdateDialog, self).__init__(parent, -1, title=title)
		self.parent = parent    # mainFrame
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		textStatic = sHelper.addItem(wx.StaticText(self))
		textStatic.SetLabel(msg)
		bHelper = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)	
		# try :
			# with urlopen(releaseNoteURL) as data :
				# data=data.read()
				# if not data : releaseNoteURL =None
		# except: releaseNoteURL =None  
		if releaseNoteURL:
			self.releaseNoteURL = releaseNoteURL
			infoButton = bHelper.addButton(self, label=_("&What's new"))
			infoButton .Bind(wx.EVT_BUTTON, self.onInfoButton)   #onInfoButton onReleaseNotesButton2
		yesButton = bHelper.addButton(self, wx.ID_YES, label=_("&Yes"))
		laterButton = bHelper.addButton(self,  label=_("&Later"))  #wx.NewId(),
		noButton = bHelper.addButton(self, wx.ID_NO, label=_("&Disable"))
		cancelButton = bHelper.addButton(self, wx.ID_CANCEL) 
		#events
		yesButton.Bind(wx.EVT_BUTTON, self.onYesButton)  # onYesButton
		laterButton.Bind(wx.EVT_BUTTON, self.onLaterButton)
		noButton.Bind(wx.EVT_BUTTON, self.onNoButton)  # onYesButton	
		sHelper.addDialogDismissButtons(bHelper)
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		#self.SetTitle(title)
		#yesButton.SetFocus()
		infoButton.SetFocus()
		self.CentreOnScreen()
		# the text in the window must be spoken.

		option = config.conf["presentation"]["reportObjectDescriptions"]
		config.conf["presentation"]["reportObjectDescriptions"] = True
		self.Show()
		winUser.setForegroundWindow(self.GetHandle())
		api.processPendingEvents()
		config.conf["presentation"]["reportObjectDescriptions"] = option 

	def onYesButton(self, event):
		self.EndModal(wx.ID_YES)

	def onLaterButton(self, event):
		self.EndModal(6666)

	def onNoButton(self, event):
		self.EndModal(wx.ID_NO)

	def onInfoButton(self, event):
		os.startfile (self.releaseNoteURL)
# end of  classe
# functions
def getURLHelp(url) :
	# 2022-12-20 localized
	from languageHandler import getLanguage
	lang = getLanguage()
	if "PT" not in   lang :
		lang = lang.split("_")[0]
	return url.format(lang)
	
# Variables to configure
baseUrl="https://www.rptools.org/"
urlHelp = getURLHelp(baseUrl + "NVDA-Thunderbird/changes5.php?lg={0}")
# urlFileInfos = baseUrl + "fileInfos.php?key=thunderbirdPlusG5"
urlFileInfos = baseUrl + "fileInfos.php?key=tbpg5upd"
# test urlFileInfos = baseUrl + "fileInfos.php?key=tbpG5Test"
isDlg = False

def isNewVersion(vLocal, vRemote) :
	# Provisoire pour versions dev : 
	# return (vRemote > vLocal)
	# version structure : YYMM.DD.BB wg-here BB is build.
	# compares only major and minor versions, not build no
	tmp = vLocal.split(".")
	vLocal = tmp[0].rjust(2, "0") + tmp[1].rjust(2, "0")
	tmp = vRemote.split(".")
	vRemote = tmp[0].rjust(2, "0") + tmp[1].rjust(2, "0")
	print("vRemote : {0}, vLocal : {1}".format(vRemote, vLocal))
	return (vRemote > vLocal)
	
def checkUpdate(autoUp) :
	global isDlg, urlHelp
	# beep(440, 30)
	if isDlg : return
	nm, curVer = getCurVersion() 
	# print("TbPlus curVer: " + nm + " curVer " + curVer)
	# décommenter la ligne ci-dessous pour provoquer test màj
	# curVer = "4.3.1" # pour provoquer test mise à jour 
	if autoUp : 
		if not hasToUpdate(nm) : return
	name, remoteVer =  getRemoteVersion()
	if not isNewVersion(curVer, remoteVer) : 
		if not autoUp : 
			core.callLater(10, cancelSpeech)
			core.callLater(50, message, name + " " + curVer + _("is up to date."))
		return
	isDlg = True
	msg = _("Do you want to update version {0} to version {1}?").format(curVer, remoteVer)
	with availableUpdateDialog(gui.mainFrame,_("ThunderbirdPlusG5 add-on update"), msg, releaseNoteURL=urlHelp) as dlg:  
		result=dlg.ShowModal()
	if result ==  6666 : # later
		core.callLater(40, setNextUpdate, nm)
	elif result ==  wx.ID_NO :
		core.callLater(40, setNextUpdate, nm, True) # disable
	elif result ==  wx.ID_YES :
		result, msg = doUpdate(curVer)
		if result < 1 :
			browseableMessage (message = msg, title = _("Addon update") + name, isHtml = False)
	isDlg = False

def getRemoteVersion() :
	global urlFileInfos
	# bytes = getFileSizeFromURL(urlFileInfos) 
	# return "taille : " + str(bytes), "1.0"
	try :
		with urlopen  (urlFileInfos) as data :
			data = data.read().decode()
	except :
		return _("Version check error"), "1.0"
	if len(data)  < 10 : # v 3.4.2 si longueur du contenu fileInfos < 10 dans le cas de TB+
		#beep(100, 20)
		return _("Error reading Info file"), "1.0"
	lines = data.split("\n")
	v = lines[0].split("=")[1] # version
	v = v.split(" ")[0]
	n = 	 lines[2].split("=")[1] # name
	return n, v

def doUpdate(oldVer, forced="") :
	global baseUrl, urlFileInfos
	# urlFileInfos = baseUrl + "fileInfos.php?key=tbpg5upd"
	if forced == "Forc" :
		urlFileInfos = urlFileInfos.replace("upd", "")
	
	beep(337, 1)
	try :
		with urlopen  (urlFileInfos) as data :
			data = data.read().decode()
	except :
		return -1, _("Error retrieving file information")
	if len(data) < 10 :
		return -1, _("Error retrieving file information")
	lines = data.split("\n")
	ver = lines[0].split("=")[1]
	# return -1, "oldVer={0}, ver={1}".format(oldVer, ver)
	# message("From {0} to {1}".format(oldVer, ver))
	dbID = lines[1].split("=")[1]
	name = 	 lines[2].split("=")[1]
	dlFile= lines[3].split("=")[1]
	path = lines[4].split("=")[1]
	beep(337, 1)
	# download addon or new major version notification
	#urlFile =  path + name + "-" + ver + "-" + type
	urlFile =  path + dlFile 
	try :
		with urlopen  (urlFile) as data :
			data = data.read()
	except :
		return -2, _("Error downloading of :\n") + urlFile
	lenData = len(data) # v 3.4.2
	if lenData < 10000 : return -3, _("Empty file error")
	# sauvegarde dans fichier
	beep(337, 1)
	if ".html" in dlFile: 
		filePath = os.getenv('temp') + "\\" + dlFile
	else : 
		filePath = os.getenv('temp') + "\\Thunderbird+-update.nvda-addon"
	# v 3.4.2 suppression fichier précédent par sécurité
	if  os.path.exists(filePath) :
		try : 
			os.remove(filePath)
		except OSError as error:
			return -4, error + _(", cannot delete : ") + filePath
	# écriture
	try :
		with open(filePath, mode="wb") as fileObj :
			fileObj.write(data)
	except :
		return -4, _("Saving error of :\n") + filePath
	# v 3.4.2 vérif taille fichier écrit 
	if os.path.getsize(filePath)  < lenData :
		return  - -4, _("Error saving addon to temporary file.")
	# starts  addon install
	# os.startfile (filePath)
	installAddon(filePath)
	return 1, "OK"

def installAddon(file):
	newAddon = "thunderbirdPlusG5"
	for addon in addonHandler.getAvailableAddons():
		if addon.name == "thunderbirdPlus" : # old version 4
			beep(440, 5)
			addon.requestRemove()
		if addon.name == newAddon :
			beep(440, 5)
			addon.requestRemove()
	# to install the new version
	killTB()
	bundle = addonHandler.AddonBundle(file)
	addonHandler.installAddonBundle(bundle)
	# to restart NVDA
	core.restart()



def forceUpdate() :
	nm, ver = getCurVersion()
	result, msg = doUpdate(ver, "Forc")
	if result < 1 :
		browseableMessage (message = msg, title = _("Addon update") + nm, isHtml = False)

import addonHandler
import time

def getCurVersion() :
	_curAddon = addonHandler.getCodeAddon()
	name = _curAddon.manifest["name"]
	ver = _curAddon.manifest["version"]
	return  name, ver.split(" ")[0]
import api
def setNextUpdate(addonName, disable=False) :
	from speech import cancelSpeech
	cancelSpeech()
	nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  addonName + "-nextUpdate.pickle"
	if not disable :
		# anciien ut = str(time.time() + 3600 * 72) 
		ut = time.time() + 3600 * 72 
		msg = _("The update will be offered again in 3 days. In the meantime, you can press AltGr+Shift+grave to perform an update search.")
		fMode = "wb"
	else :  # disable auto update
		ut = "0"
		fMode = "w"
		msg = _("Automatic update has been disabled. press AltGr+Shift+grave for a manual update.")

	try :
		with open(nextUpdateFile, mode=fMode) as fileObj :
			if disable :
				fileObj.write(ut)
			else :
					pickle.dump(ut, fileObj)  #, protocol=0
	except :
		msg = _("Saving error of :\n") + nextUpdateFile
		pass
	#os.startfile(nextUpdateFile)
	wx.CallAfter(message, msg)

def hasToUpdate(addonName) :
	nextUpdateFile = api.config.getUserDefaultConfigPath()+"\\addons\\" +  addonName + "-nextUpdate.pickle"
	if  not os.path.exists(nextUpdateFile) : return True
	if os.path.getsize(nextUpdateFile) < 5 : return False # mise à jour désactivée

	now = time.time() 
	try :
		with open(nextUpdateFile, mode="rb") as fileObj :
			ut = (pickle.load(fileObj))
		ut = float(ut)
	except :
		ut = now - 3600
		pass
	#print("TB+ update Time : " + str(ut))
	if ut < now :
		return True
	return False

def getFileSizeFromURL(url) :
	req = Request(url, method='HEAD')
	f = urlopen(req)
	#f.status # 200
	return str(f.headers['Content-Length'])

def getLatestVersion() :
	global baseUrl
	urlInfos = baseUrl + "fileInfos.php?key=tbpg5"
	errMsg = " : " + _("Undetermined version")
	try :
		with urlopen  (urlInfos) as data :
			data = data.read().decode()
	except :
		return errMsg + " 1"
	if len(data) < 10 :
		return errMsg + " 2"
	lines = data.split("\n")
	try : ver = lines[0].split("=")[1]
	except : return errMsg + " 3"
	# browseableMessage (message =data, title = _("Addon update"), isHtml = False)
	return  ver

def killTB(wait=0.5) :
	import psutil
	for proc in psutil.process_iter():
		if proc.name() == "thunderbird.exe":
			proc.terminate()
	time.sleep(wait)