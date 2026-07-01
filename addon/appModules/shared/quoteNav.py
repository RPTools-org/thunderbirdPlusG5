#-*- coding:utf-8 -*
# Thunderbird+G5.1
import addonHandler
addonHandler.initTranslation()

import re, speech, winUser
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
import utils115 as utils
import textDialog
import string

email_headers = {
	# Reference
	"en": ("From:", "Date:", "Sent:", "To:", "Subject:"),

	# ─── Western Europe ───────────────────────────────────────────
	"fr": ("De:", "Date:", "Envoyé:", "À:", "Objet:"),
	"de":    ("Von:", "Datum:", "Gesendet:", "An:", "Betreff:"),
	"es":    ("De:", "Fecha:", "Enviado:", "Para:", "Asunto:"),
	"pt":    ("De:", "Data:", "Enviado:", "Para:", "Assunto:"),
	"it":    ("Da:", "Data:", "Inviato:", "A:", "Oggetto:"),
	"nl":    ("Van:", "Datum:", "Verzonden:", "Aan:", "Onderwerp:"),
	"sv":    ("Från:", "Datum:", "Skickat:", "Till:", "Ämne:"),
	"no":    ("Fra:", "Dato:", "Sendt:", "Til:", "Emne:"),
	"da":    ("Fra:", "Dato:", "Sendt:", "Til:", "Emne:"),
	"fi":    ("Lähettäjä:", "Päivämäärä:", "Lähetetty:", "Vastaanottaja:", "Aihe:"),
	"is":    ("Frá:", "Dagsetning:", "Sent:", "Til:", "Efni:"),
	"ga":    ("Ó:", "Dáta:", "Seolta:", "Chuig:", "Ábhar:"),
	"ca":    ("De:", "Data:", "Enviat:", "Per a:", "Assumpte:"),
	"eu":    ("Nork:", "Data:", "Bidalita:", "Nori:", "Gaia:"),
	"gl":    ("De:", "Data:", "Enviado:", "Para:", "Asunto:"),
	"lb":    ("Vun:", "Datum:", "Geschéckt:", "Un:", "Betreff:"),
	"mt":    ("Minn:", "Data:", "Mibgħut:", "Lil:", "Suġġett:"),

	# ─── Eastern Europe ───────────────────────────────────────────
	"pl":    ("Od:", "Data:", "Wysłano:", "Do:", "Temat:"),
	"cs":    ("Od:", "Datum:", "Odesláno:", "Komu:", "Předmět:"),
	"sk":    ("Od:", "Dátum:", "Odoslané:", "Komu:", "Predmet:"),
	"hu":    ("Feladó:", "Dátum:", "Elküldve:", "Címzett:", "Tárgy:"),
	"ro":    ("De la:", "Dată:", "Trimis:", "Către:", "Subiect:"),
	"bg":    ("От:", "Дата:", "Изпратено:", "До:", "Относно:"),
	"hr":    ("Od:", "Datum:", "Poslano:", "Za:", "Predmet:"),
	"sr":    ("Од:", "Датум:", "Послато:", "За:", "Предмет:"),
	"sl":    ("Od:", "Datum:", "Poslano:", "Za:", "Zadeva:"),
	"bs":    ("Od:", "Datum:", "Poslano:", "Za:", "Predmet:"),
	"mk":    ("Од:", "Датум:", "Испратено:", "До:", "Предмет:"),
	"sq":    ("Nga:", "Data:", "Dërguar:", "Për:", "Subjekti:"),
	"uk":    ("Від:", "Дата:", "Надіслано:", "Кому:", "Тема:"),
	"ru":    ("От:", "Дата:", "Отправлено:", "Кому:", "Тема:"),
	"be":    ("Ад:", "Дата:", "Адпраўлена:", "Каму:", "Тэма:"),
	"lv":    ("No:", "Datums:", "Nosūtīts:", "Kam:", "Temats:"),
	"lt":    ("Nuo:", "Data:", "Išsiųsta:", "Kam:", "Tema:"),
	"et":    ("Saatja:", "Kuupäev:", "Saadetud:", "Saaja:", "Teema:"),
	"el":    ("Από:", "Ημερομηνία:", "Στάλθηκε:", "Προς:", "Θέμα:"),

	# ─── Latin America ────────────────────────────────────────────
	"es_419": ("De:", "Fecha:", "Enviado:", "Para:", "Asunto:"),        # Spanish (Latin America)
	"pt_BR":  ("De:", "Data:", "Enviado em:", "Para:", "Assunto:"),     # Brazilian Portuguese

	# ─── Oceania ──────────────────────────────────────────────────
	"mi":    ("Mai:", "Rā:", "Tukuna:", "Ki:", "Kaupeka:"),             # Māori
	"tl":    ("Mula:", "Petsa:", "Ipinadala:", "Sa:", "Paksa:"),        # Filipino/Tagalog

	# ─── Asia ─────────────────────────────────────────────────────
	"zh_CN": ("发件人:", "日期:", "发送时间:", "收件人:", "主题:"),         # Simplified Chinese
	"zh_TW": ("寄件人:", "日期:", "傳送時間:", "收件人:", "主旨:"),         # Traditional Chinese
	"ja":    ("差出人:", "日付:", "送信日時:", "宛先:", "件名:"),            # Japanese
	"ko":    ("보낸 사람:", "날짜:", "보낸 날짜:", "받는 사람:", "제목:"),    # Korean
	"hi":    ("प्रेषक:", "दिनांक:", "भेजा गया:", "प्रति:", "विषय:"),      # Hindi
	"bn":    ("প্রেরক:", "তারিখ:", "পাঠানো হয়েছে:", "প্রাপক:", "বিষয়:"), # Bengali
	"ur":    ("از:", "تاریخ:", "ارسال شده:", "به:", "موضوع:"),           # Urdu
	"fa":    ("از:", "تاریخ:", "ارسال‌شده:", "به:", "موضوع:"),           # Persian/Farsi
	"ar":    ("من:", "التاريخ:", "المُرسَل:", "إلى:", "الموضوع:"),       # Arabic
	"he":    ("מאת:", "תאריך:", "נשלח:", "אל:", "נושא:"),               # Hebrew
	"tr":    ("Kimden:", "Tarih:", "Gönderildi:", "Kime:", "Konu:"),     # Turkish
	"az":    ("Kimdən:", "Tarix:", "Göndərildi:", "Kimə:", "Mövzu:"),   # Azerbaijani
	"kk":    ("Жіберуші:", "Күні:", "Жіберілді:", "Алушы:", "Тақырып:"), # Kazakh
	"uz":    ("Kimdan:", "Sana:", "Yuborildi:", "Kimga:", "Mavzu:"),    # Uzbek
	"ky":    ("Кимден:", "Дата:", "Жөнөтүлдү:", "Кимге:", "Тема:"),    # Kyrgyz
	"mn":    ("Илгээгч:", "Огноо:", "Илгээсэн:", "Хүлээн авагч:", "Сэдэв:"), # Mongolian
	"my":    ("ပို့သူ:", "ရက်စွဲ:", "ပို့ပြီး:", "လက်ခံသူ:", "အကြောင်းအရာ:"), # Burmese
	"th":    ("จาก:", "วันที่:", "ส่งเมื่อ:", "ถึง:", "เรื่อง:"),         # Thai
	"km":    ("ពី:", "កាលបរិច្ឆេទ:", "បានផ្ញើ:", "ទៅ:", "ប្រធានបទ:"),   # Khmer
	"vi":    ("Từ:", "Ngày:", "Đã gửi:", "Đến:", "Chủ đề:"),            # Vietnamese
	"id":    ("Dari:", "Tanggal:", "Terkirim:", "Kepada:", "Subjek:"),   # Indonesian
	"ms":    ("Daripada:", "Tarikh:", "Dihantar:", "Kepada:", "Subjek:"), # Malay
	"ta":    ("அனுப்பியவர்:", "தேதி:", "அனுப்பப்பட்டது:", "பெறுநர்:", "பொருள்:"), # Tamil
	"te":    ("నుండి:", "తేదీ:", "పంపబడింది:", "కు:", "విషయం:"),        # Telugu
	"ka":    ("გამომგზავნი:", "თარიღი:", "გაგზავნილია:", "მიმღები:", "თემა:"), # Georgian
	"hy":    ("Ուղարկողը:", "Ամսաթիվ:", "Ուղարկված է:", "Ստացողը:", "Թեմա:"), # Armenian
	"ne":    ("बाट:", "मिति:", "पठाइयो:", "लाई:", "विषय:"),             # Nepali
	"si":    ("සිට:", "දිනය:", "යවන ලදී:", "වෙත:", "විෂය:"),            # Sinhala

	# ─── Africa ───────────────────────────────────────────────────
	"sw":    ("Kutoka:", "Tarehe:", "Imetumwa:", "Kwenda:", "Mada:"),    # Swahili
	"am":    ("ከ:", "ቀን:", "ተልኳል:", "ለ:", "ርዕሰ ጉዳይ:"),               # Amharic
	"ha":    ("Daga:", "Kwanan wata:", "An aika:", "Zuwa:", "Taken:"),   # Hausa
	"yo":    ("Lati:", "Ọjọ:", "Ti firanṣẹ:", "Si:", "Koko ọrọ:"),      # Yoruba
	"ig":    ("Site na:", "Ụbọchị:", "Ezigara:", "Nye:", "Isiokwu:"),   # Igbo
	"zu":    ("Ovela:", "Usuku:", "Ithunyelwe:", "Kuya:", "Isihloko:"),  # Zulu
	"xh":    ("Evela:", "Umhla:", "Ithunyelwe:", "Kuya:", "Isihloko:"), # Xhosa
	"af":    ("Van:", "Datum:", "Gestuur:", "Aan:", "Onderwerp:"),       # Afrikaans
	"so":    ("Laga:", "Taariikhda:", "La diray:", "Loo diray:", "Mawduuca:"), # Somali
	"rw":    ("Uvuye:", "Italiki:", "Yoherejwe:", "Uyu:", "Insanganyamatsiko:"), # Kinyarwanda
}

CNL = ",lf,"

# function generated by Claude AI
def getCiteHeader(lang="en"):
	"""
	Returns the Outlook email header tuple for the requested language.
	Falls back to English if the language is not found.

	Parameter:
		lang (str): language code (e.g. "fr", "de", "ar"...). Default: "en"

	Returns:
		tuple: (From, Date, Sent, To, Subject) in the requested language
	"""
	global email_headers

	return email_headers.get(lang, email_headers["en"])

class QuoteNav() :
	
	text =  subject = ""
	# the following variables are list indexes
	curItem =  lastItem = curQuote = 0

	def __init__(self) :
		self.debug = False
		self.debugLog = ""
		self.clean = not sharedVars.oSettings.getOption("mainWindow", "CleanPreview") 
		self.text = ""
		self.lLines   = []
		self.lQuotes = []
		self.nav = False
		self.translate = False # 2024.01.02
		self.browseTranslation = sharedVars.oSettings.getOption("mainWindow", "browseTranslation")
		self.browsePreview = sharedVars.oSettings.getOption("mainWindow", "browsePreview")
		self.fromSpellCheck = False
		self.iTranslate = None
		self.langTo = utis.getLang()

		# Translators : do not translate nor remove %date_sender%. Replace french words, word 2 and word 5, by your translations. 
		lbls = _("On|Le%date_sender%wrote|écrit")
		lbls = str(lbls.replace("%date_sender%", "|"))
		lbls = lbls.split("|")
		count = len(lbls)
		self.onLg = lbls[0] if count > 0 else ""
		self.onEn = lbls[1]  if count > 1 else ""
		self.wroteLg = lbls[2] if count > 2 else "" 
		self.wroteEn = lbls[3]  if count > 3 else "" 
		# sharedVars.logte("lblON, lblWrote: {} {} {} {}".format(self.onLg, self.wroteLg, self.onEn, self.wroteEn))
		# reg expressions
		# s = "(( |§|\w|\d){1,}(" + lbls[0] + ") .*?(" + lbls[1] + ")(:§| :§|:| :))"
		# # s = "(\d{4} .*?(" + lbls[1] + ")(:§| :§|:| :))" 
		# compilation
		# self.regStdHdr = re.compile(s)
		# removes special &char;
		self.regHTMLChars = re.compile("(&lt;|&gt;)") 
		# link tags
		self.regLink = re.compile("(\<a .+?\>(.+?)\</a\>)")
		# All HTML tags
		self.regHTML = re.compile("\<.+?\>")
		# to removes  multiple spaces
		self.regMultiSpaces = re.compile(" {2,}")
		# to remove multi \n
		self.regMultiNL = re.compile(r"\n{2,}")
		# replace \n that are after a letter or a digit with semicolon
		# self.regSemi = re.compile("(\w|\d)\n")
		self.regTextTags = re.compile("<span|<a|<p|<li|<td")
		# v2 issueself.regSender = re.compile("(§|&lt;| via (" + self.lblWrote  + "))")
		# self.regSubject = re.compile(u"(Re:|Ré )")
		# self.regListName = re.compile ("\[.*\]|\{.*\}") # compile ("\[(.*)\]")
	def toggleTranslation(self) :
		msgEnab = _("Enabling message translation mode, ready.")
		msgDisab = _("Disabling message translation mode, ready.")

		if self.translate : 
			self.translate = False 
			self.iTranslate = None
			return utils.message(msgDisab)
		try : 
			self.iTranslate = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
			# sharedVars.logte("Instant Translate :" + str(self.iTranslate))
		except :
			pass
		
		if not self.iTranslate :
			return utils.message(_("The Instant Translate add-on is not active or not installed."))
		self.translate = True
		utils.message(msgEnab)

	def toggleBrowseMessage(self) :
		# Translators : brace symbols will be replaced by the words enabling or disabling
		msgEnab = _("Enabling message display mode, ready.")
		msgDisab = _("Disabling message display mode, ready.")
		self.browsePreview = not   self.browsePreview
		utils.message(msgEnab if self.browsePreview else msgDisab)
	def readMail(self, oFocus, oDoc, rev = False, spkMode=1): 
		if self.debug :
			sharedVars.debugLog = "ReadMail\n"
			sharedVars.log(oDoc, "oDoc") 
			sharedVars.log(oFocus, "oFocus") 

		# spkMode : 1 with utils.longText, 2=copyToClip, 10 with ui.message
		speech.cancelSpeech()
		for i in range(0, 20) :
			if oDoc.role == controlTypes.Role.DOCUMENT :
				result = self.setDoc(oDoc, rev)
				if self.debug : sharedVars.logte("Converted message\n" + self.text)
				if result == 1 : 
					self.setText(spkMode) 
					break
				elif result == 2 : 
					# beep(100, 20)
					callLater(250, self.setText, spkMode) 
					# self.sayDraftText()
					break
				elif result == 3 :  # after  an exception with IAccessible.queryInterface
					utils.sayLongText(self.text, speech=True)
					break
			else : 
				if i % 10 == 0 :
					beep(350, 5)
				# sleep(0.1)
				oDoc =  getFocusObject()

	def setDoc(self, oDoc, nav=False, fromSpellCheck=False): 	
		# converts the doc into HTML code
		if not oDoc : 
			beep(100, 30)
			return 0 
		self.nav = nav
		self.fromSpellCheck = fromSpellCheck
		self.text = ""
		self.lLines = []
		self.lQuotes = []
		self.lastLine = self.lastQuote = -1
		self.curLine =  self.curQuote = 0		
		# document without subject as name 
		parID = str(utis.getIA2Attribute(oDoc.parent))
		if parID in ("messageEditor", "spellCheckDlg") :
			self.quoteMode = False
			# sharedVars.log(oDoc, "oDoc in message Editor")
		else :
			self.quoteMode = True

		self.subject = getEndSubject(parID)
		# sharedVars.logte("self.subject=" + self.subject)

		o=oDoc.firstChild # section ou paragraph
		# 2025-01-10 log à désactiver
		# sharedVars.log(o, u"après  oDoc.firstChild ")
		if not o : return 0
		cCount =  oDoc.childCount
		
		if o.next :
			# sharedVars.log(o.next, "quoteNav, o.next  ") 
			# beep(800, 40)
			#html simple
			# self.text = "-§" 
			i = 1
			while o :
				# # sharedVars.logte(u"HTML elem:" + str(o.role)  + ", " + str(o.name))
				try : 
					obj = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
					s=obj.innerHTML 
					if not s :s= o.name
				except :
					self.getMessageByObjects(oDoc.firstChild, "HTML")
					return 3
				if s :self.text += s + CNL # + CNL required for not self.quoteMode
				# if cCount > 75 and s and self.regTextTags.search(s) :
				if (i % 10  == 0) and s and self.regTextTags.search(s) :
					beep(350,5)
				if winUser.getKeyState(winUser.VK_CONTROL)&32768:
					return 2
				i += 1
				try : o=o.next
				except : break
		else: # plain Text
			# sharedVars.log(o, "quoteNav plainText before queryInterface o") 
			# self.text = "-§"
			try :
				o = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			except :
				self.getMessageByObjects(o, "TEXT")
				return 3
			# # sharedVars.logte("brut:" + str(o))
			self.text += str(o.innerHTML)
		return 1

	def getMessageByObjects(self, obj,kind="") :
		# message("Please wait " + " " + kind)
		utils.message(_("Please wait"))
		i = 0
		for child in obj.recursiveDescendants:
			if hasattr(child, "name") :
				if child.name :
					self.text += str(child.name) + "\n"
					i += 1
			if i == 75 : 
				break

	def sayDraftText(self) :
		self.text=self.regHTMLChars.sub(" ",self.text)
		self.text=self.regHTML.sub(" ",self.text)
		# beep(100, 20)
		# sharedVars.debugLog = "Draft :\n" + self.text
		callLater(500, utils.sayLongText, self.text, True)
	
	def getDocObjects(self, oDoc) :
		o = oDoc.firstChild
		while o :
			o = o.next
	

	def setText(self, speakMode=1) : 
		# speakMode : 1 with utils.longText, 2=copyToClip, 10 with ui.message
		# textDialog.showText("code HTML", self.text) ; return
		# prepare text for removing outlook and Windows mail headers
		self.deleteBlocks()
		# cite Thunderbird
		self.text = self.text.replace('<div class="moz-cite-prefix">', "\n-§")
		# cite iPhone
		self.text = self.text.replace('<span class="moz-txt-citetags">', "\n-§")
		self.text = self.text.replace("\r", "").replace("\n", ",lf,").replace("<br>", ",br,").replace("<span>", "").replace("&nbsp;", " ").replace("<b>", "").replace("</b>", "")
		# copyToClip(self.text)
		# return beep(250, 30)
		self.cleanLinks()
		# beep(100, 40)
		# copyToClip("Before compress MSHeaders\n" + self.text)
		self.compressMicrosoftHeaders(utis.getLang())
		# removes special &char;
		self.text=self.regHTMLChars.sub(" ",self.text)
		# Removes of all remaining HTML tags
		self.text=self.regHTML.sub("",self.text)
			# removes multiple spaces 
		self.text=self.regMultiSpaces.sub(" ",self.text)
		# replace pseudo ,lf,  and br
		self.text = self.text.replace(",lf,", "\n").replace(",br,", "\n")
		# removes multiple \n
		self.text=self.regMultiNL.sub("\n",self.text)

		# removes multiple  spaces again
		self.text = self.regMultiSpaces.sub(" ", self.text)
		self.text = self.text.replace("\n ", "") 
		# replace msgStart
		self.text = self.text.replace("msgStart", "\n")
		if not self.nav : # text
			if speakMode > 0 :
				self.speakText(0, speakMode)
		else :
			self.buildLists(speakMode)

	def buildLists(self, speakMode) :
		# self.lLines = []
		# self.lQuotes = []
		# self.lastLine = self.lastQuote = -1
				# 1: split text into lines
		txt = self.text.strip()
		# li nes are already separated by \n
		msgLines = _("{0} messages, {1} lines, ")
		# split text into lines
		needless = " ;" # string.punctuation + string.whitespace
		self.lLines = [line for line in txt.splitlines() if line.strip(needless)]
		self.lastLine = len(self.lLines) -1 		
		self.curLine = 0
		if self.lastLine == -1:
			beep(200, 20)
			return
		if self.fromSpellCheck :
			self.lQuotes = []
			self.lastQuote = -1
			self.curQuote = 0
			return

		# 2: split the text into quotes
		# lines are separated by "\n". This char can not be in the generated list
		txt =  self.text.replace("\n", " ").strip(" \n")
		txt =self.regMultiSpaces.sub(" ", txt)
		
		# quotes are separated by -§
		msgQuotes  = _("{0} messages in chronological order, ") 
		# split text into quotes
		self.lQuotes =  txt.split("-§")
		# self.lQuotes = txt.splitlines()
		txt = ""
		self.lastQuote = len(self.lQuotes) - 1
		self.curQuote  = 0
		if self.lastQuote  > -1  and not self.translate : 
			self.lQuotes.reverse()
			self.text = "\n".join(self.lQuotes) 

		msg = msgQuotes.format(self.lastQuote + 1)
		if speakMode  == 1 : # with utils115.message
				utils.sayLongText(msg + self.text)
		elif speakMode  == 10 : # with ui.message
			speech.speakMessage(msg + self.lQuotes[self.curQuote])
			utils.setBrailleMode(sharedVars.msgOpened)

	def displayMessage(self, subj, body) :
		if subj == "" : subj = _("Translation")
		body = body.replace("§\n", "").strip()
		textDialog.showText(title=subj, text=body, label="-")

	def truncateSubj(self, text, wantedLen) :
		# text=self.regSubject.sub("",text)
		# text=self.regListName.sub("",text)
		# text=self.regMultiSpaces.sub(" ", text)
		lenText = len(text)
		if lenText  <= wantedLen : return text 
		pos = wantedLen - 1
		while pos < lenText :
			if text[pos] == " " :
				return text[0:pos]
			pos += 1
		return text

	def getFirstMessages(self):
		sep = "-§"
		n = 2
		maxLen = 4950
		pos = 0
		for _ in range(n):
			idx = self.text.find(sep, pos)
			if idx == -1: # Plus de séparateur trouvé
				return self.text[:maxLen]
			pos = idx + len(sep)
		t =  self.text[:pos - len(sep)]
		return t[:maxLen]

	# def getFirstMessages(self, max=2):
		# # On découpe la chaîne en ignorant le premier élément vide avant le premier -§
		# # On utilise filter(None) pour nettoyer d'éventuels espaces ou résidus
		# messages = [msg.strip() for msg in self.text.split("-§") if msg.strip()]
		
		# count = len(messages)
		
		# if count >= 2:
			# return str(messages[:2]).replace("\\n", chr(10))
		# elif count > 0 :
			# return str(messages[:1]).replace("\\n", chr(10))
		# else:
			# return "No message found."
			
	def speakText(self, freq=0, speakMode=1) :
		# if freq > 0 :
		msg = ""
		if speakMode == 2 :
			# copyToClip(self.text)
			msg = _("Preview copied: ")
		
		if self.translate : 
			beep(500, 100) # same sound as in InstantTranslate
			subject =   self.iTranslate.translateAndCache(cleanSubject(sharedVars.curWinTitle), "auto", self.langTo).translation
			subject = self.truncateSubj(subject, 35)
			text = self.iTranslate.translateAndCache(self.getFirstMessages(), "auto", self.langTo).translation
			# pos = str(text.find("\r"))
			# sharedVars.logte("Translated:\nCR pos=" + pos + "\n" + text)
			if self.browseTranslation or self.browsePreview and not self.fromSpellCheck : self.displayMessage(subject, text)
			else : 
				if speakMode == 1 : utils.sayLongText(msg + subject + "\n" + text, True)
				elif speakMode == 10 : 
					speech.speakMessage(msg + subject + text)
					utils.setBrailleMode(sharedVars.msgOpened)
		else : # no translation
			if self.browsePreview and not self.fromSpellCheck  : 
				subject = cleanSubject(sharedVars.curWinTitle)
				subject = self.truncateSubj(subject, 25)
				self.displayMessage(subject, self.text)
			else : 
				if speakMode == 1 : utils.sayLongText(msg + self.text, True)
				elif speakMode == 10 : 
					speech.speakMessage(msg + self.text)
					utils.setBrailleMode(sharedVars.msgOpened)

	def speakQuote(self, quote) :
		if self.translate : 
			quote  = self.iTranslate.translateAndCache(quote, "auto", self.langTo).translation
		if self.browseTranslation and not self.fromSpellCheck : self.displayMessage("", quote) 
		else : 
			utils.sayLongText(quote, True)

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

		# delete Gmail's forwarded message
		if self.text.find("-- Forwarded message") > -1 :
			s = '<div dir="ltr" class="gmail_attr">---------- Forwarded message ---------'
			reg = re.compile(s + ".+?\</div\>")
			self.text = reg.sub("", self.text)

		
		self.deleteMetas()
		# removes style css tag
		if self.text.find("<style>") > 0 :
			regExp = re.compile("\<style\>.+?\</style\>")
			self.text=regExp.sub (" ",self.text)

		#  removes table of mozilla headers
		p = self.text.find('<table class="moz-email-headers-table">')
		if p != -1 :
			p2 = self.text.find("</table>", p+25)
			if p2 != -1 :
				self.text = self.text.replace(self.text[p:p2], "") 
		
		# group footers : one group in a message, we  use return after a footer  deletion
		#Removes   de google groupe  footer
		# beep(100, 40)
		# copyToClip(self.text)
		tags = [
			"</div>-- <br>",
			"--&nbsp;<br></span>",
			'<p class="MsoNormal">-- <br>',
			"-- <br>",
			"--&nbsp;<br>",
		]
		pos = self.text.rfind("+unsubscribe@googlegroups.com")
		if pos != -1:
			for t in tags :
				posTag = self.text.find(t)
				if posTag != -1 :
					break
			if posTag != -1 :
					self.text = self.text[:posTag]
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
			linkTag = str(e[0]) # contains <a until </a>
			# linkText = e[1] # the visible part of the link
			# sharedVars.logte("linkTag=" + linkTag)
			match = re.search(r'href="([^"]+)"', linkTag)
			if match:
				hRef = match.group(1)
			else:
				hRef = ""
			# sharedVars.logte("hRef=" + hRef)
			if "@" in e[1] : # link text is a mail address
				hRef = e[1].replace("@", "|arob|")
			elif "mailto" in hRef : 
				hRef = e[1] # link text is not a mail  address
				if " via "  in hRef : 
					hRef = hRef.split(" via ")[0].strip(" '")
			elif "http" in hRef :
				if "http" not in e[1] : 
					hRef =e[1] + ", " + hRef 
				hRef = shortenUrl(hRef, lbl)
			
			self.text = self.text.replace (linkTag, hRef.replace(",lf,", ""))
			# end of loop
		self.text = self.text.replace("|arob|", "@")
		
	def getTextBlock(self, start, end):
		"""
	Returns the text substring between 'start' and 'end' inclusive.
		If one of the tags is not found, returns an empty string.	"""
		startIdx = self.text.find(start)
		if startIdx == -1:
			return ""
		
		endIdx = self.text.find(end, startIdx + len(start))
		if endIdx == -1:
			return ""
		
		return self.text[startIdx : endIdx + len(end)]

	def replaceAllBlocks(self, blStart, blEnd, replace="") :
		block = self.getTextBlock(blStart, blEnd)
		if self.debug and block : self.debugLog += "\n" + "First Block found between {} and {} : {}".format(blStart, blEnd, block)
		while block :
			self.text = self.text.replace(block, replace)
			block = self.getTextBlock(blStart, blEnd)
			if self.debug and block : self.debugLog += "\n" + "Next Block found between {} and {} : {}".format(blStart, blEnd, block)

	def normalizeFrenchHeaders(self) :
		# Because they are inconsistent, normalize French headers that use a space before colon
		if "De :" not in self.text :
			return
		self.text = self.text.replace("De :", "De:")
		self.text = self.text.replace("Envoyé :", "Envoyé:")
		self.text = self.text.replace("À :", "À:")
		self.text = self.text.replace("A :", "À:")
		self.text = self.text.replace("Objet :", "Objet:")

	def compressMicrosoftHeaders(self, lang="EN"):
		global email_headers
		# some simplifications
		self.text = self.text.replace("<div>", ",lf,").replace("</div>", ",br,")
		self.normalizeFrenchHeaders()
		if self.debug :
			self.debugLog = "Before MS header compression\n" + self.text.replace(">", ">\n")
		# headers in NVDA language
		from_t, date_t, sent_t, to_t, subject_t = getCiteHeader(lang)
		# sharedVars.logte("Headers t = {} {} {} {}".format(from_t, date_t, sent_t, to_t, subject_t))
		
		for lang_code, headers in email_headers.items():
			from_h, date_h, sent_h, to_h, subject_h = headers
			# remove to headers
			self.replaceAllBlocks(to_h, ",br,", ",lf,") 
			self.replaceAllBlocks(to_h, ",lf,", ",lf,") 
			# remove headers from transferred message with MSO
			# self.replaceAllBlocks(",br," + to_h, "</p>", "msgStart")

			# subject headers 
			self.replaceAllBlocks(subject_h, "</p>", "msgStart")
			self.replaceAllBlocks(subject_h, ",lf", "msgStart")

			# self.replaceAllBlocks(to_h, ",br,", "") 
			# translate From:
			self.text = self.text.replace(from_h, from_t)
			# replace Sent: by a comma
			# MSO
			self.text = self.text.replace(",br," + sent_h, ", ")
			# WinMail
			self.text = self.text.replace(sent_h, ", ")


		# final replacements
		self.text = self.text.replace(from_t, "\n-§" + from_t)
		self.text = self.text.replace("@googlegroups.com", " at GG")
		self.text = self.text.replace("groups.io", " at GIO")
		# msgStart  will be replaced after the call of this function
		if self.debug : 
			# copyToClip(self.debugLog + "\nResult\n" + self.text)
			sharedVars.debugLog = self.debugLog
			self.debugLog = ""

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
		#  header may contain §
		

		# On Behalf Of Isabellevia groups.ioSent 
		if "Behalf Of" in header :
			s = strBetween(header, "Behalf Of", "via groups").strip()  
		elif  "via groups.io" in header : 
			# to replace:From: §  Jeremy T. via groups.io: 
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
	def skipLine(self, n=1) :
		if self.lastLine == -1 : 			self.s(False)
		# skips 1 item before or after
		if n == -1 :
			self.curLine = self.lastLine if self.curLine == 0 else self.curLine - 1
		elif n == 1 :
			self.curLine = 0  if self.curLine == self.lastLine  else self.curLine + 1
		self.speakQuote(self.lLines[self.curLine])

	def skipQuote(self, n=1) :
		if self.lastQuote == -1 : 			self.buildLists(False)
		# skips 1 quote before or after
		if n == -1 :
			self.curQuote = self.lastQuote if self.curQuote == 0 else self.curQuote - 1
		elif n == 1 :
			self.curQuote = 0  if self.curQuote == self.lastQuote  else self.curQuote + 1
		self.speakQuote(str(self.curQuote+1) + ":" + self.lQuotes[self.curQuote])

	def findLine(self, expr) : # for spellcheckDlg
		speech.cancelSpeech()
		if not hasattr(self, "lastLine") :
			msg = "Word search in text is currently unavailable. Press Escape followed by F5 to get it." 
			iTranslate = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
			if iTranslate :
				msg =   iTranslate.translateAndCache(msg, "auto", self.langTo).translation
			return utils.message(msg)
		if self.lastLine == -1 :
			self.buildLists(False)	
		lIdx, wIdx = self.indexOf(expr, self.curLine)
		if lIdx > -1 :
			self.curLine = lIdx
			self.speakQuote(self.lLines[lIdx])
		else :
			utils.message(_("Phrase not found."))

	def indexOf(self, word, start=0, backward=False) : 
		stopChar = "§" # alt+0031
		if not backward :
			step = 1
			# start is the same
			iLast = self.lastLine 
		else :
			step = -1
			iLast = 0
		
		for i in range(start, iLast, step) : 
			if i > start and stopChar in self.lLines[i] :
				break
			p = self.lLines[i].find(word)
			if p > -1 :
				return i, p
		
		return -1, -1

# normal functions
def getSenderName(header) :
	#  header may contain §
	

	# On Behalf Of Isabelle Delarue via groups.ioSent 
	if "Behalf Of" in header :
		s = strBetween(header, "Behalf Of", "via groups").strip()  
	elif  "via groups.io" in header : 
		# to replace:From: §  Jeremy T. via groups.io: 
		s = strBetween(header, ":", "via")
	else :
		# s = "à revoir : " + header
		header  = header.split(":") 
		s = (header[1] if len(header) > 1 else header[0])
		if "&lt;" in s :
			s = s.split("&lt;")[0]

	s = s.replace("§", " ").strip()
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

def getEndSubject(parentID) :
	# fo = getFocusObject()
	# role = fo.role
	# s = ""
	# if role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and utils.hasID(fo, "threadTree-row") :
		# s= utils.getColValue(fo, "subjectcol")
	# else :
	s  = utils.cleanWinTitle(sharedVars.curWinTitle)
	# get 2 last words
	aParts = s.split(" ")
	arrLen = len(aParts)
	if arrLen == 1 :
		return aParts[0]
	elif arrLen >= 2 : 
		arrLen -= 1
		return aParts[arrLen-1] + " " + aParts[arrLen]
	return s

	

def cleanSubject(subject) :
	subject = utils.cleanWinTitle(subject)
	i = subject.rfind("]")
	if i > -1 :
		subject = subject[i:]
	subject =  subject.replace("Re: ", "")
	return subject

