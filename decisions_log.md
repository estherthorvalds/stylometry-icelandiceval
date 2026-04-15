# Ákvarðanaskrá / Decisions Log

## Verkefni: stylometry-icelandiceval

Skráðu hér allar ákvarðanir sem þú tekur í verkefninu — stórar og smáar. Markmiðið er að geta rakið af hverju þú valdir eina leið fram yfir aðra.

---

## Sniðmát / Template

```
### [Númer] — [Dagsetning] — [Stutt lýsing á ákvörðun]

**Samhengi:** Hvað var verið að leysa?

**Valkostir sem voru skoðaðir:**
1. [Valkostur A] — [kostir / gallar]
2. [Valkostur B] — [kostir / gallar]

**Ákvörðun:** Hvað varð fyrir valinu?

**Rökstuðningur:** Af hverju?

**Útkoma:** Hvað þýðir þetta fyrir verkefnið?
```

---

## Ákvarðanir / Decisions

### 001 — 13. mars 2026 — Verkefnið er tvíþætt: rannsókn + mælipróf

**Samhengi:** Miðeind lagði til rannsókn auk mæliprófs

**Valkostir sem voru skoðaðir:**
1. Fara beint í að smíða mælipróf — fljótara, en hætta á að taka ákvarðanir sem nýtast ekki
2. Byrja á rannsóknarfasa, síðan smíða mælipróf — tímafrekt, en byggir á þekkingu

**Ákvörðun:** Valkostur 2 — rannsókn fyrst, síðan mælipróf

**Rökstuðningur:** Ráðlagt af Miðeind. Tryggir að skýrsla komi út úr verkefninu. Kemur í veg fyrir að endurtaka mistök annarra.

**Útkoma:** Fyrsti hluti verkefnisins verður bóklegur. Þarf að setja upp gott skráningarkerfi til að halda utan um heimildir.

### 002 — 13. mars 2026 — Repo heitir stylometry-icelandiceval

**Samhengi:** Þurfti nafn sem lýsir verkefninu og passar við nafnavenjur Miðeindar.

**Valkostir sem voru skoðaðir:**
1. stilmaelingar-maeliprof — óþjált, tvítekning á „mæling“, stílmælingar + mælipróf
2. stylometry-benchmark — samkvæmt orðtakanotkun í tíma
3. stylometry-icelandiceval — fylgir nafnavenju Miðeindar (IcelandicEval)

**Ákvörðun:** Valkostur 3 — stylometry-icelandiceval

**Rökstuðningur:** Passar við Miðeind repo (IcelandicEval). Enska gerir repo-ið aðgengilegt alþjóðlega. Íslensku hugtökin (stílmælingar, mælipróf) notuð í lýsingum og skjölun.

**Útkoma:** Repo nafn ákveðið. Íslenska notuð í innri skjölun, enska í README og kóða.


### 003 — 16. mars 2026 — Milicka et al. og Biber til hliðsjónar en nota aðeins eina vídd

**Samhengi:** Skoðaði aðrar sambærilegar rannsóknir sem gerðar hafa verið á örðum tungumálum. Slíkar rannsóknir eru stórar. Milicka kannar getu líkana til að skrifa í ákveðnum stíl og ber saman við texta skrifaðan af manneskju. Þessi rannsókn virðist mikils metin. 

**Valkostir sem voru skoðaðir:**
1. Að nota eitthvað sem líkist Milicku fyrir íslensku — Virðist gott próf, útkoman ætti að gefa mjög góða mynd á getu líkana til að skrifa á tungumálinu sem um ræðir. / Of stórt, rúmast ekki innan verkefnis.
2. Rannsókn Milicku byggir að miklu leyti á eldri rannsókn Bibers. Velja eina vídd sem Biber skrifaði um til að rannsaka - Gera góða rannsókn um þessa einu vídd og svo prófanir. / Rannsóknin verður smærri í sniðum en hún gæti nýst þeim sem útvíkka þetta og vinna með fleiri víddir.

**Ákvörðun:** Bera hugmyndina um eina vídd undir Miðeind og kennara

**Rökstuðningur:** Allar sex víddirnar er of viðamikið verkefni miðað við lokaverkefni í 6 eininga kúrsi

**Útkoma:** Það verður ekki eins nákvæmt og það gæti orðið núna. Hægt er að byggja ofan á þessa rannsókn síðar meir. 


### 004 — 16. mars — Tvöföld mæling: Lesskilningur vs. skrif

**Samhengi:** Það að athuga lesskilning líkans er ekki það sama og athuga hversu vel það getur búið til texta. Eftir að hafa skoðað ARC-prófið langaði mig að kanna séríslenskan lesskilning (ekki getu líkans til að skilja vélþýdda íslensku af ensku). Einnig var fyrirlestur Steinþórs um læsilegan vs. ólæsilegan texta áhugaverð. En það er líka mikilvægt fyrir stílmælingar að skoða hvort líkanið geti búið til texta í ákveðnum stíl.

**Valkostir sem voru skoðaðir:**
1. Velja annaðhvort lesskilning eða skrif — Rúmast mögulega betur innan verkefnisins. / Kannar aðeins hluta af því sem er mikilvægt að skoða.
2. Gera tvíþætt próf sem kannar bæði lesskilning og getu líkans til að búa til texta í ákveðnum stíl. — Mun nákvæmara og á eflaust betur við ef ein vídd Bibers verður fyrir valinu, þá myndi prófið gefa betri mynd á getu líkansins til að vinna með þann stíl. / Stærra og umfangsmeira verkefni og mögulega erfitt að nota sömu leið til að dæma árangur á lesskilningi og skrifum. 

**Ákvörðun:** Þarf að bera undir Miðeind og kennara

**Rökstuðningur:** Þarf reynslumeiri rannsakanda til að meta umfang.

**Útkoma:** Verður rætt á fundi með Miðeind. 

### 005 — 21. mars 2026 — Texti til að prófa

**Samhengi:** Hvernig best sé að skala verkefnið niður fyrir námskeiðið, nota eina textategund

**Valkostir sem voru skoðaðir:**
1. Fréttatextar — Risamálheildin inniheldur mikið af fréttatexta. Mállíkön af ýmsu tagi hafa verið þjálfuð á þessum gögnum og skilja þau betur en aðra texta. Mikilvægt er fyrir umgjörð verkefnis að það sé auðvelt að þátta textann, þá er mikilvægt að í honum séu ekki of margar villur.
2. Bækur úr MÍM - Vel yfirfarinn texti. Ólíklegt að líkönin hafi verið þjálfuð á þessum gögnum vegna leyfis, þá er ekki víst að þau geti hermt það vel eftir honum (sem auðveldar þáttun).
3. Vísindavefur - Er yfirlesinn og hefur ákveðinn stíl.
4. Wikipedia - Hefur ákveðinn stíl sem hefur einnig verið rannsakaður á öðrum tungumálum. 

**Ákvörðun:** Hvað varð fyrir valinu?
1. RÚV — Fyrirlokaverkefni, nota RÚV texta. 
2. Huni.is - Fyrir heimaverkefni 4 - gera örpróf á fyrirsögnum af Huni.is. 

**Rökstuðningur:** Á RÚV er meira lagt upp úr því að fara eftir þeim málfarsreglum sem mállíkönin læra. Ef þau eiga auðveldara með að herma eftir því verður auðveldara að þátta textann þeirra rétt. 

**Útkoma:** Mun spyrja Miðeind hvort þau samþykki ákvörðunina. Geri örprófið á Húnahorninu fyrir litla heimaverkefnið og nota sem proof of concept. 


### 006 — 24. mars 2026 — Tvær mögulegar leiðir í verkefninu
 
**Samhengi:** Miðeind getur hvorki veitt API-aðgang né þáttara. Kostnaður ef ég borga sjálf er ~5.000 kr en þáttun er óleyst.
 
**Valkostir:**
1. Leið A (praktísk): Fá API (í gegnum HÍ eða sjálf), finna góðan þáttara, keyra marktækar tilraunir
2. Leið B (fræðileg): Aðlaga Milička fræðilega, skilgreina víddir, nota fríu chat-viðmót, skrifa skýrslu
 
**Ákvörðun:** Reyna leið A fyrst. Ef þáttari og API finnast ekki, snúa sér að leið B.
 
**Rökstuðningur:** Leið A gefur sterkari niðurstöður en er háð ytri aðstæðum. Leið B er sjálfstæð og framkvæmanleg hvernig sem fer. Ekki eyða peningum fyrr en þáttaravandamálið er leyst.
 
**Útkoma:** Næstu vikur fara í að kanna forsendur (API, þáttari). Deadline á ákvörðun: áður en lokaverkefnið byrjar fyrir alvöru.


### 007 — 26. mars 2026 — IceConParse valinn sem þáttari

**Samhengi:** Þurfti áreiðanlegan þáttara. Anton nefndi nemandaþáttara sem virkaði vel. Fann IceConParse á GitHub (Ingunn Jóhanna Kristjánsdóttir, 2024).

**Valkostir:**
1. Halda áfram með Sonnet POS-merkingar — virkar en óáreiðanlegt, dýrt fyrir mikið af gögnum
2. ABLTagger — þjálfaður á IFD, POS-merking eingöngu
3. IceConParse — liðgerðarþáttari, 90,38% F-mæling, Stanza-pípa, skilar NP-SBJ merkingum
4. Þáttari Þórunnar (Berkeley) — 84,74% F-mæling, dependency vesen

**Ákvörðun:** IceConParse.

**Rökstuðningur:** Hæsta F-mæling (90,38%), liðgerðartré gefa NP-SBJ beint (einfaldari greining), Stanza-pípa auðveld í uppsetningu, og opnar á fleiri víddir (trédýpt, nafnliðalengd, aukasetningar). Sonnet POS-merking er óþörf með liðgerðarþáttara.

**Afleiðingar:** Búa til nýja útgáfu af skriftunni (milicka_headlines_ingunnparser.py). Gögn færð úr JSON í hreinar textaskrár. Mannleg grunnlína staðfest (18,5% varð 18,4%). Niðurstöður líkana breyttust meira.


### 008 — 29. mars 2026 — Stigaformúla búin til (0-100 kvarði)

**Samhengi:** b_d gildi Milička eru ótakmörkuð og ekki auðskiljanleg á stigatöflu.

**Valkostir:**
1. Nota b_d — sama og Milička en erfitt að túlka á stigatöflu
2. Búa til 0-100 kvarða — stigatöfluvænt, auðskilið

**Ákvörðun:** Valkostur 2. Formúla: stig = 100 × (1 - |v_human - v_model| / v_human)

**Rökstuðningur:** 0 þýðir ekkert af stíleinkenninu, 100 þýðir fullkomið samræmi við mannlega grunnlínu. Einfalt, gagnsætt og virkar vel þar sem v_human > 0.

**Afleiðingar:** Bætt við sem style_score() fall í skriftuna. b_d og stig eru bæði birt í niðurstöðum.


### 009 — 29. mars 2026 — Gögn færð úr JSON í textaskrár

**Samhengi:** Eldri útgáfaaf þáttara (Sonnet) notaði JSON skrár með POS-merkingum. Nýi þáttarinn þáttar hreinan texta sjálfur.

**Ákvörðun:** Fyrirsagnir vistaðar sem .txt skrár (ein fyrirsögn í línu) í stað JSON. (Skrifta fjarlægir aukalínur).

**Rökstuðningur:** IceConParse tekur inn hreinan texta og skilar liðgerðartrjám. POS-merktur JSON er óþarfur. Textaskrár eru einfaldari, minni, og auðveldari að vinna með.

**Afleiðingar:** Eldri JSON skrár færðar í archive/.


### 010 — 31. mars 2026 — Fyrirvari um RMH-gögn í greininni
**Samhengi:** RMH-textar (fréttir, blogg, fræðitextar) hafa líklega verið í þjálfunargögnum risamállíkana. Yang et al. (2023) sýna að módel geta yfirpassað mælipróf ef þjálfunargögn skarast við prófgögn, jafnvel eftir umritun. Eriksson et al. (2025) kortleggja data contamination sem eitt af helstu vandamálum mæliprófa.

**Valkostir:**
1. Finna texta sem módelin hafa ekki séð (t.d. nýir textar eftir þjálfunardagsetningu módela)
2. Nota RMH en setja skýran fyrirvara í greininni

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Þetta er skalað proof of concept, ekki lokaúttekt. Að finna sannanlega óséða texta er of tímafrekt á þessu stigi. Fyrirvari í greininni er heiðarlegt og fagmannlegt. Mælt verður með í greininni að framtíðarrannsóknir noti texta sem módelin hafa sannanlega ekki séð.

**Afleiðingar:** Bæta kafla í greinina um þennan fyrirvara. Vísa í Yang et al. og Eriksson et al.


### 011 — 31. mars 2026 — Fyrirvari um þáttarann (analogy við vélþýðingargagnrýni)
**Samhengi:** Who Benchmarks (Ingimundarson et al., 2026) gerir vel grein fyrir göllum þess að nota vélþýðingar í mæliprófum. Sama röksemd á við vélþáttun: ef IceConParse þáttar rangt, mælist stíleinkennið rangt, og prófið verður ekki marktækt.

**Ákvörðun:** Setja sama fyrirvara við þáttarann og Who Benchmarks setur við vélþýðingar. Ekki nota textategundir sem þáttarinn á erfitt með í þessari tilraun. Hægt verður að framkvæma víðtakara próf síðar þegar þáttarar verða betri.

**Rökstuðningur:** Vandamálið er samhliða. Í þeirra tilfelli: slæm þýðing → rangt próf. Í mínu tilfelli: slæm þáttun → rangt próf. IceConParse er 90.38% F-score, sem er gott en ekki fullkomið. Sérstaklega þarf að athuga hvort villur í þáttun skekkja niðurstöður kerfisbundið.

**Afleiðingar:** Bæta kafla í greinina. Prófunarskrifta (validation harness) á að hjálpa til við að meta þetta.


### 012 - [OPIN] — Frumlagsnafnliðarfallið — enn óákveðið

**Samhengi:** Á frumlagsnafnliðarfallið (NP-SBJ case marking) heima í prufunum? Spurning hvort það sé viðeigandi vídd fyrir aðra texta en fréttafyrirsagnir.

**Staða:** Fer enn fram og til baka. Þarf frekari greiningu á hvort IceConParse geti metið þetta áreiðanlega og hvort það greinir á milli textategunda.

**Næstu skref:** Keyra prufur á nokkrum textadæmum og ákveða.

Nýjar færslur fyrir decisions_log.md:

---

### 013 — 1. apríl 2026 — Punkti bætt við eftir fyrirsögnum í forvinnslunni

**Samhengi:** Fyrirsagnir og undirfyrirsagnir í RMH-textum hafa ekki setningalokapunkt. Þegar textinn er dreginn út renna fyrirsagnir og byrjun næstu málsgreinar saman og þáttarinn (IceConParse) getur ekki greint setningamörk. 

**Valkostir:**
1. Láta textann vera eins og hann er — þáttarinn ruglar saman fyrirsögnum og meginmáli
2. Bæta punkti og línuskilum eftir fyrirsögnum sem enda ekki á . ? !

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Þetta er forvinnsluákvörðun til að tryggja rétta þáttun. Það hefur ekki áhrif á formúlurnar svo framarlega sem sama meðferð er beitt á mannlegan texta og LLM-texta. Skjalfest í aðferðafræðikafla greinarinnar.

**Afleiðingar:** `extract_samples.py` bætir punkti eftir fyrirsögnum sjálfkrafa.

---

### 014 — 1. apríl 2026 — Undirfyrirsagnir endurteknar í meginmáli

**Samhengi:** Undirfyrirsagnir í fréttatextum (sem yfirleitt er ætlað að vera smá preview áður en smellt er á fréttina) eru endurteknar í safninu. Þetta er þó ekki partur af stíl heldur útfærsla fyrir vefsíður. 

**Valkostir:**
1. Láta textann vera eins og hann er — fyrsta málsgrein (yfirleitt) verður endurtekin tvisvar.
2. Fjarlægja fyrstu málsgrein ef hún er endurtekin í meginmáli. 

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Þar sem þetta er í raun ekki mennskur stíll (að endurtaka fyrstu málsgreinina) heldur skrifað fyrir vefsíður sem ætlast til að fá smell til að lesa megi alla fréttina, á þetta ekki heima í stílgreiningu. 

**Afleiðingar:** `extract_samples.py` fjarlægir endurteknar setningar. 

---

### 016 — 3. apríl 2026 — Milička-pörunaraðferð valin

**Samhengi:** Tvær leiðir til að afla LLM-texta: (a) óháð prompt (t.d. „skrifaðu frétt um...") eða (b) pörun eftir Milička (klippa mannlegan texta í tvennt, módel heldur áfram).

**Ákvörðun:** Valkostur (b) — Milička-pörun.

**Rökstuðningur:** Pörunaraðferðin er beint sambærileg við Milička et al. (2025) og gefur sterkari rök fyrir endurtekningu rannsóknarinnar í stærri skala (lokaverkefni). Módellið sér stílinn í fyrri helmingnum og reynir að halda honum — þetta er nákvæmari prófun á stílgetu og betra til að kanna hvort tilefni sé til að endurgera tilraun Milička í heild sinni fyrir íslenskt mál. 

**Afleiðingar:** `prepare_paired_experiment.py` búið til. 15 sýni × 3 flokkar = 45 pör. Promptað á íslensku.

---

### 017 — 3. apríl 2026 — Sama forvinnsla á LLM-úttaki og mannlegum texta

**Samhengi:** Gemini (og stundum Le Chat) bætti við markdown-snyrtingu (fyrirsagnir, undirfyrirsagnir, feitletur) í framhaldi sínu. Þetta er stíleinkenni útaf fyrir sig en ef mannlegi textinn er forunninn (fyrirsagnir fá punkt, XML fjarlægt) og LLM-textinn ekki, þá erum við að mæla „markdown vs. texti“ frekar en raunverulegan stílmun.

**Valkostir:**
1. Halda LLM-formatting — þá er líkani refsað fyrir óviðeigandi formatting
2. Fjarlægja markdown úr LLM-úttaki og beita sömu forvinnslu — mæla stíl, ekki format

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Formúlurnar mæla málfræðileg stíleinkenni (subordination ratio, NP-lengd, frumlagsnafnliðarleysi), ekki útlit. Markdown-merki myndu trufla þáttun og skekkja niðurstöður. Sama forvinnsla tryggir sanngjarnan samanburð. Þetta er skjalfest í aðferðafræðikafla.

**Afleiðingar:** Búa til forvinnsluforrit sem keyrir á LLM-úttaki áður en það fer í þáttun.


### 018 — 6. apríl 2026 — Meðhöndlun á misheppnuðum/endurteknum LLM-úttökum

**Samhengi:** Le Chat Fast lenti í endurtekningarlykkjum (loops) á nokkrum blogg-promptum. Tvær gerðir vandamála komu fram: (a) tæknilegar lykkjur þar sem sömu málsgreinar endurtakast orðrétt, og (b) kerfisbundin endurtekning þar sem sama sniðmát er notað aftur og aftur með nýju viðfangsefni. Gerð (b) er stílbrestur frekar en tæknilegt vandamál. Sömuleiðis þurfti stundum að stöðva líkanið því það hélt áfram að framkvæma lykkjurnar löngu eftir að 2000 orðum var náð.

**Valkostir:**
1. Eyða öllum misheppnuðum skrám
2. Geyma allt í sömu möppu og láta skrifturnar reyna að vinna úr þeim
3. Geyma misheppnuð dæmi í sérstakri möppu, útiloka úr tölfræðilegri greiningu, skjalfesta í grein

**Ákvörðun:** Valkostur 3.

**Rökstuðningur:** Lykkjurnar eru niðurstaða, ekki bilun í rannsókninni. Þær sýna að Le Chat Fast á erfiðara með að halda stíl í óformlegri/ljóðrænni blogg-texta en í fræðitexta — sem er stílmælingarniðurstaða útaf fyrir sig. Þessi dæmi þarf að vista og fjalla um í greininni.

**Útfærsla:**
- Misheppnuð dæmi geymd í `data/experiment/llm_continuations/le_chat_fast/excluded/`
- Eitt dæmi per villutegund er nóg — ekki þarf að geyma mörg eins
- Skráð í rannsóknardagbók: hvaða prompt-ID misheppnaðist, hve oft var reynt, tegund vandamáls
- Greinin mun segja: „Le Chat Fast framleiddi endurtekningarlykkjur í X af 15 blogg-promptum. Þessi sýni voru útilokuð úr tölfræðilegri greiningu en skjalfest sem vísbending um óstöðugleika í málsniði.“
- Sniðmátsendurtekning (gerð b, t.d. blog_001) er NOTUÐ í greiningu — það er ekki tæknileg lykkja heldur „stílbrestur“ sem á heima í greiningunni.

**Afleiðingar:** Le Chat Fast mun hafa færri blogg-sýni en önnur líkön. Milička-formúlurnar ráða við ójafna fjölda sýna, það mun ekki virka eins vel en þetta er heiðarlega skjalfest. Ef rannsóknin yrði endurtekin í stærra samhengi er hægt að gera ráð fyrir þessum lykkjum og taka ákvarðanir í samræmi við það.


### 019 — 13. apríl 2026 — Fjarlægja endurtekningar úr prompti í forvinnslu gervigreindartexta

**Samhengi:** Við gagnasöfnun komu fram tvær gerðir af endurtekningum: (1) líkönin virtust misskilja verkefnið og endurtóku hluta af promptinum í stað þess að halda áfram textanum, og (2) líkönin fóru í einskonar glitch-ham og endurtóku búta á óstjórnlegan hátt. Í báðum tilvikum er um að ræða villu í keyrslu, ekki stíleinkenni, og með því að halda þessum textabútum yrðu stylometric mælingar skakkar — þá yrði hluti af prompti mældur sem LLM-framleiðsla. Á að halda því inni eða fjarlægja til að mæla getu líkansins til að skrifa stíl?

**Valkostir sem voru skoðaðir:**
1. Halda endurtekningum inni — Vera trú gögnunum, nota alfarið það sem líkönin gerðu. En um er að ræða endurtekningu á mennskum texta sem er ranglega mældur sem gervigreindartexti.
2. Fjarlægja endurtekninar — Er að eiga mikið við upprunalegu gögnin. En mælingin snýst þá fyrst og fremst um getu líkana til að búa til stíl.

**Ákvörðun:** Fjarlægja endurtækningar.

**Rökstuðningur:** Mikilvægast að kanna getu líkana til að búa til stíl en ekki kópípeista það sem sent var á þau. Vandamálið var tæknilegs eðlis, sem mikilvægt er að greina frá en það er ekki tengt þessari mælingu.

**Útkoma:** Svo virðist sem sum líkönin lendi í tæknilegum örðugleikum þegar kemur að íslensku. Það þarf að gera grein fyrir því í greininni. Tekin var ákvörðun um að fjarlægja endurtekningar og mæla það sem hægt var að mæla. 



### 020 — 14. apríl 2026 — Fjórði textaflokkur: óbirtur skáldskapur

**Samhengi:** RMH-textar hafa líklega verið í þjálfunargögnum risamállíkana (sjá ákvörðun 010 og Yang et al., 2023). Þetta er skjalfestur fyrirvari en erfitt að meta hversu mikil áhrif mengunin hefur á niðurstöður. Til að prófa þetta beint þarf texta sem sannanlega er óséður af öllum líkönum.

**Valkostir sem voru skoðaðir:**
1. Halda áfram með þrjá flokka og setja fyrirvara — Einfaldara, en mengunarvandamálið helst óleyst.
2. Bæta við fjórða flokki úr óbirtum skáldskap höfundar — Leysir mengunarvandamálið beint. Hægt að bera saman: skora líkönin öðruvísi á óséðum gögnum en RMH-gögnum? Gallinn er að sumir textarnir eru óyfirlesnir svo þáttarinn gæti lent í vandræðum.

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** 15 sýni (~2.000 orð) tiltæk án viðbótarvinnu. Pípan er þegar tilbúin — þetta er eins og að bæta við líkani, ekki endurbyggja neitt. Niðurstöðurnar bæta kafla í umræðu greinarinnar þar sem mengunarveldið er rætt. Ef niðurstöður á óséðum gögnum eru verulega frábrugðnar RMH-niðurstöðum eru það áhugaverðar rannsóknarniðurstöður í sjálfu sér.

**Fyrirvari:** Textarnir eru eftir einn höfund og geta ekki talist fulltrúi skáldsagnatefnis á íslensku. Verður tekið fram í greininni.

**Afleiðingar:** Bæta „unseen authored text“ sem fjórða flokki. 15 sýni × 1 flokkur = 15 ný pör. Keyra í gegnum sömu pípu.


---

### 021 — 14. apríl 2026 — Hitastigsbreytingar

**Samhengi:** Fyrstu fjögur líkönin voru keyrð handvirkt í gegnum spjallviðmót. Það þýðir að ekki er hægt að endurtaka með breyttu hitastigi. Einnig er þetta takmarkaður fjölda líkana. Niðurstöðurnar eru nægar fyrir námskeiðsverkefni en út af sumarverkefninu er betra að fá niðurstöður sem gefa betri vísbendingu um hvað er að virka.

**Valkostir sem voru skoðaðir:**
1. Nota bara líkön með spjallviðmóti — Ókeypis en ekki hægt að endurtaka. Takmarkað við þau líkön sem hafa opið spjallviðmót. Tímafrekt.
2. Kaupa API-aðgang — Kostnaður en gefur endurtakanleika, hitastigstilraunir og fleiri líkön.

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Þrennt styrkir greinina verulega: (1) endurtakanleiki (API-köll með föstum breytum), (2) hitastigstilraunir (Milička fann áhugaverðustu niðurstöður sínar þar), (3) fleiri líkön (GPT - mögulega fleiri ef tími gefst?) þá fer greinin frá því að fjalla um „nokkur dæmi“ yfir í „yfirlit“.

**Afleiðingar:** Bæta við allavega einu GPT líkani við mismunandi hitastig. Aðferðafræðikafli greinarinnar mun lýsa tveimur lotum gagnasöfnunar: (1) handvirkt í spjallviðmóti, (2) API með stýrðum breytum.

