 #-*- coding:utf-8 -*
import addonHandler
addonHandler.initTranslation()

import re, speech, winUser
from ui import message, browseableMessage
from core import callLater
from core import callLater
from tones import beep
from time import sleep
from api import  getForegroundObject, getFocusObject, setFocusObject, copyToClip, processPendingEvents
from comtypes.gen.ISimpleDOM import ISimpleDOMNode
from NVDAObjects.IAccessible import IAccessible
import globalPluginHandler
import controlTypes
import treeInterceptorHandler, textInfos
import sharedVars
import utis 


# Attention : 2 non printable chars used here :  Alt+0031 is used as a separator of quotes / messages.  Alt+0030 as a temporary replacement of \n
CNL = chr(30) # char new line
# CNQ = chr(31) # char new quote, hard coded as 
class QuoteNav() :
	text =  subject = ""
	# the following variables are list indexes
	curItem =  lastItem = curQuote = 0

	def __init__(self) :
		self.lItems  = self.lQuotes = []
		self.translate = False # 2024.01.02
		self.browseTranslation = sharedVars.oSettings.getOption("messengerWindow", "displayTranslations")
		self.iTranslate = None
		self.langTo = utis.getLang()

		# Translators : do not translate nor remove %date_sender%. Replace french words, word 2 and word 5, by your translations. 
		# The  char Alt+0030 is a temporary replacement of \n
		lbls = _("On|Le%date_sender%wrote|écrit")
		lbls = str(lbls.replace("%date_sender%", "|"))
		lbls = lbls.split("|")
		
		self.onLg = lbls[0] 
		self.onEn = lbls[1]
		self.wroteLg = lbls[2] 
		self.wroteEn = lbls[3] 
		# sharedVars.logte("lblON, lblWrote: {} {} {} {}".format(self.onLg, self.wroteLg, self.onEn, self.wroteEn))
		# reg expressions
		self.regBrPLi = re.compile("\n|<br>|<p>|</p>|<li>|</li>|<p.+?>|<li.+?>")
		s = "(( ||\w|\d){1,}(" + lbls[0] + ") .*?(" + lbls[1] + ")(:| :|:| :))"
		# s = "(\d{4} .*?(" + lbls[1] + ")(:| :|:| :))" 
		# compilation
		self.regStdHdr = re.compile(s)
		# removes special &char;
		self.regHTMLChars = re.compile("(&nbsp;|&gt;)") 
		# link tags
		self.regLink = re.compile ("(\<a .+?\>(.+?)\</a\>)")
		# All HTML tags
		self.regHTML = re.compile("\<.+?\>")
		# to removes  multiple spaces
		self.regMultiSpaces = re.compile(" {2,}")
		# to remove multi pseudo new line :  
		self.regMultiNL = re.compile(CNL + "{2,}")
		# to clean sender name
		self.regSender = re.compile("(|\n|&lt;| via groups\.io)")
		# replace \n that are after a letter or a digit with semicolon
		self.regSemi = re.compile("(\w|\d)\n")
		self.regTextTags = re.compile("<span|<a|<p|<li|<td")
		# v2 issueself.regSender = re.compile("(|&lt;| via (" + self.lblWrote  + "))")
		self.regSubject = re.compile(u"(Re:|Ré )")
		self.regListName = re.compile ("\[.*\]|\{.*\}") # compile ("\[(.*)\]")
	def toggleTranslation(self) :
		msg = _("message translation mode ")
		if self.translate : 
			self.translate = False 
			self.iTranslate = None
			return message(msg + _("Disabled"))
		try : 
			self.iTranslate = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
			# sharedVars.logte("Instant Translate :" + str(self.iTranslate))
		except :
			pass
		
		if not self.iTranslate :
			return message(_("The Instant Translate add-on is not active or not installed."))
		self.translate = True
		message(msg + _("Enabled"))

	def toggleBrowseTranslation(self) :
		msg = _("Translation display mode {}")
		self.browseTranslation = not   self.browseTranslation
		state = _("Enabled"  if self.browseTranslation else _("Disabled"))
		message(msg.format(state))

	def readMail(self, oDoc, rev = False, spkMode=1): 
		# focus = getFocusObject()
		# setFocusObject(oDoc)
		# treeInterceptor = treeInterceptorHandler.getTreeInterceptor(oDoc)
		# setFocusObject(focus)
		# if treeInterceptor:
			# try:
				# info = treeInterceptor.makeTextInfo("all")
			# except:
				# pass
			# else:
				# message(
				# text=info.text,
				# brailleText="\n".join((oDoc.name, info.text)))
		# beep(432, 10)
		# # browseableMessage(message= str(info.text), title= str(oDoc.name), isHtml=False)
		# return
		speech.cancelSpeech()
		for i in range(0, 20) :
			if oDoc.role == controlTypes.Role.DOCUMENT :
				result = self.setDoc(oDoc, rev)
				# sharedVars.debugLog= self.text
				if result == 1 : 
					self.setText(spkMode) 
					break
				elif result == 2 : 
					# beep(100, 20)
					callLater(250, self.setText, spkMode) 
					# self.sayDraftText()
					break
			else : 
				beep(150, 5)
				# sleep(0.1)
				oDoc =  getFocusObject()

	def setDoc(self, oDoc, nav=False): 
		# converts the doc into HTML code
		if not oDoc : return 0 
		self.nav = nav
		# self.text = "\n---" # alt+0031
		self.text = "\n" # alt+0031
		self.lItems = []
		self.lQuotes = []
		self.lastItem = -1
		self.curItem = 0		
		self.quoteMode = True
		self.subject = ""
		# document without subject as name 
		parID = str(utis.getIA2Attribute(oDoc.parent))
		if parID == "messageEditor" : 
			self.quoteMode = False
			fg = getForegroundObject()
			sharedVars.curSubject = fg.name
			self.quoteMode = False
		elif parID == "spellCheckDlg" : 
			# sharedVars.curSubject = parID
			self.QoteMode = False

		self.subject  =sharedVars.curSubject.split(" - ")[0].strip() # ((" ,;:"))
		if " " in self.subject :
			p = self.subject.split(" ")
			self.subject = p[len(p)-1].strip()

		o=oDoc.firstChild # section ou paragraph
		# # sharedVars.logte(u"après  o.firstChild " + str(o.role)  + ", " + str(o.name))
		if not o : return 0
		cCount =  oDoc.childCount
		
		if o.next :
			# beep(800, 40)
			#html simple
			# self.text = "\n---" 
			i = 1
			# if cCount > 75 : message(str(cCount) + _(" text elements. Press Control to stop."))
			while o :
				# # sharedVars.logte(u"HTML elem:" + str(o.role)  + ", " + str(o.name))
				try : 
					obj = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
					s=obj.innerHTML 
					if not s :s= o.name
				except :
					s = "error retriving innerHTML"
					pass
				if s :self.text += s + CNL # + CNL required for not self.quoteMode
				if cCount > 75 and s and self.regTextTags.search(s) :
					beep(250,5)
				if winUser.getKeyState(winUser.VK_CONTROL)&32768:
					return 2
				i += 1
				try : o=o.next
				except : break
		else: # plain Text
			# self.text = "\n---"
			o = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			# # sharedVars.logte("brut:" + str(o))
			self.text += str(o.innerHTML)
		return 1

	def sayDraftText(self) :
		self.text=self.regHTMLChars.sub(" ",self.text)
		self.text=self.regHTML.sub(" ",self.text)
		# beep(100, 20)
		sharedVars.debugLog = "Draft :\n" + self.text
		callLater(500, message, self.text)
	
	def getDocObjects(self, oDoc) :
		o = oDoc.firstChild
		while o :
			o = o.next
	

	def setText(self, speakMode=1) : 
		self.deleteBlocks()
		# replace \n and <br> with 
		self.text = self.regBrPLi.sub(CNL, self.text)
		# removes special &char;
		self.text=self.regHTMLChars.sub(" ",self.text)
		# copyToClip(self.text)
		# return beep(100, 40)
		self.cleanLinks()
		# Removes of all remaining HTML tags
		self.text=self.regHTML.sub("",self.text)
			# removes multiple spaces 
		self.text=self.regMultiSpaces.sub(" ",self.text)
		# if self.quoteMode :
			# beep(440, 20)
		# removes multiple pseudo \n 
		self.text=self.regMultiNL.sub(CNL,self.text)
		self.cleanStdHeaders()
		self.cleanMSHeaders()

		# removes multiple  spaces again
		self.text = self.regMultiSpaces.sub(" ", self.text)

		if not self.nav : # text
			self.text = self.text.replace(CNL, "\n")
			if speakMode > 0 :
				self.speakText(0, speakMode)
		else :
			self.buildLists(speakMode)

	def buildLists(self, speakMode) :
		# quotes/messages are separated by alt+0031 char
		# if sharedVars.curTab == "main" :
		if self.quoteMode :
			# in order to split the text into quotes
			self.text = self.text.replace(CNL, " ; ")
			splitSep = "\n"
			self.text = self.regSemi.sub(" ; ", self.text) 
			msg = _("{0} messages in chronological order, ") 
		else :
			self.quoteMode = False 
			# in order to split the text into lines
			self.text = self.text.replace(CNL, "\n")
			splitSep = "\n"
			msg = _("{0} messages, {1} lines, ")

		self.curItem = self.lastItem = self.curQuote = 0
		self.lQuotes = []
		# split text into items
		self.lItems = str(self.text).split(splitSep) 
		if not self.lItems :
			self.lItems = []
			beep(200, 20)
			return 
		if self.quoteMode and not self.translate : # 2024.01.01
			self.lItems.reverse()
		self.lastItem = len(self.lItems) - 1

		# build quotes indexes list
		self.lQuotes = [idx for (idx, item) in enumerate(self.lItems) if item.startswith("")]
		qCount = len(self.lQuotes) + (1 if self.quoteMode else 0)
		msg = msg.format(qCount, self.lastItem + 1)
		# find first non emptuy line 
		while self.lastItem > 0 and self.curItem < 20 :
			# l =  str(self.lItems[self.curItem]).strip()
			# # sharedVars.logte("litem [" + str(self.lItems[self.curItem]) + "]")
			if str(self.lItems[self.curItem]).strip() != "" :
				break
			self.curItem += 1
		if speakMode  > 0 :
			message(msg + self.lItems[self.curItem])

	def showTranslation(self, t) :
		browseableMessage(message=t, title= _("Translation"), isHtml=False)

	def truncateSubj(self, text, minLen) :
		text=self.regSubject.sub("",text)
		text=self.regListName.sub("",text)
		text=self.regMultiSpaces.sub(" ", text)
		max = len(text)
		# sharedVars.logte("TruncateSubj " + "{}, minLen : {}, maxLen : {}".format(text, minLen, max)) 
		if minLen <= max : return text 
		pos = minLen - 1
		while pos < max :
			if text[pos] == " " :
				return text[0:pos]
			pos += 1
		return text

	def speakText(self, freq=0, speakMode=1) :
		if freq > 0 :
			beep(freq, 40)
		msg = ""
		if speakMode == 2 :
			copyToClip(self.text)
			msg = _("Preview copied: ")
		
		if self.translate : 
			t  = self.iTranslate.translateAndCache(sharedVars.curSubject, "auto", self.langTo).translation
			t = self.truncateSubj(t, 25) + " :\n" 
			t += self.iTranslate.translateAndCache(self.text.split("")[1]  , "auto", self.langTo).translation
			if self.browseTranslation : self.showTranslation(t)
			else : message(msg + t)
		else :
			message(msg + self.text)

	def speakQuote(self, quote) :
		if self.translate : 
			quote  = self.iTranslate.translateAndCache(quote, "auto", self.langTo).translation
		if self.browseTranslation : self.showTranslation(quote) 
		else : message(quote)
	def deleteMetas(self) :
		lbl = "<meta "
		metas = []
		p, pEnd = self.findWords(lbl)
		while p > -1 :
			p2 = self.text.find('">', pEnd) 
			if p2 == -1 : break
			b = self.text[p:p2] + '">'
			# # sharedVars.logte("meta:" + b)
			metas.append(b)
			# next block
			p, pEnd = self.findWords(lbl, p2+2) # +2 is then len of ">
		if len(metas) == 0 : return
		for e in metas :
			# # sharedVars.logte("e:" + e)
			self.text = self.text.replace(e, "")
			self.text = self.text.replace(e, "")

	def deleteBlocks(self) :
		# Originale message
		s = _("Original Message|E-mail d'origine|Message d'origine")
		reg = re.compile("(\-{5} ?(" + s + ") ?\-{5})")
		self.text = reg.sub("", self.text)

		self.deleteMetas()
		# removes style css tag
		if self.text.find("<style>") > 0 :
			regExp = re.compile ("\<style\>.+?\</style\>")
			self.text=regExp.sub (" ",self.text)

		#  removes table of mozilla headers
		p = self.text.find('<table class="moz-email-headers-table">')
		if p != -1 :
			p2 = self.text.find("</table>", p+25)
			if p2 != -1 :
				self.text = self.text.replace(self.text[p:p2], "") 
		
		# group footers : one group in a message, we  use return after a footer  deletion
		#Removes   de google groupe  footer
		s = _("You are receiving this message because you are subscribed to the group") #  Google")
		pos =self.text.find (s)
		if pos !=-1 :
			self.text=self.text[:pos]
			return

		#Removes groups.io footer
		# "Groups.io Links:"
		pos = self.text.find("Groups.io Links:")
		if pos != -1 :
			p2, p3 = self.findWords("_._,|-=-=")
			if p2 != -1 : pos = p2
			if pos != -1 :
				self.text=self.text[:pos]
				return
				
		# removes freeLists footer : -----------------------Infos----
		pos = self.text.find("-----------------------Infos-----------------------")
		if pos != -1 :
			self.text=self.text[:pos]
			return
			
		# removes french framalistes footer
		pos = self.text.find("Le service Framalistes vous est")
		if pos != -1 :
			self.text=self.text[:pos]

	def cleanLinks(self) :
		# mailto and clickable links replacements
		lbl = _(" link %s ").replace(" %s", "")
		l=self.regLink.findall (self.text)
		for e in l :
			self.text_link = e[1]
			# # sharedVars.logte( "e: " + str(e))
			# # sharedVars.logte( "self.text_link " + str(self.text_link))
			if "mailto" in e[0]:
				self.text = self.text.replace(e[0], self.text_link + ":")
			elif self.text_link.startswith ("http") :
				self.text = self.text.replace (e[0], shortenUrl(self.text_link, lbl))

	def findStdHeader(self, wFirst, wLast, start) : 
		global CNL
		# examples :
		# en : first:On 07-01-2023, PLR last:wrote:
		# fr : first:Le 01/07/2023, PLR a last:écrit :
		# czech : first:Dne 01.07.2023 PLR@site.com last:napsal(a):
		# tr : 07-01-2023 first:tarihinde PLR ​​şunları last:yazdı:
		pEnd = self.text.find(wLast, start)
		# # sharedVars.logte("Search of {} from {}, found at : {} :".format(wLast, start, pEnd))
		if pEnd == -1 : return -1, -1 # pos begin   , pos end
		# pBeg = self.text.rfind(wFirst, pEnd-100, pEnd)
		pBeg = -1
		# scanned = ""
		inf = min(pEnd, 20) 
		for i in range(inf, 100) :
			# scanned = self.text[pEnd-i] + scanned
			if self.text[pEnd-i] == CNL :
				pBeg = pEnd - i + 1
				break

		# # sharedVars.logte("reverse Search of new Line  from {} found at :{}, scanned=:{}".format(pEnd, pBeg, scanned))

		if pBeg == -1 : return -1, -1
		if pEnd - pBeg > 60 : return -1, -1
		pEnd += len(wLast)
		# search near new line char at the next 10 chars :
		for i in range(1, 10) :
			if self.text[pEnd+i] == CNL :
				pEnd += i
				break
		return pBeg, pEnd
		
	def cleanStdHeaders(self) :
		# Compress standard "On date sender wrot :
		# 1. findAll blocks of headers
		# 1. for user  language 
		pS = pE =0
		headers = []
		while pE > -1 : 
			pS, pE = self.findStdHeader(self.onLg, self.wroteLg, pE+1)
			# # sharedVars.logte("pS : {}, pE : {}, std header: {}".format(pS, pE, self.text[pS:pE]))
			if pS != -1 :
				headers.append(self.text[pS:pE])
		# 2. for English  language 
		if utis.getLang() != "en" : 
			pS = pE =0
			while pE > -1 : 
				pS, pE = self.findStdHeader(self.onEn, self.wroteEn, pE+1)
				if pS != -1 :
					headers.append(self.text[pS:pE])
		if len(headers) == 0 : return
		for h in headers :
			# h = e # str(e).strip()
			
			# sharedVars.logte("Old h :" + h)
			nh = str("--- ") + str(cleanH(h, self.regMultiSpaces))
			# sharedVars.logte("new h :" + nh)
			self.text = self.text.replace(h, "\n" + nh)

	def cleanMSHeaders(self) :
		# Compress  WinMail and OE headers liene 
		# 1. findAll blocks of headers
		# regExpr : De :  julien  palibau:  A : winaide2@googlegroups.com:  Sent: Monday, July 17, 2023 5:47 AM Objett: Re: [winaide2] hébergeur de  fichiers
		lenSubj = len(self.subject)
		blocks = []
		lbls = _("From|De|Expéditeur") + "|"
		a = lbls.split("|")
		lbls = ""
		for lbl in a :
			if lbl == "" : break
			lbls += lbl + ":|" + lbl + " :|"
		lbls = lbls[:-1]
		# # sharedVars.logte("from labels:" + lbls)
		# maybe for a future version > regHdr = "((" + lbls + ").+?" + self.subject + ")"
		# # sharedVars.logte("regHdr:" + regHdr)
		p, pEnd = self.findWords(lbls)
		while p > -1 :
			p2 = self.text.find(self.subject, pEnd) 
			if p2 == -1 : break
			b = self.text[p:p2] + self.subject
			# # sharedVars.logte("MS header:" + b)
			blocks.append(b)
			# next block
			p, pEnd = self.findWords(lbls, p2+lenSubj)
		if len(blocks) == 0 : return

		for e in blocks :
			# # sharedVars.logte("to replace:" + e)
			# e may contain , a pseudo \n 
			# t = "\n---" + getSenderName(e) + " " + _("wrote") + " : "
			t = "\n" + getSenderName(e) + " " + _("wrote") + " : "
			# # sharedVars.logte("t:" + t)
			self.text = self.text.replace(e, t)
		return
			# if utis.wordsMatchWord(search, e[0]) :
				# arr = str(e[0]).split(":")
				# if len(arr) > 2 :
					# repl = "--- " + getSenderName(arr[1]) + " " + _("wrote") + " :"
					# # sharedVars.logte( "replacement : " + repl)

	def strBetween2(self, sep1, sep2) :
		pos1 = self.text.find(sep1) 
		if pos1 < 0 : return ""
		pos1 +=  len(sep1)
		pos2 = txt.find(sep2, pos1)
		if  pos2 < 0 : return ""
		return self.text[pos1:pos2]

	def findWords(self, words, start=0) :
		lWords = words.split("|")
		for e in lWords :
			pos = self.text.find(e, start)
			if pos > -1 :
				return pos, pos + len(e) + 1
		return pos, pos
		

	def getSenderName(header) :
		#  header may contain 
		

		# On Behalf Of Isabellevia groups.ioSent 
		if "Behalf Of" in header :
			s = strBetween(header, "Behalf Of", "via groups").strip()  
		elif  "via groups.io" in header : 
			# to replace:From:   Jeremy T. via groups.io: 
			s = strBetween(header, ":", "via")
		else :
			# s = "à revoir : " + header
			header  = header.split(":") 
			s = (header[1] if len(header) > 1 else header[0])
			if "&lt;" in s :
				s = s.split("&lt;")[0]

		
		self.regSender.sub("", s)
		s = s.strip()
		# # sharedVars.logte("retour getSenderName :" + s)
		return s
	# methods related to quotes navigation
	def skip(self, n=1) :
		if self.lastItem == -1 : 			self.buildLists(False)
		# skips 1 item before or after
		if n == -1 :
			self.curItem = self.lastItem if self.curItem == 0 else self.curItem - 1
		elif n == 1 :
			self.curItem = 0  if self.curItem == self.lastItem  else self.curItem + 1
		if self.quoteMode :
			self.speakQuote(str(self.curItem+1) + ":" + self.lItems[self.curItem])
		else :
			self.speakQuote(self.lItems[self.curItem])

	def skipQuote(self, n=1) :
		if self.lastItem == -1 : 			self.buildLists(False)
		# skips 1 quote before or after
		lastQuote = len(self.lQuotes) - 1
		if n == -1 :
			self.curQuote = lastQuote if self.curQuote == 0 else self.curQuote - 1
		elif n == 1 :
			self.curQuote = 0  if self.curQuote == lastQuote  else self.curQuote + 1

		self.curItem = self.lQuotes[self.curQuote]
		# return message(" curquote {},  curItem {}".format(self.curQuote, self.curItem))
		self.speakQuote(str(self.curQuote+1) + ":" + self.lItems[self.curItem])

	def findItem(self, expr) :
		if self.lastItem == -1 : 			self.buildLists(False)
		lIdx, wIdx = self.indexOf(expr, self.curItem)
		if lIdx > -1 :
			self.curItem = lIdx
			self.speakQuote(self.lItems[lIdx])
		else :
			beep(120, 20)
	# self.lQuotes = [idx for (idx, item) in enumerate(self.lItems, self.curIndex) if item.find(expr) > -1]
		# try:
			# self.CurItem = self.lItems.index(expr) # ,self.curItem)
			# message(self.lItems[self.curItem])
		# except ValueError:
			# beep(100, 20)			
		
			
	def indexOf(self, word, start=0, backward=False) : 
		stopChar = "" # alt+0031
		if not backward :
			step = 1
			# start is the same
			iLast = self.lastItem 
		else :
			step = -1
			iLast = 0
		
		for i in range(start, iLast, step) : 
			if i > start and stopChar in self.lItems[i] :
				break
			p = self.lItems[i].find(word)
			if p > -1 :
				return i, p
		
		return -1, -1
# normal functions
def getSenderName(header) :
	#  header may contain 
	

	# On Behalf Of Isabelle Delarue via groups.ioSent 
	if "Behalf Of" in header :
		s = strBetween(header, "Behalf Of", "via groups").strip()  
	elif  "via groups.io" in header : 
		# to replace:From:   Jeremy T. via groups.io: 
		s = strBetween(header, ":", "via")
	else :
		# s = "à revoir : " + header
		header  = header.split(":") 
		s = (header[1] if len(header) > 1 else header[0])
		if "&lt;" in s :
			s = s.split("&lt;")[0]

	s = s.replace("", " ").strip()
	# # sharedVars.logte("retour getSenderName :" + s)
	return s
	
def shortenUrl(lnk, label) :
	lnk = lnk.replace("https://", label)
	lnk = lnk.replace("http://", label)
	return lnk.split("/")[0]
	
def strBetween(t, sep1, sep2) :
	pos1 = t.find(sep1) 
	if pos1 < 0 : return ""
	pos1 +=  len(sep1)
	pos2 = t.find(sep2, pos1)
	if  pos2 < 0 : return ""
	return t[pos1:pos2]

def findNearWords(inStr, w1, w2, max) :
	len1 = len(w1)
	len2 = len(w2)
	p1 = inStr.find(w1) 
	# # sharedVars.logte("premier p1 :" + str(p1))
	while p1 > -1 :
		p2 = inStr.find(w2, p1+len1)
		# # sharedVars.logte("p2 :" + str(p2))
		if p2 == -1 : 
			# # sharedVars.logte(w2 + " not Found")
			break
		if  p2-len2 - p1 + len1  < max :
			# # sharedVars.logte("found")
			return inStr[p1:p2+len2+2]
		p1 = inStr.find(w1, p2) 
		# # sharedVars.logte("p1 :" + str(p1))
	return ""

def cleanH(s, reg) :
	global CNL
	try :
		# removes pseudo \n
		s = s.replace(CNL, "")
		s = delMailAddrs(s).strip()

		if ", " in s :
			s = s.split(", ")
			# # sharedVars.logte("s1 {}, s2 {}".format(s[0], s[1]))
			s = s[1]
	finally :
		return s

def delMailAddrs(s) :
	lt = " &lt;"
	if s.startswith(lt) :
		s = s[4:]
	p = s.find("&lt;")
	if p != -1 :
		pS = s.find(" ", p)
		if pS != -1 : s= s.replace(s[p:pS], "")

	p = s.find("@") 
	if p != -1 :
		pS = s.find(" ", p)
		if pS != -1 : s= s.replace(s[p:pS], "")
	s = s.replace("via groups.io", "") 
	return s.replace("  ", " ")
	
# def detect_language(text):
	# response=urllib.urlopen("https://translate.yandex.net/api/v1.5/tr.json/detect?key=trnsl.1.1.20150410T053856Z.1c57628dc3007498.d36b0117d8315e9cab26f8e0302f6055af8132d7&"+urllib.urlencode({"text":text.encode('utf-8')})).read()
	# response=json.loads(response)
	# return response['lang']

