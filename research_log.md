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