#-*- coding:utf-8 -*
# Thunderbird+G5.1
import addonHandler
addonHandler.initTranslation()

import re, speech, winUser
from wx import CallLater
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
from collections import namedtuple
# email_headers = {
	# # Reference
	# "en": ("From:", "Date:", "Sent:", "To:", "Subject:"),

	# # ─── Western Europe ───────────────────────────────────────────
	# "fr": ("De:", "Date:", "Envoyé:", "À:", "Objet:"),
	# "de":    ("Von:", "Datum:", "Gesendet:", "An:", "Betreff:"),
	# "es":    ("De:", "Fecha:", "Enviafdo:", "Para:", "Asunto:"),
	# "pt":    ("De:", "Data:", "Enviado:", "Para:", "Assunto:"),
	# "it":    ("Da:", "Data:", "Inviato:", "A:", "Oggetto:"),
	# "nl":    ("Van:", "Datum:", "Verzonden:", "Aan:", "Onderwerp:"),
	# "sv":    ("Från:", "Datum:", "Skickat:", "Till:", "Ämne:"),
	# "no":    ("Fra:", "Dato:", "Sendt:", "Til:", "Emne:"),
	# "da":    ("Fra:", "Dato:", "Sendt:", "Til:", "Emne:"),
	# "fi":    ("Lähettäjä:", "Päivämäärä:", "Lähetetty:", "Vastaanottaja:", "Aihe:"),
	# "is":    ("Frá:", "Dagsetning:", "Sent:", "Til:", "Efni:"),
	# "ga":    ("Ó:", "Dáta:", "Seolta:", "Chuig:", "Ábhar:"),
	# "ca":    ("De:", "Data:", "Enviat:", "Per a:", "Assumpte:"),
	# "eu":    ("Nork:", "Data:", "Bidalita:", "Nori:", "Gaia:"),
	# "gl":    ("De:", "Data:", "Enviado:", "Para:", "Asunto:"),
	# "lb":    ("Vun:", "Datum:", "Geschéckt:", "Un:", "Betreff:"),
	# "mt":    ("Minn:", "Data:", "Mibgħut:", "Lil:", "Suġġett:"),

	# # ─── Eastern Europe ───────────────────────────────────────────
	# "pl":    ("Od:", "Data:", "Wysłano:", "Do:", "Temat:"),
	# "cs":    ("Od:", "Datum:", "Odesláno:", "Komu:", "Předmět:"),
	# "sk":    ("Od:", "Dátum:", "Odoslané:", "Komu:", "Predmet:"),
	# "hu":    ("Feladó:", "Dátum:", "Elküldve:", "Címzett:", "Tárgy:"),
	# "ro":    ("De la:", "Dată:", "Trimis:", "Către:", "Subiect:"),
	# "bg":    ("От:", "Дата:", "Изпратено:", "До:", "Относно:"),
	# "hr":    ("Od:", "Datum:", "Poslano:", "Za:", "Predmet:"),
	# "sr":    ("Од:", "Датум:", "Послато:", "За:", "Предмет:"),
	# "sl":    ("Od:", "Datum:", "Poslano:", "Za:", "Zadeva:"),
	# "bs":    ("Od:", "Datum:", "Poslano:", "Za:", "Predmet:"),
	# "mk":    ("Од:", "Датум:", "Испратено:", "До:", "Предмет:"),
	# "sq":    ("Nga:", "Data:", "Dërguar:", "Për:", "Subjekti:"),
	# "uk":    ("Від:", "Дата:", "Надіслано:", "Кому:", "Тема:"),
	# "ru":    ("От:", "Дата:", "Отправлено:", "Кому:", "Тема:"),
	# "be":    ("Ад:", "Дата:", "Адпраўлена:", "Каму:", "Тэма:"),
	# "lv":    ("No:", "Datums:", "Nosūtīts:", "Kam:", "Temats:"),
	# "lt":    ("Nuo:", "Data:", "Išsiųsta:", "Kam:", "Tema:"),
	# "et":    ("Saatja:", "Kuupäev:", "Saadetud:", "Saaja:", "Teema:"),
	# "el":    ("Από:", "Ημερομηνία:", "Στάλθηκε:", "Προς:", "Θέμα:"),

	# # ─── Latin America ────────────────────────────────────────────
	# "es_419": ("De:", "Fecha:", "Enviado:", "Para:", "Asunto:"),        # Spanish (Latin America)
	# "pt_BR":  ("De:", "Data:", "Enviado em:", "Para:", "Assunto:"),     # Brazilian Portuguese

	# # ─── Oceania ──────────────────────────────────────────────────
	# "mi":    ("Mai:", "Rā:", "Tukuna:", "Ki:", "Kaupeka:"),             # Māori
	# "tl":    ("Mula:", "Petsa:", "Ipinadala:", "Sa:", "Paksa:"),        # Filipino/Tagalog

	# # ─── Asia ─────────────────────────────────────────────────────
	# "zh_CN": ("发件人:", "日期:", "发送时间:", "收件人:", "主题:"),         # Simplified Chinese
	# "zh_TW": ("寄件人:", "日期:", "傳送時間:", "收件人:", "主旨:"),         # Traditional Chinese
	# "ja":    ("差出人:", "日付:", "送信日時:", "宛先:", "件名:"),            # Japanese
	# "ko":    ("보낸 사람:", "날짜:", "보낸 날짜:", "받는 사람:", "제목:"),    # Korean
	# "hi":    ("प्रेषक:", "दिनांक:", "भेजा गया:", "प्रति:", "विषय:"),      # Hindi
	# "bn":    ("প্রেরক:", "তারিখ:", "পাঠানো হয়েছে:", "প্রাপক:", "বিষয়:"), # Bengali
	# "ur":    ("از:", "تاریخ:", "ارسال شده:", "به:", "موضوع:"),           # Urdu
	# "fa":    ("از:", "تاریخ:", "ارسال‌شده:", "به:", "موضوع:"),           # Persian/Farsi
	# "ar":    ("من:", "التاريخ:", "المُرسَل:", "إلى:", "الموضوع:"),       # Arabic
	# "he":    ("מאת:", "תאריך:", "נשלח:", "אל:", "נושא:"),               # Hebrew
	# "tr":    ("Kimden:", "Tarih:", "Gönderildi:", "Kime:", "Konu:"),     # Turkish
	# "az":    ("Kimdən:", "Tarix:", "Göndərildi:", "Kimə:", "Mövzu:"),   # Azerbaijani
	# "kk":    ("Жіберуші:", "Күні:", "Жіберілді:", "Алушы:", "Тақырып:"), # Kazakh
	# "uz":    ("Kimdan:", "Sana:", "Yuborildi:", "Kimga:", "Mavzu:"),    # Uzbek
	# "ky":    ("Кимден:", "Дата:", "Жөнөтүлдү:", "Кимге:", "Тема:"),    # Kyrgyz
	# "mn":    ("Илгээгч:", "Огноо:", "Илгээсэн:", "Хүлээн авагч:", "Сэдэв:"), # Mongolian
	# "my":    ("ပို့သူ:", "ရက်စွဲ:", "ပို့ပြီး:", "လက်ခံသူ:", "အကြောင်းအရာ:"), # Burmese
	# "th":    ("จาก:", "วันที่:", "ส่งเมื่อ:", "ถึง:", "เรื่อง:"),         # Thai
	# "km":    ("ពី:", "កាលបរិច្ឆេទ:", "បានផ្ញើ:", "ទៅ:", "ប្រធានបទ:"),   # Khmer
	# "vi":    ("Từ:", "Ngày:", "Đã gửi:", "Đến:", "Chủ đề:"),            # Vietnamese
	# "id":    ("Dari:", "Tanggal:", "Terkirim:", "Kepada:", "Subjek:"),   # Indonesian
	# "ms":    ("Daripada:", "Tarikh:", "Dihantar:", "Kepada:", "Subjek:"), # Malay
	# "ta":    ("அனுப்பியவர்:", "தேதி:", "அனுப்பப்பட்டது:", "பெறுநர்:", "பொருள்:"), # Tamil
	# "te":    ("నుండి:", "తేదీ:", "పంపబడింది:", "కు:", "విషయం:"),        # Telugu
	# "ka":    ("გამომგზავნი:", "თარიღი:", "გაგზავნილია:", "მიმღები:", "თემა:"), # Georgian
	# "hy":    ("Ուղարկողը:", "Ամսաթիվ:", "Ուղարկված է:", "Ստացողը:", "Թեմա:"), # Armenian
	# "ne":    ("बाट:", "मिति:", "पठाइयो:", "लाई:", "विषय:"),             # Nepali
	# "si":    ("සිට:", "දිනය:", "යවන ලදී:", "වෙත:", "විෂය:"),            # Sinhala

	# # ─── Africa ───────────────────────────────────────────────────
	# "sw":    ("Kutoka:", "Tarehe:", "Imetumwa:", "Kwenda:", "Mada:"),    # Swahili
	# "am":    ("ከ:", "ቀን:", "ተልኳል:", "ለ:", "ርዕሰ ጉዳይ:"),               # Amharic
	# "ha":    ("Daga:", "Kwanan wata:", "An aika:", "Zuwa:", "Taken:"),   # Hausa
	# "yo":    ("Lati:", "Ọjọ:", "Ti firanṣẹ:", "Si:", "Koko ọrọ:"),      # Yoruba
	# "ig":    ("Site na:", "Ụbọchị:", "Ezigara:", "Nye:", "Isiokwu:"),   # Igbo
	# "zu":    ("Ovela:", "Usuku:", "Ithunyelwe:", "Kuya:", "Isihloko:"),  # Zulu
	# "xh":    ("Evela:", "Umhla:", "Ithunyelwe:", "Kuya:", "Isihloko:"), # Xhosa
	# "af":    ("Van:", "Datum:", "Gestuur:", "Aan:", "Onderwerp:"),       # Afrikaans
	# "so":    ("Laga:", "Taariikhda:", "La diray:", "Loo diray:", "Mawduuca:"), # Somali
	# "rw":    ("Uvuye:", "Italiki:", "Yoherejwe:", "Uyu:", "Insanganyamatsiko:"), # Kinyarwanda
# }

CNL = ",lf,"
# function generated by Gemini
def iterLines(text):
	"""Generates lines from a string one by one to avoid memory allocation."""
	startPos = 0
	while True:
		endPos = text.find("\n", startPos)
		if endPos == -1:
			# Yield the remaining part of the string if not empty
			if startPos < len(text):
				yield text[startPos:]
			break
		yield text[startPos:endPos]
		startPos = endPos + 1

class QuoteNav():
	
	text =  subject = ""
	# the following variables are list indexes
	curItem =  lastItem = curQuote = 0

	def __init__(self):
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
		# Define the C-like structure. 
		# It has the exact same memory footprint as a standard tuple!
		self.EmailHeaders = namedtuple("EmailHeaders", ["from_", "date", "sent", "to", "subject", "on", "wrote"])

		# A single flat string representing the CSV data.
		self.rawHeaders = (
			"dummy;From:;Date:;Sent:;To:;Subject;On;wrote\n"
			"en;From:;Date:;Sent:;To:;Subject;On;wrote\n"
			"fr;De:;Date:;Envoyé:;À:;Objet;Le;a écrit\n"
			"de;Von:;Datum:;Gesendet:;An:;Betreff;Am;schrieb\n"
			"es;De:;Fecha:;Enviado:;Para:;Asunto;El;escribió\n"
			"pt;De:;Data:;Enviado:;Para:;Assunto;Em;escreveu\n"
			"it;Da:;Data:;Inviato:;A:;Oggetto;Il;ha scritto\n"
			"nl;Van:;Datum:;Verzonden:;Aan:;Onderwerp;Op;schreef\n"
			"sv;Från:;Datum:;Skickat:;Till:;Ämne;Den;skrev\n"
			"no;Fra:;Dato:;Sendt:;Til:;Emne;Den;skrev\n"
			"da;Fra:;Dato:;Sendt:;Til:;Emne;Den;skrev\n"
			"fi;Lähettäjä:;Päivämäärä:;Lähetetty:;Vastaanottaja:;Aihe;Kirjoitti;kirjoitti\n"
			"is;Frá:;Dagsetning:;Sent:;Til:;Efni;Þann;skrifaði\n"
			"ga;Ó:;Dáta:;Seolta:;Chuig:;Ábhar;Ar;scríobh\n"
			"ca;De:;Data:;Enviat:;Per a:;Assumpte;El;va escriure\n"
			"eu;Nork:;Data:;Bidalita:;Nori:;Gaia;Eguna;idatzi zuen\n"
			"gl;De:;Data:;Enviado:;Para:;Asunto;O;escribiu\n"
			"lb;Vun:;Datum:;Geschéckt:;Un:;Betreff;Am;schriwwen\n"
			"mt;Minn:;Data:;Mibgħut:;Lil:;Suġġett;Nhar;kiteb\n"
			"pl;Od:;Data:;Wysłano:;Do:;Temat;Dnia;napisał\n"
			"cs;Od:;Datum:;Odesláno:;Komu:;Předmět;Dne;napsal\n"
			"sk;Od:;Dátum:;Odoslané:;Komu:;Predmet;Dňa;napísal\n"
			"hu;Feladó:;Dátum:;Elküldve:;Címzett:;Tárgy;Ekkor;írta\n"
			"ro;De la:;Dată:;Trimis:;Către:;Subiect;Pe;a scris\n"
			"bg;От:;Дата:;Изпратено:;До:;Относно;На;написа\n"
			"hr;Od:;Datum:;Poslano:;Za:;Predmet;Dana;napisa\n"
			"sr;Од:;Датум:;Послато:;За:;Предмет;Дана;написа\n"
			"sl;Od:;Datum:;Poslano:;Za:;Zadeva;Dne;napisal\n"
			"bs;Od:;Datum:;Poslano:;Za:;Predmet;Dana;napisa\n"
			"mk;Од:;Датум:;Испратено:;До:;Предмет;На;напиша\n"
			"sq;Nga:;Data:;Dërguar:;Për:;Subjekti;Më;shkroi\n"
			"uk;Від:;Дата:;Надіслано:;Кому:;Тема;Дата;написав\n"
			"ru;От:;Дата:;Отправлено:;Кому:;Тема;Дата;написал\n"
			"be;Ад:;Дата:;Адпраўлена:;Каму:;Тэма;Дата;напісаў\n"
			"lv;No:;Datums:;Nosūtīts:;Kam:;Temats;Datums;rakstīja\n"
			"lt;Nuo:;Data:;Išsiųsta:;Kam:;Tema;Data;rašė\n"
			"et;Saatja:;Kuupäev:;Saadetud:;Saaja:;Teema;Kuupäev;kirjutas\n"
			"el;Από:;Ημερομηνία:;Στάλθηκε:;Προς:;Θέμα;Στις;έγραψε\n"
			"es_419;De:;Fecha:;Enviado:;Para:;Asunto;El;escribió\n"
			"pt_BR;De:;Data:;Enviado em:;Para:;Assunto;Em;escreveu\n"
			"mi;Mai:;Rā:;Tukuna:;Ki:;Kaupeka;I te;tuhituhi\n"
			"tl;Mula:;Petsa:;Ipinadala:;Sa:;Paksa;Noong;isinulat\n"
			"zh_CN;发件人:;日期:;发送时间:;收件人:;主题;在;写道\n"
			"zh_TW;寄件人:;日期:;傳送時間:;收件人:;主旨;在;寫道\n"
			"ja;差出人:;日付:;送信日時:;宛先:;件名;に;書きました\n"
			"ko;보낸 사람:;날짜:;보낸 날짜:;받는 사람:;제목;에;작성\n"
			"hi;प्रेषक:;दिनांक:;भेजा गया:;प्रति:;विषय;को;लिखا\n"
			"bn;প্রেরक:;তারিখ:;পাঠানো হয়েছে:;প্রাপক:;বিষয়;তারিখ;লিখেছেন\n"
			"tr;Kimden:;Tarih:;Gönderildi:;Kime:;Konu;Tarihinde;yazdı\n"
			"az;Kimdən:;Tarix:;Göndərildi:;Kimə:;Mövzu;Tarixdə;yazdı\n"
			"kk;Жіберуші:;Күні:;Жіберілді:;Алушы:;Тақырып;Күні;жазды\n"
			"uz;Kimdan:;Sana:;Yuborildi:;Kimga:;Mavzu;Sanasida;yozdi\n"
			"ky;Кимден:;Дата:;Жөнөтүлдү:;Кимге:;Тема;Датасында;жазган\n"
			"mn;Илгээгч:;Огноо:;Илгээсэн:;Хүлээн авагч:;Сэдэв;Огноонд;бичсэн\n"
			"my;ပို့သူ:;ရက်စွဲ:;ပို့ပြီး:;လက်ခံသူ:;အကြောင်းအရာ;ရက်စွဲတွင်;ရေးသားခဲ့သည်\n"
			"th;จาก:;วันที่:;ส่งเมื่อ:;ถึง:;เรื่อง;เมื่อวันที่;เขียนว่า\n"
			"km;ពី:;កាលបរិច្ឆេទ:;បានផ្ញើ:;ទៅ:;ប្រធានបទ;នៅថ្ងៃ;បានសរសេរ\n"
			"vi;Từ:;Ngày:;Đã gửi:;Đến:;Chủ đề;Vào ngày;đã viết\n"
			"id;Dari:;Tanggal:;Terkirim:;Kepada:;Subjek;Pada;menulis\n"
			"ms;Daripada:;Tarikh:;Dihantar:;Kepada:;Subjek;Pada;menulis\n"
			"ta;அனுப்பியவர்:;தேதி:;அனுப்பப்பட்டது:;பெறுநர்:;பொருள்;அன்று;எழுதினார்\n"
			"te;నుండి:;తేదీ:;పంపబడింది:;కు:;விषయం;నాడు;రాशారు\n"
			"ka;გამომგზავნი:;თარიღი:;გაგზავნილია:;მიმღები:;თემა;თარიღს;დაწერა\n"
			"hy;Ուղարկողը:;Ամսაթիվ:;Ուղարկված է:;Ստացողը:;Թեմա;Օրը;գրեց\n"
			"ne;बाट:;मिति:;पठाइयो:;लाई:;विषय;मा;लेख्नुभयो\n"
			"si;සිට:;දිනය:;යවන ලදී:;වෙත:;විෂය;දින;ලියන ලදි\n"
			"sw;Kutoka:;Tarehe:;Imetumwa:;Kwenda:;Mada;Mnamo;aliandika\n"
			"am;ከ:;ቀን:;ተልኳል:;ለ:;ርዕሰ ጉዳይ;በ;ጻፉ\n"
			"ha;Daga:;Kwanan wata:;An aika:;Zuwa:;Taken;A ranar;ya rubuta\n"
			"yo;Lati:;Ọjọ:;Ti firanṣẹ:;Si:;Koko ọrọ;Ní ọjọ́;kọwe\n"
			"ig;Site na:;Ụbọchị:;Ezigara:;Nye:;Isiokwu;Na;dere\n"
			"zu;Ovela:;Usuku:;Ithunyelwe:;Kuya:;Isihloko;Ngo;wabhala\n"
			"xh;Evela:;Umhla:;Ithunyelwe:;Kuya:;Isihloko;Ngo;wabhala\n"
			"af;Van:;Datum:;Gestuur:;Aan:;Onderwerp;Op;geskryf\n"
			"so;Laga:;Taariikhda:;La diray:;Loo diray:;Mawduuca;Taariikhda;qoray\n"
			"rw;Uvuye:;Italiki:;Yoherejwe:;Uyu:;Insanganyamatsiko;Ku;yanditse"
		)

		# reg expressions
		self.regMOZillaCITE = re.compile(r'(<div class="moz-cite-prefix">.*?</div>)', re.DOTALL)
		self.regVia = re.compile(r"' .*?&gt;")
		self.regGoogleGroupsAddr = re.compile(r"\s(.+?@googlegroups\.com)")

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
	def logadd(self, label, msg, init=False): 
		if init: self.debugLog =""
		self.debugLog += "\n" + label + ": "    + str(msg)
		
	# def getHeaders(self, langCode):
		# """Fast lookup that returns a lightweight C-like structure (namedtuple)."""
		# prefix = f"\n{langCode};"
		
		# if self.rawHeaders.startswith(f"{langCode};"):
			# startPos = 0
		# else:
			# startPos = self.rawHeaders.find(prefix)
			# if startPos == -1:
				# return None
			# startPos += 1

		# endPos = self.rawHeaders.find("\n", startPos)
		# line = self.rawHeaders[startPos:] if endPos == -1 else self.rawHeaders[startPos:endPos]
			
		# prefixLen = len(langCode) + 1
		# elements = line[prefixLen:].split(";")
		
		# # Instantiate and return the namedtuple
		# # "*" unpacks the list of 7 elements directly into the named fields
		# return self.EmailHeaders(*elements)


	def toggleTranslation(self):
		msgEnab = _("Enabling message translation mode, ready.")
		msgDisab = _("Disabling message translation mode, ready.")

		if self.translate: 
			self.translate = False 
			self.iTranslate = None
			return utils.message(msgDisab)
		try: 
			self.iTranslate = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
			# sharedVars.logte("Instant Translate:" + str(self.iTranslate))
		except:
			pass
		
		if not self.iTranslate:
			return utils.message(_("The Instant Translate add-on is not active or not installed."))
		self.translate = True
		utils.message(msgEnab)

	def toggleBrowseMessage(self):
		# Translators: brace symbols will be replaced by the words enabling or disabling
		msgEnab = _("Enabling message display mode, ready.")
		msgDisab = _("Disabling message display mode, ready.")
		self.browsePreview = not self.browsePreview
		utils.message(msgEnab if self.browsePreview else msgDisab)
	def readMail(self, oFocus, oDoc, rev = False, spkMode=1): 
		if self.debug:
			sharedVars.debugLog = "ReadMail\n"
			sharedVars.log(oDoc, "oDoc") 
			sharedVars.log(oFocus, "oFocus") 

		# spkMode: 1 with utils.longText, 2=copyToClip, 10 with ui.message
		speech.cancelSpeech()
		for i in range(0, 20):
			if oDoc.role == controlTypes.Role.DOCUMENT:
				result = self.setDoc(oDoc, rev)
				if self.debug: sharedVars.logte("Converted message\n" + self.text)
				if result == 1: 
					self.setText(spkMode) 
					break
				elif result == 2: 
					# beep(100, 20)
					CallLater(250, self.setText, spkMode) 
					# self.sayDraftText()
					break
				elif result == 3:  # after  an exception with IAccessible.queryInterface
					utils.sayLongText(self.text, speech=True)
					break
			else: 
				if i % 10 == 0:
					beep(350, 5)
				# sleep(0.1)
				oDoc =  getFocusObject()

	def setDoc(self, oDoc, nav=False, fromSpellCheck=False): 	
		# converts the doc into HTML code
		if not oDoc: 
			beep(100, 30)
			return 0 
		self.nav = nav
		self.fromSpellCheck = fromSpellCheck
		self.text = ""
		self.lLines = []
		self.lQuotes = []
		self.lastLine, self.lastQuote = -1, -1
		self.curLine =  self.curQuote = 0		
		# document without subject as name 
		parID = str(utis.getIA2Attribute(oDoc.parent))
		if parID in ("messageEditor", "spellCheckDlg"):
			self.quoteMode = False
			# sharedVars.log(oDoc, "oDoc in message Editor")
		else:
			self.quoteMode = True

		self.subject = getEndSubject(parID)
		# sharedVars.logte("self.subject=" + self.subject)

		o=oDoc.firstChild # section ou paragraph
		# 2025-01-10 log à désactiver
		# sharedVars.log(o, u"après  oDoc.firstChild ")
		if o is None: return 0
		cCount =  oDoc.childCount
		
		if o.next:
			# sharedVars.log(o.next, "quoteNav, o.next  ") 
			# beep(800, 40)
			#html simple
			# self.text = "" # 2026-07-13 "-§" 
			i = 1
			while o is not None:
				# # sharedVars.logte(u"HTML elem:" + str(o.role)  + ", " + str(o.name))
				try: 
					obj = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
					s=obj.innerHTML 
					if not s:s= o.name
				except:
					self.getMessageByObjects(oDoc.firstChild, "HTML")
					return 3
				if s:self.text += s + CNL # + CNL required for not self.quoteMode
				# if cCount > 75 and s and self.regTextTags.search(s):
				if (i % 10  == 0) and s and self.regTextTags.search(s):
					beep(350,5)
				if winUser.getKeyState(winUser.VK_CONTROL)&32768:
					return 2
				i += 1
				try: o=o.next
				except: break
		else: # plain Text
			# sharedVars.log(o, "quoteNav plainText before queryInterface o") 
			# self.text = "" # 2026-07-13 "-§"
			try:
				o = o.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			except:
				self.getMessageByObjects(o, "TEXT")
				return 3
			# # sharedVars.logte("brut:" + str(o))
			self.text += str(o.innerHTML)
		return 1

	def getMessageByObjects(self, obj,kind=""):
		# message("Please wait " + " " + kind)
		utils.message(_("Please wait"))
		i = 0
		for child in obj.recursiveDescendants:
			if hasattr(child, "name"):
				if child.name:
					self.text += str(child.name) + "\n"
					i += 1
			if i == 75: 
				break

	def sayDraftText(self):
		self.text=self.regHTMLChars.sub(" ",self.text)
		self.text=self.regHTML.sub(" ",self.text)
		# beep(100, 20)
		# sharedVars.debugLog = "Draft:\n" + self.text
		CallLater(500, utils.sayLongText, self.text, True)
	
	def getDocObjects(self, oDoc):
		o = oDoc.firstChild
		while o is not None:
			o = o.next
	

	def regExtract(self, compiledPattern):
		match = compiledPattern.search(self.text)
		return match.group(1) if match else None


	def setText(self, speakMode=1): 
		# speakMode: 1 with utils.longText, 2=copyToClip, 10 with ui.message
		# prepare text for removing outlook and Windows mail headers
		self.deleteBlocks()
		if self.debug: sourceCode  = "\n#h2# Original Source code with some ,lf,\n" + self.text
		# Mozilla style citations
			
		# thunderbird cite prefixes
		self.replaceMozCitePrefixes(self.regMOZillaCITE)
		# google groups via web
		self.replaceMozillaHeaders('<div class="gmail_quote gmail_quote_container">', blEnd=":\n", blEnd2=":<br>")
		# replace all ends of line
		self.text = self.text.replace("\r", "").replace("\n", ",lf,").replace("<br>", ",br,").replace("<span>", "").replace("&nbsp;:", ":").replace("&nbsp;", " ").replace("<b>", "").replace("</b>", "").replace(":", ":")

		self.cleanLinks()
		self.compressMicrosoftHeaders(utis.getLang())
		# removes special &char;
		self.text=self.regHTMLChars.sub(" ",self.text)
		# Removes of all remaining HTML tags
		self.text=self.regHTML.sub("",self.text)
			# removes multiple spaces 
		self.text=self.regMultiSpaces.sub(" ",self.text)
		# replace pseudo ,lf,  and br
		self.text = self.text.replace(",lf,", "\n").replace(",br,", "\n")
		
		# removes multiple  spaces again
		self.text = self.regMultiSpaces.sub(" ", self.text)
		self.text = self.text.replace(" \n", "\n") 
		# replace /mlHeaders
		self.text = self.text.replace("/mlHeaders", "\n")
		# removes multiple \n
		self.text=self.regMultiNL.sub("\n",self.text)

		if self.debug: 
			self.debug = False
			fileName  = "D:\Develo\debugLogs\quoteNav-" + makeFilenameSafe(self.subject) + ".txt"
			saveToFile(self.debugLog + sourceCode, fileName, show=True)  
			self.debugLog = ""
		
		if not self.nav: # text
			if speakMode > 0:
				self.speakText(0, speakMode)
		else:
			self.buildLists(speakMode)

	def buildLists(self, speakMode):
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
		if self.fromSpellCheck:
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
		if self.lastQuote  > -1  and not self.translate: 
			self.lQuotes.reverse()
			self.text = "\n".join(self.lQuotes) 

		msg = msgQuotes.format(self.lastQuote + 1)
		if speakMode  == 1: # with utils115.message
				utils.sayLongText(msg + self.text)
		elif speakMode  == 10: # with ui.message
			speech.speakMessage(msg + self.lQuotes[self.curQuote])
			utils.setBrailleMode(sharedVars.msgOpened)

	def displayMessage(self, subj, body):
		if subj == "": subj = _("Translation")
		body = body.replace("§\n", "").strip()
		textDialog.showText(title=subj, text=body, label="-")

	def truncateSubj(self, text, wantedLen):
		# text=self.regSubject.sub("",text)
		# text=self.regListName.sub("",text)
		# text=self.regMultiSpaces.sub(" ", text)
		lenText = len(text)
		if lenText  <= wantedLen: return text 
		pos = wantedLen - 1
		while pos < lenText:
			if text[pos] == " ":
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
		# elif count > 0:
			# return str(messages[:1]).replace("\\n", chr(10))
		# else:
			# return "No message found."
			
	def speakText(self, freq=0, speakMode=1):
		# if freq > 0:
		msg = ""
		if speakMode == 2:
			# copyToClip(self.text)
			msg = _("Preview copied: ")
		
		if self.translate: 
			beep(500, 100) # same sound as in InstantTranslate
			subject =   self.iTranslate.translateAndCache(cleanSubject(sharedVars.curWinTitle), "auto", self.langTo).translation
			subject = self.truncateSubj(subject, 35)
			text = self.iTranslate.translateAndCache(self.getFirstMessages(), "auto", self.langTo).translation
			# pos = str(text.find("\r"))
			# sharedVars.logte("Translated:\nCR pos=" + pos + "\n" + text)
			if self.browseTranslation or self.browsePreview and not self.fromSpellCheck: self.displayMessage(subject, text)
			else: 
				if speakMode == 1: utils.sayLongText(msg + subject + "\n" + text, True)
				elif speakMode == 10: 
					speech.speakMessage(msg + subject + text)
					utils.setBrailleMode(sharedVars.msgOpened)
		else: # no translation
			if self.browsePreview and not self.fromSpellCheck: 
				subject = cleanSubject(sharedVars.curWinTitle)
				subject = self.truncateSubj(subject, 25)
				self.displayMessage(subject, self.text)
			else: 
				if speakMode == 1: utils.sayLongText(msg + self.text, True)
				elif speakMode == 10: 
					speech.speakMessage(msg + self.text)
					utils.setBrailleMode(sharedVars.msgOpened)

	def speakQuote(self, quote):
		if self.translate: 
			quote  = self.iTranslate.translateAndCache(quote, "auto", self.langTo).translation
		if self.browseTranslation and not self.fromSpellCheck: self.displayMessage("", quote) 
		else: 
			utils.sayLongText(quote, True)

	def deleteMetas(self):
		lbl = "<meta "
		metas = []
		p, pEnd = self.findWords(lbl)
		while p > -1:
			p2 = self.text.find('">', pEnd) 
			if p2 == -1: break
			b = self.text[p:p2] + '">'
			# # sharedVars.logte("meta:" + b)
			metas.append(b)
			# next block
			p, pEnd = self.findWords(lbl, p2+2) # +2 is then len of ">
		if len(metas) == 0: return
		for e in metas:
			# # sharedVars.logte("e:" + e)
			self.text = self.text.replace(e, "")
			self.text = self.text.replace(e, "")

	def deleteBlocks(self):
		# Originale message
		# s = _("Original Message|E-mail d'origine|Message d'origine")
		# reg = re.compile("(\-{5} ?(" + s + ") ?\-{5})")
		# self.text = reg.sub("", self.text)
		pattern = r"-{2,5}.*?-{2,5}"
		self.text  = re.sub(pattern, "<mlHeaders>", self.text)

		# remove Gmail's forwarded message
		if self.text.find("-- Forwarded message") > -1:
			s = '<div dir="ltr" class="gmail_attr">---------- Forwarded message ---------'
			reg = re.compile(s + ".+?\</div\>")
			self.text = reg.sub("", self.text)

		
		self.deleteMetas()
		# removes style css tag
		if self.text.find("<style>") > 0:
			regExp = re.compile("\<style\>.+?\</style\>")
			self.text=regExp.sub (" ",self.text)

		#  transform  table of mozilla headers
		block = self.getTextBlock('<table class="moz-email-headers-table">', "</table>")
		if block:
			# sharedVars.logte("Moz forward original block\n" + block)
			block2 = block.replace("\n", "").replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")
			pos =   findOccurrence(block2, "<tr>", 4)
			if pos != -1:
				block2 = block2[:pos]
			block2 = block2.replace(": ", "").replace("<tr>", "\n")
			block2 = re.sub(r"[+-]\d{4}", "", block2)
			block2 = "\n" + self.regHTML.sub("", block2) 
			# sharedVars.logte("Moz forward block2\n" + block2 + "\n")
			self.text = self.text.replace(block, block2 + "\nmsgStart")
		
		# group footers: one group in a message, we  use return after a footer  deletion
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
			for t in tags:
				posTag = self.text.find(t)
				if posTag != -1:
					break
			if posTag != -1:
					self.text = self.text[:posTag]
			return

		#Removes groups.io footer
		# "Groups.io Links:"
		pos = self.text.find("Groups.io Links:")
		if pos != -1:
			p2, p3 = self.findWords("_._,|-=-=")
			if p2 != -1: pos = p2
			if pos != -1:
				self.text=self.text[:pos]
				return
				
		# removes freeLists footer: -----------------------Infos----
		pos = self.text.find("-----------------------Infos-----------------------")
		if pos != -1:
			self.text=self.text[:pos]
			return
			
		# removes french framalistes footer
		pos = self.text.find("Le service Framalistes vous est")
		if pos != -1:
			self.text=self.text[:pos]

	def cleanLinks(self):
		# mailto and clickable links replacements
		lbl = _(" link %s ").replace(" %s", "")
		l=self.regLink.findall (self.text)
		for e in l:
			linkTag = str(e[0]) # contains <a until </a>
			# linkText = e[1] # the visible part of the link
			# sharedVars.logte("linkTag=" + linkTag)
			match = re.search(r'href="([^"]+)"', linkTag)
			if match:
				hRef = match.group(1)
			else:
				hRef = ""
			# sharedVars.logte("hRef=" + hRef)
			if "@" in e[1]: # link text is a mail address
				hRef = e[1].replace("@", "|arob|")
			elif "mailto" in hRef: 
				hRef = e[1] # link text is not a mail  address
				if " via "  in hRef: 
					hRef = hRef.split(" via ")[0].strip(" '")
			elif "http" in hRef:
				if "http" not in e[1]: 
					hRef =e[1] + ", " + hRef 
				hRef = shortenUrl(hRef, lbl)
			
			self.text = self.text.replace (linkTag, hRef.replace(",lf,", ""))
			# end of loop
		self.text = self.text.replace("|arob|", "@")
		
	def getTextBlock(self, start, end, exclude="", end2=""):
		"""
	Returns the text substring between 'start' and 'end' inclusive.
		If one of the tags is not found, returns an empty string.	"""
		startIdx = self.text.find(start)
		if startIdx == -1:
			return ""
		
		endIdx = self.text.find(end, startIdx + len(start))
		if endIdx == -1:
			if end2: endIdx = self.text.find(end2, startIdx + len(start))
			if endIdx == -1: return ""
		result = self.text[startIdx: endIdx + len(end)]
		if exclude and exclude in result:
			return ""
		return  result

	def replaceMozCitePrefixes(self, compiledPattern):
		if self.debug: self.logadd("#h2# replaceMozCitePrefixes with", compiledPattern)
		while True:
			match = compiledPattern.search(self.text)
			if not match: return
			block = match.group(1)
			block2 = self.regHTML.sub("", block)
			if self.debug: 
				self.logadd("#h3# moz block HTML", block)
				self.logadd("#h3# moz block plain text", block2)
			self.text = self.text.replace(block, "\n-§" + block2 + "/mlHeaders")

	def replaceOnWrote(self, hdrOn, hdrWrote):
		# on wrote of standard citations
		patternOnWrote = r"(?<!§)(" + re.escape(hdrOn) + r".*?" + re.escape(hdrWrote) + r":)"

		if self.debug: self.logadd("#h2# replaceOnWrote with", patternOnWrote)
		while True:
			match = re.search(patternOnWrote, self.text)
			if not match: return
			block = match.group(1)
			block2 = block.replace("&lt;", "<").replace("&gt;", ">")
			block2 = self.regHTML.sub("", block2)
			block2 = self.regVia.sub("", block2)
			if self.debug: 
				self.logadd("#h3# OnWrote block HTML", block)
				self.logadd("#h3# OnWrote block plain text", block2)
			self.text = self.text.replace(block, "\n-§" + block2 + "/mlHeaders")

	def replaceMozillaHeaders(self, blStart, blEnd, blEnd2="", hertz=0):
		if self.debug: self.debugLog += "\n#h2# Mozilla header search: " + blStart   
		# domPattern = r"@.*? "

		while True:
			block = self.getTextBlock(blStart, blEnd, exclude="", end2=blEnd2)
			if not block: return
			if self.debug: self.debugLog += "\n\tMoz block found: " + block
			block2 = "\n-§" + self.regHTML.sub("", block)
			block2 = self.regVia.sub("", block2)
			if self.debug: self.debugLog += "\nBefore remove @domain: \n"  + block2
			block2 = re.sub(r"@[^\s]+", " ", block2)
			self.text = self.text.replace(block, block2+ "\n")
			if hertz: beep(hertz, 100)
			if self.debug: self.debugLog += "\n\tMozilla header     replaced with:" + block2

	def replaceOutlookHeaders(self, blStart, lblFrom, lblSent, lblTo, lblSubject, translatedFrom):
		blStart +=  lblFrom
		if self.debug: self.debugLog += "\n#h2# Outlook headers search: " + blStart   
		blEnd = "</p>" 
		# mailPattern = r" [\w\.-]+@[\w\.-]+\.\w{2,} "
		domainPattern = r"@[^\s,]+"

		while True:
			block = self.getTextBlock(blStart, blEnd)
			if not block: return
			if lblSubject not in block:
				# in plain text, each header is in a paragraph
				block = self.getTextBlock(blStart, 'oNormal">' + lblSubject)
				if block: block = self.getTextBlock(block, blEnd)
				if not block: return
			if self.debug: self.debugLog += "\n\t" + "Outlook Headers,  Block found between {} and {}: {}".format(blStart, blEnd, block)
			block2 =  block.replace('<p class="MsoNormal">', "").replace(lblSent, ", ").replace(",lf,", "").replace(",br,", "").replace("</p>", ",br,")	.replace(lblFrom, translatedFrom)
			pos = block2.find(lblTo)	
			if self.debug: self.debugLog += "\nSearched for {}, position: {}".format(lblTo, pos)
			if pos != -1:
				block2 = block2[:pos]
			block2 = self.regHTML.sub("", block2)
			block2 = self.regVia.sub("", block2)
			header = getBlock(block2, lblFrom, "googlegroups.com&gt;") 
			if header: block2 = block2.replace(header, lblFrom + " ")
			# block2 =  self.regGoogleGroupsAddr.sub("", block2)
			# block2 = self.regHTML.sub("", block2)
			block2 = block2.replace(",br,", "").replace(",lf,", "")
			self.text = self.text.replace(block, "\n" + block2 + "/mlHeaders")
			if self.debug: self.debugLog += "\n\tOutlook headers  replaced with:" + block2


	def replaceAllBlocks(self, blStart, blEnd, replace=""):
		block = self.getTextBlock(blStart, blEnd)
		while block:
			self.text = self.text.replace(block, replace)
			block = self.getTextBlock(blStart, blEnd)

	def replaceWinMailHeaders(self, lblFrom, lblSent, lblTo, lblSubject, translatedFrom):
		blStart = "<mlHeaders>"
		blEnd = "</mlHeaders>" 
		if self.debug: self.debugLog += "\n#h2# WinMail  search for <mlHeaders> with lblFrom=" + lblFrom
		domainPattern = r"@[^\s,]+"
		viaPattern = r"' .*?&gt;"
		# by Gemini: pattern = rf"{re.escape(lblTo)}.*?(?:</div>|,lf,)"
		toPattern = rf"{re.escape(lblTo)}.*?(?:,br,|,|,lf,)"
	
		while True:
			block = self.getTextBlock(blStart, blEnd, exclude='<p class="Mso')
			if not block: return
			if lblSent not in block and lblTo not in block and lblSubject not in block:
				return
			if self.debug: self.debugLog += "\n\tWinMail headers  found between {} and {}: {}".format(blStart, blEnd, block)
			block2 =  block.replace('"', "").replace("<mlHeaders>", "").replace(lblSent, ", ").replace(",lf,", "").replace(",br,", "").replace("</mlHeaders>", ",br,").replace(lblFrom, translatedFrom)
			block2 = re.sub(viaPattern, ",", block2)
			block2 = re.sub(domainPattern, "", block2)
			block2 = self.regHTML.sub("", block2)
			# if self.debug: self.debugLog += "\nBlock2 before apply toPattern: " + block2
			block2 = re.sub(toPattern, "", block2)
			block2 = block2.replace("'", "").replace(",br,", "").replace(",lf,", "")
			# if self.debug: self.debugLog += "\n\tBlock2 after apply toPattern: " + block2
			self.text = self.text.replace(block, "\n" + block2 + "/mlHeaders")
			if self.debug:
				self.debugLog += "\n\tWinMail Headers  Replaced with:" + block2

	def translateFromHeader(self, lg) :
		default = "\n-§From:"
		search =  "\n" + lg + ";"
		startPos = self.rawHeaders.find(search)
		if startPos == -1:
			return default
		endPos = self.rawHeaders.find("\n", startPos + len(search))
		if endPos == -1:
			return default
		line = self.rawHeaders[startPos+1:endPos]
		if line:
			return "-§" + line.split(";")[1]
		return default

	def normalizeFrenchHeaders(self):
		# Because they are inconsistent, normalize French headers that use a space before colon
		if "De:" not in self.text:
			return
		self.text = self.text.replace("De:", "De:")
		self.text = self.text.replace("Envoyé:", "Envoyé:")
		self.text = self.text.replace("À:", "À:")
		self.text = self.text.replace("A:", "À:")
		self.text = self.text.replace("Objet:", "Objet:")

	def compressMicrosoftHeaders(self, lang="EN"):
		
		# some simplifications
		self.text = self.text.replace("<mlHeaders>,br,", "<mlHeaders>")
		s = r'<span lang="[^"]*">'
		self.text = re.sub(s, "", self.text)
		self.normalizeFrenchHeaders()
		if self.debug:
			self.debugLog += "\n#h2# Text nBefore MS header compression\n" + self.text.replace("<p class", "\n<p class").replace("</p>", "</p\n")
		# headers in NVDA language
		# from_t, date_t, sent_t, to_t, subject_t = getCiteHeader(lang)
		from_t = self.translateFromHeader(lang)
		# sharedVars.logte("translateFromHeader returned=" + from_t)

		
		for headerLine in iterLines(self.rawHeaders):
			headers  = headerLine.split(";")
			lang_code, from_h, date_h, sent_h, to_h, subject_h, on_h, wrote_h = headers
			if self.debug: self.debugLog += "\nlang_code {}, from_h {} , to_h {}, subject_h {}".format(lang_code, from_h, to_h, subject_h)
			self.replaceOutlookHeaders('<p class="MsoNormal">', from_h, sent_h, to_h, subject_h, from_t)
			self.replaceOutlookHeaders('<p class="MsoPlainText"><mlHeaders>', from_h, sent_h, to_h, subject_h, from_t)
			self.replaceAllBlocks("<div>" + subject_h, "</div>", "</mlHeaders>")
			self.replaceAllBlocks(subject_h, ",lf,", "</mlHeaders>")
			self.replaceWinMailHeaders(from_h, sent_h, to_h, subject_h, from_t)
			self.replaceOnWrote(on_h, wrote_h)

		# end for
		# final replacements
		self.text = self.text.replace("groups.io", " at GIO")
		if self.debug: 
			self.debugLog +=  "\nResult\n" + self.text

	def strBetween2(self, sep1, sep2):	
		pos1 = self.text.find(sep1) 
		if pos1 < 0: return ""
		pos1 +=  len(sep1)
		pos2 = txt.find(sep2, pos1)
		if pos2 < 0: return ""
		return self.text[pos1:pos2]

	def findWords(self, words, start=0):
		lWords = words.split("|")
		for e in lWords:
			pos = self.text.find(e, start)
			if pos > -1:
				return pos, pos + len(e) + 1
		return pos, pos
		

	def getSenderName(header):
		#  header may contain §
		

		# On Behalf Of Isabellevia groups.ioSent 
		if "Behalf Of" in header:
			s = strBetween(header, "Behalf Of", "via groups").strip()  
		elif  "via groups.io" in header: 
			# to replace:From: §  Jeremy T. via groups.io: 
			s = strBetween(header, ":", "via")
		else:
			# s = "à revoir: " + header
			header  = header.split(":") 
			s = (header[1] if len(header) > 1 else header[0])
			if "&lt;" in s:
				s = s.split("&lt;")[0]

		
		self.regSender.sub("", s)
		s = s.strip()
		# # sharedVars.logte("retour getSenderName:" + s)
		return s
	# methods related to quotes navigation
	def skipLine(self, n=1):
		if self.lastLine == -1: 			self.buildList(False)
		# skips 1 item before or after
		if n == -1:
			self.curLine = self.lastLine if self.curLine == 0 else self.curLine - 1
		elif n == 1:
			self.curLine = 0  if self.curLine == self.lastLine  else self.curLine + 1
		self.speakQuote(self.lLines[self.curLine])

	def skipQuote(self, n=1):
		if self.lastQuote == -1: 			self.buildLists(False)
		# skips 	1 quote before or after
		if n == -1:
			self.curQuote = self.lastQuote if self.curQuote == 0 else self.curQuote - 1
		elif n == 1:
			self.curQuote = 0  if self.curQuote == self.lastQuote  else self.curQuote + 1
		self.speakQuote(str(self.curQuote+1) + ":" + self.lQuotes[self.curQuote])

	def findLine(self, expr): # for spellcheckDlg
		speech.cancelSpeech()
		if not hasattr(self, "lastLine"):
			msg = "Word search in text is currently unavailable. Press Escape followed by F5 to get it." 
			iTranslate = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
			if iTranslate:
				msg =   iTranslate.translateAndCache(msg, "auto", self.langTo).translation
			return utils.message(msg)
		if self.lastLine == -1:
			self.buildLists(False)	
		lIdx, wIdx = self.indexOf(expr, self.curLine)
		if lIdx > -1:
			self.curLine = lIdx
			self.speakQuote(self.lLines[lIdx])
		else:
			utils.message(_("Phrase not found."))

	def indexOf(self, word, start=0, backward=False): 
		stopChar = "§" # alt+0031
		if not backward:
			step = 1
			# start is the same
			iLast = self.lastLine 
		else:
			step = -1
			iLast = 0
		
		for i in range(start, iLast, step): 
			if i > start and stopChar in self.lLines[i]:
				break
			p = self.lLines[i].find(word)
			if p > -1:
				return i, p
		
		return -1, -1

# normal functions
def getSenderName(header):
	#  header may contain §
	

	# On Behalf Of Isabelle Delarue via groups.ioSent 
	if "Behalf Of" in header:
		s = strBetween(header, "Behalf Of", "via groups").strip()  
	elif  "via groups.io" in header: 
		# to replace:From: §  Jeremy T. via groups.io: 
		s = strBetween(header, ":", "via")
	else:
		# s = "à revoir: " + header
		header  = header.split(":") 
		s = (header[1] if len(header) > 1 else header[0])
		if "&lt;" in s:
			s = s.split("&lt;")[0]

	s = s.replace("§", " ").strip()
	# # sharedVars.logte("retour getSenderName:" + s)
	return s
	
def shortenUrl(lnk, label):
	lnk = lnk.replace("https://", label)
	lnk = lnk.replace("http://", label)
	return lnk.split("/")[0]
	
def strBetween(t, sep1, sep2):
	pos1 = t.find(sep1) 
	if pos1 < 0: return ""
	pos1 +=  len(sep1)
	pos2 = t.find(sep2, pos1)
	if pos2 < 0: return ""
	return t[pos1:pos2]

def findNearWords(inStr, w1, w2, max):
	len1 = len(w1)
	len2 = len(w2)
	p1 = inStr.find(w1) 
	# # sharedVars.logte("premier p1:" + str(p1))
	while p1 > -1:
		p2 = inStr.find(w2, p1+len1)
		# # sharedVars.logte("p2:" + str(p2))
		if p2 == -1: 
			# # sharedVars.logte(w2 + " not Found")
			break
		if p2-len2 - p1 + len1  < max:
			# # sharedVars.logte("found")
			return inStr[p1:p2+len2+2]
		p1 = inStr.find(w1, p2) 
		# # sharedVars.logte("p1:" + str(p1))
	return ""

def cleanH(s, reg):
	global CNL
	try:
		# removes pseudo \n
		s = s.replace(CNL, "")
		s = delMailAddrs(s).strip()

		if ", " in s:
			s = s.split(", ")
			# # sharedVars.logte("s1 {}, s2 {}".format(s[0], s[1]))
			s = s[1]
	finally:
		return s

def delMailAddrs(s):
	lt = " &lt;"
	if s.startswith(lt):
		s = s[4:]
	p = s.find("&lt;")
	if p != -1:
		pS = s.find(" ", p)
		if pS != -1: s= s.replace(s[p:pS], "")

	p = s.find("@") 
	if p != -1:
		pS = s.find(" ", p)
		if pS != -1: s= s.replace(s[p:pS], "")
	s = s.replace("via groups.io", "") 
	return s.replace("  ", " ")
	
# def detect_language(text):
	# response=urllib.urlopen("https://translate.yandex.net/api/v1.5/tr.json/detect?key=trnsl.1.1.20150410T053856Z.1c57628dc3007498.d36b0117d8315e9cab26f8e0302f6055af8132d7&"+urllib.urlencode({"text":text.encode('utf-8')})).read()
	# response=json.loads(response)
	# return response['lang']

def getEndSubject(parentID):
	# fo = getFocusObject()
	# role = fo.role
	# s = ""
	# if role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM) and utils.hasID(fo, "threadTree-row"):
		# s= utils.getColValue(fo, "subjectcol")
	# else:
	s  = utils.cleanWinTitle(sharedVars.curWinTitle)
	# get 2 last words
	aParts = s.split(" ")
	arrLen = len(aParts)
	if arrLen == 1:
		return aParts[0]
	elif arrLen >= 2: 
		arrLen -= 1
		return aParts[arrLen-1] + " " + aParts[arrLen]
	return s

	

def cleanSubject(subject):
	subject = utils.cleanWinTitle(subject)
	i = subject.rfind("]")
	if i > -1:
		subject = subject[i:]
	subject =  subject.replace("Re: ", "")
	return subject
# generated by Gemini
def findOccurrence(text, findStr, occurr=1):
	"""
	Finds the N-th occurrence (defined by 'occurr') of 'findStr' within 'text'.
	The search is performed forward from the beginning of the text.
	
	Returns the index of the occurrence if found, otherwise returns -1.
	"""
	# An occurrence count less than 1 makes no sense, so we return -1 early.
	if occurr < 1:
		return -1

	position = -1
	count = 0

	while count < occurr:
		# Search for the next occurrence starting just after the last found position
		position = text.find(findStr, position + 1)
		
		# If text.find returns -1, the string doesn't exist or there are no more occurrences
		if position == -1:
			return -1
			
		count += 1

	return position

def getBlock(text, start, end):
		startIdx = text.find(start)
		if startIdx == -1:
			return ""
		
		endIdx = text.find(end, startIdx + len(start))
		if endIdx == -1:
			return ""
		
		return text[startIdx: endIdx + len(end)]

def makeFilenameSafe(text):
	import unicodedata
	# 1. Normalize text to decompose accented characters
	# Example: "é" becomes "e" + "accent grapheme"
	text = unicodedata.normalize('NFKD', text)
	# Encode to ASCII, ignoring characters that cannot be converted (decomposed accents)
	text = text.encode('ascii', 'ignore').decode('ascii')
	
	# 2. Replace everything that is not a letter, a number, a dash, or a dot with an underscore
	text = re.sub(r'[^\w\s\.-]', '_', text)
	
	# 3. Replace spaces with underscores and remove duplicate underscores
	text = re.sub(r'\s+', '_', text)
	text = re.sub(r'_+', '_', text)
	
	# 4. Strip underscores and spaces from the beginning and end
	return text.strip('_ ')
def saveToFile(text, filePath, show=False):
	import os
	with open(filePath, 'w', encoding='utf-8') as file:
		file.write(text)
	if show:
		if os.path.exists(filePath):
			CallLater(1000, os.startfile, filePath)

import sys

def getDeepSize(obj, seen=None):
	"""Calculates the actual memory size of any Python object recursively."""
	if seen is None:
		seen = set()
		
	objId = id(obj)
	if objId in seen:
		return 0
	
	seen.add(objId)
	size = sys.getsizeof(obj)
	
	if isinstance(obj, dict):
		size += sum(getDeepSize(k, seen) + getDeepSize(v, seen) for k, v in obj.items())
	elif isinstance(obj, (tuple, list, set)):
		size += sum(getDeepSize(item, seen) for item in obj)
		
	return size

