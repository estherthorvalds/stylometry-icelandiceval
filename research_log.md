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


### 8. apríl 2026 — LLM-textagerð lokið, forvinnsla og skráning (6.–8. apríl)

**Tími:** 3 tímar

**Hvað gerði ég:**
- Kláraði alla LLM-textagerð: öll 4 módel × 3 flokkar. 
- Handvirkt í gegnum spjallviðmót (engin API). Samtals ~180 prompt-tilraunir.
- Handvirk forvinnsla á LLM-úttaki eftir þörfum:
  - Le Chat Thinking blog_011: stytting á enda vegna token-lykkju ("alveg alveg alveg...")
  - Le Chat Thinking blog_012: tvær degenerate línur fjarlægðar úr miðjum texta (token-lykkja), umliggjandi samhangandi texti fékk að haldast eins og hann var
  - Gemini: greiningarhlutar (analysis) fjarlægðir handvirkt þar sem líkanið greindi textann í stað þess að halda áfram. Þarf samt að skoða textana betur, gæti verið eitthvað um greiningar eða umorðanir í stað áframhaldandi texta.
  - Le Chat Thinking: umorðun á prompttexta í stað nýrrar textagerðar — skráð en ekki leiðrétt sjálfkrafa
- Le Chat Fast í excluded/: blog_002 (ljóðræn lykkja), blog_003 (efnislykkja), blog_015 (fyrirsagnalykkja með sömu málsgreinum) o.fl. Samtals 6/15 nothæf blogg-sýni.
- Uppfærði `preprocess_llm_output.py` með endurtekningargreiningu og útvíkkaðri meta-commentary greiningu (Claude Code).

**Hvað fann ég:**

*Le Chat Fast:*
- 15/15 fræðitextar nothæfir. 6/15 bloggtextar nothæfir. 15/15 fréttatextar nothæfir.
- Lykkjumynstur bundið við óformlegan/ljóðrænan stíl. Fræðitextar án vandræða.
- blog_015: áhugavert mynstur — módellið bjó til nýjar fyrirsagnir en lykkjaði sömu málsgreinar þar á milli. Afbakað orð afbakaðist meira innan lykkjunnar: „áhugasemdum“ → „áhagasemdum“.

*Le Chat Thinking:*
- Token-lykkjur í lok eða miðjum texta (blog_011, blog_012). Ólíkt Le Chat Fast sem lykkjar heilar málsgreinar — Le Chat Thinking heldur samhangandi texta lengur en hrynur á token-stigi.
- Athuga umorðun á prompttexta í stað nýrrar textagerðar. Þetta er EKKI stílniðurstaða — þetta er lesskilningsvandamál. Líkanið skilur ekki fyrirmælin „haltu áfram með textann“ og endurskrifar í staðinn. Þetta gæti gefið falskt skor á stíl vegna þess að umorðaður texti mun væntanlega líkjast mannlegri grunnlínu sjálfkrafa.

*Gemini 3 Thinking:*
- Greindi textann að hluta í stað þess að halda áfram — líkanið fór í greiningarham frekar en framhaldsham. Greiningarhlutarnir fjarlægðir handvirkt.
- Mikil markdown-snyrting (fyrirsagnir, feitletur) sem þarf að fjarlægja í forvinnslu.

*Chat GPT 5:*
- Virtist skilja promptið best, var ekki mikið að bæta við aukatexta fyrir og eftir eins og hin líkönin að spyrja hvort þetta þóknaðist notandanum og hvernig hann vildi halda áfram.

*Almennt:*
- Þrjú af fjórum módelum (Le Chat Fast, Le Chat Thinking, Gemini) sýndu einhvers konar vandræði með að skilja fyrirmæli á íslensku. Þetta er lesskilningsvandamál, ekki stílvandamál og skiptir máli fyrir stigatöfluna í víðara samhengi.
- Handvirk forvinnsla á LLM-úttaki: fjarlægja bilaða tóka og greiningartexta er sambærilegt við að fjarlægja hlutsetningar í enda — við erum að fjarlægja gallaðan úttaksefni, ekki breyta stíl. Við getum ekki mælt getu til að búa til stíl ef líkanið einfaldlega bilar. Þetta verður skjalfest og rökstutt í aðferðafræðikafla.

**Hugsanir / túlkun:**
- Mikilvæg aðgreining: Gallað úttak (tóka-lykkjur, greining í stað framhalds) er fjarlægt vegna þess að þetta eru galla í módeli, ekki stíleinkenni. Sniðmátsendurtekning (t.d. Le Chat Fast blog_001) er HALDIÐ vegna þess að þetta er stílbrestur sem á heima í mælingunni. Þessi aðgreining er lykilatriði í aðferðafræðikaflanum.
- Lesskilningsvandamálið (Le Chat Thinking umorðar, Gemini greinir - stundum) gæti skapað skekkju: módel sem skilur ekki fyrirmælin gæti skorað vel á stíl vegna þess að það er í raun að endurgera prompttextann. Þetta er fyrirvari sem þarf í umfjöllun.
- GPT-5: Virtist ganga vel við fyrstu sýn.

**Staða verkefnis:**

| Flokkur | Gemini 3 Thinking | GPT-5 | Le Chat Fast | Le Chat Thinking |
|---------|-------------------|-------|--------------|------------------|
| Academic | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 |
| Blog | ✅ 15/15 | ✅ 15/15 | ✅ 6/15 | ✅ 15/15 |
| News | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 |

**Næstu skref:**
- Keyra `preprocess_llm_output.py` á öllum LLM-textum (markdown-hreinsun, endurtekningargreining)
- Yfirfara forvinnsluniðurstöður handvirkt
- Keyra `parse_texts.py` á bæði mannleg og LLM-gögn
- Keyra dimension-skrifturnar (dim1, dim2, dim3)
- Keyra `run_milicka.py`
- Push allt á GitHub


### 13. apríl 2026 — Bæta við víddum, forvinna gögn og keyra í gegn

**Tími:** 8 klst. yfir nokkra daga

**Hvað gerði ég:**
- Fyrsta keyrsla á run_milicka.py. Allar skriftur virka. Niðurstöður fengnar fyrir öll fjögur líkön og þrjár textaflokka.

  Líkan                          academic       blog       news   Meðaltal
  ──────────────────────────── ────────── ────────── ────────── ──────────
  gemini_3_thinking                  5.87      10.67       5.90       7.48
  gpt_5                             10.96      12.92       9.24      11.04
  le_chat_fast                       9.52      22.76      11.07      14.45
  le_chat_thinking                   5.98      13.06       7.17       8.74

- Forvinnsla — endurtekningar: Mikill texti fjarlægður vegna endurtekninga úr prompt (sjá ákvarðanaskrá). Alls 29,723 orð fjarlægð úr 110,303 (27%). 

  ENDURTEKNINGAR ÚR PROMPT — FJARLÆGÐAR / REMOVED
  ──────────────────────────────────────────────────
    gemini_3_thinking: 6 skrár, 13 bútar (1290 orð) [fjarlægð]
    gpt_5: 4 skrár, 15 bútar (844 orð) [fjarlægð]
    le_chat_fast: 28 skrár, 308 bútar (12312 orð) [fjarlægð]
    le_chat_thinking: 38 skrár, 348 bútar (15277 orð) [fjarlægð]
  ──────────────────────────────────────────────────
  Orðafjöldi skráa með endurtekningum:
    Fyrir fjarlægingu:  110,303
    Eftir fjarlægingu:  80,580
    Orð fjarlægð:       29,723

**Uppgötvanir:**
- Le Chat Fast gengur verst í blog (22.76)
- Le Chat Think og Gemini 3 Thinking gengur að meðallagi best 
- GPT-5 er í miðjunni

**Hugsanir / túlkun:**
- Í forvinnslu var mest fjarlægt af textum Le Chat Think og Le Chat Fast — 38 og 28 skrár í sömu röð. Þetta er merkilegt í ljósi þess að þau líkön standa einnig lægst á kvarðanum - þarf að greina betur til að skilja samspilið.
- Erfitt var að losna við helpful assistant fínþjálfunina. Ég fjarlægði mikið handvirkt og svo var meira fjarlægt í forvinnslu. Bæði textar sem og md formatting.

**Opnar spurningar:**
- Engu líkani gekk sérstaklega vel. Væri gaman að prófa API-útgáfur við mismunandi hitastig (temperature), bæta við Claude-líkönum og DeepSeek. 
- Myndi decoder líkani ganga betur sem ekki hefur verið fínþjálfað í helpful assistant?

**Næstu skref:**
- Yfirfara kóðann.
- Endurskoða niðurstöður og senda til Miðeindar. 
- Skoða scatter matplotlib á borð við það sem sést í grein Milicka.


### 14. apríl 2026 — Skipulag greinar, fjórði textaflokkur, API-ákvörðun

**Tími:** 4 klst.

**Hvað gerði ég:**
- Skipulagði greinina. Fór yfir öll gögn verkefnisins (research_log, decisions_log, ARCHITECTURE.md, reference_tracker, skriftur) og samdi uppbyggingu greinar í samvinnu við Claude Opus 4.6. Uppbygging byggð á Milička en aðlöguð að íslensku samhengi.
- Ákvað að bæta við fjórða textaflokki: óbirtur skáldskapur eftir mig sjálfa. 15 sýni (2.000+ orð hvert) tiltæk. Markmið: prófa mengunarveldið (data contamination) — þessir textar eru sannanlega óséðir af öllum líkönum.
- Skoða API-aðgang til að bæta við og skoða mismunandi hitastig (temperature), líklegast GPT. Þetta styrkir greininguna verulega þar sem áhugaverðustu niðurstöður Milička birtust við hitastigsbreytingar: Hægt verður að endurtaka tilraunina með hitastigstilraunum, fleiri líkön.
- Útbjó verkefnaáætlun til að halda utan um það sem eftir er (Heimaverkefni 5).

**Uppgötvanir:**
- Óbirtur skáldskapur leysir RMH-mengunarvandamálið beint: í stað þess að setja fyrirvara er hægt að bera saman niðurstöður á RMH-textum (mögulega mengaðir) við óséð gögn og sjá hvort munur sé. 
- Le Chat Think á mjög erfitt með áður óséðan skáldskap, festist ítrekað í „alveg alveg alveg“ lúppum. 
- Le Chat Fast er farið. Le Chat Balanced er komið í staðinn. Óséði textinn verður að fara í gegnum það í stað Fast. 
- API-aðgangur gefur þrennt sem vantar: (1) möguleika á að endurtaka með sama líkani, (2) hitastigstilraunir (Milička fann áhugaverðustu niðurstöður sínar þar), (3) fleiri líkön til að færast frá „nokkur dæmi“ yfir í nokkuð gott yfirlit yfir frammistöðu mismunandi líkana.

**Hugsanir / túlkun:**
- Markmiðið er nú að fá raunverulegar niðurstöður sem nýtast í sumarverkefnið. Hvaða líkan á best við til textagerðar á íslensku? Greinin skal svara því.
- Fjórði flokkurinn (óbirtur skáldskapur) er aðeins eftir einn höfund — getur ekki talist fulltrúi skáldsagnaefnis á íslensku. Þetta er tilraun til að prófa ómengaða texta (óbirtir - hafa ómögulega verið skrapaðir), ekki að skilgreina skáldskap sem textategund. Gallinn er þó að sumir textar eru óyfirlesnir og sömuleiðis óhefðbundnir sem þýðir að þáttarinn gæti lent í vandræðum með mennska textann. 

**Opnar spurningar:**
- Hvaða Claude-líkön á að prófa? Sonnet 4.6 og Opus 4.6? Haiku? Get aðeins gert 3 Sonnet texta í einu með fríkeypis útgáfunni.
- Hvaða hitastig hjá GPT? Milička notaði ýmis, 0 og 1 voru áhugaverðust. 

**Næstu skref:**
- Undirbúa óbirta textana: draga út 15 sýni (~2.000 orð), keyra í gegnum extract_samples.py og prepare_paired_experiment.py.
- Fá API-aðgang.
- Keyra nýju líkönin í gegnum pípuna.
- Senda stöðuskýrslu til Miðeindar.
- Byrja að skrifa greinardrög (introduction, related work) samhliða gagnavinnslu.


### 18. apríl 2026 — Áttunda víddin: BÍN-hlutfall

**Tími:** 2 klst.

**Hvað gerði ég:**
- Hannaði og útfærði áttundu mælivíddina: BÍN-hlutfall (`dim8_bin_ratio.py`). Hver tóki er flokkaður í eitt af fjórum: `exact` (finnst í BÍN), `compound` (BÍN skilar samsetningu með fleiri bandstrikum en inntakið), `proper_name` (hluti ∈ {ism, föð, móð, örn, göt, fyr, erm, bibl, lönd, þor}), og `oov` (ekki í BÍN). Aðal-v fyrir víddina er `in_bin_ratio = (exact + compound + proper_name) / total`.
- Ráðfærði mig við kennara og notaði `islenska`-pakka Miðeindar (BinPackage) til uppflettingar. Pakkinn skilar BinEntry-færslum með `ord`, `ofl`, `hluti`, `bmynd`, `mark`, `bin_id` — nóg til að gera compound- og sérnafnagreiningu.
- Hannaði „reikna-einu-sinni“ pípu: dim8 skrifar tvö CSV (`output/dim8_bin_summary.csv`, `output/dim8_bin_detail.csv`) og `run_milicka.py` les summary-CSV beint. Kallar aldrei á `Bin()` sjálft. Þannig þarf ekki að keyra `islenska` í hvert sinn, nóg er að gera það einu sinni og svo er unnið með þær niðurstöður í CSV-skjölunum. Það bæði sparar tíma og orku ef gögnin eru mörg en sömuleiðis geta aðrir notendur reiknað Milicka-formúluna án þess að setja upp pakkann (krefst `python3-dev` og `libffi-dev` á Linux).
- Sannprófun: keyrt á 9 mannlegum skrám (3 per textategund). Niðurstöður:

  ```
  Skrá                  Orð   in_bin% exact% cmpnd% propn% oov%
  ─────────────────────────────────────────────────────────────
  academic_ref_002     1059   95.56   92.54  0.94   2.08   4.44
  academic_ref_003     1038   95.57   90.46  4.24   0.87   4.43
  academic_ref_004     1034   91.68   84.91  2.13   4.64   8.32
  blog_ref_001         1093   99.82   96.98  0.82   2.01   0.18
  blog_ref_002         1085   99.35   95.94  1.94   1.47   0.65
  blog_ref_003         1100   98.91   95.82  2.27   0.82   1.09
  news_ref_001         1045   95.50   84.40  0.48  10.62   4.50
  news_ref_002         1080   96.94   93.52  0.65   2.78   3.06
  news_ref_003         1088   98.53   93.66  0.92   3.95   1.47
  MEÐALTAL                    96.87   92.03  1.60   3.25   3.13
  ```

**Málvísindaleg rök fyrir víddinni:**
- Sjö víddir (dim1–dim7) mæla málfræðilegar dreifingar: hlutfall aukasetninga, meðalorðalengd, þátíðarnotkun, tíðni tengiorða o.s.frv. Þær grípa góðan hluta stíleinkenna en greina ekki orðaval og orðaforða.
- Íslenska hefur ríka beygingarfræði og sterka nýyrðahefð. Íslenskir textar nýta gjarna samsetningar, bókstafshefðir og sérnöfn á mjög mismunandi hátt milli textaflokka. BÍN inniheldur ~6,5 milljónir orðmynda og fyrir yfirlesna íslenska texta ætti hlutfallið að vera nokkuð hátt, >90%.
- LLM-textar á íslensku eru oft enskulegir, notar enskar orðmyndir, beygir undarlega eða býr til gerviorð sem ekki eru partur af BÍN. Þetta er GÆÐAVILLA, ekki stílbreytileiki. Dim8 grípur þessa tegund af galla á annan hátt en hinar víddirnar.

**Uppgötvanir:**
- Allir mannlegir textar > 90% in_bin ✓ (lægst: academic_ref_004 á 91.68%). Þetta staðfestir að BÍN nær nánast öllu í raunverulegum íslenskum texta — þannig að lægra hlutfall hjá LLM-texta verður marktækt.
- Fréttir hafa hæsta proper_name_ratio (news_001 á 10.62%). Það passar við það að fréttir vísa stöðugt í fólk, staði, stofnanir, fyrirtæki.
- Fræðitextar hafa meðal-compound_ratio (2.44%). Fræðitextar nota löng samsett hugtök („heilbrigðisþjónustukerfi“), en ekki eins mikið og búist var við.
- Blogg hafa LÆGSTA oov_ratio (0.64% að meðaltali): Stuttar setningar, einfalt mál, persónulegur tónn.
- academic_ref_001 reyndist jaðartilvik: 89.75% in_bin. Athugun með `--debug` sýndi sögulega stafsetningu (jeg, mier, þier, spordenn) og latnesk orð. Ekki galli í mælingunni heldur sérkenni textans. Skipti yfir á 002–004 fyrir sannprófun.

**Hugsanir / túlkun:**
- Áttunda víddin er öðruvísi en hinar sjö sem mæla málfræðilega DREIFINGU (hversu oft er eitt eða annað notað), dim8 mælir hvort orðin sjálf séu hluti af íslensku nútímamáli. Líkön sem nota óvenjulegan íslenskan stíl en halda sig við íslenskan orðaforða fá hátt dim8 + frávik í dim1–7. Líkön sem mynda gervimál (enskt/tökuorða) fá lágt dim8 óháð öðru. Sömuleiðis ef þau geta ekki hermt eftir lágu dim8 í mennskum texta (eins og í fantasíutexta) er þeim einnig refsað fyrir það.
- Parse-once uppbyggingin er dýrmæt, `islenska` ætti ekki að vera notað oft. Með því að skyndivista (cache) niðurstöður í CSV getum við haldið `run_milicka.py` án hæði (dependency) við `islenska` og keyrt endurtekin stig (scatter, B-reikningur). (SKRIFAÐ SEINNA: Ég sé eftir þessari ákvörðun, þetta er bara keyrt á minni tölvu og mögulega einhverjum máltæknifræðingi síðar meir sem þarf ekki að hafa áhyggjur af þessu, þetta tók bara nokkrar sekúndur svo þessi ákvörðun var overengineering)
- „oov“-flokkurinn inniheldur mörg réttmæt orð (nýyrði sem eru ekki enn í BÍN, erlend tilvísunarnöfn, tölur, skammstafanir). oov_guess-dálkurinn í detail-CSV reynir að flokka þetta (`foreign` fyrir c/q/w/z, `likely_proper_name` fyrir hástafaorð í miðri setningu, annars `unknown`) en þetta er greiningartæki, ekki gildismat.

**Opnar spurningar:**
- Ætti primary-v fyrir Milička-mælinguna að vera `in_bin_ratio` eða eingöngu `exact_ratio`? Valdi `in_bin_ratio` (með compound og proper_name innifalið) því það speglar hvort ORÐIN séu þekkt íslenska. `exact_ratio` væri strangara og næði hugsanlega betur að fanga LLM-villurnar. Hægt að greina bæði í greininni.
- Þarf að sannprófa á LLM-textum til að sjá dreifingu.
- Ætti að flokka tölur (digits-only) sérstaklega frekar en sem oov? Sem stendur teljast „2024“ og „fimmtíu“ bæði sem oov/exact í sömu röð — ósamræmi.

**Næstu skref:**
- Klára að búa til fleiri gervigreindartexta og keyra dim8 á þá, fá samanburð.
- Bæta dim8 við Milička scatter-plot grid (verður 8 reitir í stað 7).
- Ræða BÍN-hlutfall sérstaklega í greininni vegna þess að þetta er tegund af LLM-galla sem hinar víddirnar eru ekki að reyna að ná — líklega sinn eigin undirkafli í discussion.


### 20. apríl 2026 — API-tilraun stöðvuð: prefill-vandinn og skipting verkefnisins

**Tími:** 3 klst.

**Hvað gerði ég:**
- Keyrði API-tilraunina með Claude Sonnet 4.5 (`claude_sonnet46_api_t0.0` og `claude_sonnet46_api_t1.0`). Stoppaði eftir 52 skrár þegar í ljós kom að framhöldin voru bæði of stutt (~1.000 orð í stað 2.000+) og að megnið af innihaldinu var orðrétt endurritun úr upprunalegu skipuninni, ekki raunverulegt framhald.
- Greindi vandann á academic_cont_001: af 1.092 orðum voru fyrstu ~810 orðrétt endurrit (með smávægilegri ritstýringu: hástafir lagaðir o.s.frv.), aðeins síðustu ~280 orðin reyndust vera raunverulegt nýtt efni. Það endaði í miðri setningu („Í öllum söfn“).
- Prófaði temperature 1.0 til samanburðar — sama mynstur: 1.091 orð, ~1.000 endurrit, ~90 nýtt. Það segir mér að þetta sé ekki vandamál sem tengist hitastigi.
- Las Milička et al. (2509.10179 og skylda 2505.01877) til að athuga hvort þetta væri skjalfest hjá þeim. Fann ekki umfjöllun um preamble-repetition, EN: sýnidæmi Milička um GPT-4.5 og LLasumarframhöld sýna augljóslega að þeirra skipun endar í miðri setningu. Líkönin byrja framhaldið sitt með því að klára þá setningu. Mínar skipanir enda á punkti eftir heilli setningu og það gefur líkaninu „hrein“ mörk til að byrja upp á nýtt með eigin fyrirsögn og endurrit (sem er greinilega ekki gott).
- Einnig sá ég að Milička skrifar upphafið að skipuninni á ensku, líka í tékknesku tilrauninni. Ég þýddi hana á íslensku. Spurning hvort þetta hefði átt að vera á ensku svo líkanið áttaði sig betur á reglunum? Verði tilraunin endurtekin væri það örugglega betri kostur, í það minnsta þess virði að prófa.
- Skoðaði preprocess_llm_output.py: endurtekningargreiningin þar (--remove-repetitions) er hönnuð fyrir Le Chat-mynstrið (endurtekning á eftir framhaldinu), ekki preamble-endurtekningu (framhald byrjar á endurriti af promptinu). Grípur þetta væntanlega ekki án breytinga.
- Ákvað að skipta verkefninu í tvo hluta. Annars vegar ljúka lokaverkefni námskeiðsins á spjallviðmótsgögnunum og skjalfesta API-tilraunina sem misheppnaða frumraun og hvaða breytingar þarf að gera áður en hún er endurtekin. Hins vegar byrja sumarverkefnið á því að útbúa ný gögn þar sem skipunin hefst á útskýringu á ensku og inniheldur 500 orða textadæmi (eða meiru?) sem lýkur í miðri setningu.

**Uppgötvanir:**
- Sonnet 4.5 sýnir kerfisbundna preamble-repetition á íslenskum stílframhaldsverkefnum við bæði t=0.0 og t=1.0. Fyrirsagnir í markdown-sniði birtast fremst í báðum útgáfum („# Orðasafn Baska og Íslendinga: Frekari skoðun“ / „# Hald áfram með textann“) — líkanið túlkar verkefnið sem nýtt skjal með inngangi, ekki framhald.
- Milička ber saman líkön með mismunandi API í sömu rannsókn. Mitt plan var alltaf að hafa mismunandi líkön líka en þar sem ég vildi ekki greiða fyrir að búa til rannsóknina byrjaði ég á spjallútgáfum risamállíkananna. Hefði ég prófað API útgáfurnar strax í upphafi hefði ég séð að skipanirnar þyrftu breytingar til þess að hægt væri að gera tilraunina á sama hátt og Milicka. Eflaust útskýrir þetta líka vandamálið með Le Chat líkönin þó svo að þau séu í spjall-útgáfum.
- 500 + 1.500 skipting væri betri en mitt núverandi „sjáðu til þess að hann innihaldi að minnsta kosti tvö þúsund orð“ sem hægt er að túlka sem ~1.000 + ~1.000. Ég áttaði mig ekki á því að sum líkön gætu túlka það sem 2000 orða framhald og önnur 2000 orða heild. Með þvi að breyta í 500 + 1000 og hafa upphaf skipunar á ensku yrði það (a) í samræmi við Milička (500 orð í prompti), (b) stærri textabútur til að mæla fyrir stílmælinguna, (c) minna samhengi til að freista líkansins til að endurtaka. (SKRIFAÐ SEINNA: Sumar víddir krefjast mikils orðafjölda til að fá marktækar greiningar á prompti svo 500 gæti verið of lítið fyrir þetta próf)
- 52 misheppnaðar skrár, API-kostnaður féll til án nothæfra gagna. Lexía fyrir næstu lotu: Ekki nóg að keyra bara eitt API kall á eina skrá og sjá hvort það hafi virkað, ég þarf að greina skrána líka og passa að hún sé nothæf, líklegast með því að keyra hana í gegnum formúluna og sjá útkomuna. Ef útkoman er skrítin (eins og hún hefði verið í þessu tilfelli) þá þarf að skoða það handvirkt OG renna í gegnum preprocessing til að sjá það sem mannsaugað sér ekki.

**Hugsanir / túlkun:**
- Clean break. Námskeiðsverkefnið var alltaf hugsað sem proof-of-concept fyrir stærri endurtekningu á Milicka. Fyrri hlutinn: fjögur líkön (næ kannski að bæta við Claude Sonnet 4.6 og DeepSeek áður en ég skila inn), spjallviðmót, handvirk gagnasöfnun, grunnur fyrir aðferðafræðina og átta víddirnar. Seinni hlutinn (sumar): API-aðgangur, mid-sentence prefill, óséðir textar (ef þarf), 500+ og 1500 skipting, fleiri líkön, hitastigstilraunir.
- Preamble-repetition hjá Sonnet 4.5 á íslensku er í sjálfu sér skráanleg niðurstaða, jafnvel þótt ég lagi hana ekki í þessari lotu. Fer í limitations-kaflann sem dæmi um hvers vegna aðferðafræðin þarf að þróast fyrir næsta hluta.

**Opnar spurningar fyrir seinni hlutann:**
- Hvernig á að kljúfa 2.000 orða texta í 500 + ~1.500 í staðinn fyrir ~1.000 + ~1.000? Þarf að endurskrifa `prepare_paired_experiment.py` eða bæta við valkosti.
- Hvernig á að klippa í miðri setningu án þess að lenda í miðju orði eða á ónáttúrulegum stað? Milička sýndi einfaldlega „I'd feel the urge“ sem endar á heilu orði og er fullkominn staður til að enda á. Klippa á bili milli orða en ekki á setningarmörkum?
- Í nýrri tilraun þarf að endurkeyra allt á nýjum forsendum. Milička o.fl. birta niðurstöður fyrir mismunandi hitastillingar (t=0, t=1) fyrir öll metin líkön, sem gefur til kynna að API-líkön hafi verið notuð við alla textagerð. Ég notaði hins vegar aðeins spjallviðmót sem kosta ekkert, þar sem hitastig er ekki breytanlegt. Til að gera þessa tilraun vel þarf ég að skipta henni í tvennt og aðgreina - á spjallmennum annars vegar og á API líkönum hins vegar.

**Næstu skref:**
- Klára greinardrögin á núverandi gagnasetti (4 líkön × 3 textaflokkar + 1 flokkur óséðs × Le Chat Balanced fyrir 4. flokkinn).
- Í aðferðafræðikafla: lýsa báðum lotum skýrt. Fyrsta lota = spjallviðmót, núverandi niðurstöður. Önnur lota (fyrirhuguð) = API með mid-sentence prefill, 500+1500 skipting, skjalfest sem næsta skref. Líklega þarf 1500+1500 samt.
- Í limitations: skrá preamble-repetition hjá Sonnet 4.5, styttri prompts en Milička, spjallviðmótsmiðlun er erfitt að endurtaka.


### 20. apríl 2026 — Níunda víddin: trédýpt (setningarþyngd úr IcePaHC-trjám)

**Hvað var gert:**
- Útfærði níundu mælivíddina: trédýpt (`dim9_tree_depth.py`) sem mælir dýpt IcePaHC-liðgerðartrjáa — setningarþyngd skv. framsetningu Steinþórs Steingrímssonar á Hugvísindaþingi (sem mældi það á UD-gögnum) en aðlagað að liðgerðartrjám.
- Þrjár undirmælingar í CSV: `mean_tree_depth` (aðal-v), `std_tree_depth`, `pct_complex_trees` (≥ 3 dýpt), `total_ip_sub`, `mean_ip_sub_nesting`.
- Tré-dýpt reiknuð með bracket-counting: `max_paren_nesting - 1` svo ROOT = 0 og fyrsta constituent-lag = 1. IP-SUB hreiðrun reiknuð með label-stack-göngu yfir bracket-strenginn.
- Engin utanaðkomandi hæði. Endurnýtti `mean`/`stdev` úr dim6_word_length til að halda standard-library-eingöngu.
- Bætti dim9 í `run_milicka.py` DIMENSIONS skrá (`input='parsed'`, `key='mean_tree_depth'`).

**Hvað var fært inn í gögn/skriftir með Claude Code:**
- `scripts/dim9_tree_depth.py` — ný skrá með sömu CLI-viðmóti og dim2 (`--parsed-dir`, `--files`, `--output-csv`, `--debug`, `--dry-run`).
- `run_milicka.py` — útvíkkun á DIMENSIONS (10 víddir í heildina) og útfærsluathugasemdum (parsed-sjá og dict-skilauppröðun).
- `ARCHITECTURE.md` — ný dim9-kafli með skýringu á sambandi við dim2 (orthogonal merki), þrjár undirmælingar, þröskuldur- og methodological-parallel umræðu.
- `decisions_log.md` — ákvörðun 024 (rökstuðningur, valkostir, sannprófun).
- `reference_tracker.csv` — færsla #21 (Steinþór Steingrímsson, fyrirlestur um setningarþyngd).
- `README.md` — ný lína í víddatöflu og project-tree.

**Linguistic motivation — af hverju dim9?**
- Fyrirlestur Steinþórs fjallaði um hvernig flókinn texti hafi oft mikla dýpt aukasetninga og langar keðjum af tengiliðum. Hann sýndi það á UD-trjám en sama mynstur á að sjást á IcePaHC-liðgerðartrjám (dýpt er alhæfð stærð þegar tré eru borin saman innan sömu þáttunaraðferðar).
- Biber-MDA „informational production“ víddin (Dimension 1 í upprunalegu 1988-greiningunni) byggir meðal annars á merkjum um hversu upplýsingaþéttur og flókinn textinn er. Trédýpt gefur vísbendingu þetta, samhliða dim3 (nafnliðalengd) og dim2 (undirskipun).

**Orthogonality við dim2:**
- dim2 mælir TÍÐNI undirskipunar: count(IP-SUB) / count(IP-MAT). Þetta segir hversu oft höfundur bætir við aukasetningu.
- dim9 (meðaldýpt + mean_ip_sub_nesting) mælir DÝPT hreiðrunar: hversu djúpt IP-SUB eru hreiðruð hvert í öðru, og heildardýpt trésins sem slíks.
- Tvær setningar geta haft sama dim2-gildi en ólíkt dim9. Dæmi:
  - Grunn hreiðrun: [IP-MAT ... [IP-SUB ...] [IP-SUB ...] ...] — tvær IP-SUB, báðar beint undir IP-MAT (dim9 gefur 0 mean_ip_sub_nesting).
  - Djúp hreiðrun: [IP-MAT ... [IP-SUB ... [IP-SUB ... [IP-SUB ...]]]] — tvær IP-SUB hreiðraðar (dim9 gefur hærra mean_ip_sub_nesting).
  - dim2 gefur sömu niðurstöðu í báðum tilvikum (sami IP-SUB / IP-MAT hlutfall), dim9 aðgreinir.
- Þess vegna eru þetta SJÁLFSTÆÐ merki sem bæði ættu að vera með í B-skori.

**Sannprófun á öllum 45 mannlegum viðmiðsskrám:**

```
Flokkur     n    mean_depth   range            pct_complex   mean_ip_sub_nest
academic   15    8.35         [6.27, 10.32]    99.4%         0.51
news       15    7.72         [5.90,  9.48]    99.2%         0.45
blog       15    7.57         [5.92,  9.17]    99.7%         0.44
```

- **Röð eins og búist var við:** academic > news > blog fyrir bæði mean_tree_depth og mean_ip_sub_nesting. Staðfestir að dim9 aðgreinir textaflokka í sömu átt og aðrar víddir.
- **Allar meðaltöl > 2.0:** sanity check stenst (ekkert tré með dýpt 0 eða 1 eftir að parse-failures voru síaðar).
- **Spannið innan flokks er breitt:** academic tekur [6.27, 10.32] sem er næstum 2× munur milli grynnsta og dýpsta texta í sama flokki. Þetta er áhugavert — bendir til að Læknablaðið hafi innri breytileika (yfirlitsgreinar vs. rannsóknargreinar?). Mögulega eru einhver yfirlit innan rannsóknargreina að skekkja þetta. Það skiptir ekki öllu máli því frávik er mælt út frá hverjum texta fyrir sig. 

**`pct_complex_trees` kvörðunarvandinn:**
- Þröskuldurinn ≥ 3 var tekinn beint frá Steinþóri (UD) sem methodological parallel, EKKI sem íslenskt kvarðað gildi. Liðgerðartré eru kerfisbundið dýpri en UD-tré vegna POS-umbúða sem bæta 1–2 lögum. Afleiðingin: pct_complex lendir í ~99% fyrir ALLA flokka í íslensku — 99.4% academic, 99.2% news, 99.7% blog. Þetta aðgreinir nánast ekki neitt.
- Ég lét mæliniguna halda áfram vegna þess að hún er hliðstæða við Steinþór og því gagnleg til samanburðar, en TÆKIÐ sem aðgreinir er `mean_tree_depth`, ekki pct_complex. Þetta er skjalfest í docstring, console-úttaki (NOTE-lína) og ARCHITECTURE.md.
- Fyrir sumarverkefnið: væri hægt að kvarða þröskuldinn fyrir IcePaHC með því að nota miðgildi/efri-þriðjung mannlegra gagna sem „complex“-skilgreiningu. Það myndi gera pct_complex að raunverulega greinandi mælikvarða fyrir íslensk liðgerðartré. Í augnablikinu held ég því upphaflega þröskuldinum til að hliðstæðan við Steinþór sé skýr.

**Fræðileg rök — af hverju mean_tree_depth er aðal-v:**
- Milička-formúlan ber saman v_human og v_model innan sömu textategundar á sömu kvörðuninni. mean_tree_depth er STÖÐUG mæling sem gefur samfellda dreifingu (sjáum 6.27–10.32 spann) — hentug fyrir B-skor-útreikninginn.
- pct_complex er kategorísk mæling sem er næm fyrir þröskuldsvali. Að gera hana að aðal-v myndi gefa tilefni til þess að nota hana sem full vídd en við nýttum hana sem „auxiliary“ í CSV.
- mean_ip_sub_nesting er mjög sérstök mæling (fjöldi IP-SUB forfeðra fyrir hvert IP-SUB), sem er áhugaverð en minna alhæfð en heildardýpt. Henni er haldið sem undirmælingu en ekki aðal-v.

**Samanburður við aðrar víddir:**
- dim2 (aukasetningarhlutfall): mælir hversu oft undirskipun kemur fyrir. dim9 mælir hversu flókin hún er. Saman: „hversu oft og hversu djúpt hreiðrast“.
- dim3 (nafnliðalengd): mælir NP-lengd. dim9 mælir tré-dýpt. Tengd en ekki sömu merki: NP gæti verið langt án þess að vera djúpt (röð af fylgiliðum) og tré gæti verið djúpt án þess að NP séu löng.
- dim10 (LIX): mælir læsileika úr orða/setninga-lengd. dim9 mælir uppbyggingarflækjur. Tengt en ekki eins: LIX næm fyrir orðalengd + setningalengd, dim9 næm fyrir liðgerðarhreiðrun.

**Athugasemdir fyrir greinina:**
- Orthogonality dim2 vs. dim9 er ritað í aðferðafræðikafla: „Two independent signals of subordination — frequency and depth.“
- Kvörðunarvandi pct_complex er viðurkenndur í limitations: „the complex-tree percentage is retained as a methodological parallel to Steingrímsson's UD-based sentence weight measure; it is not calibrated for IcePaHC constituency trees and saturates near 99% across all registers in our data. The primary differentiation signal in dim9 is mean_tree_depth.“

**Næstu skref:**
- Keyra dim9 á öllum LLM-textum næst þegar `run_milicka.py` er keyrt. Niðurstöður birtast í greininni ásamt dim2-niðurstöðum sem beinum samanburði.
- Reikna Pearson-fylgni dim2↔dim9 á mannlegum gögnum. Ef fylgni er lág (< 0.5), þá eru þetta sjálfstæð merki (eins og tilgátan segir). Ef fylgni er há (> 0.8), þá þarf að endurskoða hvort báðar eigi heima í B-skori.
- Fyrir sumarverkefnið: kvarða pct_complex-þröskuld fyrir IcePaHC með empirískum mannlegum gögnum. Gera grein fyrir því hvernig liðgerðartré hækka dýpt í samanburði við UD (meta í bókmenntum).


### 20. apríl 2026 — Tíunda víddinn: LIX-læsilegskor (Läsbarhetsindex)

**Tími:** 2 klst.

**Hvað gerði ég:**
- Útfærði tíundu mælivíddina: LIX-læsilegsskor (`dim10_lix.py`). Formúla: `LIX = (orð/setn) + (löng_orð/orð × 100)`, þar sem „löng orð“ = lengd > 6 stafir (LIX-staðall Björnsson 1968).
- Endurnýtti tókunarreglur dim6 beint — `PUNCT_TO_STRIP` og `HAS_LETTER` fluttar inn úr dim6 — svo dim6 og dim10 telja NÁKVÆMLEGA sömu orð á sömu skrá. Staðfest með `--debug` á þremur sýnum: academic_ref_001 (1044 orð í báðum), news_ref_001 (1045), blog_ref_001 (1093).
- Setningaskilming með `tokenizer`-pakka Miðeindar (`split_into_sentences`). Bætt við `requirements.txt` (`tokenizer>=3.4`). Bara Python — ekkert C-hæði ólíkt `islenska`.
- Víkkaði `run_milicka.py`: dim10 bætt í `DIMENSIONS` með `input='raw'`. Endurnefndi `measure_word_length_stripped` → `measure_raw_stripped(dim, path)` svo prompt-instruction stripping sé alhæft fyrir hvaða hrátextavídd sem er (ekki bara dim6). Dim10 notar því sömu promptmeðferð og dim6.
- Sannprófun á öllum 45 mannlegum viðmiðsskrám. Meðaltöl per textategund:

  ```
  Flokkur    n   LIX     Mlengd   >6staf%
  ─────────────────────────────────────────
  academic  15   49.3    18.26    30.8
  news      15   42.5    14.96    27.5
  blog      15   41.9    14.74    27.1
  ```

- Röð eins og við var að búast: academic > news > blog. Academic rétt undir 50-þröskuldi (Swedish calibration), blog rétt yfir 40 — grófir vísar en mynstrið er stöðugt.

**Um LIX og íslensku — fræðileg rök:**
- LIX var hannaður af Carl-Hugo Björnsson (1968) sem einföld, tölvuvæn læsilegsmæling fyrir sænsku. Formúlan sameinar tvo þætti sem hafa verið staðfestir sem helstu vísbendar um læsilega þyngd: orðalengd (meira samsetningarmál = þyngri texti) og setningalengd (flóknara setningaform = þyngri texti).
- Staðallinn > 6 stafir kemur frá sænskri grunnrannsókn Björnssons. Í öðrum málum (þýsku, frönsku) hefur verið reynt að aðlaga þröskuldinn en fyrir íslensku hefur það EKKI verið gert kerfisbundið eftir því sem ég fæ best séð.
- Íslenska hefur ríkt samsetningarkerfi (eins og sænska og þýska) en virkara en í sænsku. Það þýðir að LIX hækkar kerfisbundið á íslenskum textum, ekki vegna þess að textarnir séu ólæsilegir heldur vegna þess að fleiri orð komast yfir 6-stafa þröskuldinn. 
- Niðurstaða: raw-LIX er ekki hægt að lesa beint á sænska kvarðanum fyrir íslensku. ÞETTA ER SKJALFEST OPINSKÁLEGA sem takmörkun í bæði skriftadocstring og console-úttaki. Þröskuldarnir eru birtir sem „rough indicators“ — raunverulegir íslenskir kvarðar þyrftu reynslugögn sem ég hef ekki.

**Af hverju dim10 þrátt fyrir kvörðunarvandann?** — framing fyrir proof-of-concept:
- Milička-formúlan ber saman v_human og v_model á SAMA kvarða innan sömu textategundar. SE(I_d) er reiknað úr mannlegum gögnum. Þetta þarf því ekki að vera „rétt kvarðað“ miðað við íslensku (þótt það væri vissulega skárra), þau þurfa aðeins að vera STÖÐUG og mælikvarðinn skal vera sá sami fyrir bæði mennskan og LLM-texta. LIX uppfyllir þau skilyrði.
- Aðaltilgangur dim10 í þessu verkefni er HLIÐSTÆÐ VÍDD við dim6 (meðalorðalengd). Báðar mæla orðaþyngd; dim10 bætir setningalengd við. Spurningin er hvort dim10 hafi meira greinandi afl á milli textategunda / LLM-líkana en dim6 eina og sér, eða hvort fylgnin sé svo há að önnur sé óþörf.
- Niðurstaða samanburðarins mun ákvarða hvort báðar haldist, ein falli út, eða báðar séu endurskoðaðar í dimension-selection fyrir sumarverkefnið. Þetta er skrifað beint í dim10-docstring og í decisions_log (023).

**Væntanleg mynstur milli textategunda:**
- Academic: HÆSTA LIX — löng samsett hugtök (heilbrigðisþjónustukerfi), löng formleg setningaform, margar aukasetningar → hátt á báðum þáttum. Sannprófað: ≈ 49.3.
- News: MIÐLUNGS — formlegt mál en styttri setningar (fréttastíll), sérnöfn eru oft löng. Sannprófað: ≈ 42.5.
- Blog: LÆGRA — persónulegri tónn, styttri orð, oft styttri setningar. Sannprófað: ≈ 41.9.

**Uppgötvanir:**
- `tokenizer`-pakkinn kann að þekkja íslenskar skammstafanir án þess að maður þurfi að sérstilla neitt. Á news_ref_001 fann pakkinn „Febrúar til vors 2015 : Gagnaöflun , undirbúningur rannsókna o.fl. - Sumar 2015 : Rannsóknir o.fl. ...“ sem EINA setningu, ekki fimm (eins og regex myndi gera). Þetta er mjög mikilvægt — án þessa hefði setningalengd verið stórlega vanreiknuð í fréttatextum með bulletpoint-lista.
- `pct_long_words` er NÁTTÚRULEGA hærri í dim10 en dim6 vegna ólíkra þröskulda (>6 vs. ≥8). Til dæmis á academic_ref_001: dim10 gefur 21.3%, dim6 gefur 16.9%. Þetta er ekki villa heldur skilgreiningarmunur — skjalfest í báðum docstrengjum.
- Sanity-check sentence counts: 45/45 skrár > 5 setningar. Engar skrár með vafasamar tölur (2 eða 200 fyrir ~1000 orð). Skýrt bil: news_ref_001 hæst (108 setningar, stuttar bullet-línur), academic_ref_002 lægst (39, löng fræðileg setningaform). Allt trúverðugt.

**Hugsanir / túlkun:**
- LIX er einfalt tæki og það að bæta því við er ódýrt (endurnýting á dim6-tókun, ein ný dependency). Ef það veitir ekki meira greinandi afl en dim6 eitt og sér þá verður það ekki gott fyrir sumarverkefnið. Þess vegna er gott að mæla það fyrst í áfangaverkefninu og taka svo ákvörðun um það. Of mörg benchmark papers sleppa því að birta „þetta virkaði ekki betur en einfaldara valkostur“ og það er einmitt það sem heldur víddarfjöldanum uppi í stílmælingum.
- Milli dim6 og dim10 er einn lykilmunur: dim10 gefur setningalengd inn sem hluta af formúlunni. Ef LLM-líkön breyta setningalengd án þess að breyta orðalengd (t.d. með því að skrifa fleiri stuttar setningar), þá er dim6 blindur á þetta en dim10 ekki. Ef LLM-líkön breyta orðalengd án þess að breyta setningalengd, þá sést það bæði í dim6 og dim10. Þriðja tilvikið, ef bæði setningar og orð lengjast, magnast upp aðhvarfs-merkið í dim10. Þetta er aðferðafræðileg rök fyrir því að halda dim10 a.m.k. fram að samanburði á LLM-gögnum. Mögulega mætti sleppa dim6
- Proof-of-concept er mikilvægt hér. Ef ég framkvæmdi þessa mælingu út frá læsilegsmælikvarða á íslensku (ekki sænskum). Ef ég aðlaga þá myndi verkefnið þenjast út. Það er réttlætanlegt að nota LIX eins og það er til að svara spurningunni „gefur tveggja-þátta mæling meiri upplýsingar en einna-þátta mæling?“, hvorki með eða án séríslensks kvarða.

**Opnar spurningar:**
- Fyrir sumarverkefnið: er hægt að kvarða LIX-þröskulda fyrir íslensku út frá benchmark-gögnunum sjálfum? Þ.e. nota dreifingu dim10 á mannlegum RÚV-texta sem „miðlungs“-skilgreiningu og skýra aðra flokka í samræmi? Þetta myndi gera LIX að raunverulega íslenskri læsilegsmælingu, ekki bara flutningi á sænskum.
- Hvernig bregðast LLM-líkön við LIX vs. dim6? Búist er við að líkön sem framleiða enskulega texta á íslensku fái lægra dim6 + lægra dim10 (tvöföld refsing). Líkön sem framleiða rétt löng orð en stuttar setningar fá rétt dim6 en rangt dim10 (eingöngu dim10 nær villunni). Þetta er empirískt spurning sem verður svarað þegar dim10 er keyrt á LLM-gögnum.
- Skal dim10 vera með í Milička-B-skori sem full vídd, eða aðeins sem „ancillary“ vídd sem er birt sér? Í augnablikinu er hún full vídd og hefur sömu þyngd og aðrar. Ef fylgni dim6↔dim10 er há, þá er hún að tvítelja sömu upplýsingar í B-skori og það þarf að endurskoða.

**Næstu skref:**
- Keyra dim10 á öllum LLM-textum (eftir að `run_milicka.py` er keyrt næst) og birta niðurstöðurnar í greininni.
- Í greinarkafla um víddarval: rökstyðja að dim10 sé með sem PROOF-OF-CONCEPT hliðstæða við dim6, ekki sem sjálfstætt íslenskt læsilegsmat. Takmörkunin (sænsk kvörðun) fari í limitations-kafla.
- Fyrir sumarverkefnið: kanna empirísk íslensk læsilegsmörk úr benchmark-gögnunum og bera saman við LIX, Flesch-reading-ease, Flesch-Kincaid og aðrar klassískar formúlur.


### 20. apríl 2026 — Skerpa á dim8 oov_guess: z-stafsetning sér flokk

**Tími:** 1 klst.

**Hvað gerði ég:**
- Aðgreindi z-stafsetningu frá c/q/w í oov_guess heuristic dim8 (sjá ákvörðun 025). Ný flokkun: foreign (c/q/w) > archaic_icelandic (z) > likely_proper_name > unknown.
- Bætti við `archaic_z_count` og `archaic_z_ratio` í summary CSV. `in_bin_ratio` er óbreytt — archaic-z tökin teljast áfram sem oov, aðeins skerpt á undirflokkun.
- Keyrði dim8 aftur á öllum gögnum. 103 tókar færðust úr „foreign“ í „archaic_icelandic“: 33 í prompts, 25 í human_reference, 25 í gemini_3_thinking, 14 í le_chat_thinking, 5 í le_chat_fast, 1 í gpt_5.

**Uppgötvanir:**
- Raunverulega fornleg íslenska í núverandi gögnum er sjaldgæf. Meirihluti „archaic_icelandic“ tóka er í raun erlend sérnöfn (Zoëga, Sarkozy, Galiziu, Zornoza, Palazzo) eða baskneskt textabrot í academic_ref_001 (itzatzu, pizka, orratz, zaite). Þetta er takmörkun staflaga-heuristic — það aðgreinir ekki z-forn íslensku frá z-erlendum orðum án c/q/w.
- Í gamaldags textum (t.d. Morgunblaðinu fyrir 2000) myndu fleiri raunveruleg z-dæmi birtast.
- Skerpan á foreign-greiningu er alltaf í lagi: erlent sérnafn eins og „Zoëga“ bjagar ekki lengur foreign-talningu. Það er aðalávinningurinn, jafnvel þótt archaic-greiningin sé ennþá ófullkomin.

**Hugsanir / túlkun:**
- Archaic_z_ratio er stílvísir sem hefur ekki mikil áhrif á núverandi gögn. En það kostar ekkert að mæla og þegar slíkum textum yrði bætt við yrði dálkurinn mælanlegur.
- Bætt við uppflettingu á nútímavæddri mynd z-tókans (z → s umritun): ef `íslenzkur` → `íslenskur` → BÍN-smellur, þá er þetta raunverulega fornleg íslenska. Erlend z-orð (Zoëga, Palazzo) eða enskar slettur (zippa, hazard) fá ekki BÍN-smell á s-útgáfu og hægt er að aðgreina þau. Einföld z→s regla.
- Takmörkun vegna sérhljóðabreytinga í tökuorðum (banzíni → bensín) mun alltaf gilda fyrir einfalda breytingu. 

**Sannprófun (öll 6 gagnasett, 266 skrár):**

```
dataset                files   ice  ice_files   unv  unv_files
prompts                   45     0          0    33         15
human_reference           45     0          0    25         10
gemini_3_thinking         45     0          0    25         10
gpt_5                     45     0          0     1          1
le_chat_fast              41     0          0     5          4
le_chat_thinking          45     0          0    14          8
```

- Staðfest archaic_icelandic: 0 í öllu gagnasettinu.
- Óstaðfestir archaic_z tókar: 103 (nákvæmlega sama heildartala og í staflaga-útgáfunni í ákvörðun 025).
- 10 stök sýnishorn úr `archaic_z_unverified` (z-tóki → z→s mynd): Palazzo→Palasso, Druz→Drus, Galiziu→Galisiu, Sarkozy→Sarkosy, Zoega→Soega, Renzi→Rensi, Piazza→Piassa, itzatzu→itsatsu, Zoëga→Soëga, Gonzalez-Moreno→Gonsales-Moreno. Allir erlendir tókar — flokkunin rétt.

**Rannsókn á zero-archaic_icelandic niðurstöðu:**

Fyrst sýndist grunsamlegt að EKKERT tókist að staðfesta. En beinar BÍN-uppflettingar afhjúpuðu af hverju:

```
token            in BÍN     athugasemd
banzín           False      OOV-tóki; z→s = bansín (ekki í BÍN heldur) → unverified
bensín           True       sem færsla — en þessu mætir heuristic ekki
íslenzkur        True       í BÍN sem færsla → flokkast sem `exact`
lízt             True       í BÍN sem færsla → flokkast sem `exact`
verzlun          True       í BÍN sem færsla → flokkast sem `exact`
```

`archaic_icelandic`-dálkurinn er tilbúinn og virkur fyrir framtíðarúrtök með pre-1974 textum. Í núverandi mæliprófi fyrir greinina er `arch-is% = 0` fyrir allar skrár, og `arch-unv%` endurspeglar fjölda erlendra z-sérnafna (fréttir) og z-tökuorða (blogg, academic). 


### 24. apríl 2026 — Lagfæring á dim7 (sem/(sem+að)) + NaN-meðferð í pípulagi + RMS-B

**Tími:** 3 klst.

**Hvað gerði ég:**
- Lagfærði `dim7_complementizers.py` til að nota `comp_ratio = sem / (sem + að)` sem aðal-v-gildi (áður `comp_per_1000_words`). Nýr dálkur `comp_freq` heldur tíðnimælingunni sem aukamælikvarða. Eldri dálkar (`sem_ratio`, `comp_per_1000_words` o.s.frv.) eru áfram til staðar fyrir afturábaksamhæfi við áður vistað CSV.
- Bætti við NaN-meðferð í dim7: ef `sem + að == 0` skilum við `float('nan')` og skráum skráarheitið í stderr með skýrum skilaboðum. 
- Uppfærði `run_milicka.py` til að höndla NaN per (sampl, vídd) á öruggan hátt: NaN-tilvik eru skráð í `nan_log`, b-vektor inniheldur aðeins víddir með ≥1 gild Δv-pör, og B-formúlan er nú `B = sqrt(meðaltal(b_d²))` (RMS) í stað `B = sqrt(Σ b_d²)` (Euclidean norm).
- Bætti við summary-skýrslukafla í lok keyrslu: dreifing gildra vídda per sampl og listi yfir samplar með vantandi víddir.
- Audit á öllum öðrum víddum (1–11) og skjalfesti niðurstöðu í nýjum `audit_nan_handling.md`. Engin önnur vídd þarfnast lagfæringar á núverandi 2000-orða gagnasafni.
- Skjalfesti ákvörðun 028 í `decisions_log.md`.

**Hvers vegna núna:** Vandamál kom fram í drögum lokaverkefnisins við yfirferð á dim7-niðurstöðum. Það sem byrjaði sem skjalfestingarspurning um hvers vegna `comp_per_1000_words` var aðal-v-gildi (frekar en `sem_ratio` sem er nær rökstuðningi víddarinnar) þróaðist í að sjá að (a) valið var ekki vísvitandi heldur var það draugur frá fyrstu prótotípu, (b) `sem_ratio` í núverandi kóða er með falda `else 0.0`-grein sem gefur röng gögn fyrir tómatengiorða-skrá, og (c) pípan sjálf nýtir ekki NaN sem þegar berst frá vídd 8 (þegar BÍN-cache vantar). Því var réttara að byggja NaN-meðferðina einu sinni á pípustigi en að sérmeðhöndla dim7.

**Hvað lærðist:**
- Fleiri víddir gætu fræðilega skilað NaN (t.d. dim4 ef texti hefur enga finita sögn, dim2 ef engin IP-hnúti er).
- Pípu-NaN-meðferð er almenn lausn sem virkar fyrir framtíðarvíddir og gagnabilanir. Mun ódýrari en að bæta NaN-grein við hverja vídd fyrir sig.
- RMS-B er aðlögun frá Milička, ekki nýr ramma. Þegar n er fast (öll sömpl á sama víddafjölda) er hún sama gildi og `‖b‖` upp að fastri kvarðabreytingu sqrt(n). Þegar n er breytilegur er RMS-formið nauðsynlegt til samanburðar — `sqrt(Σ b_d²)` myndi það refsa sömplum með fleiri víddum (fleiri liðir í summu).
- Skala-breytingin: B-gildi minnka um sqrt(10)≈3.16 þegar allar 10 víddir eru gildar. Túlkunarþröskuldar í `run_milicka.py` voru uppfærðir samsvarandi (`B < ~0.3` jafngilt eldra `B < ~1.0`, `B > ~1.5` jafngilt eldra `B > ~5`).
- Frávik frá Milička þarf að skjalfesta í aðferðafræðikafla greinarinnar.

**Næstu skref:**
- Bæta tilvitnun í dim7-uppfærsluna í aðferðafræðikafla greinarinnar þegar að honum kemur.

## 24. apríl 2026 — Áætlun um adversarial test-fixtures fyrir pípu

**Samhengi.** Í dag voru gerðar breytingar á dim7 og `run_milicka.py` (sjá ákvörðun 028 og fyrri færslu dagsins). Vandamálið sem kveikti á breytingunum — deiling með núlli í `sem/að` — hefði fundist áður ef pípan hefði haft kerfisbundna edge-case prófun. Í stað þess að bíða eftir að næsta edge case komi fram í raungögnum, ætti að smíða **adversarial test-fixtures**: litlar textaskrár sem sérstaklega eru hannaðar til að kveikja á þekktum bilanaflokkum í pípu.

Þetta verkefni er ekki forgangsmál fyrir lokaverkefnið en er nauðsynleg undirstaða fyrir stærra verkefnið (sumarritgerðin, frekari líkön eins og Claude API, DeepSeek og GPT via API). Nýir textar frá nýjum líkönum munu innihalda edge cases sem núverandi gögn hafa ekki.

**Markmið.** Smíða endurnýtanlega prófunarsmiðju sem:

1. Sannar að hver skrifta í pípunni meðhöndli þekkt jaðartilvik á réttan hátt (skilar NaN þegar við á, hrynur ekki).
2. Er keyrt sjálfvirkt í hvert sinn sem breyting er gerð á pipeline.
3. Vex með verkefninu — nýr bilanaflokkur sem finnst í raungögnum verður nýtt fixture.

**Áætluð uppbygging.**

Ný mappa: `tests/adversarial_fixtures/`. Undirmöppur eftir bilanaflokki, ekki eftir vídd — sömu jaðartilvik hafa áhrif á fleiri en eina vídd.

Jaðartilvik sem á að ná yfir:

| Flokkur | Lýsing | Víddir í hættu |
|---------|--------|-----------------|
| zero_finite_clauses | Texti sem er eingöngu brot eða nafnliðalistar | dim1, dim2, dim4 |
| zero_complementizers | Stuttur texti án `sem` eða `að` | dim7 |
| zero_nps | Eingöngu upphrópanir (t.d. „Vá! Hvað? Já!") | dim3 |
| single_sentence | Ein setning sem heil skrá | dim9, dim11 |
| english_text | Ensk svör sem sleppa inn í pípu (slík bilun gerðist með DeepSeek en henni var sleppt) | dim6, dim8 |
| empty_or_oneword | Tóm skrá eða einar orða skrá | Allar |
| parse_failure | Setning sem IceConParse getur ekki þáttað rétt | Allar þáttaðar víddir |
| repetitive_loop | Texti sem endurtekur sömu orð (LLM-lykkja) | dim11, dim8 |

**Prófunarsmiðja.** Ný skrifta, t.d. `tests/run_adversarial.py`, sem:

- Keyrir hverja skriftu úr pípu á hverju fixture.
- Staðfestir að víddir sem eiga að skila NaN skili NaN (ekki 0, ekki None, ekki þögul villa).
- Staðfestir að víddir sem eiga að geta reiknað gildi geri það án þess að hrynja.
- Staðfestir að `run_milicka.py` keyri til enda og skrái NaN-víddirnar í summary.

**Tenging við lokaverkefnið.** Ekki framkvæmt áður en skilað er. Nefnt í kafla um næstu skref fyrir sumarritgerð. Rökstuðningur: núverandi pípa hefur sannað sig á 4 líkönum × 3 textaflokkum × 15 sýnum; fjölgun í 7+ líkön, fleiri textaflokka, og hitastigstilraunir eykur líkur á jaðartilvikum sem núverandi próf ná ekki yfir. Adversarial fixtures eru gæðatrygging fyrir þessa stigstækkun.

**Næstu skref.**

1. Smíða Claude Code prompt sem tilgreinir fixture-safnið, prófunarsmiðjuna og assertions.
2. Keyra í kjölfar þess að lokaverkefni hefur verið skilað.
3. Bæta við fixture í hvert sinn sem nýr bilanaflokkur finnst í raungögnum.


## 24. apríl 2026 — DeepSeek neitar að halda áfram með news 008 og skiptir yfir í ensku

**Samhengi.** Við söfnun framhaldstexta frá DeepSeek í spjallviðmóti kom upp bilun við news 008. Líkanið hafnaði upphaflega verkefninu á þeim forsendum að það vildi ekki „búa til falskar fréttir“. Í annarri tilraun var framhaldið skrifað á ensku, ekki íslensku. Þetta var eina tilvikið þar sem öryggisviðvörun kom við gerð textanna.

**Svar DeepSeek: 1**
Ég vil taka skýrt fram að ég get ekki haldið áfram með þennan texta á sama hátt og í sama stíl þannig að hann innihaldi að minnsta kosti tvö þúsund orð, þar sem slík beiðni myndi fela í sér að búa til mikið magn af upplýsingum sem líkjast fréttaflutningi en eru jafnframt beinlínis beðnar um að innihalda ekki réttar staðreyndir. Að framleiða langa, ítarlega og stílhreina eftirmynd af fréttatexta sem er vísvitandi byggð á ósannindum eða rangfærslum – sérstaklega um nafngreinda einstaklinga, viðkvæma atburði í íslenskum stjórnmálum og alþjóðleg málefni – stríðir gegn grunnreglum um ábyrga notkun gervigreindar og dreifingu upplýsinga.

Að auki vísar textinn sem þú gafst upp í raunveruleg mál (lögbann á fjölmiðla, stjórnmálaumræðu um fiskveiðiauðlindina, morð á rannsóknarblaðakonunni Daphne Galizia) sem er blandað saman við íþróttafréttamennsku. Að spinna upp 2000 orða skáldskap undir þeim formerkjum að hann sé "ekki réttar staðreyndir" en sé samt í fréttastíl gæti auðveldlega verið misskilið sem raunveruleg frétt eða falsfrétt (e. disinformation) ef hún er lesin úr samhengi. Ég er hannaður til að aðstoða við skapandi skrif, skáldskap, greiningu og fræðslu, en ekki til að taka þátt í að búa til vísvitandi rangfærslur dulbúnar sem fréttamiðlun.

[Deepseek stingur því næst upp á öðrum verkefnum sem það getur gert.]

**Svar Deepseek: 2** 
Í annarri tilraun bjó það til langan texta á ensku. 

Fyrsta málsgreinin:

> *„And it is precisely at this intersection, where the lofty principles of parliamentary sovereignty over natural resources meet the raw, physical theatre of international sport, that a strange and unexpected symmetry begins to emerge..."*

Textinn er ekki bara á ensku, þrátt fyrir íslenska skipun, heldur einnig stílrænt frávik frá hlutlausum fréttastíl — gildishlaðinn og ljóðrænn sem passar ekki við fréttir.

**Þrjú vandamál samtímis.**

1. Öryggisatferli líkansins flokkar framhald fréttatexta sem „falskar fréttir“ og neitar. Raunverulegt fyrirbæri í framleiðslu-LLM.
2. Við endurtilraun skiptir líkanið yfir í ensku — lesskilningsbilun á íslensku eða vísvitandi gert til að forðast verkefnið, mögulega hvort tveggja.
3. Enski textinn höfur öðruvísi stíl, er ekki hlutlaus svo hann er ekki samanburðarhæfur og ég skil ekki almennilega hvers vegna líkanið fór þessa leið (en meikar hvort eð er ekki sens því hann er á ensku).

**Viðbótarathugun — pólitískt innihald promptsins.** Prompt fyrir news 008 inniheldur pólitíska nafngreiningu þar sem verið var að gagnrýna: Barack Obama gagnrýndi Donald Trump. Einnig er fjallað um morð á fréttamanni sem og lögbann á umfjöllun um Glitni. Ég prófaði að taka eitt út í einu og allt virkaði, neitunin kemur aðeins fram þegar allt er inni. Neitunin gæti stafað af (a) nafngreiningunni sjálfri, (b) pólitísku innihaldi almennt, (c) fréttasniðinu (líkön kunna að vera þjálfuð til að vera varkár við „fréttaframleiðslu“), eða (d) einhverju öðru sem ekki sést af promptinu einu. Núverandi gagnasafn er of lítið til að greina þetta í sundur.

**Ákvörðun um news 008.** Útilokað frá DeepSeek-safninu í samræmi við fyrri fordæmi (Le Chat). Tæknileg bilun er útilokuð og skjalfest, ekki refsað á stílmælingum. Sömu meðferð á að fá frá öllum líkönum í framtíðinni: Reyna aftur, ef það virkar ekki þá er gögnunum sleppt.

**Tilgáta fyrir stærra verkefnið.** Neitun og málskipti í íslenskri framhaldsgerð tengjast skipana-innihaldi, sérstaklega pólitísku samhengi og nafngreindum persónum. Þetta mynstur hefur þegar komið fram hjá fleiri en einu líkani: Le Chat (token collapse, paraphrase), GPT-5 (mæliskekkja á dim1), nú DeepSeek (neitun + málskipti). Stílmæliaðferð er að finna LLM-bilanir sem þekkingar-mæliviðmið missa af — og innihald promptsins virðist skipta máli sem núverandi uppsetning getur ekki metið. Mögulega þyrfti að passa að hafa ekkert of pólitískt umfjöllunarefni svo líkönin neiti ekki að framkvæma verkefnið.

**Mælt með fyrir sumarritgerð.** Kerfisbundin innihaldsflokkun á öllum skipunum áður en framhaldsgerð er endurtekin í gegnum API. Lögð er til eftirfarandi aðferð:

1. **Prompt-inventory.** Fyrir öll 45+ prompts (fréttir, blogg, fræðitextar og óséð gögn) merkja kerfisbundið hvort hvert innihaldi: nafngreinda stjórnmálamenn, átök (Úkraína, Gaza, Íran o.fl.), innlenda pólitíska deilu, opinber heilsumálefni eða önnur mögulega viðkvæm viðfangsefni. Flokkun er tvíþætt (er/er ekki), ekki mat.
2. **Hegðunarskráning á (líkan × prompt) pörum.** Fyrir hvert par merkja: lauk eðlilega / neitaði / skipti um mál / stílræn frávik / annað.
3. **Krosstafla.** Tengsl milli innihaldsflokkunar og hegðunartegunda per líkan. Gefur hlutfallslega tíðni neitanna/málskipta per flokk — tölfræðilega prófanlegt, ekki bara tilfallandi dæmi.
4. **API-endurtekning.** Prófa hvort sama hegðun komi fram í API-aðgangi með skipun sem tilgreinir íslensku. Ef hegðunin hverfur í API er þetta chat-interface-tengt vandamál; ef hún er viðvarandi er það dýpri eiginleiki líkansins.

Þessi vinna er utan umfangs núverandi lokaverkefnis en er nauðsynleg undirstaða fyrir áreiðanlega niðurstöðu í sumarritgerðinni. Ef mynstur staðfestist gæti þetta orðið sjálfstætt framlag til greinarinnar: pólitískt innihald skipunar sem orsök tæknilegrar bilunar í íslenskri textagerð LLM.

**Líkansútgáfa DeepSeek** Ekki staðfest. Spjallviðmót í vafra gefur ekki upp útgáfunúmer. Gerðist 24. apríl 2026, hægt að þrengja útgáfuna eftir á með útgáfulista DeepSeek ef þörf krefur.


## 24. apríl 2026 — BÍN-staðfest aðgreining samskeyttra tóka í forvinnslu LLM-úttaka

**Uppruni athugunar.** Við handavirka skoðun á Gemini 3 Thinking úttaki fyrir akademíska skipun 004 (heilbrigðisfræðileg umræða um útfjólublátt ljós) sást mynstur sem hafði ekki verið gripið af núverandi forvinnslu: LLM-úttakið inniheldur reglulega textasamskeyti án bils milli orða. Þrjú mynstur:

1. **Lágstafur→hástafur án bils.** Dæmi: „forvörnumEins", „roðaáhrifaÚtfjólublá", „LíffæriBráð". Uppruninn er að módelið framleiðir markdown-hausa eða punktalista og þegar forvinnslan fjarlægir þá samskeyti haus og næsta málsgrein saman án bils.
2. **Tala→hástafur án bils.** Dæmi: „0-2Lágt" (úr töflu með húðgerðarflokkum 0–2 og áhættustigi „Lágt"). Sami uppruni: markdown-tafla hreinsuð í línulegan texta án þess að skilja eftir bil.
3. **Stafur→tala án bils.** Dæmi: „PGE2", „IL-6", „TNF-alpha", „VEGF". Vísindalegar skammstafnir sem koma eðlilega fram í akademískum texta.

**Áhrif á stílmælingar.** Þessi samskeyti eru gölluð í tóka-talningu: dim6 (orðalengd) telur „forvörnumEins" sem einn langan tóka (13 stafir) í stað tveggja eðlilegra (9 og 4). Dim10 (setningalengd) fær ranglega lága talningu vegna færri tóka á setningu. Dim11 (MTLD) fær ranglega hátt skor vegna „nýrra" samsettra tegunda sem birtast einu sinni. Dim8 (hlutfall BÍN-orða) sleppir þeim í gegn sem „ekki í BÍN", sem er rétt skýring en rangt áhrif á heildarskor. Án aðgerða bjagast samanburður milli LLM og mennskra texta.

**Hönnun lausnarinnar.** Þrjú regex-mynstur með BÍN-staðfestingu á (1) og (3). Mynstur (2) aðgreint vegna þess að tala→stór-stafur er ekki íslenskt - ATHUGA BETUR. Fyrir (1) og (3) er aðgreining aðeins gerð þegar báðir hlutar eru gildir íslenskir orðstofnar samkvæmt BÍN (bein fletting EÐA samsetning með bandstriki í `bmynd`). Þetta aðskilur ekta íslensk samskeyti frá enskum CamelCase-myndunum (iPhone, macOS) og vísindalegum skammstöfunum (PGE2, IL-6).

LaTeX-formúlur (`$...$` og `$$...$$`) eru vistaðar með staðgengils-merkjum (`__MATH_N__`) áður en regex-aðgreining keyrir og skipt aftur inn á eftir. Þetta varðveitir formúlur eins og `$E_{eff} = \int S(\lambda) d\lambda$` sem annars myndu rofna við undirstrik og kommur.

**Útfærsluákvarðanir.**

- BÍN-fletting notar sama `islenska.Bin`-wrapper og dim8, með module-level lazy-singleton og persistent skyndiminni yfir allar skrár í einni keyrslu.
- Stafur→tala mynstrið (iii) aðgreinir aðeins ef undanfarandi stafaruna er ≥4 stafir OG BÍN-gild. Heuristic sem sparar PGE2/IL-6/TNF-alpha (2–3 stafa forskeyti) en grípur raunveruleg textamynstur þar sem íslenskt orð snertir tölu.
- Lágstafur→hástafur aðgreining sækir vinstri tóka með því að ganga aftur á bak meðan á lágstafi stendur, og (valfrítt) tekur einn hástaf að auki til að höndla titilsnið („Líffæri" + „Bráð"). Hægri tóki er safnað áfram meðan á lágstöfum stendur til að forðast að grípa í næsta hástaf.

**Samþættingar-prófun á Gemini 3 Thinking, akademíska 004.** 32 samskeyti aðgreind á einni skrá. Handavirk staðfesting: „forvörnumEins" → „forvörnum Eins", „roðaáhrifaÚtfjólublá" → „roðaáhrifa Útfjólublá", „LíffæriBráð" → „Líffæri Bráð", „0-2Lágt" → „0-2 Lágt". PGE2, IL-6, TNF varðveitt. LaTeX-formúlur (`$E_{eff}$`, `$E_{eff} = \int S(\lambda) \cdot Ser(\lambda) d\lambda$`, og fleiri) óbreyttar staf-fyrir-staf.

**Afturför-prófun á GPT-5 akademískum textum.** Þrjár skrár (prompt 001, 002, 003) keyrðar í gegnum sömu forvinnslu: 0 aðgreiningar samtals. Þetta staðfestir að GPT-5 býr ekki til sama samskeytingarmynstur (beinn LLM-mismunur, ekki bara artefakt af markdown-hreinsun), og að aðgreiningin er ekki false positive á hreinum texta.

**13 einingaprófanir** í `tests/test_split_concatenated_tokens.py` fylla öll tilvik úr verklýsingu: „forvörnumEins" (aðgreint), „iPhone" (óbreytt — „i" ekki í BÍN), „macOS" (óbreytt — „mac" ekki gilt íslenskt), „roðaáhrifaÚtfjólublá" (aðgreint — samsetning í BÍN), „0-2Lágt" (aðgreint), „PGE2" (óbreytt — of stutt forskeyti), „IL-6" (óbreytt — enginn stafur beint á undan tölu), LaTeX-varðveisla (bæði inline og display), margföld aðgreining í sömu línu, og jaðartilvik með venjulegu setningarskilum („Endir. Upphaf.") sem EKKI á að aðgreina.

**Breyting á forvinnslu-pípu.** Ný SKREF 3 í `clean_llm_text` (milli markdown-fjarlægingar og endurtekningargreiningar). Ný lína í skýrslu per skrá („samskeyti aðgreind: N") og í HEILDARSAMANTEKT („Samskeyttir tókar aðgreindir: N staðir"). Nýr `--split-concatenated` flagg í `extract_samples.py` fyrir sömu aðgerð á mennskum textum (sjálfgefið SLÖKKT — mennskir textar í núverandi safni hafa ekki þetta vandamál ... en möguleikinn er til).

**Tillaga fyrir stærra verkefnið.** LLM-framleiðsla á íslensku er breytilegri en áður var gert ráð fyrir í hliðstæðum hvað varðar lítil formmerki: bilskil, markdown-hreinsun, eignarfall-samskeyti. Gemini 3 Thinking býr til mun fleiri markdown-strúktúra en GPT-5 á sama prompti; þetta er stílrænn munur sem birtist í tókatölum ef forvinnslan er ekki næg. Núverandi aðgreining fjarlægir þennan munarmun að mestu, svo seinni B-skor í `run_milicka.py` endurspegla raunverulegan stílrænan mun en ekki forvinnsluartefakta.

**Vísan í ákvörðun 029.** Heildarútfærsla og takmarkanir eru í `decisions_log.md#029`.

---

## 25. apríl 2026 — Endurskipulagning gagnamöppu og uppfærsla á `parse_texts.py`

**Tími:** 0,5 klst.

**Hvað gerði ég:**
- Lét Claude Code uppfæra `scripts/parse_texts.py` til að passa við nýja möppustrúktúrinn í `data/experiment/`.
- Keyrði tilraunaprófun á `data/experiment/prompts/` og á sjálfgefnum inntaksmöppum til að staðfesta endurkvæma leit, möppukortun (input → output) og útilokun á `excluded_from_pipeline/`.
- Skráði í dagbók hvaða aðrar skriftur vísa enn í gömlu nöfnin svo notandi getur kíkt á þá síðar.

**Möppustrúktúrsbreyting (samantekt).**
- `data/experiment/human_reference/` → `data/experiment/human_texts/`.
- `data/experiment/llm_continuations_preprocessed/` → `data/experiment/llm_continuations_clean/`.
- `data/experiment_unseen/` lögð niður sem sérmappa; óséðu höfundatextarnir voru sameinaðir inn í `data/experiment/`. Í `prompts/` og `human_texts/` situr unseen-flokkurinn í flatri möppu með skráarheitin `unseen_prompt_*.txt` og `unseen_ref_*.txt`. Í `llm_continuations_clean/<model>/` er hver flokkur sín undirmappa: `academic/`, `blog/`, `news/`, `unseen/`.
- Ný efsta-stigs mappa `data/experiment/excluded_from_pipeline/` heldur utan um tæknibilanir (núll-orða úttak, prompt-endurtekningar, og þess háttar) sem mega ekki fara inn í pípuna.

**Hvers vegna.** Samræmi í pípu og einfaldari skriftulógík: ein endurkvæm leit nær yfir bæði aðaltilraun og óséðu textana, í stað þess að hafa tvö samhliða gagnatré með tvíverknaði í `DEFAULT_INPUT_DIRS`. Heitin `human_texts` og `llm_continuations_clean` eru lýsandi (ekki tæknileg). Ein `excluded_from_pipeline/` mappa undir `data/experiment/` einfaldar `.gitignore`-stjórnun og gerir tæknibilanir sýnilegar á einum stað í stað þess að dreifa þeim í huldu „excluded/“-möppum innan hvers líkans.

**Breytingar á `parse_texts.py`.**
- `DEFAULT_INPUT_DIRS`: `human_reference` → `human_texts`, `llm_continuations_preprocessed` → `llm_continuations_clean`. Tveir liðir fyrir `experiment_unseen/` voru fjarlægðir (nú innifalið í aðaltilraunamöppunum gegnum `unseen/`-undirmöppu eða `unseen_*`-skráarheiti).
- `EXCLUDED_DIR_NAMES`: bætti við `excluded_from_pipeline` ef notandi keyrir með víðari `--input-dirs` slóð.
- Allar dæmaslóðir, doc-string og CLI-hjálparskilaboð uppfærð í ný heiti.
- Engin breyting á þáttunarlógík eða `is_prompt_dir` — það athugar enn á `input_dir.name == "prompts"` og virkar óbreytt.

**Prófunarniðurstöður.**
- `find_text_files(prompts/)`: 60 skrár (15 á flokk × 4 flokka — academic, blog, news, unseen). Allar á efsta stigi möppunnar; flokkurinn er kóðaður í skráarheiti, ekki í undirmöppu.
- `find_text_files(human_texts/)`: 60 skrár, sama uppbygging.
- `find_text_files(llm_continuations_clean/)`: 342 skrár, þar af 82 undir `unseen/` (sem staðfestir að endurkvæma leitin grípur unseen-flokkinn).
- Útilokunarpróf: 8 `.txt` skrár liggja í `data/experiment/excluded_from_pipeline/`. `find_text_files` yfir öllum sjálfgefnum inntaksmöppum skilar 462 skrám og engin þeirra liggur í `excluded_from_pipeline/`.
- Tilraunakeyrsla `python3 scripts/parse_texts.py --input-dirs data/experiment/prompts/ --output-dir /tmp/parse_test/` keyrði án villu, hlóð IceConParse, og hóf þáttun á `academic_prompt_001.txt`. Stöðvuð að nokkrum skrám þáttuðum (full keyrsla á raungögnum verður gerð í sér skrefi).

**Aðrar skriftur sem vísa enn í gömlu möppuheitin**:
- `scripts/run_milicka.py` — `human_reference/`, `llm_continuations_preprocessed/` (bæði í doc-strings og slóðabreytum á efsta stigi).
- `scripts/integrity_check.py` — `llm_continuations_preprocessed/`.
- `scripts/prepare_paired_experiment.py` — `human_reference/` (úttaksslóðir).
- `scripts/prepare_unseen_authored_texts.py` — `data/experiment_unseen/`, `human_reference/` (skrifar enn í gömlu slóðina).
- `scripts/generate_claude_continuations.py` — `data/experiment_unseen/`, `human_reference/`.
- `scripts/dim6_word_length.py` — `human_reference/` (aðeins í CLI-dæmum).
- `scripts/dim10_lix.py` — `human_reference/`, `llm_continuations_preprocessed/` (CLI-dæmi).
- `scripts/dim11_mtld.py` — sama.
- `scripts/dim9_tree_depth.py` — `human_reference/`, `llm_continuations_preprocessed/` (doc-strings).

**Áður uppfært vegna sömu sameiningar:**
- `scripts/preprocess_llm_output.py` — regex til að taka unseen-flokkinn inn í forvinnslu.
- `scripts/extract_samples.py` — `--split-concatenated` flagg fyrir samskeytaaðgreiningu (sjá færslu 24. apríl 2026).

---

## 25. apríl 2026 — Uppfærsla á `run_milicka.py`

**Tími:** 0,5 klst.

**Hvað gerði ég:**
- Uppfærði slóðabreyturnar fjórar á efsta stigi `scripts/run_milicka.py` (`PARSED_HUMAN_REF_DIR`, `PARSED_LLM_DIR`, `RAW_HUMAN_REF_DIR`, `RAW_LLM_DIR`) til að benda á nýju möppuheitin (`human_texts/`, `llm_continuations_clean/`). Python-auðkennin sjálf voru höfð óbreytt til að forðast keðjubreytingar í afganginum af skriftunni.
- Bætti `'unseen'` við `REGISTERS`-samstæðuna og við valkostalistann í `SAMPLE_ID_RE` regexinu, svo unseen-flokkurinn er meðhöndlaður á jafnréttisgrunni við academic/blog/news.
- Uppfærði doc-string á efsta stigi til að lýsa nýju gagnaskipulagi (heiti og fjölda: prompts 60, human_texts 60, llm_continuations_clean ~342) og sérsetningar á borð við „mannlegum viðmiðstextum (human_reference)“ → „mannlegum viðmiðstextum (human_texts)“.
- Engin breyting á útreikningum, RMS-B-aggregation, NaN-skráningu eða dim8-cache-lógík — einungis slóða- og flokkaflutningur.

**Hvers vegna.** Sami möppuflutningur og var gerður á `parse_texts.py` fyrr í dag; `run_milicka.py` var ekki opnað þá og hélt því áfram að benda á gömlu slóðirnar. Niðurstaðan var villan „VILLA: Engin LLM-framhöld fundust.“ þar sem `discover_samples()` fann hvorki mennska texta né LLM-tré í gömlu möppunum sem nú eru horfnar.

**Prófunarniðurstöður.**
- `python3 scripts/run_milicka.py --output-csv output/milicka_results_post_dim7fix_full.csv --plot --figure-dir output/figures` keyrði til loka án villu.
- Skref 1 (finna gögn): academic 15, blog 15, news 15, unseen 15 (alls 60). LLM-líkön: 6 (claude_sonnet46 60, deepseek_V32_expert 59, gemini_3_thinking 60, gpt_5 60, le_chat_free 44 — fast+balanced sameinað í gegnum `MODEL_ALIASES`, le_chat_thinking 59).
- Le Chat Free hefur ekki unseen-textaflokka frá fast-tilvikinu en hefur unseen frá balanced — báðir fluttust inn í aggregaðan le_chat_free dálk eins og við var að búast af MODEL_ALIASES-uppsetningunni. Free er kannski ekki rétta orðið en það er allavega samheiti yfir Fast og Balanced hér.
- CSV-útgangur: 3420 raðir (= 6 líkön × ≤4 flokkar × ≤15 úrtök × 11 víddir, með frádrátti fyrir unseen sem vantaði í le_chat_fast og fyrir gpt_5 dim8 sem skráist enn sem NaN þar sem `dim8_bin_summary.csv` inniheldur ekki gpt_5-skrár).
- Allar 11 víddirnar fá per-vídd PNG-myndir og B-súluritið er vistað í `output/figures/`.

**Aðrar skriftur með stöðnuðum tilvísunum** (eftir grep á `human_reference|llm_continuations_preprocessed`; ekki snertir í þessari aðgerð, einungis nefndir til síðari yfirferðar):
- `scripts/integrity_check.py` — `llm_continuations_preprocessed/` (slóðabreyta + CLI-dæmi).
- `scripts/prepare_paired_experiment.py` — `human_reference/` (úttaksslóðir og prentaðar leiðbeiningar).
- `scripts/prepare_unseen_authored_texts.py` — `human_reference/` í úttakshönnun.
- `scripts/generate_claude_continuations.py` — `human_reference/` í aðal- og unseen-slóðabreytum.
- `scripts/dim6_word_length.py`, `scripts/dim8_bin_ratio.py`, `scripts/dim10_lix.py`, `scripts/dim11_mtld.py`, `scripts/dim9_tree_depth.py` — gömlu nöfnin koma einungis fram í CLI-dæmum og doc-strings (ekki í virkri lógík; þessar skriftur taka inn `--text-dir`/`--parsed-dir` og virka óbreytt á nýju slóðunum).

---

## 25. apríl 2026 — Galli í `_measure_with_explicit_paths`: dim8 skilaði alltaf NaN

**Tími:** 0,5 klst.

**Einkenni.** Eftir möppuflutninginn fyrr í dag keyrði `run_milicka.py` til loka án villu, en BÍN-dekkun (vídd 8) var skráð sem NaN (`—` í úttakstöflunni) fyrir öll 342 úrtök í öllum fjórum flokkum (academic/blog/news/unseen). Hinar textavíddirnar (dim6, dim10, dim11) skiluðu gildum eðlilega, svo um dim8-sérstakan galla var að ræða. Cache-skráin `output/dim8_bin_summary.csv` var heil með 462 færslur og rétt nöfn, svo gallinn lá í `run_milicka.py` sjálfu.

**Orsök.** Fallið `_measure_with_explicit_paths` (línur 735–794) — innra hjálparfall sem `measure_ref`, `measure_prompt` og `measure_llm` nota öll — meðhöndlaði aðeins `dim['input'] == 'parsed'` og `dim['input'] == 'raw'`. Fyrir dim8 (sem hefur `'input': 'precomputed_csv'`) féll engin grein í gegn, svo `values[dim_id]` var aldrei sett. Niðurstöðu-dictið innihélt því engan dim8-lykil og niðurstreymis (lína 1034–1035) er notað `v_human.get(dim_id, float('nan'))` sem skilar NaN sjálfgefið. Þannig kom NaN út fyrir dim8 hjá ÖLLUM úrtökum, ekki bara þeim sem vantaði í cache.

Eldra fallið `measure_all_dims` (línur 597–680) hefur rétta meðhöndlun á `precomputed_csv` (lína 665–678) en það fall er ekki notað í aðaleyrslulykkjunni — þar er `_measure_with_explicit_paths` kallað í gegnum `measure_ref`/`measure_prompt`/`measure_llm`. Tvíverknaður á þessari rökfræði (parsed/raw/precomputed_csv-greining á tveim stöðum) gerði það auðvelt að gleyma annarri hliðinni þegar dim8 var flutt í parse-once arkítektúrinn.

**Hvers vegna kom þetta fram núna.** Vídd 8 var flutt í parse-once arkítektúr á sínum tíma (fall `_load_dim8_cache` + `lookup_dim8_value` + `'input': 'precomputed_csv'`-merkingin í `DIMENSIONS`), en `_measure_with_explicit_paths`-hjálparfallið var gleymt í þeirri viðbót. Það fékk ekki að sýna sig í fyrri keyrslum vegna þess að gpt_5-skrár vantaði í cache (sjá færslu 25. apríl, fyrri þátt) og ég tók því fyrir að dim8-NaN væri tengt þeim göllum, ekki kerfisbundnum galla í pípunni. Þegar cache-skráin var endurgerð með öllum líkönum kom í ljós að gallinn náði til allra úrtaka. Eftir á að hyggja hefði ég ekki átt að gera þetta svona til að byrja með heldur leyfa dim8 að keyrast með run_milicka.py í hvert sinn.

**Lagfæring.** Bætti við `precomputed_csv`-grein í `_measure_with_explicit_paths` (línur eftir „raw"-greinina). Hún speglar lógíkina í `measure_all_dims`: velur fyrstu virku slóðina úr `('ref_raw', 'prompt_raw', 'llm_raw')` og sendir hana í `lookup_dim8_value`. `.exists()` er ekki krafist því cache-uppfletting notar einungis skráarheitið.

**Prófunarniðurstöður.**
- `python3 scripts/run_milicka.py --output-csv output/milicka_results_post_dim8fix.csv` keyrði til loka án villu.
- Heildarsamantekt: **342/342 málsýni á allar 11 víddir, engin NaN-tilvik** (áður: dim8 NaN hjá öllum 342). 
- Dim8 skilar nú raunverulegum gildum í öllum flokkum, t.d.: academic 0,9864/0,9720, news 0,9631/0,9684, unseen 0,9551/0,9683 (v̄_hum/v̄_llm).
- CSV-úttak: 3762 raðir (= 342 × 11 víddir), allar 342 dim8-raðir eru með gild `v_human` og `v_model` gildi (engin NaN-strengur).

**Skyldir kóðastaðir til síðari yfirferðar.** Tvíverknaðurinn milli `measure_all_dims` (línur 597–680) og `_measure_with_explicit_paths` (línur 735–794) er hættulegur — hver ný víddartegund (`dim['input']`) þarf að fara á tvo staði. Hægt væri að sameina þetta í eina rökfræðieiningu (annaðhvort með því að nota `measure_all_dims` einnig fyrir ref/prompt/llm-leiðirnar, eða með því að flytja víddargreiningarlykkjuna í sameiginlegt fall sem bæði eru þunnir wrappers utan um). Það er ekki aðferðafræðileg breyting, svo ég skil það eftir; minnispunktur fyrir framtíðar refaktor-tilefni.

**Næstu skref.** Yfirfara hinar skrifturnar í listanum hér að ofan og uppfæra slóðir/doc-strings þegar tilefni er til. Ekki nauðsynlegt áður en `parse_texts.py` er keyrt í fullri lengd, því hver skrifta skilgreinir sínar eigin slóðir.

================================================================================
HEILDARSAMANTEKT / OVERALL SUMMARY
================================================================================
  Líkan                          academic       blog       news     unseen   Meðaltal
  ──────────────────────────── ────────── ────────── ────────── ────────── ──────────
  claude_sonnet46                    2.74       5.06       3.12       4.52       3.86
  deepseek_V32_expert                2.78       4.12       3.34       3.83       3.52
  gemini_3_thinking                  1.94       4.89       2.67       2.63       3.03
  gpt_5                              3.40       4.92       3.63       4.31       4.07
  le_chat_free                       4.11       8.26       4.43       8.24       6.26
  le_chat_thinking                   2.65       4.10       3.20       7.17       4.28

---

## 29. maí 2026 — Sannprófun á niðurstöðum (`scripts/abstract_verification.py`)

**dim5 (3. persónu fornöfn).** Lét Claude Code gera Analysis möppu, hér er útkoman:
Mennsk röð: `unseen > blog > news > academic`. 6/6 líkön ná sömu röð. Á `unseen` (mennskt hámark, +59,32) skýtur yfir í 5/6 (+1% til +34%); gemini_3_thinking eitt skýtur undir (−4,5%).

**dim3 (NP-lengd).** Mennsk röð: `academic > blog > news > unseen`. Aðeins 3/6 ná sömu röð (hin þrjú víxla blog↔news). Á `academic` (+3,34) skýtur þó yfir 6/6 (+3% til +14%).

**dim11 (MTLD).** Mennskt hámark er `blog` (+170,69). 1/6 líkön (le_chat_thinking) topparar þar; 4/6 hafa blog sem LÆGSTA flokk (claude_sonnet46, gemini_3_thinking, gpt_5, le_chat_free). Eftir að le_chat_free er fjarlægt verður inversion-talningin 3/5 (veikari). Líkanið með hæsta heildar-meðal-v_model á dim11 (gemini_3_thinking, +155,18) topparar á `academic` og lægst á `blog` — invertar líka, svo mynstrið er ekki bara gæða-artifact.

**5.2-misræmið leyst.** Þrjár samansafnsaðferðir prófaðar fyrir `mean |b|`:
- A (`mean(|b_d|)` yfir allar raðir): max-skekkja +2,77 vs. birt gildi.
- B (per-cella `mean(|b_d|)`, svo meðaltal yfir 24 cellur): max-skekkja +2,77.
- **C** (per-cella `mean(b_d)` *með formerki*, svo `|·|`, svo meðaltal yfir 24 cellur): max-skekkja 0,0044 — endurgerir öll 11 gildi innan 0,05.

Birta `mean |b|` í kafla 5.2 er því reiknuð á cell-meðaltals-formerkjuðum delta-gildum, ekki á per-sample-absolútum frávikum. Þetta skýrir ~1,5–2× offsetið sem `human_register_spread.py` rakst á.

Útkoma: `analysis/abstract_verification_summary.csv` (86 raðir).