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
- Wiki - Þekking af Wikipediu. GPT-4o fer yfir. Hér eru einnig villur, ætli 4o myndi refsa fyrir það að módelið leiðrétti villurnar? - 1900 dæmi
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
- Instruction-tuned módel vs. base módel: base módel frá Anthropic/OpenAI ekki aðgengileg. Milička notaði opin módel (Llama o.fl.) fyrir þann samanburð. 
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
- Siðfræðileg spurning: Milička talar um að mæliprófið sé m.a. fyrir LLM-framleiðendur. En ef við hjálpum módeli að líkja betur eftir mannlegum stíl, erum við þá að hjálpa gervigreind að búa til list án mannlegrar þátttöku (agency)? Þetta var ekki markmið verkefnisins en gæti orðið afleiðing. Þarf að hugsa meira um þetta og hugsanlega ræða í skýrslunni.

**Opnar spurningar:**
- Hvaða málheild ætti að nota sem grunn? RMH, MÍM, eða byggja eitthvað nýtt?
- Hversu stórt LLM-málheild þyrfti ég að búa til? Hversu mörg módel, hversu margir textar per tegund?
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
- 65 módel á stigatöflu Miðeindar — þarf líklega ekki að prófa öll, heldur velja stefnumarkandi úrtak (efstu, miðjuna, opin módel).

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
- Hvaða módel á að prófa? 

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
- Bæði LLM módelin sýna minni subject drop en mannlegir fréttamenn (Le Chat er þó ómarktækt).
- Le Chat hafði hærra hlutfall nafnyrða í nefnifalli (0,3166) en mannlegur texti (0,2778) — útskýrir meira en náttúrulegar fyrirsagnir.
- Le Chat niðurstöður eru ekki áreiðanlegar vegna endurtekningarlúppu — módel sem festist í lykkju framleiðir ekki fjölbreytt úrtak.

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
- Le Chat Thinking (b_d = +0,27) — EINA módelið innan mennskra marka
- Gemini 3 Thinking (b_d = +2,31) — verulegt frávik
- GPT 5 (b_d = +2,71) og Le Chat Fast (b_d = +2,71) — gera engar fyrirsagnir án frumlagsnafnliðar
- Le Chat Fast festist í endurtekningarlúppu — niðurstöður óáreiðanlegar og segja ekkert um getu módelsins í 520 dæmum
- Fallið er ekki fullkomið. Gögnin ekki fullkomin heldur. T.d. rangflokkun vegna erlendra sérnafna (t.d. KPMG merkt 'e' án fallupplýsinga), en ég lét það ekki stoppa proof of concept!

**Hugsanir / túlkun:**
- Formúla Milička virkar á þessu íslenska örprófi. b_d gefur samanburðarhæfan kvarða.
- Hugmyndin um "eitt rétt svar" leysist þannig: mannlega grunnlínan skilgreinir svæðið, SE skilgreinir mörkin, og b_d mælir hversu langt líkanið er frá þeim mörkum.
- Frumlagsnafnliðarleysi er áhugavert stíleinkenni vegna þess að það er næstum einstakt fyrir fréttafyrirsagnir — gerir afmörkun auðveldari.
- Þáttun er veikasti hlekkurinn — Sonnet sem POS-tagger er ekki jafn áreiðanlegur og RMH merking, en fyrir proof of concept dugir það.

**Opnar spurningar:**
- Hvernig bregðast Miðeind við þessari nálgun? Er b_d nógu gott fyrir stigatöfluna?
- Hvaða módel á stigatöflunni á að prófa í lokaverkefninu? (65 módel!)
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
- Ræddum fleiri víddir: boðháttur í uppskriftum (Íslensk tunga) kom upp. Nöfn sem bárust: Lilja Björk Stefánsdóttir og Haukur Þorgeirsson — athuga hvort þau hafi skrifað um mælanleg stíleinkenni.
 
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