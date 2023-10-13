#-*- coding:utf-8 -*
import addonHandler
addonHandler.initTranslation()

import re, speech, winUser
from tones import beep
from time import sleep
from api import  getForegroundObject, getFocusObject, copyToClip, processPendingEvents
from comtypes.gen.ISimpleDOM import ISimpleDOMNode
from NVDAObjects.IAccessible import IAccessible
import controlTypes

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

		# Translators : do not translate nor remove %date_sender%. Replace french words, word 2 and word 5, by your translations. 
		# The  char Alt+0030 is a temporary replacement of \n
		lbls = _("On|Le%date_sender%wrote|écrit")
		lbls = str(lbls.replace("%date_sender%", "|"))
		lbls = lbls.split("|")
		
		self.onLg = lbls[0] 
		self.onEn = lbls[1]
		self.wroteLg = lbls[2] 
		self.wroteEn = lbls[3] 
		# sharedVars.tlog("lblON, lblWrote: {} {} {} {}".format(self.onLg, self.wroteLg, self.onEn, self.wroteEn))
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
		self.regHTML = re.compile ("<.+?>")
		# to removes  multiple spaces
		self.regMultiSpaces = re.compile(" {2,}")
		# to remove multi pseudo new line :  
		self.regMultiNL = re.compile(CNL + "{2,}")
		# to clean sender name
		self.regSender = re.compile("(|\n|&lt;| via groups\.io)")
		# replace \n that are after a letter or a digit with semicolon
		self.regSemi = re.compile("(\w|\d)\n")
		# v2 issueself.regSender = re.compile("(|&lt;| via (" + self.lblWrote  + "))")

	def readMail(self, oDoc, rev = False, spkMode=1): 
		speech.cancelSpeech()
		for i in range(0, 20) :
			if oDoc.role == controlTypes.Role.DOCUMENT and self.setDoc(oDoc, rev) :
				self.setText(spkMode)
				break
			else : 
				beep(1, 200)
				# sleep(0.1)
				oDoc =  getFocusObject()

	def setDoc(self, oDoc, nav=False): 
		# converts the doc into HTML code
		if not oDoc : return False 
		self.nav = nav
		self.text = "\n---" # alt+0031
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
		# # sharedVars.tlog(u"après  o.firstChild " + str(o.role)  + ", " + str(o.name))
		if not o : return False
		cCount =  oDoc.childCount
		
		if o.next :
			# beep(800, 40)
			#html simple
			# self.text = "\n---" 
			i = 1
			if cCount > 75 : speech.speakText(str(cCount) + _(" text elements. Press Control to stop."))
			while o :
				# # sharedVars.tlog(u"HTML elem:" + str(o.role)  + ", " + str(o.name))
				try : 
					obj = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
					s=obj.innerHTML 
					if not s :s= o.name
				except :
					s = "error retriving innerHTML"
					pass
					
				if s :self.text += s + CNL # + CNL required for not self.quoteMode
				if winUser.getKeyState(winUser.VK_CONTROL)&32768:
					beep(100, 30)
					return True

				i += 1
				if cCount > 100 :
					perc = (i / cCount) * 100
					if perc % 10 == 0 :
						if perc == 50.0 : beep(350, 20)
						else : beep(350, 2) # message(str(int(perc)) + "%")
				try : o=o.next
				except : break # fix v 3.4.1
		else: # plain Text
			# self.text = "\n---"
			o = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			# # sharedVars.tlog("brut:" + str(o))
			self.text += str(o.innerHTML)
		return True

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
		if self.quoteMode :				
			self.lItems.reverse()
		self.lastItem = len(self.lItems) - 1

		# build quotes indexes list
		self.lQuotes = [idx for (idx, item) in enumerate(self.lItems) if item.startswith("")]
		qCount = len(self.lQuotes) + (1 if self.quoteMode else 0)
		msg = msg.format(qCount, self.lastItem + 1)
		# find first non emptuy line 
		while self.lastItem > 0 and self.curItem < 20 :
			# l =  str(self.lItems[self.curItem]).strip()
			# # sharedVars.tlog("litem [" + str(self.lItems[self.curItem]) + "]")
			if str(self.lItems[self.curItem]).strip() != "" :
				break
			self.curItem += 1
		if speakMode  > 0 :
			speech.speakText(msg + self.lItems[self.curItem])



	def speakText(self, freq=0, speakMode=1) :
		if freq > 0 :
			beep(freq, 40)
		msg = ""
		if speakMode == 2 :
			copyToClip(self.text)
			msg = _("Preview copied: ")
		
		speech.speakText(msg + self.text)

	def deleteMetas(self) :
		lbl = "<meta "
		metas = []
		p, pEnd = self.findWords(lbl)
		while p > -1 :
			p2 = self.text.find('">', pEnd) 
			if p2 == -1 : break
			b = self.text[p:p2] + '">'
			# # sharedVars.tlog("meta:" + b)
			metas.append(b)
			# next block
			p, pEnd = self.findWords(lbl, p2+2) # +2 is then len of ">
		if len(metas) == 0 : return
		for e in metas :
			# # sharedVars.tlog("e:" + e)
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
			# # sharedVars.tlog( "e: " + str(e))
			# # sharedVars.tlog( "self.text_link " + str(self.text_link))
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
		# # sharedVars.tlog("Search of {} from {}, found at : {} :".format(wLast, start, pEnd))
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

		# # sharedVars.tlog("reverse Search of new Line  from {} found at :{}, scanned=:{}".format(pEnd, pBeg, scanned))

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
			# # sharedVars.tlog("pS : {}, pE : {}, std header: {}".format(pS, pE, self.text[pS:pE]))
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
			
			# sharedVars.tlog("Old h :" + h)
			nh = str("--- ") + str(cleanH(h, self.regMultiSpaces))
			# sharedVars.tlog("new h :" + nh)
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
		# # sharedVars.tlog("from labels:" + lbls)
		# maybe for a future version > regHdr = "((" + lbls + ").+?" + self.subject + ")"
		# # sharedVars.tlog("regHdr:" + regHdr)
		p, pEnd = self.findWords(lbls)
		while p > -1 :
			p2 = self.text.find(self.subject, pEnd) 
			if p2 == -1 : break
			b = self.text[p:p2] + self.subject
			# # sharedVars.tlog("MS header:" + b)
			blocks.append(b)
			# next block
			p, pEnd = self.findWords(lbls, p2+lenSubj)
		if len(blocks) == 0 : return

		for e in blocks :
			# # sharedVars.tlog("to replace:" + e)
			# e may contain , a pseudo \n 
			t = "\n---" + getSenderName(e) + " " + _("wrote") + " : "
			# # sharedVars.tlog("t:" + t)
			self.text = self.text.replace(e, t)
			
		return
			# if utis.wordsMatchWord(search, e[0]) :
				# arr = str(e[0]).split(":")
				# if len(arr) > 2 :
					# repl = "--- " + getSenderName(arr[1]) + " " + _("wrote") + " :"
					# # sharedVars.tlog( "replacement : " + repl)

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
		# # sharedVars.tlog("retour getSenderName :" + s)
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
			speech.speakText(str(self.curItem+1) + ":" + self.lItems[self.curItem])
		else :
			speech.speakText(self.lItems[self.curItem])

	def skipQuote(self, n=1) :
		if self.lastItem == -1 : 			self.buildLists(False)
		# skips 1 quote before or after
		lastQuote = len(self.lQuotes) - 1
		if n == -1 :
			self.curQuote = lastQuote if self.curQuote == 0 else self.curQuote - 1
		elif n == 1 :
			self.curQuote = 0  if self.curQuote == lastQuote  else self.curQuote + 1

		self.curItem = self.lQuotes[self.curQuote]
		# return speech.speakText(" curquote {},  curItem {}".format(self.curQuote, self.curItem))
		speech.speakText(str(self.curQuote+1) + ":" + self.lItems[self.curItem])

	def findItem(self, expr) :
		if self.lastItem == -1 : 			self.buildLists(False)
		lIdx, wIdx = self.indexOf(expr, self.curItem)
		if lIdx > -1 :
			self.curItem = lIdx
			speech.speakText(self.lItems[lIdx])
		else :
			beep(120, 20)
	# self.lQuotes = [idx for (idx, item) in enumerate(self.lItems, self.curIndex) if item.find(expr) > -1]
		# try:
			# self.CurItem = self.lItems.index(expr) # ,self.curItem)
			# speech.speakText(self.lItems[self.curItem])
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
	# # sharedVars.tlog("retour getSenderName :" + s)
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
	# # sharedVars.tlog("premier p1 :" + str(p1))
	while p1 > -1 :
		p2 = inStr.find(w2, p1+len1)
		# # sharedVars.tlog("p2 :" + str(p2))
		if p2 == -1 : 
			# # sharedVars.tlog(w2 + " not Found")
			break
		if  p2-len2 - p1 + len1  < max :
			# # sharedVars.tlog("found")
			return inStr[p1:p2+len2+2]
		p1 = inStr.find(w1, p2) 
		# # sharedVars.tlog("p1 :" + str(p1))
	return ""

def cleanH(s, reg) :
	global CNL
	try :
		# removes pseudo \n
		s = s.replace(CNL, "")
		s = delMailAddrs(s).strip()

		if ", " in s :
			s = s.split(", ")
			# # sharedVars.tlog("s1 {}, s2 {}".format(s[0], s[1]))
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
	