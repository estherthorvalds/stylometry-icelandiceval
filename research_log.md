# Rannsóknardagbók / Research Log

## Verkefni: stylometry-icelandiceval

**Rannsakandi:** Esther Ýr Þorvaldsdóttir
**Ráðgjafi:** Miðeind (tengiliður: Hulda Óladóttir)
**Upphaf:** 13. mars 2026

---

## Hvernig á að nota þessa dagbók / How to use this log

Sniðmát:

```
### [Dagsetning] — [Stutt lýsing]

**Tími:** [t.d. 2 klst]

**Hvað gerði ég:**
-

**Uppgötvanir:**
-

**Hugsanir / túlkun:**
-

**Opnar spurningar:**
-

**Næstu skref:**
-
```

---

## Færslur / Entries

### 13. mars 2026 — Verkefni hefst / Project kickoff

**Tími** 2 klst.

**Hvað gerði ég:**
- Fékk staðfestingu frá Miðeind á ráðgjöf 12. mars 2026 kl. 11:30
- Setti upp skráningarkerfi (research log, reference tracker, decisions log)
- Setti upp GitHub repo: stylometry-icelandiceval

**Uppgötvanir:**
- Miðeind er með útistandandi NSN umsókn til að útbúa fleiri mælipróf — verkefnið rímar vel við þá vinnu
- Ráðlagt að byrja á yfirliti yfir próf sem eru til fyrir önnur tungumál
- Verkefnið tvíþætt: rannsókn + mælipróf (og keyrsla á völdum líkönum)
- Lágmarksstærð fyrst, bæta við ef tími gefst
- Lykiláskorun: að skilgreina eitt rétt svar fyrir stílbragð
- Miðeind notar orðið "mælipróf" yfir benchmark
- Fann Hinrik Hafsteinsson MLT201F-stylometry repo — stílmælingar á íslensku frá HÍ 2019
- Fann Global MMLU (ACL 2025) — menningarlega hlutdrægni í þýddum mæliprófum

**Hugsanir / túlkun:**
- 

**Opnar spurningar:**
- Hvaða tungumál eru best til samanburðar við íslensku? (málsvæði með rýr málföng, formfræðilega flókin)
- Hvaða einkenni stílbragðs er hægt að mæla með sjálfvirku prófi?

**Næstu skref:**
- Hefja leit að mæliprófum fyrir stíl á öðrum tungumálum


### 16. mars 2026 — Yfirferð á mæliprófum Miðeindar + heimildaleit

**Tími:** 5 klst.

**Hvað gerði ég:**
- Fór yfir öll sex mæliprófin á Miðeind stigatöflu og skráði niður
- Skoðaði GED (icelandic-sentences-gec) og Belebele (facebook/belebele isl_Latn) í smáatriðum á HuggingFace
- Byrjaði að leita að stílmælingum á öðrum tungumálum
- Fann 6 viðeigandi greinar, þar á meðal Milička (2025) um tékknesku sem byggir á Biber (1988)
- Skoðaði „Benchmark of stylistic variation in LLM-generated texts“ eftir Milička et al.

**Uppgötvanir:**
- WinoGrande - Samhengi og tengingar (persónufornöfn) - 1000 dæmi
- GED - Málfræðivillur úr villubankanum - 200 dæmi
- Inflection - 1 shot perfect match - 300 dæmi
- Babele - Lesskilningur með 4 valmöguleikum - 900 dæmi
- ARC-challenge - Er ekki tungumálapróf!! Margar villur, illskiljanlegt þótt villur yrðu lagfærðar. - 1.230 dæmi
- Wiki - Þekking af Wikipediu. GPT-4o fer yfir. Hér eru einnig villur, ætli 4o myndi refsa fyrir það að líkanið leiðrétti villurnar? - 1900 dæmi
- Milička (2025) notaði Multi-Dimensional Analysis (Biber 1988) til að mæla stílbreytileika í LLM-texta á tékknesku og ensku. 
- Biber (1988) skilgreindi 6 víddir textabreytileika í ensku. Biber (1995) útvíkkaði í 4 tungumál — aðferðin er tungumálayfirfæranleg en víddirnar sjálfar breytast
- WikiQA-IS notar GPT-4o sem dómara — en Gemini 3.1 Pro er betri í íslensku en GPT-4o. Veikari líkan dæmir sterkara líkan — „ceiling problem"
- Belebele: hætta á overfitting þar sem sama prófið er á 122 tungumálum
- Steinþór Steingrímsson: læsileikamælingar (LIX, Dale-Chall, setningaþyngd) ná ekki til stíls — setningagerð vantar
- Samtal við ferðamann: mínimalískur ritháttur (stuttar setningar, engin lýsingarorð) skorar „auðvelt" á formúlum en er erfitt að lesa — sönnun þess að yfirborðsmælingar duga ekki

**Hugsanir / túlkun:**
- Öll prófin á stigatöflu Miðeindar hafa kosti og galla. ARC virðist þó ekki gegna því hlutverki að kanna íslenskugetu risamállíkana. 
- Til að hafa 1 rétt svar væri betra að nota 4 valmöguleika en 2 (minna af ágiskunum sem gefa rétt svar fyrir).
- Þýdd próf geta verið lærð utanbókar á öðrum málum - ofmátun.
- Mikilvæg atriði geta týnst í vélþýddum spurningum (ARC prófið mjög undarlegt).
- Biber/Milička aðferðin er fræðilega sterk en full aðlögun að íslensku er of stórt verkefni.
- Möguleg lausn: proof of concept með einni vídd (frásagnarvídd / narrativity) sem er vel skilgreind með markaðri íslenskri málheild (eða aðra vel þáttaða texta?).
- Verkefnið gæti verið: skýrsla + ein vídd útfærð og prófuð sem proof of concept.
- Fríða Á. Sigurðardóttir gæti verið dæmi um mínimalískan stíl á íslensku.
- Biber/Milička aðferðin leysir hugsanlega vandamál Miðeindar um „eitt rétt svar“ — í stað þess að dæma hvort stíll sé réttur eða rangur er textinn mældur í víddum (t.d. frásagnarvídd). Þetta er ekki spurning um rétt/rangt heldur hvar textinn lendir á kvarða.

**Opnar spurningar:**
- Væri betra að nota nokkra „dómara“ og finna meðaltal? 
- Hvaða málfræðilegir eiginleikar myndu skilgreina frásagnarvídd í íslensku? (beyging sagna, persónufornöfn, tíð)
- Er til nógu stórt merkt málheild á íslensku til að keyra factor analysis?
- Gæti perplexity (eins og Steinþór notaði) verið viðbótarmæling við hliðina á stílvíddum?

**Næstu skref:**
- Lesa Milička (2025) — hvaða eiginleikar voru notaðir fyrir tékknesku?
- Skoða Biber (1995) Dimensions of Register Variation — hvernig aðlagaði hann aðferðina að öðrum tungumálum?
- Væri góð hugmynd að gera tvöfalt próf um frásagnargetu líkana? Kanna getu þeirra til að flokka frásögn í texta vs. að búa hann til?
- Er frásagnargeta mögulega of marglaga til að nota sem fyrsta proof of concept? Væri betra að nota eitthvað einfaldara eins og formlegt vs. óformlegt? Eða læsilegt vs. ólæsilegt sbr. Steinþór?
- Bæta öllum nýjum heimildum í reference_tracker.csv
- Hafa samband við Steinunni um stöðu verkefnis og proof of concept hugmynd.
- Bera undir Huldu hjá Miðeind.


### 17. mars 2026 — Lestur á Milička + rammi að myndast

**Tími:** 3 klst.

**Hvað gerði ég:**
- Las fyrsta hluta Milička et al. (2025)
- Biber er aðgengilegur á Landsbókasafni 4. hæð 400.141 Bib
- Glósur um MDA aðferðafræðina og lykilspurningar Biber
- Uppfærði decisions log: tvíþætt mæliprófshönnun og proof of concept umfang

**Uppgötvanir:**
- MDA (fjölvíddargreining): Aðferð sem telur margar málfræðilega eiginleika í texta og notar síðan þáttagreiningu til að finna hvaða eiginleikar þyrpast saman. Hver þyrping myndar vídd (t.d. frásagnarstíll) þar sem hægt er að gefa hvaða texta sem er stig og bera saman við aðra.
- Milička skoðaði aðeins textagerð (generation), ekki greiningu (detection). 
- Instruction-tuned model vs. base model: base model frá Anthropic/OpenAI ekki aðgengileg. Milička notaði opin líkön (Llama o.fl.) fyrir þann samanburð. 
- Stíltilfærsla (stylistic shift) = hversu mikið LLM-texti víkur frá mannlegum texta á MDA víddum. Tilgáta: tilfærsla meiri á tungumálum með rýr málföng vegna færri þjálfunargagna (og þar með minni stílfjölbreytni). Þess vegna skiptir máli að skoða ensku og íslensku hlið við hlið.
- Rannsóknarspurningar Milička sem eiga við mína rannsókn:
    (1) How well can current LLMs produce stylistically diverse texts from various genres and text types? // Hversu vel geta stór tungumálalíkön (LLM) dagsins í dag búið til stílfræðilega fjölbreytta texta úr ýmsum bókmenntagreinum og textategundum?
    (2) Are texts created using current LLMs stylistically shifted consistently across different models? I.e., is there some AI-language stylistic attractor? // Eru textar sem búnir eru til með stórum málalíkönum (LLM) í dag með stöðug stílfræðileg frávik þvert á mismunandi líkön? Þ.e.a.s. er til einhvers konar stílfræðilegur aðdráttarpunktur í gervigreindarmáli?
    (4) What is the difference between texts generated using a simple system prompt and texts generated using long helpful assistant system prompt? // Hver er munurinn á textum sem eru búnir til með einfaldri kerfisábendingu og textum sem eru búnir til með langri kerfisábendingu frá hinum hjálpsama aðstoðarmanni sem risamállíkön eru fínþjálfuð til að verða?
    (5) Are stylistic features dependent on the sampling temperature? // Eru stíleigenleikar háðir hitastigi (temperature)?
    (6) Is the stylistic shift smaller in English than in a language underrepresented in the training data? // Er stíltilfærsla minni á ensku en á tungumáli með rýr málföng?
- CL vs. NLP: Reiknileg málvísindi nota tölvur til að skilja tungumál. NLP notar tungumál til að byggja tækni. Verkefnið situr á mörkum beggja — CL aðferðafræði, NLP útkoma.

**Hugsanir / túlkun:**
- Milička og félagar gerðu rannsóknina á ensku OG tékknesku til að sýna stíltilfærslu á tungumáli með rýr málföng. Sama uppbygging (enska + íslenska) gæti mögulega gert mína rannsókn samanburðarhæfa.
- Tvíþætt hönnun (greining + textagerð) gæti verið framlenging á vinnu Milička og félaga.
- Málheildir: Þarf ég að byggja íslensk LLM-málheild svipað og AI-Brown? Og Risamálheildina (RMH) sem viðmið fyrir mannlegan texta og búa til LLM-hliðstæðu? Mörkuð íslensk málheild (MÍM) gæti nýst ef ég fer dýpra í setningafræði sbr. fyrirlestur Steinþórs.
- Siðfræðileg spurning: Milička talar um að mæliprófið sé m.a. fyrir LLM-framleiðendur. En ef við hjálpum líkani að líkja betur eftir mannlegum stíl, erum við þá að hjálpa gervigreind að búa til list án mannlegrar þátttöku (agency)? Þetta var ekki markmið verkefnisins en gæti orðið afleiðing. Þarf að hugsa meira um þetta og hugsanlega ræða í skýrslunni.

**Opnar spurningar:**
- Hvaða málheild ætti að nota sem grunn? RMH, MÍM, eða byggja eitthvað nýtt?
- Hversu stórt LLM-málheild þyrfti ég að búa til? Hversu mörg líkön, hversu margir textar per tegund?
- Gæti ég endurnýtt hluta af Milička aðferðinni beint (t.d. fyrirmæla-snið) eða þarf að aðlaga allt fyrir íslensku? Væri þá hægt að nota aðferðina sem Annika talaði um á fyrirlestrinum um færeysku? Menningarleg aðlögun eða staðfærsla (cultural adaptation or localization, culturally-aware evaluation or cultural grounding).
- Spurning um að einblína á instruction-tuned líkön með mismunandi fyrirmælum?
- Siðfræði: Ætti skýrslan að fjalla um hvernig betri stílmælingar gætu verið misnotaðar?

**Næstu skref:**
- Halda áfram að lesa Milička, sérstaklega aðferðafræðikaflann um málheildir og val á eiginleikum.
- Skoða Biber (1995) til að skilja hvernig MDA var aðlagað að öðrum tungumálum.
- Kanna RMH og MÍM betur - hvaða textategundir eru fyrir hendi og hversu vel ná þær yfir mismunandi málsnið?
- Reyna að bóka fund með Huldu og Svanhvíti og fara yfir þessi atriði. Svo tala við Steinunni.

### 18. mars 2026 — Lestur á Milička (gögn) + tokenization + málheildir

**Tími:** 2 klst. 

**Hvað gerði ég:**
- Las kafla 2 í Milička og íhugaði sambærileg gögn og málheildir fyrir þessa rannsókn. 
- Prófaði OpenAI tokenizer á íslensku vs. ensku vs. frönsku — sama fréttartexti, þýddur af Erlendi.
- Rannsakaði RMH og MÍM til samanburðar við Koditex (málheild Milička).
- Bjó til data/figures og færði inn myndir af mismunandi tókunum (enska, íslenska, pólska).

**Uppgötvanir:**
- BPE tokenization: Íslenski textinn: 531 tókar / 1.546 stafir (2,9 stafir/tóki). Enska: 349 tókar / 1.929 stafir (5,5 stafir/tóki). Franska: 459 tókar / 2.101 stafir (4,6 stafir/tóki). Líkanið þarf 52% fleiri tóka til að vinna íslenska textann. Mörk tókanna skera oft í gegnum beygingarendingar og samsett orð.
- Gerði betri tilraun á tókun. Notaði texta frá RÚV á þremur mismunandi tungumálum en allt um sama efni. Ekki beinþýtt en þó nálægt. Icelandic: 266 tokens, 829 characters — 3.1 characters/token, English: 161 tokens, 823 characters — 5.1 characters/token, Polish: 276 tokens, 851 characters — 3.1 characters/token
- RMH: 1,3 milljarðar orða, þáttað
- MÍM: 25 milljón orð, inniheldur 24% bækur, 22% dagblöð (má nota í rannsóknarskyni en ekki í gróðastarfsemi)
- Milička valdi tékknesku vegna (1) var þegar til fyrir MDA pipeline (Cvrček) og (2) Koditex málheildar. Ekki vegna þess að þeir tala tékknesku, heldur vegna málfanga.
- Þarf líklega að búa til AI-málheild fyrir íslensku (láta LLM búa til texta sem samsvara textategundum í MÍM/RMH).
- Milička sleppti líkönum sem gátu ekki framleitt texta á tékknesku við hitastig 0 (endurtóku sömu setningu). Áhugaverð ákvörðun þar sem það eitt og sér gefur af sér merkilegar niðurstöður fyrir rannsóknina; stundum endurtóku þau sömu setninguna aftur og aftur á tékknesku ef hiti var 0. Ef líkan „bilar“ á íslensku ætti ekki að skrá það sem bilun?
- 65 líkön á stigatöflu Miðeindar — þarf líklega ekki að prófa öll, heldur velja stefnumarkandi úrtak (efstu, miðjuna, opin líkön).

**Hugsanir / túlkun:**
- Mismunurinn á tókun milli tungumála sýnir að líkön vinna íslensku á allt annan hátt en ensku. Virtist ekki splittað á myndan orða. Hefur bein áhrif á getu til að læra og endurskapa stílmynstur sem byggja á beygingarformum.
- Líklegast best að handvelja kafla úr bæði RMH og MÍM. 
- Spurning fyrir Miðeind: er til MDA pipeline eða eitthvað sambærilegt fyrir íslensku? Ef ekki, þá er stærsta verkefnið að búa það til - EF rannsóknin byggir mest á Milicka, sem er stórt ef. 

**Opnar spurningar:**
- Er til MDA pipeline fyrir íslensku?
- Hvaða líkön ætti að prófa? Spyrja Miðeind.
- Hvernig ætti að skrá bilun þegar líkan getur ekki búið til íslenskan texta (sbr. þegar tékkneskar setningar voru endurteknar þegar hiti var 0)? Fengi líkanið bara 0 eða yrði því sleppt?
- Væri gott að nota valda kafla úr bæði RMH og MÍM? 

**Næstu skref:**
- Lesa næsta kafla Milička.
- Undirbúa spurningalista fyrir fund með Miðeind.
- Skoða hvort MDA-verkfæri eða eitthvað sambærilegt sé til fyrir íslensku.


### 19. mars 2026 — Málheildir, Milička aðferðafræði

**Tími:** [fylltu inn]

**Hvað gerði ég:**
- Yfirferð á tókatilraun með Karolinu. Pólskumælandi vinnufélagi settist hjá mér og las hvernig tokenizer OpenAI splittaði orðum á pólsku. Henni þótti margt einkennilegt en stundum splittað á merkingarbærum einingum (hún lýsti því á sama hátt og morfem). Svipaðar niðurstöður á íslensku þar sem stundum er splittað morfem en stundum virðist það vera af handahófi. 
- Skoðaði RMH og MÍM — innihald, stærð, textategundir.
- Las áfram Milička, sérstaklega kafla 3.2 (tölfræðileg úrvinnsla) og AI-Brown/.AI-Koditex corpus greinina.
- Fékk Claude Opus 4.5 til að gera Python skriftu sem útfærir formúlur Milička (1-4). Mun gera prófanir hér. 

**Uppgötvanir:**
- Milička notaði 500 orð sem prompt (orig1).
— Líkönin beðin um að skrifa 5.000 orð (model).
- AI-Koditex inniheldur bæði LLM-texta og mannlegan samanburðartexta (orig2) í pörum frá sama upphafi - þarf að athuga betur síðar. 
- AI Koditex skoðað nánar: ENG 864k tokens per model (27 m. í heild) og CZE 768k tokens per model (21,5 m. í heild).
- Formúlur: (1) Δv = munur LLM vs. mannlegur texti per vídd, (2) i = náttúrulegur breytileiki innan mannlegs texta, (3) b_d = staðlaður samanburður, (4) B = ein tala yfir allar víddir. Formúlur handskrifaðar í dagbók. 

**Hugsanir / túlkun:**
- 500 orð sem prompt er vel framkvæmanlegt, auðvelt að fá úr RMH/MÍM.
- MÍM líkist Koditex í hlutverki (nokkrar mismunandi textategundir, hannað fyrir málrannsóknir) en er mun minna (25M vs. 9M orð).
- RMH og MÍM eru þegar merkt — POS, lemma, fall, tala, kyn — sem þýðir að eiginleikar fyrir MDA eru nú þegar til staðar í gögnunum.
- Þarf samt að búa til AI-hliðstæðu (LLM-texta).
- Formúla 3 er kjarninn; staðlar sjálfkrafa fyrir víddir sem eru náttúrulega breytilegri.
- Formúla 4 óþörf fyrir proof of concept með einni vídd (væri ekki að leita að meðaltali fyrir allar víddir).
- Gæti Greynir leyst af hólmi regex-nálgun í skriftunni? Það gefur málfræðigreiningu (fall, tölu, kyn, tíð) í stað ágiskunar út frá endingum en hefur ekki reynst vel á óformlegum textum (41% þáttun í verkefni um Bland.is og Hugi.is). Líklegast betra að finna texta í RMH og MÍM.

**Opnar spurningar:**
- Hvernig er AI-Koditex skipulagt í raun? Skoða heima, niðurhal.
- Hversu mörg textapör per textategund þarf til að fá tölfræðilega marktækar niðurstöður?
- Er til MDA pipeline eða sambærilegt verkfæri fyrir íslensku?
- Hvaða líkan á að prófa? 

**Næstu skref:**
- Skoða AI-Koditex skráarstrúktúr.
- Prófa Python skriptuna með mismunandi textategundum.
- Halda áfram lestri á Milička.


### 21. mars 2026 — Proof of concept keyrt

**Tími:** 8 klst.

**Hvað gerði ég:**
- Tók 600 fréttatitla frá Húna (huni.is) til að vinna með. 
- Lét nokkur risamállíkön búa til texta sem líktist fréttatitlum Húna. 
- Spurði Steinunni hvernig fólk er almennt á POS-merkja textana sína, Greynir nær ekki öllu.
- Lét Sonnet 4.6 POS-merkja alla textana (bæði mannlegu og gervigreindar).
- Keyrði samanburð á frumlagsleysi í fréttatitlum, fyrst á 2x40 fréttafyrirsögnum, mannlegum vs. fjórum mismunandi risamállíkönum (allt í spjalli, ekkert API).
- Keyrði samanburð á frumlagsleysi í fréttatitlum, síðar á 520 fyrirsögnum: mannlegum vs. Gemini 3 Thinking og Le Chat Fast.
- Uppgötvaði að Le Chat festist í endurtekningarlúppu.
- Greindi vandamál með v2 skriftu sem ég fékk frá Claude Opus 4.6; það var röng staðsetning á falltagi. Hætti við að nota hana. 
- Notaði v1 skriftuna til að bera saman og athuga hvort ég fengi niðurstöður til að prófa aðferðir Milička. 

**Niðurstöður:**
- Mannlegar fyrirsagnir: 11,2% subject drop (58 af 520).
- Gemini 3 Thinking: 2,3% subject drop (12 af 520).
- Le Chat Fast: 0,0% subject drop (0 af 520) - Ómarktækt!
- Bæði LLM-líkönin sýna minni subject drop en mannlegir fréttamenn (Le Chat er þó ómarktækt).
- Le Chat hafði hærra hlutfall nafnyrða í nefnifalli (0,3166) en mannlegur texti (0,2778) — útskýrir meira en náttúrulegar fyrirsagnir.
- Le Chat niðurstöður eru ekki áreiðanlegar vegna endurtekningarlúppu — líkan sem festist í lykkju framleiðir ekki fjölbreytt úrtak.

**Hugsanir / túlkun:**
- Nú skil ég af hverju Milička sleppti líkönum sem festust í endurtekningum. Þetta er ekki útilokun á gögnum — gögnin eru einfaldlega ónothæf til stílsamanburðar. Le Chat endurtók sama mynstur og framleiddi aldrei þær setningagerðir þar sem frumlagið er horfið. Kannski hefði það gert það á einhverjum tímapunkti, ef villan hefði ekki komið upp. Þetta gerir það að verkum að 0% er ekki áreiðanlegt hlutfall til að horfa til.
- Málfræði og stíll eru samtvinnuð á íslensku. Le Chat Fast greip stíl en gerði málfræðivillur. Le Chat Thinking gerði færri málfræðivillur, þó einhverjar. Gemini 3 Thinking komst næst mannlegri hegðun og var því valið á móti Le Chat Fast. 
- Sonnet-merking er ekki jafn áreiðanleg og RMH/MÍM merking. Sá eina lemmuvillu bara við það að opna skjalið, líklega fleiri sem ég sá ekki. Fyrir stærra verkefni eða áreiðanlegri tilraun þarf betri merkingu.
- Greynir vandamál á óformlegum texta er enn óleyst, ég veit ekki hvort Greynir nær fréttatitlum þar sem þeir hafa oft óvanalega setningamyndan. 

**Opnar spurningar:**
- Ætti ég að sleppa Le Chat úr niðurstöðum eða skrá sem bilun? (Svar: skrá sem bilun með útskýringu, eins og ég ræddi áðan).
- Hversu margar aðrar stílbreytur get ég bætt við án þess að þurfa djúpa þáttun?
- Er 520 fyrirsagnir nóg til að sýna tölfræðilega marktækt? (chi-squared segir já en þarf að prófa Milicka leiðina líka).

**Næstu skref:**
- Taka til í repoinu, allt of mikið af prófunum sem gerðu ekkert merkilegt. 
- Gera próf byggt á formúlu Milicka (spurning hvort það verði í Heimaverkefni 4 eða hvort þetta dugi). 
- Undirbúa spurningalista fyrir Miðeind.
- Skrifa upp niðurstöður fyrir Heimaverkefni 4. 


### 22. mars 2026 — Proof of concept tilbúið

**Tími:** 8 klst.

**Hvað gerði ég:**
- Gerði fjölda tilrauna með Claude Opus 4.6 til að fullkomna Milička-formúluna. Er nú ímilicka_headlines.py með íslenskum athugasemdum.
- Keyrði formúlu 1, 2 og 3 á öllum fjórum risamállíkönum (Gemini 3 Thinking, Le Chat Fast, Le Chat Thinking, GPT 5).
- Útfærði bootstrap SE (1000 endurúrtök, seed=42) þar sem ég hafði ekki pöruð gögn eins og Milička.
- Fínpússaði flokkun: harðkóðaði útilokun á boðhætti (sb...), gervifrumlag ("það" + sögn), og nafnliðarfyrirsögnum (engin sögn).
- Skrifaði fyrstu drög að svörum við Q3 í heimaverkefni 4.
- Bjó til PowerPoint kynningu (10 glærur) með bakgrunnsskýringum um stigatöfluna, bilið, og formúlu Milička, svo tillagan sé skýr fyrir Miðeind.

**Hvað fann ég:**
- Ég keyrði margar mismunandi tegundir formúlu og allar virkuðu (kúnstin var að greiða úr málvísindalegum rökvillum, formúlan og kóðinn var flottur)
- Mannleg grunnlína: 18,5% fyrirsagna án frumlagsnafnliðar (af 520 fyrirsögnum af huni.is / Húnahorninu)
- Bootstrap SE: 6,82% (staðalskekkja)
- Náttúrulegt frávik: 8,8% (mismunur á tveimur helmingum mannlegu gagnanna)
- Le Chat Thinking (b_d = +0,27) — EINA líkanið innan mennskra marka
- Gemini 3 Thinking (b_d = +2,31) — verulegt frávik
- GPT 5 (b_d = +2,71) og Le Chat Fast (b_d = +2,71) — gera engar fyrirsagnir án frumlagsnafnliðar
- Le Chat Fast festist í endurtekningarlúppu — niðurstöður óáreiðanlegar og segja ekkert um getu líkansins í 520 dæmum
- Fallið er ekki fullkomið. Gögnin ekki fullkomin heldur. T.d. rangflokkun vegna erlendra sérnafna (t.d. KPMG merkt 'e' án fallupplýsinga), en ég lét það ekki stoppa proof of concept!

**Hugsanir / túlkun:**
- Formúla Milička virkar á þessu íslenska örprófi. b_d gefur samanburðarhæfan kvarða.
- Hugmyndin um "eitt rétt svar" leysist þannig: mannlega grunnlínan skilgreinir svæðið, SE skilgreinir mörkin, og b_d mælir hversu langt líkanið er frá þeim mörkum.
- Frumlagsnafnliðarleysi er áhugavert stíleinkenni vegna þess að það er næstum einstakt fyrir fréttafyrirsagnir — gerir afmörkun auðveldari.
- Þáttun er veikasti hlekkurinn — Sonnet sem POS-tagger er ekki jafn áreiðanlegur og RMH merking, en fyrir proof of concept dugir það.

**Opnar spurningar:**
- Hvernig bregðast Miðeind við þessari nálgun? Er b_d nógu gott fyrir stigatöfluna?
- Hvaða líkan á stigatöflunni á að prófa í lokaverkefninu? (65 líkön!)
- Er MDA pipeline til fyrir íslensku eða þarf að byggja það?
- Hvaða málheild er best fyrir lokaverkefnið — RMH, MÍM, eða bæði?
- Fæ ég API-aðgang frá Miðeind?

**Næstu skref:**
- Fundur með Miðeind — sýna niðurstöður og spyrja spurninganna hér að ofan
- Bæta heimildum í reference_tracker.csv


### 23. mars 2026 — Fundur með Miðeind + tölvupóstur til kennara
 
**Tími:** 2 klst (fundur + skrif)
 
**Hvað gerði ég:**
- Fundur með Miðeind (Huldu og Svanhvíti) — sýndi niðurstöður úr proof of concept
- Sendi tölvupóst til kennara (Steinunnar Rutar) með spurningum um heimaverkefni og verkefnið
 
**Hvað fann ég:**
- Miðeind leist vel á verkefnið, sérstaklega að rannsóknin horfði ekki aðeins til ensku heldur líka tékknesku (Milička)
- Þáttari: Miðeind hefur gervigreindaþáttara sem virðist virka vel, en hann er ekki aðgengilegur. Ekki hægt að fá aðgang.
- Þær bentu á að val á þáttara gæti farið eftir víddinni (hvort þurfi setningatré eða ekki).
- Ekkert API frá Miðeind — bentu á Haffa (Hafstein Einarsson) eða Gervigreindarsetrið. 
- Áætlaður kostnaður ef ég borga sjálf: ~5.000 kr — ekki mikið en mögulega ekki þess virði að greiða ef þáttaravandamálið leysist ekki.
- Prófanir Steinþórs Steingrímssonar voru ræddar á læsilegum og ólæsilegum texta. 
- Ræddum fleiri víddir: boðháttur í uppskriftum (Íslenzk tunga) kom upp. Nöfn sem bárust: Lilja Björk Stefánsdóttir og Haukur Þorgeirsson — athuga hvort þau hafi skrifað um mælanleg stíleinkenni.
 
**Hugsanir / túlkun:**
- Tvær leiðir: (A) Praktískt vel — API + góður þáttari + marktækar tilraunir, eða (B) Fræðileg aðlögun — aðlaga Milička formúlur að íslensku, skilgreina víddir, skrifa góða skýrslu með chat-viðmótum. Leið B er raunhæfari miðað við aðstæður og er samt gott framlag.
- Þáttaravandamálið er lykillinn: ef þáttun er slæm eru allar mælingar óáreiðanlegar, óháð því hvort ég hafi API eða ekki.
- Ætti að skoða ABLTagger (Háskólinn í Reykjavík) — þjálfaður á IFD tagsetinu sem flokkunarfallið mitt notar.
- 5.000 kr er lítið en skynsamlegt að bíða þar til þáttaravandamálið er leyst.
 
**Opnar spurningar:**
- Fæ ég API í gegnum HÍ? (Spyrja Haffa og/eða Gervigreindarsetrið)
- Er ABLTagger nógu góður sem aðalþáttari?
- Hvað hafa Lilja Björk Stefánsdóttir og Haukur Þorgeirsson skrifað um stíleinkenni?
- Gildir örprófið eins og það er fyrir heimaverkefni, eða þarf ég að bæta við HuggingFace líkani?
- Hvaða víddir eru mælanlegar og henta vel fyrir íslensku?
 
**Næstu skref:**
- Klára heimaverkefni 4 (frestur 29. mars)
- Hafa samband við Haffa / Gervigreindarsetrið um API
- Skoða ABLTagger
- Fletta upp Lilju Björk og Hauki Þorgeirssyni
- Hreinsa repo: eyða óþörfum RMH gögnum, skipuleggja möppustrúktúr, setja eldri skriftur í archive/
 

### 29. mars 2026 — Heimaverkefni 4 skilað + IceConParse-þáttarinn

**Tími:** ~10-15 klst (yfir nokkra daga)

**Hvað gerði ég:**
- Fann IceConParse eftir Ingunn Jóhönnu Kristjánsdóttur (Anton hafði minnst á þennan)
- Setti upp Stanza + IceConParse og prufukeyrði á nokkrar fyrirsagnirnar
- Endurskrifaði milicka_headlines_ingunnparser.py til að nota liðgerðartré í stað POS-merkja
- Harðkóðaði nokkrar reglur þar sem frumlagsnafnliðsgreining (NP-SBJ) var ekki næg ein og sér: sagngreining (finite verbs only), boðháttur (IP-IMP), aukasetningar (þarf að athuga miðmynd)
- Bjó til style_score fallið fyrir stigagjöf (0-100 kvarði)
- Bjó til archive möppu og færði allar JSON skrár þangað

**Hvað fann ég:**
- IceConParse gefur 90,38% F-mælingu og skilar liðgerðartrjám — NP-SBJ greining í stað POS-giskunar
- Mannleg grunnlína: 18,4% (næstum óbreytt frá 18,5% Sonnet) — staðfestir mælinguna
- Niðurstöður líkana breyttust verulega milli þáttara:
  - Le Chat Thinking: 99,6 stig (ennþá best)
  - Gemini 3 Thinking: 86,3 stig (mikil breyting frá Sonnet)
  - GPT 5: 79,0 stig (úr 0 stigum með Sonnet — mælingarvilla, ekki stílvilla)
  - Le Chat Fast: 0,0 stig (endurtekningarlúppa, óbreytt)
- Miðmynd (hefst, tókst) veldur vandræðum — þáttarinn merkir ekki sem NP-SBJ
- Aðeins 49 af 520 fyrirsögnum hafa persónubeygða sögn samkvæmt þáttara, þetta virðist of lágt, þarf rannsókn

**Hugsanir / túlkun:**
- Mannlega grunnlínan breyttist nánast ekkert (18,5% varð 18,4%) — mælingin sjálf er harðgerð
- En niðurstöður líkana sveiflast mikið eftir þáttara — þáttarinn er veikasti hlekkurinn
- 49/520 fyrirsagnir með sögn er of lágt — eitthvað er enn að í sagngreiningunni
- Stigaformúlan virkar vel og er auðskiljanleg fyrir stigatöflu

**Opnar spurningar:**
- Af hverju aðeins 49 fyrirsagnir með persónubeygða sögn? Er regexið of þröngt?
- Hvernig á að meðhöndla miðmynd (hefst, tókst) — þáttaravilla eða setningafræðilegt álitamál?
- Hvaða víddir næst? Ingunn mældi meðaldýpt þáttunartrjáa, meðallengd nafnliða, hlutfall aukasetninga — allt eru þetta mögulegar Milička-víddir

**Næstu skref:**
- Rannsaka af hverju sagngreining nær aðeins 49 fyrirsögnum
- Skipuleggja repo (archive/ möppu, hreinsa)
- Byrja að hugsa um næstu vídd


### 31. mars 2026 — Arkítektúr og gallar

**Tími:** 4 tímar

**Hvað gerði ég:**
- Las Who Benchmarks the Benchmarks? 
- Tók ákvarðanir um arkítektúr og gerði MD fæl þess efnis. 

**Uppgötvanir:**
- Með Who Benchmarks greininni er verið að kalla eftir vönduðum vinnubrögðum svo hægt sé að taka mark á prófunum (vélþýðingar mikið gagnrýndar)

**Hugsanir / túlkun:**
- Þetta er tilraun, henni er ætlað að skoða hvort tilefni sé að endurtaka/gera prófið í heild sinni á íslensku. Greinin mun endurspegla það.
- Hugmynd um sérstaka prófunarskriftu sem notar random sampling til að sannreyna að þáttarinn og skrifturnar vinni rétt — ekki til að skipta gögnum, heldur sem validation/sanity-check harness. T.d. taka slembiúrtak úr þáttuðum texta, athuga handvirkt hvort skrifturnar flokka rétt, og mæla samræmi. Þetta myndi styrkja aðferðafræðikaflann. 
- Enn óviss um frumlagsnafnliðarfallið, fer fram og til baka með það. Sjá ákvörðun í decisions_log.

**Opnar spurningar:**
- Hvað notar Milička nákvæmlega til að meta frammistöðu? (svar: b_d, ekki Krippendorff's alpha)
- Ætti ég að bæta Yang og Eriksson við heimildaskrána? Já, bæði tengjast data contamination sem er lykilfyrirvari.
- Hvernig á prófunarskriftan að virka nákvæmlega? Handvirkt slembiúrtak vs. sjálfvirk krossstaðfesting?
- Frumlagsnafnliðarfallið — nota eða ekki?

**Næstu skref:**
- Uppfæra reference_tracker.csv (bæta við #14 Who Benchmarks, #15 Yang, #16 Eriksson)
- Ákveða endanlega um frumlagsnafnliðarfallið
- Hanna prófunarskriftuna (validation harness)
- Halda áfram með arkitektúr


### 1. apríl 2026 — Unnið í gagnavinnslu

**Tími:** 2 klst.

**Hvað gerði ég:**
- Fór yfir skrifturnar sem Claude Code gerði (þarf að laga villur síðar). 
- Prófaði extract_samples.py og þurfti að gera breytingar (var að setja saman orð, þurfti að setja punkta á eftir fyrirsögnum og eyða út tvítekningum sem urðu í undirfyrirsögnum). 
- Notaði nýja útgáfu af extract_samples.py til að búa til textafæla fyrir alla 3 þrjár textategundirnar (tvær sources fyrir hverja). 

**Uppgötvanir:**
- Vibe coding er mun betra en að forrita sjálf, get gert mun nákvæmari (stærri) tilraun með því að fókusera á málvísindi og aðferðafræði í stað kóðans.

**Hugsanir / túlkun:**
- Það þarf að passa upp á að mennski textinn sem notaður er í formúlunni sé það sem verið er að prófa. Ég þarf ekki að vera trú upprunatextanum, enda verður hvort tveggja þátttað með IceConParse-þáttaranum. Betra er að forvinna textann.

**Næstu skref:**
- Laga parse_texts.py þannig að það finni mennska texta.
- Skoða betur úttökin sem extract_samples.py gerði í öðrum tilfellum en News.
- Byrja á að láta risamállíkönin búa til texta. Það mun taka tíma! Þarf að hanna skipunina nákvæmlega. 
- Skoða skipanahönnun Milicka betur.


### 3. apríl 2026 — Gagnaútdráttur, pöruð tilraun, LLM-textagerð (1.–3. apríl)
 
**Tími:** ~10+ klst yfir 3 daga
 
**Hvað gerði ég:**
- Keyrði `extract_samples.py` á RMH gögn. 
- Lenti í vandamálum með XML-útdrátt: orð runnu saman (t.d. „landsinsNýju-Delí") vegna þess að fyrirsagnir og undirfyrirsagnir höfðu ekki setningalokapunkt. Ákvörðun tekin: bæta punkti eftir fyrirsögnum í forvinnslunni svo þáttarinn meðhöndli þær sem aðskildar setningar.
- Gæðavandamál: gæsalappir koma sem ,, í stað „ í sumum RMH skrám. Líklega kóðunarvandamál í upprunagögnum, ekki í skriftunni. Áhrif á þáttun: óþekkt en líklega engin.
- Lokaniðurstaða útdráttar: news: 30.228 sýni, blog: 3.492 sýni, academic: 2.590 sýni. Allt ~2.000 orð per sýni.
- Bjó til `prepare_paired_experiment.py` — Milička-aðferðin: velur 15 slembiúrtök per flokk, klippir í tvennt við setningamörk, fyrri helmingur verður prompt, seinni helmingur er mennskt viðmið.
- Prompt á íslensku: „Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til þess að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn þarf ekki að innihalda réttar staðreyndir en gættu þess að hann passi við stílinn: <fyrri texti>“
- Byrjaði að búa til LLM-texta handvirkt í gegnum spjallviðmót (án API-aðgangs). 15 prompts × 4 líkön = 60 textar. Ætti að vera nóg til að gefa hugmynd að niðurstöðum fyrir þessa grein.
- Gemini bætti við mikilli markdown-snyrtingu (fyrirsagnir, undirfyrirsagnir) sem er stíleinkenni útaf fyrir sig.
- Yfirfór dim1_frumlagsnafnfall.py.
 
**Hvað fann ég:**
- Brown-málheildarstaðallinn (sem Milička byggir á) notar ~2.000 orð per textaúrtak
- Milička klippir texta í miðju og lætur líkan halda áfram — pöruð gögn gefa Δv beint
- Ég er ekki að nota temperature-stillingar þar sem ég nota spjallviðmót, ekki API. Milička fann áhugaverðustu niðurstöðurnar tengdar temperature. Mögulegt að bæta við síðar.
 
**Hugsanir / túlkun:**
- Hvers vegna er ekki talað um þáttun (parsing) í Milička? Hafa enska og tékkneska betri NLP-tól þar sem þáttun er sjálfgefin? Biber-víddir á ensku byggjast á POS-merkingum og einföldum talningum, ekki liðgerðartrjám. Þáttun virðist stærsta hindrunin á íslensku ef gera á jafnstóra rannsókn og Milička gerði á tékknesku.
- Þarf að skoða skriftur Milička betur: hvað þýða víddirnar nákvæmlega? Hver er stærðfræðin á bak við? Hvaða features voru í hverri vídd?
- Spurning um „vector length“ í kafla 5 hjá Milička: „how far a model's stylistic profile diverges from human text — Euclidean length of the normalized stylistic shift vector.“ Þetta er heildarfrávik yfir allar víddir — eins konar samantekt. Þarf að skilja nánar hvernig þetta tengist b_d.
- Gemini-formatting: Gemini bætti við markdown-fyrirsögnum og undirfyrirsögnum í framhaldinu. Þetta er stíll útaf fyrir sig. En ég breytti fyrirsögnum í forvinnslunni (bætti punkti og fjarlægði endurtekningar í undirfyrirsögnum), svo spurningin er: á ég að forvinna Gemini-úttakið á sama hátt (fjarlægja markdown) eða refsa fyrir formattinguna? Líklegast hefur líkanið áttað sig á fyrirsögnum þrátt fyrir að formatið gaf það ekki til kynna. Ákvörðun: líklega forvinna á sama hátt og mannlega textann — annars er ég að mæla markdown vs. texta, ekki stíl vs. stíl.
- Milička kafli 9: „Declaration on using AI“ — þarf að gera sambærilega yfirlýsingu í minni grein. Er að kóða mikið gegnum Claude Code til að auka hraða.
- Boðháttur með frumlagi: ER TIL í fornu máli (t.d. „þú far...“). Þarf sérstaklega að taka fram að hér er aðeins verið að rannsaka íslenskt nútímamál. Þáttarinn virðist geta greint þetta — „far“ var merkt sem VBI í prufukeyrslu — en skrifturnar leita ekki sérstaklega að þessu.
- Modal-vandamálið: Claude (sem aðstoðarmaður) vill flokka modal sem sérflokk en telur upp næstum allar hjálparsagnir. „Modal“ er yfirflokkur á undirflokkum sem á erfitt uppá á sama stigi og hinir. Dæmi: „Ég veit eina bauglínu af henni tendrast vann" — hér er „vann“ hjálparsögn, það er ekki algengt og myndi því ekki falla undir hina hjálparsagnaflokkana. Þetta er jaðarfrávik.
 
**Opnar spurningar:**
- Hvernig á að meðhöndla Gemini-formatting í LLM-úttaki? (sjá hugsanir)
- Hvað þýða Milička-víddirnar nákvæmlega og hvernig tengist vector length við b_d?
 
**Næstu skref:**
- Klára LLM-textagerð (60 textar handvirkt)
- Ákveða forvinnslu á LLM-úttaki (sérstaklega Gemini-formatting)
- Lesa Milička nánar: víddir, stærðfræði, features per vídd
- Keyra parse_texts.py 

### 6. apríl 2026 — LLM-textagerð: framvinda og niðurstöður (4.–6. apríl)

**Tími:** ~5+ klst yfir 3 daga

**Hvað gerði ég:**
- Kláraði alla fræðitexta (academic) fyrir öll 4 líkön (Gemini 3 Thinking, GPT-5, Le Chat Fast, Le Chat Thinking). 15 sýni × 4 líkön = 60 textar.
- Kláraði blogg-texta (blog) fyrir Le Chat Fast. Enn að vinna í blogg hjá hinum þremur líkönunum.
- Le Chat Fast átti í miklum vandræðum með blogg-flokk: aðeins 6 af 15 promptum skiluðu nothæfum texta.
- Geymdi nokkur dæmi í `excluded/` möppu: Eitt dæmi um ljóðræna lykkju (blog_002, „Hann hefur kennt mér að elska..." endurtekið orðrétt), eitt um efnislega lykkju (blog_003, sömu kaflar endurteknir þrisvar), og eitt áhugavert dæmi (blog_015) þar sem líkanið bjó til nýjar fyrirsagnir en endurtók sömu málsgreinar á milli þeirra
- Uppfærði `preprocess_llm_output.py` (í gegnum Claude Code) með endurtekningargreiningu og víðtækari meta-commentary greiningu.

**Hvað fann ég:**
- Le Chat Fast: 6/15 nothæf blogg-sýni. Fræðitextar voru allir nothæfir — engar lykkjur.
- Lykkjumynstrið er skýrt: líkanið á í vandræðum með óformlegan/ljóðrænan stíl en ræður vel við fræðilegan stíl. Þetta eru áhugaverðar niðurstöður útaf fyrir sig hvað stílmælingu varðar.
- Blog_015 Le Chat Fast sýnir áhugavert mynstur; líkanið framleiðir nýjar fyrirsagnir (Framleiðsluráð landbúnaðarins → Stjórnkerfið → Alþingi → Stjórnmálin → Niðurstaða → Lokahugleiðingar) en lykkjar sömu málsgrein á milli þeirra. Eins og líkanið geti skipulagt texta á yfirborðinu (kaflaheiti) en ekki framleitt nýtt efni undir.
- Blog_015 Le Chat Fast sýnir einnig stafsetningarbreytingu innan lykkjunnar: „áhugasemdum“ breytist smátt og smátt í „áhagasemdum" (ef við gefum okkur það að hið fyrrnefnda sé alvöru orð) — undarleg stafsetningarvilla sem er endurtekin í einhvern tíma og svo hverfur fyrri stafsetningin alveg upp undir lokin.
- Þrjú tilvik voru prófuð tvisvar (retry í nýju spjalli). Svo virtist sem endurtekningin gerðist alltaf við vissar skipanir. Eftir þrjár tilraunir hætti ég að prófa sömu skipun margsinnis - Ef sú fyrsta virkaði ekki var farið í þá næstu. 

**Hugsanir / túlkun:**
- Munurinn á frammistöðu Le Chat Fast á fræðitexta (0 lykkjur) og bloggtexta (9 lykkjur/misheppnuð) er töluverður. Fræðitexti er formlegri, fyrirsjáanlegri í uppbyggingu — líkanið virðist hafa auðveldara með að halda í þann ramma. Blogg-textinn krefst meiri persónuleika, frásagnar og tónbreytinga sem líkanið á erfitt með.
- „áhugasemdum“ → „áhagasemdum“ breytingin er merkileg. Líkanið er ekki bara að endurtaka, í lokin afbakar það eigin texta innan lykkjunnar. Þetta gæti bent til þess að athygli líkansins (e. attention) sé að dreifast eftir því sem textinn lengist.
- Ég hef ákveðið að sniðmátsendurtekningar séu gjaldgengar í tilrauninni en endurtekningar á texta séu það ekki. Sjá ákvörðun 018 (já) — en ég endurskoða þegar ég sé niðurstöður úr formúlunum. Stundum er erfitt fyrir mannsaugað að spotta lykkjur, sérstaklega ef þær mynda ekki mynstur í textanum. Claude Code fær frekari fyrirmæli um að láta skriftu flagga endurtekningar á þann hátt að notandinn (ég) geti tekið ákvörðun um það sjálfur.

**Opnar spurningar:**
- Munu hin líkönin (Gemini, GPT-5, Le Chat Thinking) eiga í svipuðum vandræðum með blogg-texta? Fyrstu niðurstöður sýna það ekki.
- Hvernig mun árangur Le Chat Fast í textum úr journals (akademísku textana) vera í samanburði við hin líkönin — er það gott þar eða bara „ekki í lykkju“? Í fljótu bragði virðist þetta ekki vera góður texti per se en sé engar lykkjur.
- Hve mörg sýni þarf bootstrap-aðferðin? Eru 6 nóg?

**Staða verkefnis:**

| Flokkur | Gemini 3 Thinking | GPT-5 | Le Chat Fast | Le Chat Thinking |
|---------|-------------------|-------|--------------|------------------|
| Academic | ✅ 15/15       | ✅ 15/15 | ✅ 15/15      | ✅ 15/15 |
| Blog     | ⏳             | ⏳       | ✅ 6/15       | ⏳ |
| News     | ⏳             | ⏳       | ⏳            | ⏳ |

**Tilraun á gölluðum eða ekki gölluðum gögnum**
gemini_3_thinking:    4 files,  9 passages,    169 words
gpt_5:                1 file,   1 passage,      19 words
le_chat_fast:        11 files, 192 passages,  5,471 words
le_chat_thinking:    15 files,  66 passages,  3,879 words

**Næstu skref:**
- Klára blogg-texta fyrir Gemini 3 Thinking, GPT-5, Le Chat Thinking
- Byrja á frétta-textum (news) fyrir öll líkön
- Keyra `preprocess_llm_output.py` á kláruðum fræðitextum til að prófa forvinnslu
- Athuga hvort 6 sýni dugi fyrir bootstrap
- Skoða lechat_thinking_academic_prompt_009.txt: 93% repetition (1033 of 1112 words)