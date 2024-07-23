# Thunderbird+G5 Thunderbird için >= 115

* Yazarlar: Pierre-Louis Renaud (Thunderbird 78'den 115'e) ve Cyrille Bougot (TB 102), Daniel Poiraud (TB 78'den 91'e), Yannick (TB 45'ten 60'a);
* Eklenti Sayfası: [Thunderbird+ G5 ve G4 eklentilerinin ana sayfası][4];

  [Geçmişi Değiştir][5];  
  [İletişim][6];  

* İndirin: [Kararlı sürüm] [3]
* İndirin: [RPTools.org'daki en son sürüm][3]
* NVDA uyumluluğu: 2021.1 ve sonrası;
* [gitHub'daki kaynak kodu][2]


## Giriş:

Thunderbird+G5, Thunderbird 115 e-posta istemcisinin verimliliğini ve kullanım rahatlığını önemli ölçüde artıran bir NVDA eklentisidir.

Thunderbird'de yerel olarak bulunmayan komutları sağlayarak üretkenliğinizi artırır:

* Klasör ağacına, ileti listesine ve önizleme bölmesine doğrudan erişim için klavye kısayolları.
* Sekme ve escape tuşlarını kullanarak ana pencere bölmeleri arasında kesintisiz gezinme.
* Odağı değiştirmeden ileti listesi alanlarını ve ileti başlıklarını görüntülemek ve kopyalamak için kısayollar.
* Eklere doğrudan erişim.
* Düzenleme penceresinin adresleme alanlarına odaklanma ve doğrudan erişim için kısayollar.
* Yazım denetimi iletişim kutusunun kullanımı önemli ölçüde iyileştirildi.
* Adres defterlerinin ve posta listelerinin daha kolay yönetimi (v.2402.14.00).
* Eklenti güncelleme menüsü (v.2402.14.00)
* Ve daha fazlası... 

Bu sayfada Thunderbird+G5 tarafından sunulan klavye kısayolları belgelenmektedir. 

Bu klavye kısayollarının çoğu, Thunderbird 115 için NVDA Menüsü / Tercihler / Girdi Hareketleri / ThunderbirdPlusG5 kategorisi aracılığıyla yapılandırılabilir.

## Ana pencerede gezinme

Not: Bu sayfanın geri kalanında adı geçen tuş (Sekme üzerindeki tuş), Escape'in altında, Sekme'nin üstünde ve 1 sayısının solunda bulunan tuşu belirtir. İfadesi klavyenin diline bağlı olarak değişir.

### Genel kısayollar:

* (Sekmenin üstündeki tuş): ​​Eklentiye ilişkin çeşitli komutların menüsünü görüntüler.
* Shift+(Sekmenin üstündeki tuş): ​​Eklenti seçenekleri menüsünü görüntüler.
* Önizleme bölmesini göstermek veya gizlemek için F8: bu komut Eklenti tarafından seslendirilir.
* Control+F1: geçerli sayfayı görüntüler. Bazı açıklamalar için [sürüm4][7] belgelerini ziyaret edebilirsiniz;

### Ana pencere bölmeleri arasında gezinme:

Bu kısayollar klasör ağacı, İleti listesi ve İleti önizleme bölmesi içindir.

* control+(Sekme üzerindeki tuş): ​​Bir basış, odağı İleti listesine yerleştirir, iki basış, odağı İleti listesine yerleştirir ve ardından son İletiyi seçer.
* Alt+c: seçilen hesabın hesaplar menüsünü, ardından klasörler menüsünü görüntüler. 2312.14 sürümünden bu yana, klasör ağacının "birleşik klasörler" modunu desteklemektedir.
* Kontrol+Alt+c:seçilen hesap için hesaplar menüsünü ve ardından okunmamış klasörler menüsünü görüntüler. (2023.11.15)
* Sekme: Hemen sonraki bölüme gider.<br>
Not: Bu son iki kısayol, Girdi Hareketleri iletişim kutusu aracılığıyla değiştirilebilir.
* alt+Başlat: 1 basış, klasör ağacındaki geçerli klasörü seçer, 2 basış, ağaçta ulaşacağınız e-posta hesabını seçmenizi sağlayan bir menü görüntüler 
* Control+Alt+Home: aynı ancak okunmamış İletiların bulunduğu klasörler için. (2023.10.31)
* Sekme: odağı bir sonraki bölmeye getirir ve özellikle:<br>
 İleti listesinden ve önizleme bölmesi görüntüleniyorsa: Tek basış: odağı İletiın gövdesine getirir, İki basış: odağı yanıtlama düğmelerinin ve İletiın başlıklarının başlığına getirir. (v.2404.23) 
* Escape: yoldan sapmadan önceki bölüme döner. 
Escape ayrıca klasör ağacı ile İleti listesi arasında geçiş yapmanıza da olanak tanır. 
* Shift+Sekme: Bu sürümde yerel davranışı korunmuştur.

### Ana pencere sekmelerinde gezinme

* Shift tuşuyla veya Shift tuşu olmadan Control+Sekme ve Control+1'den 9'a: Eklenti, sipariş numaralarını ve toplam sekme sayısını duyurmak için sekme değişikliklerini keser.<br>
Ayrıca Eklenti, ilk kez etkinleştirildiğinde sekmenin içeriğine odaklanılmasını sağlar. İlk sekme için odak, İleti listesindeki son İletiye veya ilk okunmamış İletiye getirilebilir. Ana pencerenin seçenekler menüsü / Seçenekler aracılığıyla şu seçeneği işaretleyebilirsiniz: İlk sekme ilk etkinleştirildiğinde ilk okunmamış İletia erişin, aksi takdirde son İletia erişin (v.2402.14.00));
* Control+geri tuşunun solunda bulunan ilk tuş: mevcut sekmelerin listesini içeren bir menü görüntüler. İlgili sekmeyi etkinleştirmek için bir menü öğesi üzerinde Enter tuşuna basın.
* Alt+geri tuşunun solundaki ilk tuş: sekme içerik menüsünü görüntüler. Bu menü Thunderbird'e özgüdür.

Not: Geri tuşunun solundaki ilk tuşun etiketi klavye diline göre değişir.

## İleti listesi

<!-- 2023.11.10'da başlıyor -->

### Satırların özel seslendirilmesi (2023.11.10)

Varsayılan olarak devre dışı bırakılan bu kişiselleştirilmiş mod, İleti listesindeki satırların daha rahat dinlenmesini sağlar.

Ancak bazı dezavantajları vardır:

* İleti listesinin kart görünümü ile uyumlu değildir. Tablo görünümüne dönmek için İleti listesine gidin, Shift+Sekme tuşlarına basarak "İleti listesi seçenekleri" düğmesine basın, Enter tuşuna basın ve içerik menüsünde "Tablo görünümü"nü işaretleyin.
* Yavaş PC'lerde İleti listesindeki oklarla gezinmede gözle görülür bir yavaşlamaya neden olabilir. 
*Son satırda aşağı ok tuşuna basarsanız duyurulmaz.Shift+power2 tuşlarına basarak ve menüdeki "Ana pencere seçenekleri" öğesini seçip ardından "İleti listesi: satırların kişiselleştirilmiş seslendirilmesi" seçeneğini işaretleyerek bu modu etkinleştirebilirsiniz.

Bu alt menü ayrıca yalnızca özel seslendirme etkinleştirildiğinde çalışan diğer özelleştirme seçeneklerini de içerir.
<br>
Algılanan :

Bazı kullanıcılar normal modda boş satırlarla ilgili sorun yaşıyor. Bu durumdaysanız “İleti listesi: hala boşsa satırları doldurmaya zorla” seçeneğini etkinleştirin.

Ancak ideal olarak bu sorun, Thunderbird'de e-posta hesaplarının yeniden yapılandırılmasını içeren yeni bir kullanıcı profili oluşturularak çözülmelidir.

#### Satırların özel seslendirilmesi için ipucu

İlgili avantajlarını birleştirmek için "Okuma Durumu" ve "Durum" adlı iki sütunu birlikte kullanabilirsiniz:

* Okuma durumunu tersine çevirmek için m harfine bastığınızda "Okuma Durumu" sütunu "okunmadı" İletiını verir.
* "Durum" sütunu "Yeni", "cevaplandı" ve "İletildi" durumlarını duyurur.
* Eklenti, "Okunmadı"nın yalnızca bir kez duyurulmasını ve "Okundu"nun hiçbir zaman bildirilmemesini sağlayacaktır.

<br>
ayrıca [Sütunların seçimi ve düzenlenmesi](#cols) bölümünü de okuyun 

### İleti listesi kısayolları:

<!-- 2023.11.10 sonu -->

* Önizleme bölmesi görüntüleniyorsa sekme: 1 basış: odağı İletiın gövdesine getirir, 2 basış: odağı yanıtlama düğmelerinin ve İleti başlıklarının başlığına getirir. (v.2404.23) 
* İleti listesinde Escape: Bir filtre etkinse devre dışı bırakılır ve İleti listesi seçili kalır. Aksi takdirde bu kısayol, odağı klasör ağacına taşır.
* İleti listesinde NVDA+yukarı ok veya NVDA+l (dizüstü bilgisayar):<br>
Basın: İleti listesinin geçerli satırını duyurur. NVDA+Sekme kısayolu, bu Eklentiyı kullanmadan aynı sonucu üretir.<br>
İki basış: satırın ayrıntılarını, klavyeyi kullanarak satırın analizine olanak tanıyan bir metin penceresinde görüntüler. Sürüm 2404.23'ten itibaren, kişiselleştirilmiş satır seslendirmesi etkinse bu orijinal satırdır.
* Grup konuşması modunda Control+sağ ok: görüşmedeki son İletiı seçer. Bu, daraltılmışsa ilk önce genişletilir. (2312.14.00)
* Grup konuşmaları modunda Control+sol ok: görüşmedeki ilk İletiı seçer. Bu, daraltıldığında ilk olarak genişletilir.<br>Bu son iki kısayolun çalışması için "Toplam" sütununa ihtiyaç vardır.
* Boşluk, F4 veya Alt+aşağı ok: İleti listesinden ayrılmadan, önizleme bölmesinden iletinin temiz veya çevrilmiş bir sürümünü okur.<br>
Not: Bir İleti 75'ten fazla HTML öğesi içeriyorsa, alınan her metin öğesi için bir bip sesi duyulacaktır. Kontrol tuşuna hızlıca basarak,tamamlanmamış İletiı hemen duyurmaya başlayabilirsiniz. (2401.09.0)
* Kaydırma kilidi. : Boşluk çubuğu, F4 veya Alt+aşağı ok tuşlarıyla hızlı okuma için İleti Çeviri modunu etkinleştirir veya devre dışı bırakır. Anında Çeviri Eklentisinin kurulup etkinleştirilmesi gerektiğini unutmayın. (2401.02.0)
* Shift+Kaydırma kilidi: Çevirinin aranabilir bir metin penceresinde gösterilmesini etkinleştirir veya devre dışı bırakır. Bu mod, İletinin tamamının Braille alfabesinde okunmasına olanak tanır.  (2401.02.0) <br>
Not: İleti çevirisi, İleti görüntüleyen pencerelerde ve sekmelerde de mevcuttur.
* Alt+yukarı ok: İletiyi sanal alıntı tarayıcısına yerleştirir;<br>
* Windows+aşağı veya yukarı oklar: sonraki veya önceki alıntıyı okur. Çeviri modu etkinse alıntı çevrilecektir. 

Not: Bu alıntı tarayıcısı İleti listesinden, İleti ayrı okuma penceresinden, İleti oluşturma penceresinden ve yazım denetimi iletişim kutusundan kullanılabilir.

### İleti listesi alanlarının duyurulması, yazılması ve kopyalanması:

Listenin her satırı, sütunlara karşılık gelen çeşitli alanlara bölünmüştür. Bir alanı Excel tablosundaki bir hücreyle karşılaştırabilirsiniz.

Aşağıdaki kısayollar odağı değiştirmeden yapılabilir:

* Harflerin üzerindeki satırın 1'den 9'a kadar olan sayı tuşları: İleti listesinin sütun satırına karşılık gelen sayı ile aşağıdaki işlemler yapılabilir:<br>
Basın: alanın değerini duyurur. Örneğin sütunlarınızın sırasına bağlı olarak 1 göndereni, 2 ise konuyu duyurur.<br>
İki kez bastığınızda: alanın değeri yazılır.<br>
Üç basış: alan değerini panoya kopyalar.

İpucu: Birden fazla klasör kullanıyorsanız hepsine aynı sütun sırasını uygulayın. Bu şekilde bir sayı her zaman aynı sütuna karşılık gelir.

### Önizleme bölmesinden veya ayrı okuma penceresinden başlıkları duyurma ve kopyalama:

* Listeden ve ayrı okuma penceresinden Alt+1'den Alt+6'ya:<br>
Bir basış başlığın değerini duyurur,<br>
İki kez basıldığında başlık değerini içeren bir düzenleme kutusu açılır. Bu iletişim kutusunu Enter ile kapattığınızda, bu değer panoya kopyalanır; bu, bir gönderenin e-posta adresini almak için çok pratiktir. <br>
Üç kez basıldığında ilgili başlığın içerik menüsü açılır. Bu yerel bir Thunderbird menüsüdür.

### Ana penceredeki ekler bölmesi ve ayrı okuma penceresi:
Aşağıdaki kısayollar ekleri duyurmanıza, açmanıza veya kaydetmenize olanak tanır.

* Alt+9 veya Alt+sonraki sayfa:<br>
Tek basış: Eklerin sayısını ve tüm eklerin adlarını duyurur. (2312.18.00)<br>Thunderbird ekler bölmesini otomatik olarak görüntülemezse, Eklenti bunu yapacak ve Thunderbird ilk eki seçecektir.<br>
İki destek:<br>
Yalnızca bir ek varsa,odağı ona taşır ve ardından içerik menüsünü görüntüler.<br>
Birden fazla ek varsa listedeki ilk eki seçin. (2312.18.00)

### Etiketleri İleti listesinden yönetme
Aşağıdaki kısayollar, Thunderbird içerik menüsünde gezinmeye gerek kalmadan etiketlerin sesli yönetimine olanak tanır.

* Shift+1'den Shift+9'a: Seslendirmeyle etiket ekler veya kaldırır.
* Shift+0: Seçilen İletideki tüm etiketleri kaldırır.
* alt+0: Tüm İleti etiketlerini duyurur.

### İleti listesinin a, c, j ve m kısayollarının seslendirilmesi

2023.11.10 sürümünden itibaren bu işaretleme kısayolları artık Eklenti tarafından seslendirilmemektedir. NVDA ilgili satırın içeriğindeki değişikliği derhal duyurur.

### Hızlı İleti filtreleme (2023.11.10)

f harfi: Hızlı filtre çubuğunu görüntülemek veya ona ulaşmak için Control+Shift+k'ye ergonomik bir alternatif. Bu kısayol, Girdi hareketleri iletişim kutusunda yapılandırılabilir.
<br>Not: Odak noktasının boş olmayan bir ileti listesinde olması gerekir. Etkin filtreyi devre dışı bırakmak için Escape tuşuna basın.

Filtreleme sonuçlarına anahtar kelime giriş alanından doğrudan erişmek için aşağı oka basın.

Bir filtre etkin olduğunda, İleti listesine her odaklanıldığında tıslamaya benzeyen bir ses çalınır. Bu özellikle pencereleri veya sekmeleri değiştirip daha sonra İleti listesine döndüğünüzde kullanışlıdır.

Bu ses sizi rahatsız ediyorsa iki seçeneğiniz var:

1. Shift+ menüsünü açın (Sekmenin üzerindeki tuş) ve Devre Dışı Bırak alt menüsünde şu seçeneği işaretleyin:<br>
İletileri listele: Liste filtrelendiğinde ve odaklanıldığında ses çalma.

2. Shift+ menüsünü açın (Sekme'nin üzerindeki tuş) ve ardından öğe üzerinde Enter'a basın: Sesler klasörünü aç. 
<br>Bu klasör Dosya Gezgini'nde açılacak,
<br>Burada filter.wav dosyasını bulacaksınız.
<br> Dosyanız aynı ada sahip olduğu sürece bu dosyayı başka bir dosyayla değiştirebilirsiniz: filter.wav.
<br>İşlem tamamlandıktan sonra NVDA'yı yeniden başlatın.

<!-- 31.10.2023 sonu -->

### Durum çubuğu ve hızlı filtre bilgilerinin duyurusu

* Alt+end veya Alt+(sol geri tuşundan ikinci tuş): 
İleti listesinden veya hızlı filtre çubuğundan: toplam veya filtrelenen İleti sayısını, birden fazla İleti varsa seçilen İleti sayısını ve filtre tanımlanmışsa filtre ifadesini duyurur. Bu bilgiler artık durum çubuğundan değil, hızlı filtre çubuğundan geliyor.<br>
Başka bir sekme veya pencereden: durum çubuğunu duyurur.
* İleti listesine odaklanıldığında, hızlı filtreleme etkinken bir ıslık sesi duyulur.


### Akıllı Cevaplama: kontrol+R ile posta listelerine Cevap verin:

Belirli posta listelerine cevap vermek için Control+Shift+L tuşlarına basmanız gerekir.Yanlış alıcıya cevap vermekten kaçınmak için listeyi cevaplamak için Control+R tuşlarına, İletiyi gönderene özel olarak cevaplamak için Control+r tuşlarına iki kez basın. 

Not: group.io bu özellikten etkilenmez.

<a İsim = "sütunlar">
<!-- 31.10.2023'te başlıyor -->

### Sütunların seçimi ve düzenlenmesi (2023.10.31)

Bu prosedür Thunderbird 115'e özgüdür ancak yeterince belgelenmediğinden burada açıklanmaktadır.

* Sütun başlıkları listesine gitmek için İleti listesinde Shift+sekme tuşlarına basın.
* Bir sütunu seçmek için sol ve sağ okları kullanın.
* "Görüntülenecek sütunları seçin" özel sütununa ulaştığınızda, üzerinde enter tuşuna basın.
* Menüde sütunları işaretleyin veya işaretlerini kaldırın, ardından bu menüyü kapatmak için Escape tuşuna basın. 
* Sütun başlıkları listesine geri döndüğünüzde, bir sütuna gitmek için sol oka basın.
* Daha sonra istediğiniz konuma yerleştirmek için Alt+sol veya sağ ok tuşlarına basın. Bu doğru şekilde seslendirilecektir.
* Diğer sütunları taşımak için bu işlemleri tekrarlayın.
* Sütun düzenlemesi tamamlandığında İleti listesine dönmek için Sekme tuşuna basın.

## klasör ağacı: hızlı gezinme (2023.10.31)

Bazı komutlar, ilk harflere göre gezinmeye izin vermek için ağaç yapısındaki klasörleri içeren bir menü görüntüler. Performans nedeniyle, komut dosyası daraltılmış dalların alt klasörlerini görüntülemez.

Ayrıca, bir hesabın veya klasörün adı kısa çizgiyle bitiyorsa okunmamış klasörler menüsüne dahil edilmeyecektir. 

Bu nedenle, az kullanılan dalları kapatarak veya hesapların adının sonuna kısa çizgi ekleyerek hesapları ve klasörleri hariç tutmanız önerilir.

<br>
2312.14.00 sürümünden beri "Birleşik Klasörler" modu desteklenmektedir. Bu modda tüm hesap adlarının @ karakterini içermesi gerekir. Bir hesabı yeniden adlandırmak için onu ağaçta seçin, Uygulamalar tuşuna basın ve ardından içerik menüsünde Ayarlar'a basın. Daha sonra “Hesap Adı” alanına gidin.

### Klasör ağacında bulunan komutlar:

* NVDA+yukarı ok veya NVDA+l (taşınabilir): seçilen klasörün adını duyurur. NVDA artık bunu tek başına yapmıyor.  
* Okunmamış klasöründe boşluk çubuğu: odağı İleti listesindeki ilk okunmamış İletiye yerleştirir.
* Enter veya Alt+yukarı ok: seçilen klasörün ait olduğu hesaptaki tüm klasörlerin menüsünü görüntüler.
* Control+Enter veya Alt+aşağı ok: seçilen klasörün ait olduğu hesap için okunmamış klasörlerin menüsünü görüntüler.
<br>Her iki durumda da son menü öğesi hesaplar menüsünü görüntüler. Oradan bir hesap seçmek için boşluk çubuğuna basabilirsiniz.
* Shift+Enter: ağaçtaki tüm hesapları ve klasörleri içeren bir menü görüntüler.
* Shift+Kontrol+Enter:ağaçtaki tüm okunmamış hesapları ve klasörleri içeren bir menü görüntüler.

Notlar :

Bu son iki komut için, menü görüntülenmeden önce biraz zaman geçecektir, çünkü komut dosyasının menüyü oluşturmak için tüm ağacı geçmesi gerekir.

Bunun yerine şu iki küçük ipucundan birini kullanın:

1. Hesaplar menüsünü görüntülemek için Alt+C tuşlarına basın, 
<br>Bir hesap seçin ve ardından Enter'a basın. 
<br>Bu hesaba ait klasörleri içeren yeni bir menü açılacaktır ve birini etkinleştirmek için bir harf kullanabilirsiniz.
2. Okunmamış klasörlerin bulunduğu hesaplar menüsünü görüntülemek için Control+Alt+Home tuşlarına iki kez hızlı bir şekilde basın. 
<br>Bir hesap seçin ve ardından Enter'a basın. 
<br>Bu hesabın okunmamış klasörlerini içeren yeni bir menü açılacaktır ve birini etkinleştirmek için bir harf kullanabilirsiniz.

<!-- 31.10.2023 sonu -->

## Pencereleri ve sekmeleri kapatma:

* Escape tuşu ayrı İleti okuma penceresini ve İleti oluşturma penceresini kapatır. İlgili seçeneklere bakın.
* Control+Geri: sekmeleri ve pencereleri kapatmak için de kullanılır. Metni düzenlerken bu kısayol önceki kelimeyi siler.

## Oluşturma penceresi:

Bu penceredeki kısayollar adresleme alanları ve ekler bölmesiyle ilgilidir.

* Alt+1'den Alt+8'e:<br>
Basın: adresleme alanının veya ekler bölmesinin değerini duyurur,<br>
İki kez basın: odağı adres alanına veya ekler bölmesine yerleştirir.
* Alt+sonraki sayfa: Ekler bölmesi için Alt+3 ile aynıdır. 
*Notlar:<br>
Alt+3 ile ekler bölmesinin duyurusunda dosya adlarının numaralandırılmış bir listesi ve bunların toplam boyutu belirtilir,<br>
Odak ek listesinde olduğunda escape tuşu ileti gövdesine geri döner.
* Alt+yukarı ok: yazılmakta olan İletiı sanal alıntı tarayıcısına yerleştirir;
* Windows+Aşağı/yukarı oklar: alıntı tarayıcısının sonraki veya önceki satırını duyurur; Bu, yanıtladığınız İletiı pencereleri değiştirmeden dinlemenize olanak tanır.
* Windows+sağ/sol oklar: pencereleri değiştirmeden sonraki veya önceki alıntıya gider.<br>

## Yazım denetimi iletişim kutusu:

Bu iletişim kutusu açıldığında, Eklenti otomatik olarak sözcükleri ve yazımlarını duyurur. Bu, oluşturma penceresi seçeneklerinde devre dışı bırakılabilir.

Sözcüğü değiştirme düzenleme alanında aşağıdaki kısayollar mevcuttur:

* Alt+yukarı ok: yanlış yazılan sözcüğü ve değiştirme önerisini duyurur. 
* Çift basıldığında Alt+yukarı ok: Bu bağlamda otomatik olarak başlatılan sanal alıntı tarayıcısı sayesinde yanlış yazılan kelimenin bulunduğu cümleyi duyurur.
* Enter: düzenleme alanından çıkmadan "Değiştir" düğmesine basın.
* Shift+enter: “Tümünü değiştir” düğmesine basın.
* Control+Enter: “Yoksay” düğmesine basın.
* Shift+kontrol+Enter:“Tümünü Yoksay” düğmesine basın.
* Alt+Enter: Yanlış yazıldığı bildirilen kelimeyi sözlüğe ekler.

## Adres defteri, daha kolay yönetim (v.2024.02.07)

Eklenti, adres defteri duyurularını iyileştirir ve sanal sürükle ve bırak yöntemiyle adres defterlerini ve posta listelerini düzenlemenize olanak tanıyan klavye komutları sağlar.

### Geliştirilmiş duyurular:

* Adres defterleri ve posta listeleri ağacı: Eklenti aynı zamanda bir öğenin türünü de duyurur: adres defteri veya ana adres defterinin listesi,
* kişi listesi: Eklenti aynı zamanda seçilen kişinin e-posta adresini de duyurur.

### Arama özeti:

* Arama alanından Sekme tuşu: "Görüntüleme seçeneklerini listele" düğmesini atlayarak doğrudan kişiler tablosuna gider. Buna kişiler tablosundan Shift+Sekme tuşlarıyla erişilebilmektedir;  .  
* Escape tuşu:
	* Adres defteri ağacından odağı arama alanına getirin;
	* Arama alanından odağı adres defteri ağacına getirin;
	* Kişiler tablosundan odağı arama alanına getirin;
 * Control+Uygulamalar veya Sekme üzerindeki tuş: aşağıdakileri içeren bir içerik menüsü açar: Adres defterleri ve posta listeleri ağacına erişim, Kişiler tablosuna erişim, Yeni adres defteri, Yeni kişi, Yeni liste, İçe aktarma. İlk ikisinin dışında bu öğeler Adres Defteri araç çubuğundan gelir. 
* Kişiler tablosundaki "a" harfi: seçilen kişileri hedef olarak tanımlanan dağıtım listesine veya adres defterine sürükleyip bırakır. Bu tuşa ilk bastığınızda bir menü aracılığıyla varış noktası sorulur. Daha sonra kaynak listesini veya adres defterini değiştirene kadar hedef size tekrar sorulmaz.
* Kişiler tablosundaki "d" harfi: listeler ve hedef adres defterleri menüsünü görüntüler.

### Örnek 1: Kişisel Adres Defterinde posta listesi oluşturma:

* Adres defteri ağacına gidin ve "Kişisel adresler"i seçin. Yalnızca seçilen not defterinde yeni bir liste oluşturulur;
* Control+Uygulama veya Sekme'nin üzerindeki tuşa basın ve menüde Enter'a basın: Yeni liste;
* Açılan iletişim kutusunda listenin adını girin, örneğin: Ailem. Bu iletişim kutusunu kullanarak kişileri ekleyebilirsiniz ancak örneğin bu iletişim kutusunu Tamam düğmesini kullanarak kapatın;
* Adres defterleri ve listeler ağacına döndüğünüzde şunun görünümünü fark edeceksiniz: Ailem, Kişisel adresler listesi, <br>
"Kişisel adresler"i seçin;
* Kişiler tablosuna bir arama anahtar sözcüğü veya Sekme girmek için Sekme tuşuna basın veya Control+Uygulamalar menüsünü veya Sekme'nin üzerindeki tuşu kullanın;
* Kişiler tablosunda, Control+Boşluk çubuğu, Control+aşağı ok, Control+Boşluk çubuğu vb. standart yöntemle bir veya daha fazla kişiyi seçin; 
* Bunları posta listesine sürükleyip bırakmak için a harfine basın. İlk kez yetkili varış noktalarının menüsü görüntülenecektir. "Yeni liste adı" öğesini seçin ve Enter tuşuna basın. a harfine bir sonraki basışınızda, bu menü görüntülenmeden aynı hedef kullanılacaktır. 
* Sürükle bırak işlemi sonunda bir bip sesi duyulacak ve odak arama kutusuna verilecektir.
* Yeni bir kelime girin, Sekme tuşuna basın, kişileri seçin ve ardından onları "Yeni liste adı" listesine eklemek için a harfine tekrar basın 

### Kişileri Toplanan Adreslerden Farklı Adres Defterlerine Taşıma:

1. Adres defteri ağacına gidin ve “Toplanan adresler”i seçin;
2. Kişiler tablosuna gidin;
3. Bir veya daha fazla kişiyi seçin;
4. Yeni bir varış yerini önceden seçmek için isteğe bağlı olarak "d" harfine basın;
5. Kişiler tablosuna geri döndüğünüzde sürükleyip bırakmak için "a" harfine basın;
6. İşlem tamamlandıktan sonra odak arama alanına verilir. İsteğe bağlı olarak bir ad girin ve 2'den 5'e kadar olan işlemleri tekrarlayın.


## Eklenti güncelleme menüsü (v.2402.26.00)

Bu menüye erişmek için Sekme tuşunun üzerindeki AltGr+Shift+ tuşuna basabilir veya aşağıdakileri yapabilirsiniz:

* Ana Thunderbird penceresine gidin,
* Sekme tuşunun üzerindeki tuşa basın,
* Bağlam menüsünde Güncelleme öğesini seçmek için yukarı oka basın, ardından Enter'a basın,
* Daha sonra yeni bir içerik menüsü size şu seçeneklerden birini sunar: Güncellemeyi kontrol et, Otomatik güncellemeleri Etkinleştir veya Devre Dışı Bırak ve YYMM.DD sürümünü yükle; burada YYMM.DD, indirilebilecek sürümdür. İkincisi, otomatik güncellemede mevcut olandan daha yeni olabilir.

## Dış tamamlayıcılar

### Thunderbird 115 (2023.10.31)1 için Gelen Kutusuyla Eklenti Başlangıcı

Thunderbird başladığında bu Eklenti otomatik olarak şunları seçer:

* klasör ağacında seçtiğiniz hesabın “Gelen Posta” klasörü.
* Seçilen hesabın gelen posta klasöründeki son İleti. 
* Seçilen hesabın gelen posta klasöründeki ilk okunmamış İleti. 

Tesis :

* Thunderbird'de “Araçlar” menüsünü açın ve aşağıdakileri doğrulayın: Eklentiler ve temalar;
* Modül Yöneticisi sayfasında kendinizi arama kutusuna yerleştirin. Navigasyon modunda e harfine basarak hızlı bir şekilde ulaşabilirsiniz;
* yaz: Gelen Kutusu ile başlayın ve ardından Enter tuşuna basın;
* örneğin "Gelen kutusuyla başla :: Ara :: Thunderbird Modülleri" sekmesini manuel olarak seçin.daha sonra aradığınız modülün adını taşıyan 3. düzey başlığa ulaşana kadar 3 tuşuna veya tırnak işaretine basın; 
* Aşağı oku kullanarak "Thunderbird'e Ekle" bağlantısına gidin ve Enter tuşuna basın;
* Prosedürü takip edin ve Thunderbird'ü yeniden başlatın;
* Her şey yolunda giderse Thunderbird ana sekmede açılacak ve İleti listesine odaklanacaktır;


Gelen Kutusuyla Başlat seçeneklerini ayarlayın:

* "Eklenti Yöneticisi" sekmesine dönün;
* Gerekirse kendinizi navigasyon moduna geçirmek için arama alanını bırakın;
* Yüklü modüller listesinde "Gelen Kutusuyla Başla" başlıklı 3. seviye başlığa ulaşmak için 3 tuşuna gerektiği kadar basın;
* Daha sonra şu düğmeyi kullanarak doğrulayın: Modül seçenekleri. Bu, şu başlıklı yeni bir sekme açar: Gelen Kutusu, Ayarlar ile Başlat;
* Seçenekleri ayarlayın ve ardından Thunderbird'ü yeniden başlatın.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2404.23.00/thunderbirdPlusG5-2404.23.00.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=fr

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=fr