# -*- coding: utf-8 -*-
# Thunderbird+ 4.x

try: 	from urllib import urlopen
except Exception: from urllib.request import urlopen
try: 	from urllib import Request
except Exception: from urllib.request import Request

import api, globalVars
import os, wx
# import  gui
from ui import  message, browseableMessage
import addonHandler
addonHandler.initTranslation()
import api
import time, datetime, winUser
import config
from tones import beep
import pickle

def dateTS(sDateTime) :
	# example  = "2023-04-03 10:56"
	return time.mktime(datetime.datetime.strptime(sDateTime, "%Y-%m-%d %H:%M").timetuple())


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

urlFileInfos = baseUrl + "fileInfos.php?key=tbpg5Notif"


def checkNotif() :
	# tsFar  pour rattraper une erreur de date dans  le fichier de dernière notification
	# tsFar = dateTS("2123-01-01 08:00") 
	tsFar = 4828230000.0
	# print("Far date : {0}, far timestamp : {1} ".format("2123-01-01 08:00", str(tsFar)))
	# for test setLastDisplayed(tsFar + 10000)
	date, tsRemote = getRemoteDateTime()
	tsLocal = getLastDisplayed()
	# print("Remote date : {0}, Remote timestamp : {1}, Local ts : {2}".format(str(date), str(tsRemote), str(tsLocal)))
	if tsLocal > tsFar : tsLocal = 1000000000.0
	if tsRemote > tsLocal :
		setLastDisplayed(tsRemote)
		return  True
	return False

def getRemoteDateTime() :
	global urlFileInfos
	failDT = "2030-03-29 00:00"
	failTS =  dateTS(failDT)
	try :
		with urlopen  (urlFileInfos) as data :
			data = data.read().decode()
	except :
		# print("error reading : " + urlFileInfos) 
		return failDT, failTS
	if len(data)  < 10 : 
		# beep(100, 20)
		return failDT, failTS
	lines = data.split("\n")
	DT = lines[0].split("=")[1]
	# dt format : YYYY-MM-DD HH:MM
	# must convert v to time stamp
	try : TS = dateTS(DT)
	except : return failDT, failTS
	# print("date notif : " +str(DT))
	return DT, TS 

def showNotif() :
	from languageHandler import getLanguage
	lang = getLanguage()
	# lang = "en"
	if "fr" in lang :
		url = "https://www.rptools.org/NVDA-Thunderbird/notificationsG5.html"
	else :
		url = "https://www-rptools-org.translate.goog/NVDA-Thunderbird/notificationsG5.html?_x_tr_sl=fr&_x_tr_tl=@lg&_x_tr_hl=@lg&_x_tr_pto=sc"
		url = url.replace("@lg", lang)
	#  the translated content is displayeed via javascript so it cannot be displayed with ui.browseableMessage()
	os.startfile (url)

# import addonHandler
import time

def getLastDisplayed() :
	tbLastNotifFile = api.config.getUserDefaultConfigPath()+"\\addons\\tbpLastNotif.pickle"
	# print("tbLastNotifFile : " + tbLastNotifFile)
	if  not os.path.exists(tbLastNotifFile) : return 1000000000.0
	if os.path.getsize(tbLastNotifFile) < 10 : return 1000000000.0

	try :
		with open(tbLastNotifFile, mode="rb") as fileObj :
			ut = (pickle.load(fileObj))
		ut = float(ut)
	except :
		ut = 1000000000.0
		pass
	# print("TB+ update Time : " + str(ut))
	return ut
	
import api
def setLastDisplayed(ts) :
	msg = ""
	tbLastNotifFile = api.config.getUserDefaultConfigPath()+"\\addons\\tbpLastNotif.pickle"
	# print("setLastDisplayed, tbLastNotifFile : " + tbLastNotifFile)
	# print("setLastDisplayed, ts : " + str(ts))
	try :
		with open(tbLastNotifFile, mode="wb") as fileObj :
			pickle.dump(ts, fileObj)  #, protocol=0
		# os.startfile(tbLastNotifFile)
		return True
	except :
		msg = _("Error saving of :\n") + tbLastNotifFile 
		pass
		
	if msg :
		from speech import  cancelSpeech
		cancelSpeech()
		wx.CallLater(1000, message, msg)
		return False

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

