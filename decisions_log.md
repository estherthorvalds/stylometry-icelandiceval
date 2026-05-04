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


### 003 — 16. mars 2026 — Milička et al. og Biber til hliðsjónar en nota aðeins eina vídd

**Samhengi:** Skoðaði aðrar sambærilegar rannsóknir sem gerðar hafa verið á örðum tungumálum. Slíkar rannsóknir eru stórar. Milička kannar getu líkana til að skrifa í ákveðnum stíl og ber saman við texta skrifaðan af manneskju. Þessi rannsókn virðist mikils metin. 

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

**Afleiðingar:** Búa til nýja útgáfu af skriftunni (Milička_headlines_ingunnparser.py). Gögn færð úr JSON í hreinar textaskrár. Mannleg grunnlína staðfest (18,5% varð 18,4%). Niðurstöður líkana breyttust meira.


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

**Rökstuðningur:** Þetta er ákvörðun fyrir forvinnsluna - til að tryggja rétta þáttun. Það hefur ekki áhrif á formúlurnar svo framarlega sem sömu aðferð er beitt á mennskan texta og LLM-texta. Fjallað um í aðferðafræðikafla greinarinnar.

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



### 021 — 14. apríl 2026 — Hitastigsbreytingar

**Samhengi:** Fyrstu fjögur líkönin voru keyrð handvirkt í gegnum spjallviðmót. Það þýðir að ekki er hægt að endurtaka með breyttu hitastigi. Einnig er þetta takmarkaður fjölda líkana. Niðurstöðurnar eru nægar fyrir námskeiðsverkefni en út af sumarverkefninu er betra að fá niðurstöður sem gefa betri vísbendingu um hvað er að virka.

**Valkostir sem voru skoðaðir:**
1. Nota bara líkön með spjallviðmóti — Ókeypis en ekki hægt að endurtaka. Takmarkað við þau líkön sem hafa opið spjallviðmót. Tímafrekt.
2. Kaupa API-aðgang — Kostnaður en gefur endurtakanleika, hitastigstilraunir og fleiri líkön.

**Ákvörðun:** Valkostur 2.

**Rökstuðningur:** Þrennt styrkir greinina verulega: (1) endurtakanleiki (API-köll með föstum breytum), (2) hitastigstilraunir (Milička fann áhugaverðustu niðurstöður sínar þar), (3) fleiri líkön (GPT - mögulega fleiri ef tími gefst?) þá fer greinin frá því að fjalla um „nokkur dæmi“ yfir í „yfirlit“.

**Afleiðingar:** Bæta við allavega einu GPT líkani við mismunandi hitastig. Aðferðafræðikafli greinarinnar mun lýsa tveimur lotum gagnasöfnunar: (1) handvirkt í spjallviðmóti, (2) API með stýrðum breytum.



### 022 — 18. apríl 2026 — Áttunda vídd: BÍN-hlutfall með `islenska`-safninu

**Samhengi:** Vil bæta við vídd sem mælir hlutfall orða sem eru í BÍN (Beygingarlýsingu íslensks nútímamáls). Grunnhugsun: Oft er það huti af stílnum að nota óhefðbundin orð (nota slettur, óformlegheit, óalgeng íorð, stafsetningarvillur o.s.frv.). En ekki síður: LLM-texti á íslensku er oft enskuskotinn, hefur að geyma uppskálduð orð eða með stafsetningar- og málfarsvillum. Þessi mæling myndi ná að greina þetta sem hinar sjö víddirnar (málfræðilegar dreifingar) ná ekki.

**Valkostir sem voru skoðaðir:**
1. Greynir / GreynirCorrect — getur markað stafsetningarvillur. Flóknara, en kannski áhugavert fyrir framtíðarvídd um „villur vs. sköpun“.
2. Nota ABLTagger/Nefnir fyrir nafnorða-flokkun — góður fyrir sérnöfn en engin uppflettingsgögn fyrir samheiti/lemma.
3. Keyra BÍN-uppflettingu beint gegn XML-dumpi af BÍN — hámarks-stjórn en mikil innviðaskrif (parser, lemmatizer, samsetningargreining frá grunni).
4. Nota `islenska`-pakka Miðeindar (BinPackage) — vel við haldið, gefur `bmynd`, `ofl`, `hluti`, samsetningagreiningu í einni uppflettingu. (Kennari benti á þennan kost).

**Ákvörðun:** Valkostur 4 — `islenska`-pakkinn.

**Rökstuðningur:** Miðeind er einnig ráðgjafi verkefnisins, pakkanum er viðhaldið (er það ekki annars?) og uppfletting er einföld (`Bin.lookup(word)` → `(word, [BinEntry, ...])`). Einnig er samsetningargreining innbyggð: BÍN skilar `bmynd` með bandstrikum milli samsetningaleiða (`heilbrigðis-þjónustukerfi`) sem gerir auðvelt að flokka samsett orð (bmynd hefur fleiri bandstrik en inntak).

**Hönnun:**
- Fjórir flokkar: `exact` / `compound` / `proper_name` / `oov`.
- Sérnöfn flokkast sérstaklega (ekki `exact`) með `hluti ∈ {ism, föð, móð, örn, göt, fyr, erm, bibl, lönd, þor}`.
- Compound-greining: `bmynd.count('-') > used_form.count('-')`.
- Aðal-v fyrir Milička: `in_bin_ratio = (exact + compound + proper_name) / total`.
- Tvö CSV í úttaki: `dim8_bin_summary.csv` (ein lína per skrá) og `dim8_bin_detail.csv` (ein lína per tóka með `oov_guess`-leiðbeiningum).

**Reikna-einu-sinni (parse-once caching):** `dim8_bin_ratio.py` keyrir Bin() beint og skrifar CSV-niðurstöður. `run_Milička.py` les CSV-ið og kallar ALDREI á `Bin()`. Þetta heldur `islenska` sem valkvæðu hæði — það þarf ekki að installa pakkanum til að geta keyrt `run_Milička` ef csv-skjölin eru tilbúin (annars krefst það `python3-dev` og `libffi-dev` á Linux). 

SKRIFAÐ SEINNA: Þetta var slæm hugmynd, hefði ekki átt að gera þetta.

**Sannprófun:** Keyrt á 9 mennskum skrám (3 per textategund). Allar > 90% in_bin_ratio (lægst: academic_ref_004 91,68%). Fréttir hæstar í proper_name_ratio (news_001 10,62%) eins og búist var við. Fræði meðal-samsetningar (2,44%).

**Útkoma:** Átta víddir í heildina. Víkkar út `run_Milička.py` með nýrri `input='precomputed_csv'` stöðu. Fyrirhugað að ræða BÍN-hlutfall sérstaklega í greininni vegna þess að mælingin nær LLM-galla sem hinar víddirnar ná ekki (orðaforðaval er annars konar galli en málfræðileg dreifing).


### 023 — 20. apríl 2026 — Tíunda víddin: LIX-læsileikaskor sem hliðstæða við dim6

**Samhengi:** Fyrirlestur Steinþórs um læsileikamælingar vakti spurningu um hvort klassískar læsileikaformúlur hafi meira greinandi afl á milli textategunda en ein orðalengdarmæling. Dim6 mælir meðalorðalengd eina og sér; LIX bætir setningalengd við sömu formúlu. Spurningin er hvort dim6 og dim10 séu nógu ólíkar til að halda báðum, eða hvort önnur dekki hlutverk hinnar.

**Valkostir sem voru skoðaðir:**
1. Halda því við átta víddir (dim1–dim8). Einfaldara, ekki fleiri háð. En missi af samanburði orðalengd vs. orðalengd+setningalengd sem getur nýst við víddarval í sumarverkefninu.
2. Bæta við LIX sem dim10. Tvöfaldar textavíddir (dim6, dim10) — sömu orð, ólíkar formúlur. Gefur tækifæri á beinum samanburði í greiningarkaflanum: ef fylgni dim6↔dim10 er mjög há, þá dugar önnur; annars gefa báðar upplýsingar. Gallinn er að LIX er kvörðuð fyrir sænsku og þröskuldarnir eiga ekki strangt við íslensku.
3. Smíða íslenskt læsileikamat frá grunni. Betra fræðilega en alltof tímafrekt fyrir námskeiðsverkefni.

**Ákvörðun:** Valkostur 2 — LIX sem dim10, kvörðunarfyrirvari skjalfestur.

**Rökstuðningur:**
- LIX-formúlan er mjög einföld (orð/setn + pct_long_words) og endurnýtir tókunarreglur dim6 beint. Lítill aukakostnaður, gagnleg samanburðarmæling.
- Kvörðunarvandi LIX fyrir íslensku er raunverulegur en ekki úrslitaatriði í stílmæliprófinu: Milička-formúlan ber saman v_human og v_model á SAMA kvarða. SE(I_d) er reiknað úr mennskum gögnum. Hrávirðin þurfa ekki að vera „rétt kvörðuð“, þau þurfa bara að vera STÖÐUG. Þröskuldarnir eru birtir aðeins til gagnlegra vísbendinga í skrárúttaki — ekki notaðir í Milička-formúluna sjálfa.
- Dim10 er tilraunakennd vídd: hún verður með í proof-of-concept en ákveðið verður fyrir sumarverkefnið hvort hún, dim6, báðar eða hvorug haldi áfram.

**Hönnun:**
- Formúla: LIX = (orð/setningar) + (löng_orð/orð × 100), „löng orð“ = lengd > 6 stafir (LIX-staðall, ÖÐRUVÍSI en dim6 sem notar ≥ 8).
- Tókunarreglur endurnýttar úr dim6: `PUNCT_TO_STRIP` og `HAS_LETTER` fluttar inn beint. Orðatalningar eru IDENTICAL á milli dim6 og dim10 — staðfest á þremur sýnum (academic_ref_001, news_ref_001, blog_ref_001), allar ná sömu tölu gildra orða.
- Setningaskilming: `tokenizer`-pakki Miðeindar (`split_into_sentences`). Naive regex á `.!?` brotnar á íslenskum skammstöfunum (þ.e., o.s.frv., t.d., m.a.) og tugabrotum — tokenizer-pakkinn kann þessar reglur.
- Aðal-v fyrir Milička: `lix_score`. Sub-measures í CSV: `total_words`, `total_sentences`, `mean_sentence_length`, `pct_long_words`.
- Þröskuldar í console-úttaki: Swedish-calibrated (< 30, 30–40, 40–50, 50–60, > 60), merktir sem GRÓFIR vísar fyrir íslensku.

**Háðni:** `tokenizer>=3.4`. Hreint Python, engin C-hæði — engin sérstök uppsetning á Linux (ólíkt `islenska`). Bætt við `requirements.txt`.

**Sannprófun:** Keyrt á öllum 45 mannlegum viðmiðsskrám. Meðaltal per textategund:
- academic (15 skrár): LIX ≈ 49.3 (væntanleg: 50+; nálægt)
- news (15 skrár): LIX ≈ 42.5 (væntanleg: 40–50 ✓)
- blog (15 skrár): LIX ≈ 41.9 (væntanleg: 30–40; aðeins hærra)

Röð eins og búist var við: academic > news ≈ blog. Academic er jaðarlega undir 50-þröskuldi, blogg eru jaðarlega yfir 40 — sem staðfestir að sænskir þröskuldar skila aðeins grófri nálgun fyrir íslensku (íslensk samsetning hækkar LIX kerfisbundið).

**Afleiðingar:** Tíu víddir í heildina (dim9 sleppt, dim10 tekin með til að halda LIX-merkingunni). `run_Milička.py` víkkað: `measure_word_length_stripped` endurnefnt og alhæft sem `measure_raw_stripped(dim, path)` svo textavíddir geti allar deilt prompt-strippunarlógíkinni. Greinin mun innihalda stutta umfjöllun um dim6↔dim10-samanburð og hvers vegna báðar eru haldnar í proof-of-concept.


### 024 — 20. apríl 2026 — Níunda víddin: trédýpt (setningarþyngd úr IcePaHC-trjám)

**Samhengi:** Fyrirlestur Steinþórs Steingrímssonar um „setningarþyngd“ á UD-þáttuðum gögnum vakti upp spurningu um hvort hliðstæð mæling — dýpt liðgerðartrjáa — væri sjálfstæð stílvídd í okkar mæliprófi. Dim2 (aukasetningahlutfall) mælir TÍÐNI undirskipunar (IP-SUB / IP-MAT) en segir ekkert um DÝPT hreiðrunar: tvær setningar geta haft sama aukasetningahlutfall en aðra með djúpri hreiðrun [IP-MAT [IP-SUB [IP-SUB [IP-SUB ...]]]] og hina með sundruðum, óbundnum IP-SUB. Þetta minnir á Biber-MDA „informational production“ víddina.

**Valkostir sem voru skoðaðir:**
1. Hætta við tíu víddir. Einfaldara, minna um hæði. En missir af beinni hliðstæðu við Steinþór og viðurkennda vídd í hefðbundnum MDA-rannsóknum.
2. Bæta við dim9 með einni mælingu (mean_tree_depth). Hrein og einföld, en missir af nýju upplýsingunum sem hreiðrun IP-SUB gefur.
3. Bæta við dim9 sem vegur saman þrjár undirmælingar (meðaldýpt, prósentu djúpra trjáa, IP-SUB hreiðrun). Veitir bæði aðalgildi og auðlesna undirmælikvarða sem má bera saman við dim2.

**Ákvörðun:** Valkostur 3 — dim9 með þremur undirmælingum, aðal-v er `mean_tree_depth`.

**Rökstuðningur:**
- Þrjár undirmælingar gefa skýra mynd á mismunandi hliðum flækjustigs: heildardýpt, hversu oft setningar eru djúpar (≥ 3), og hversu djúpt IP-SUB hreiðrast (þá saman við dim2 sem mælir TÍÐNI IP-SUB).
- Bracket-talningarlausn er einföld, hröð og ekki háð neinu öðru (standard library eingöngu).
- Þröskuldur ≥ 3 er METHODOLOGICAL PARALLEL við Steinþór (UD) — ekki kvarðaður fyrir IcePaHC. Liðgerðartré eru kerfisbundið dýpri en UD-tré (POS-umbúðir auka dýpt um 1–2), svo pct_complex lendir í ~99% fyrir alla flokka í íslensku. Þetta er viðurkennt í doc-strings, console-úttaki og ARCHITECTURE.md. Aðal-differentiation-signalið er `mean_tree_depth`; `pct_complex_trees` er haldið vegna hliðstæðu við Steinþór en dugar ekki eitt og sér.

**Hönnun:**
- `tree_depth(tree)`: bracket-counting, `max_paren_nesting - 1` svo ROOT = 0, undir-ROOT = 1.
- `collect_ip_sub_nesting(tree)`: label-stack ganga; fyrir hvert IP-SUB, fjöldi IP-SUB forfeðra í stack. Meðalgildi yfir allar IP-SUB hnúta, 0 ef engin IP-SUB í skrá.
- CSV-skil: `total_sentences, mean_tree_depth, std_tree_depth, pct_complex_trees, total_ip_sub, mean_ip_sub_nesting`.
- Aðal-v fyrir Milička: `mean_tree_depth`.

**Hæði:** Endurnýtir `mean`/`stdev` úr dim6_word_length til að halda standard-library-eingöngu.

**Sannprófun:** Keyrt á öllum 45 mannlegum viðmiðsskrám (15 per flokki). Meðaltal per textategund:
- academic: mean_tree_depth = 8.35, range [6.27, 10.32], pct_complex = 99.4%, mean_ip_sub_nesting = 0.51
- news: mean_tree_depth = 7.72, range [5.90, 9.48], pct_complex = 99.2%, mean_ip_sub_nesting = 0.45
- blog: mean_tree_depth = 7.57, range [5.92, 9.17], pct_complex = 99.7%, mean_ip_sub_nesting = 0.44

Röð eins og búist var við: academic > news > blog. Öll meðaltöl > 2.0 (sanity check). `mean_ip_sub_nesting` fylgir sömu röð en er ekki stór munur — bendir til að íslensk aukasetningahreiðrun sé grynnri en í fræðilegri ensku, sem meikar sens þar sem hægt er að búa til löng orð í íslensku þar sem enskan verður að liði af orðum.

**Afleiðingar:** Tíu víddir í heildina (dim1–dim10 öll notuð). `run_Milička.py` DIMENSIONS skrá útvíkkuð með dim9 færslu (`input='parsed'`, `key='mean_tree_depth'`). Greining í greininni: samanburður dim2 (tíðni IP-SUB) vs. dim9 (dýpt IP-SUB hreiðrunar) gefur tvö sjálfstæð undirskipunarmerki.


### 025 — 20. apríl 2026 — Aðgreining á z-stafsetningu í dim8 (archaic_icelandic vs. foreign)

**Samhengi:** Upprunaleg dim8-útfærsla (sjá ákvörðun 022) notaði einfalt heuristic fyrir OOV-flokkun: tóki sem innihélt c, q, w eða z var merktur „foreign“. Það er rangt fyrir z. z var staðlað íslenskt ritmál fram að réttritunarbreytingunni 1973–74 og birtist enn í eldri textum (Morgunblaðið hélt sig við z fram til 2000), í vitnunum í pre-1974 heimildir, og í fornum stíl. Að merkja `íslenzkur` eða `lízt` sem „foreign“ hendir burt stílupplýsingum og beinir villugreiningu í ranga átt.

Ath. að z-myndir sem héldu sér í BÍN eftir breytinguna (t.d. `verzlun` sem BÍN-færsla) flokkast þegar sem `exact` og sjá aldrei OOV-heuristic. Breytingin snertir því AÐEINS þær z-myndir sem duttu út — nákvæmlega hreinu fornlegu tilfellin þar sem merking sem `archaic_icelandic` er upplýsandi.

**Valkostir sem voru skoðaðir:**
1. Fjarlægja z úr foreign-regluseðlinum og hætta — einfalt, en kastar burt stílmerki sem er í raun áhugavert. z-forn stafsetning er EKKI gæðavandamál; hún er vísbending um kafla úr eldri heimild, hefðarhyggju eða stílbrag.
2. Halda z sem foreign — einfalt en rangt.
3. Bæta við þriðja gildinu `archaic_icelandic` og mæla það sérstaklega — gefur stílvísi og heldur foreign-greiningunni skarpri. Nýr dálkur (archaic_z_count / archaic_z_ratio) bætist við summary CSV.
4. Uppfletta hverja z-OOV aftur með nútímavæddri rithætti (`íslenzkur` → prófa `íslenskur` → ef BÍN-smellur → „staðfest fornleg“) — traustari en flóknari og krefst sérgreiningarreglna (z → s) sem eru ekki alltaf einhlítar.

**Ákvörðun:** Valkostur 3 — aðskilinn `archaic_icelandic`-flokkur. Valkostur 4 er skráður sem framtíðarumbót fyrir sumarritgerðina.

**Forgangsregla:** foreign (c/q/w) > archaic (z) > likely_proper_name (hástafur í miðri setningu) > unknown. Rökstuðningur: tóki sem inniheldur BÆÐI z og c (sjaldgæft en mögulegt í erlendum umritunum) skal merkjast foreign — c/q/w eru afdráttarlausari ekki-íslensk merki en z.

**Hvers vegna z fær sinn eigin flokk en er ekki bara fjarlægð úr foreign-reglunni:** Ef z væri aðeins tekin úr foreign-reglunni myndu z-tókar lenda í „unknown“ eða „likely_proper_name“ og glata merkingu. Með eigin flokk getum við mælt `archaic_z_ratio` sem sjálfstæðan stílvísi. `archaic_z_ratio` með a.m.k. einni tölu gefur til kynna pre-reform ritmál, Morgunblaðshefð, vitnanir í eldri heimildir eða vísvitandi fornleika. Þetta eru mælanlegar stílupplýsingar.

**Dæmi:**
- `íslenzkur` — OOV (ekki í BÍN); hefði verið ragnlega merkt sem foreign. Nú rétt: `archaic_icelandic`.
- `verzlun` — BÍN-færsla, flokkast sem `exact`. Engin breyting.
- `Celsíus` — inniheldur c, merkt foreign. Engin breyting.
- `Zoëga` — inniheldur z, ekkert c/q/w. Nú merkt `archaic_icelandic` (hreint letur-heuristic). Þetta er í reynd erlent sérnafn — takmörkun á núverandi heuristic sem valkostur 4 mun leiðrétta í sumarverkefninu.

**Áhrif á mælingar:** `in_bin_ratio` óbreytt (archaic-z tökin teljast áfram sem oov). `oov_guess` flokkun skerpt. Nýr dálkur `archaic_z_ratio` gefur mælanlega stílvísun.

**Framtíðarumbót (sumarritgerð):** Fletta upp nútímaformi z-tóka í BÍN (z → s umritun): `íslenzkur` → `íslenskur` → staðfestur smellur gefur sterka fornleiksmerkingu. Erlend z-orð eins og Zoëga/Galizia/Palazzo myndu ekki fá BÍN-smell á s-útgáfu og gætu því skilist frá raunverulegri fornlegri íslensku. Núverandi útgáfa er einfaldara staflaga-heuristic.

**Sannprófun:** Keyrt á öllum gögnum eftir breytingu:

```
Gagnasett                 skrár  tot_archaic  skrár_m/archaic  hámark
prompts                      45           33              15       5
human_reference              45           25              10       6
gemini_3_thinking            45           25              10       6
gpt_5                        45            1               1       1
le_chat_fast                 41            5               4       2
le_chat_thinking             45           14               8       4
```

Heildarfjöldi tóka sem færðist úr „foreign“ í „archaic_icelandic“: 103 á öllum gagnasettum. Það staðfestir að flokkunin grípi raunveruleg dæmi (ef enginn hefði færst, hefði verið eitthvað að).

10 stök sýnishorn:
- `banzíni` (blog_ref_006.txt) — raunverulega fornleg/dagleg íslenska (nútímamynd: „bensín“).
- `itzatzu`, `pizka`, `orratz`, `zaite` (academic_ref_001.txt) — baskneskur textabrot í vísindatexta.
- `Zoëga`, `Sarkozy`, `Zapatero`, `Renzi` (news_ref_*) — erlend sérnöfn.
- `Zornoza`, `Zuaznabar` (academic_ref_001) — spænsk/baskneskt sérnöfn.
- `Gonzalez-Moreno` (academic_ref_003) — spænskt sérnafn.

Þetta sýnir takmörk núverandi heuristic skýrt: meirihluti tóka sem nú eru merktir „archaic_icelandic“ eru í raun erlendir (sérnöfn, vitnanir í erlenda texta). Raunverulega fornleg íslenska birtist aðeins í `banzíni`. Það er í lagi fyrir núverandi áfanga vegna þess að (a) `in_bin_ratio` er óháð þessari flokkun og (b) foreign-greiningin er nú skarpari (z-innihaldandi erlent orð truflar hana ekki). Hægt að skoða valkost 4 fyrir sumarverkefnið til að aðgreina gamla íslensku frá erlendum z-tókum.

**Útkoma:** Viðbótardálkar (archaic_z_count, archaic_z_ratio) í `dim8_bin_summary.csv`. Nýtt gildi `archaic_icelandic` í `oov_guess` dálki `dim8_bin_detail.csv` (engin skemusbreyting). `--debug` prentar fyrstu 5 archaic-z tóka þvert á skrár til staðfestingar. Skjalfest í ARCHITECTURE.md og stutt athugasemd í research_log.md.


### 026 — 20. apríl 2026 — BÍN-staðfesting á gamalli z-stafsetningu í dim8 (valkostur 4 útfærður)

**Samhengi:** Ákvörðun 025 kynnti `archaic_icelandic`-flokkinn en með hreinu staflaga-heuristic (ef z í tóka → `archaic_icelandic`). Sannprófun sýndi að meirihluti tóka sem lentu í þeim flokki voru í raun erlend sérnöfn (Zoëga, Sarkozy, Zapatero, Renzi, Gonzalez-Moreno, baskneskur textabrot) en ekki raunveruleg fornleg íslenska. Eini raunverulega fornlega tókinn í öllu gagnasettinu var `banzíni` í blog_ref_006. Þessi valkostur 4 úr ákvörðun 025 útfærir BÍN-staðfestingu til að aðgreina staðfesta fornleika frá erlendum z-tókum.

**Málvísindagrunnur (1973–74 réttritunarbreyting):** Réttritunarbreytingin 1973–74 (auglýsing menntamálaráðuneytisins nr. 132/1973, tekur gildi 1. september 1974) skipti z út fyrir s hvar sem hún kom fyrir í íslenskum orðum. Sjá Wikipedia-greinina „Íslensk stafsetning“ og auglýsingu RÁÐH 132/1973. Þar af leiðir að EINA strengbreyting (`z` → `s`, `Z` → `S`) er fullkomið módel af nútímavæðingu fornlegrar z-stafsetningar.

**Valkostir sem voru skoðaðir:**
1. Halda staflaga-heuristic ákvörðunar 025 — einfalt en framleiðir marga falsjákvæða (erlend sérnöfn merkt sem archaic_icelandic).
2. Fletta beint upp í sögulegri BÍN-útgáfu fyrir réttritunarbreytinguna.
3. Útfæra BÍN-staðfestingu með z→s umritun á tóka; ef nútímamyndin finnst í BÍN þá er fornleikurinn staðfestur. Annars nýr flokkur `archaic_z_unverified`.

**Ákvörðun:** Valkostur 3 — nýr `verify_archaic_z(token, bin_instance)` hjálpari sem gerir strengbreytingu (`z`→`s`, `Z`→`S`, varðveitir hástaf) og flettir upp í BÍN með sömu upprunaleg/lágstafs-fallback-reglu og aðalflettingin. Endurnýtir staka BÍN-tilvikið (`_BIN_INSTANCE`) — engin ný tilvik per tóki.

**Ný fimm-þrepa forgangsregla í `guess_oov_class`:**
1. Inniheldur c/q/w → `foreign`
2. Inniheldur z OG z→s mynd er í BÍN → `archaic_icelandic` (staðfest)
3. Inniheldur z EN z→s mynd er EKKI í BÍN → `archaic_z_unverified`
4. Byrjar á hástaf og er EKKI fyrsti tóki → `likely_proper_name`
5. Annars → `unknown`

**Rökstuðningur staðfestingar:** Gamaldags íslenska breytist í nútímaform (t.d. `íslenzkur` → `íslenskur`, `lízt` → `líst`) sem er lögmætt íslenskt orð og er í BÍN. Erlend sérnöfn (Zoëga → Soëga, Sarkozy → Sarkosy) gera það ekki. z→s prófunin eyðir helsta false-positive mynstri af staflaga-heuristic ákvörðunar 025.

**Takmörk (þekkt):**
- `banzíni` → z→s mynd er `bansíni`, sem er EKKI í BÍN (nútímamyndin er `bensín`, með sérhljóðabreytingu umfram z→s). Slík tilvik verða merkt `archaic_z_unverified` þótt þau séu í reynd íslensk tökuorð úr eldra ritmáli. Þetta er meðvituð takmörkun — einfalda z→s reglan grípur ekki samsettar hljóðfræðilegar breytingar.
- Orð sem eru bæði í erlendri og gamalli íslenskri mynd (ef einhver) gætu lent röngu megin. Þetta er ekki skráð raunverulegt mynstur í gögnunum.

**Breytingar á skemu:**
- summary CSV: `archaic_z_count` → `archaic_icelandic_count`; `archaic_z_ratio` → `archaic_icelandic_ratio`; nýir dálkar `archaic_z_unverified_count` og `archaic_z_unverified_ratio`.
- detail CSV: `oov_guess` fær nýtt mögulegt gildi `archaic_z_unverified` (skemabreyting aðeins í enum-listanum).
- Prenttafla: tveir dálkar (`arch-is%` og `arch-unv%`) í stað eins (`arch-z%`).
- Debug-úttak: fyrstu 5 STAÐFEST dæmi (með z→s mynd við hliðina) og fyrstu 5 ÓSTAÐFESTIR dæmi, sér sýnishorn.

**Dæmi:**
- `íslenzkur` — z→s = `íslenskur` → í BÍN → `archaic_icelandic` (staðfest). Óbreytt frá 025.
- `Zoëga` — z→s = `Soëga` → ekki í BÍN → `archaic_z_unverified`. Rétt aðgreining frá 025.
- `Sarkozy` — z→s = `Sarkosy` → ekki í BÍN → `archaic_z_unverified`. Rétt.
- `banzíni` — z→s = `bansíni` → ekki í BÍN → `archaic_z_unverified`. False-negative (sjá takmörk).
- `verzlun` — í BÍN beint sem `exact`. Engin breyting, sér aldrei heuristic.

**Áhrif á mælingar:** `in_bin_ratio` óbreytt (báðir z-flokkar undirmengi oov). `oov_ratio` óbreytt. 

**Hæði:** Ekkert nýtt. Notar staka BÍN-tilvikið sem þegar er hlaðið.

**Sannprófun:** Sjá research_log.md færslu 20. apríl 2026 — heildarniðurstöður á öllum 6 gagnasettum, bucket-talningar og 10 stök sýnishorn per flokki.

**Útkoma:** `dim8_bin_summary.csv` með uppfærðum dálkanöfnum + nýjum dálkum. `dim8_bin_detail.csv` með nýju mögulegu `oov_guess`-gildi. ARCHITECTURE.md oov_guess-listi uppfærður. False-positives á erlendum sérnöfnum lagað (Zoëga, Sarkozy o.s.frv. merkjast nú rétt sem `archaic_z_unverified`). Þekkt takmörkun (`banzíni`) skráð sem framtíðar-umbót.

**Upplýsandi niðurstaða: `archaic_icelandic` = 0 í öllu gagnasettinu.** Sannprófun eftir keyrslu gaf 0 staðfest archaic_icelandic tóka á öllum 266 skrám, en öll 103 tókar sem áður voru í staflaga-archaic-flokknum færðust óbreyttir í `archaic_z_unverified`. Þetta er EKKI villa heldur afhjúpandi niðurstaða um BÍN: raunverulega gömul z-orð (`íslenzkur`, `lízt`, `verzlun` o.fl.) eru í BÍN sem færslur og flokkast sem `exact` — þau ná aldrei OOV-heuristic. Sannprófað með beinum BÍN-uppflettingum: `íslenzkur`, `lízt`, `verzlun` — smellir í BÍN. 


### 027 — 23. apríl 2026 — Ellefta víddin: MTLD (lexical diversity) — Hugmynd og hönnun

**Samhengi:** Verkefnið hefur hingað til tíu víddir (dim1–dim10). Orðaforðafjölbreytni (lexical diversity) er ekki á meðal þeirra. Biber (1988) notaði „type/token ratio“ (TTR) sem eitt af einkennum „Informational production“-víddarinnar og lexical-diversity mælingar eru almennt mikið notaðar í stílgreiningum. TTR er hins vegar háð lengd á texta: lengri texti hefur lægri TTR AF STÆRÐFRÆÐILEGUM ÁSTÆÐUM, sem gerir hana óhæfa til samanburðar á textum af ólíkri lengd. Ellefta víddin bætir við orðaforðafjölbreytni með MTLD (Measure of Textual Lexical Diversity, McCarthy & Jarvis 2010) sem virkar eins og TTR nema hægt að nota með mismunandi textalengdir.

**Hugmynd könnuð (pre-flight) — heimildir og reiknirit:**

1. **Aðalheimild:** McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. *Behavior Research Methods*, 42(2), 381–392. DOI: [10.3758/BRM.42.2.381](https://doi.org/10.3758/BRM.42.2.381). Staðfest tilvitnun í Springer og PMC. PDF frá útgefanda var ekki aðgengileg án áskriftar; reiknirit staðfest með þremur óháðum lýsingum (PMC-samdrætti, koRpus-skjölum í R, og Lingua::Diversity::MTLD á metacpan).

2. **Verksmiðjugildi þröskulds (factor size threshold):** 0.72. Höfundar könnuðu [0.660, 0.750]; 0.72 er staðlað gildi í öllum síðari útfærslum (koRpus, lexical-diversity, Lingua::Diversity::MTLD).

3. **Stefna þröskuldar:** STRÖNG („<“, ekki „≤“). Heimildir: metacpan („falls below“), koRpus („drops below“), PMC-samdráttur („maintains TTR above threshold“). Útfærslan er því: þegar rúllandi TTR fer UNDIR 0.72 (strictly less), loka faktor og endurstilla.

4. **Formúla hlutafaktors (incomplete factor at end of text):**
   ```
   partial_factor = (1 - TTR_at_end) / (1 - 0.72)
   ```
   Þetta er „fjarlægðin frá 1 sem eftir er“ deilt með „heildarbilinu“. Sumar heimildir lýsa þessu lauslega sem „hlutfall núverandi TTR og þröskulds“ — sú setningatækni er villandi. Stöðluð útfærsla er `(1 - current_TTR) / (1 - threshold)`, sem er það sem þessi vídd notar. Tókafjöldi hlutafaktors er bætt við heildarfaktorafjöldann sem hlut (e.g. 40 tókar með TTR = 0.80 í lok → 0.80 er > 0.72 svo faktorinn er ÓLOKIÐ; bæti `(1-0.80)/(1-0.72) = 0.714` við faktorafjöldann).

5. **Forward + reverse meðaltal:** Staðfest í öllum heimildum. Lokagildi MTLD = meðaltal af fram-göngu og afturábak-göngu á sömu tókaröð. Ástæða: fram-ganga „klárar ekki“ endurtekin orð í lok texta; afturábak-ganga jafnar þessa bjögun.

6. **Lágmarks textalengd:** McCarthy & Jarvis (2010) könnuðu texta ≥ 100 tóka. Almenn ráðgjöf: MTLD verður óstöðugt undir ~100 tókum (lokagildi dregið af einum eða tveimur faktorum). 500-tóka prompt/viðmiðunar-úrtökin í þessu verkefni eru yfir þessum mörkum (~200 tókar eftir hreinsun).

7. **Milička-víddarsett (athugun):** Milička o.fl. (2025, arxiv 2509.10179v2) nota Biber-MDA með 6 ensk víddum (67 eiginleikum) og 8 tékkneskum víddum (137 eiginleikum). Hvorki MTLD né TTR, vocd-D eða HD-D eru í víddarsettinu. MATTR er nefnd í framhjáhlaupi í umræðu um hitastig. Þess vegna er dim11 **ekki hliðstæða neinna Milička-vídda** — hún er framlenging af hugmyndum Bibers um „Informational production“ og stendur utan við hinn upprunalega ramma. Þessi staða er skjalfest undir TAKMARKANIR í docstreng skriftu víddarinnar.

8. **Valkostir sem voru skoðaðir:**
   - (a) Sleppa orðaforðafjölbreytni alfarið — einfalt en skilur eftir augljósa eyðu milli Biber-ramma og víddarsetts okkar.
   - (b) Nota barefnan TTR — einfalt en háð lengd, þar af leiðandi ósamanburðarhæft milli texta af ólíkri lengd.
   - (c) Nota vocd-D eða HD-D — flóknari líkananálganir, krefjast Monte Carlo-sýnatöku (vocd-D) eða ofháðs reiknings (HD-D). Lítil reiknanleg ávinningur umfram MTLD.
   - (d) Nota MTLD — lengdarstöðug, klassísk, vel skjalfest, útfærsla er einföld með staðal-Python. 

9. **Valkostir á útfærslustigi fyrir D:**
   - (a) Nota ytri pakka (`lexical-diversity`, `textstat`, rpy2+koRpus) — eykur hæði, minnkar gagnsæi um reikniritið.
   - (b) Útfæra sjálf með standard Python — engin ný háð umfram `tokenizer` (þegar á sínum stað fyrir dim10), reikniritið er skýrt skjalfest í kóðanum. 

10. **Ákvarðanir um útfærslu:**
    - D valið með leið B.
    - **Lemmatization?** Nei. `measure_mtld` skilar *wordform* MTLD. Lemmatization myndi breyta skilaboðum: beygingarform (`hestur`, `hests`, `hesti`, `hesta`) teldust sem eitt. Það er réttmætt val fyrir tungumál með ríkt beygingarkerfi EN breytir skilningi MTLD-skoranna frá McCarthy & Jarvis-staðli. Wordform-útgáfan er einfaldari og gagnsærri. Íslensk beyging getur verið stíleinkenni í sjálfu sér (formlegur fræðitexti notar fleiri fallabeygingar). Sumarritgerð getur síðar bætt við lemma-MTLD sem samanburði.
    - **Fastur tókari:** Sama pípa og dim6 og dim10 nota fyrir orðatalningu — `text.split()` á whitespace, strippa greinarmerki með `dim6.PUNCT_TO_STRIP`, sía tóka án bókstafs með `dim6.HAS_LETTER`. Sömu reglur tryggja að dim6/dim10/dim11 telji NÁKVÆMLEGA sömu orð. 
    - **Lágstafir fyrir tegundatalning:** Já (wordform-MTLD stendur og fellur með þessu, annars teljast byrjunarstafir setninga sem nýjar gerðir).
    - **Tilhöfn í vídd:** Skila `final_mtld` sem aðal-v, ásamt forward/reverse/faktorafjöldum í dict fyrir villuleit.

11. **Takmarkanir sem verða skjalfestar í docstring:**
    - Wordforms, ekki lemma — íslensk beyging getur blásið upp fjölbreytni.
    - Stutt textabrot (< 100 tókar) gefa óáreiðanleg gildi.
    - MTLD er blindur á merkingu: staðsetning sem endurtekur málfræðilegt mynstur („talar um X, talar um Y“) skorar hærra en endurtekning sömu orðmynda.
    - Sama gildir um umorðun: texti sem endurtekur sömu hugmynd með mismunandi orðmyndum skorar hærra.
    - Endurtekningarmynstur sem við sjáum í LLM-úttaki (template-endurtekningar) munu LÆKKA MTLD — það er bein hliðarverkun: dim11 ætti að grípa stílfræðilegt tap vegna slíkra mynstra. Ein aðalástæða víddarinnar!

**Ákvörðun:**
Útfæra `scripts/dim11_mtld.py` með tveimur föllum:
- `compute_mtld(tokens: list[str]) -> dict` — innri reiknari sem skilar `{forward_mtld, reverse_mtld, final_mtld, factor_count_forward, factor_count_reverse, total_tokens, total_types}`.
- `measure_mtld(text_file: Path) -> float` — pípa sem tekur inn `.txt` skrá, tókar með `tokenizer.tokenize`, hreinsar með dim6-reglum, setur í lágstafi og kallar `compute_mtld`. Skilar v-gildi plús dict.

Þröskuldur 0.72, ströng „<“-samanburður. Hlutafaktor: `(1 - TTR_at_end) / (1 - 0.72)`. Engin hæði að utan umfram `tokenizer` (þegar á sínum stað).

**Rökstuðningur:**
MTLD fyllir áberandi eyðu í víddarsettinu (orðaforðafjölbreytni). Lengdarstöðugleikinn er nauðsynlegur vegna þess að LLM-framhöld og mennsk viðmið eru af ólíkri lengd. McCarthy & Jarvis-aðferðin er staðallinn í stílfræðibókmenntum og er nógu einföld til að útfæra gagnsætt með Python. Athugun leiddi í ljós að engar faldar reiknifræðilegar útfærslur eru til staðar í pakka-heiminum sem sumarritgerð gæti nýtt sér betur; sjálf-útfærsla með skjalfestum reiknirit gefur bestu stjórn á skilgreiningunni (lágstafrænun, lemma-status, tokenization).

**Prófun:**
Keyra dim11 á mennskri viðmiðunarskrá (human_reference) og á tveimur LLM-textum til að staðfesta að v-gildi séu á eðlilegu sviði (~60–100 fyrir 500-orða íslenska texta samkvæmt hliðstæðum rannsóknum á öðrum málum — kvörðunarfyrirvari svipaður og fyrir LIX). Villuleitarhamur `--debug` prentar forward/reverse/faktorafjölda til yfirferðar.


### 028 — 24. apríl 2026 — Dim7 endurskilgreind sem hlutfall sem/(sem+að) + NaN-meðferð í aggregation

**Samhengi:** Fyrri útfærsla á vídd 7 tók `comp_per_1000_words = (sem + að) / orð × 1000` sem aðal-v-gildi, en aukamælingin `sem_ratio = sem / (sem + að)` var einnig til staðar í niðurstöðum. Innan drátta lokaverkefnisins og eftir vikuleg viðmiðun við fyrri niðurstöður kom í ljós að tíðnimælingin sjálf (comp_per_1000_words) er ekki túlkanleg sem sá „aðferð undirskipunar“ sem vídd 7 átti að fanga — hún mælir aðeins hversu algeng tengiorð eru yfirleitt, ekki HVORT undirskipun er fallsetningadrifin (CP-THT, með `að`) eða tilvísunaraukasetning (CP-REL, með `sem`). Eldra `sem_ratio` var nær markmiði víddarinnar en var ennþá með þann galla að skila `0.0` þöglu gildi þegar `sem + að == 0` (deiling með núlli í fyrri prótotýpu, smoothing í núverandi kóða). Þetta sameinaðist við aðra spurningu um pípulagnina sem hafði vaknað í ákvörðun 027: hvað gerist ef vídd skilar NaN fyrir stakt málsýni? Fyrri útfærsla sleppti slíkum málsýnum með 0.0 — sem bjagar B-heildarskorið niður.

**Valkostir sem voru skoðaðir:**

1. Halda `sem / að` með add-one smoothing (Laplace) — einfalt en handahófskennt, felur upplýsingar um texta með engu `að`-tengiorði og býr til rangt háa fráviksmælingu fyrir jaðartilvik.
2. Skipta yfir í `sem / (sem + að)` sem aðal-v, og skila NaN þegar sem+að == 0 — bundið á [0,1], túlkanlegt sem hlutfall, stillir við stílrökstuðning víddarinnar (hvaða tegund undirskipunar ráðast í texta), og NaN er heiðarleg merking á óskilgreindu gildi.
3. Nota aðeins absolút tíðni (sem_per_1000, ad_per_1000) sem tvær sérstakar víddir — engin deiling milli teljara, en missir „hvor tegund ræður“ upplýsingar sem vídd 7 á að mæla. Hefði þurft að breyta víddarskriftu (skipta dim7 í dim7a og dim7b).

**Ákvörðun:** Valkostur 2 — `comp_ratio = sem / (sem + að)`, NaN á tómum tengiorðum, skráð í stderr. Að auki uppfærð NaN-meðferð í `run_Milička.py`: útiloka NaN-víddir úr b-vektor per málsýni, skipta úr `B = ‖b‖ = sqrt(Σ b_d²)` yfir í RMS-form `B = sqrt(meðaltal(b_d²))` til að halda sambærilegri skala þvert á málsýni með ólíkan fjölda gildra vídda.

**Rökstuðningur:**
- `sem / (sem + að)` er bundið við [0,1], túlkanlegt sem hlutfall tegunda tengiorða, samhverft um 0.5, og svarar beint rökstuðningi víddarinnar: hvaða tegund aukasetninga ráðast í textanum (CP-REL vs CP-THT).
- Útilokun málsýna þar sem báðir teljarar eru 0 er lögmæt: slíkur texti hefur enga undirskipun með C-hnút að flokka. Að þvinga fram 0.0 eða 1.0 á slíku tilfelli er rangur staðhæfingur.
- NaN er heiðarleg merking á óskilgreindu gildi. Pípulagningin þarf hvort eð er að höndla NaN fyrir vídd 8 (þegar `dim8_bin_summary.csv` vantar — sjá ákvörðun 022), svo hluturinn er ekki eingöngu vegna dim7.
- RMS-form B er aðlögun frá Milička (2025), ekki aðferðafræðileg frávik. Þegar allar n víddir eru gildar gildir `sqrt(mean(b_d²)) = ‖b‖ / sqrt(n)` — sama gildi upp að fastri skalabreytingu `sqrt(n)`. Röðun líkana helst óbreytt þegar n er fast; aðeins algild B-gildi minnka um þátt sqrt(10)≈3.16 fyrir n=10. RMS-formið verður hins vegar lykilmál þegar n er breytilegur milli málsýna — summa-formið refsar málsýnum með fleiri gildum víddum (fleiri liðir í summu), en RMS-formið jafnar skalann.

**Útkoma:**
- `scripts/dim7_complementizers.py` uppfært: Nýir dálkar `comp_ratio` (aðal-v, NaN-meðvitað) og `comp_freq` (aukamælikvarði, sama og `comp_per_1000_words`). Eldri dálkar `sem_ratio`, `comp_per_1000_words` o.s.frv. haldnir fyrir afturábaksamhæfi við áður vistað CSV og rit. NaN-atvik skráð í stderr með skráarheiti.
- `scripts/run_Milička.py` uppfært: `dim7.key` breytt í `comp_ratio`. Inner loop skráir NaN-tilvik í `nan_log` per (líkan, textategund, númer, vídd). B-útreikningur útilokar víddir án gildra para úr RMS-nefnaranum. Nýr summary-skýrslukafli prentar dreifingu gildra vídda per málsýni og lista yfir málsýni með víddir sem vantar. Túlkunar-leiðbeiningar uppfærðar til að endurspegla nýja B-skala (sqrt(n)×-minni en Milička).
- Nýr `audit_nan_handling.md` skjalfestir að engin önnur vídd (1–11 fyrir utan 7) þarfnast sambærilegrar lagfæringar á núverandi 2000-orða gagnasafni. Pípulagningin meðhöndlar NaN framtíðarlega á öruggan hátt.
- Þetta er **frávik frá upprunalegri aðferðafræði Milička**. B-formið var `‖b‖ = sqrt(Σ b_d²)`. RMS-aðlögunin verður skjalfest sérstaklega í aðferðafræðikafla greinarinnar með útskýringu á því hvers vegna: til að halda B-skori sambærilegu þvert á málsýni með ólíkum fjölda gildra vídda. Röðun milli líkana er óbreytt; aðeins algild gildi skala niður.
- Regressionsprófun á núverandi gagnasafni verður gerð til að staðfesta að röðun líkana er óbreytt. Fyrri B-gildi × ~1/sqrt(10) ættu að samsvara nýju B-gildum, innan fljótandi-punkta-skekkju.

**Afleiðing fyrir síðari keyrslur:**
Endurkeyra `run_Milička.py` á öllum gagnasafni með nýju útfærslunni. Sammála breyting: B-gildi minnka um `sqrt(10)≈3.16` þegar allar víddir eru gildar. Interpretation-þröskuldar í túlkunar-leiðbeiningum uppfærðir samsvarandi (`B < ~0.3` jafngilt eldra `B < ~1.0`, o.s.frv.).


### 029 — 24. apríl 2026 — BÍN-staðfest aðgreining samskeyttra tóka í forvinnslu

**Samhengi:** Við handavirka skoðun á hreinsuðum LLM-úttökum (sérstaklega Gemini 3 Thinking á akademíska prompti 004) kom í ljós mynstur þar sem líkön skiluðu textasamskeytum án bils á milli: (a) lágstafur beint við stóran staf (t.d. „forvörnumEins", „roðaáhrifaÚtfjólublá", „LíffæriBráð"), (b) tala beint við stóran staf í töflulíkum línum (t.d. „0-2Lágt" fyrir húðgerðarflokk), og (c) stafur beint við tölu. Mynstrin (a) og (b) eiga uppruna sinn í því að markdown-hausar voru fjarlægðir án þess að skilja eftir aðskilið bil, og þar sem prompt-hefðin í þessu verkefni er linutexti án markdown verður þetta að flæða inn í tóka-talningu stílfræðivídda. Mynstur (c) birtist eðlilega í vísindalegum skammstöfunum (PGE2, IL-6, TNF-alpha) og VERÐUR að halda. Án aðgerða blása tóka-talningar dim6 (orðalengd), dim10 (setningalengd tala), og dim11 (MTLD) upp rangt vegna rangra „samsettra" tóka sem BÍN-vídd 8 sleppir í gegn sem „ekki í BÍN".

**Valkostir sem voru skoðaðir:**

1. **Reglubundin regex-aðgreining alls staðar þar sem lowercase→uppercase eða digit→uppercase sést.** Einfalt en brýtur CamelCase-vörumerki (iPhone, macOS) og vísindalegar skammstafnir (PGE2, IL-6). Of árasargjörn regla, býr til falska aðgreiningu sem bjagar gagnasafnið jafnvel verr en upphaflegt vandamál.

2. **Punktvís handleiðrétting í hreinsuðum skrám.** Örugg en óskalanleg: ný LLM-keyrsla fæli í sér nýja samskeyti að finna og leiðrétta, og handleiðrétting er ekki reproducible án skráar af öllum leiðréttingum.

3. **BÍN-staðfest aðgreining: aðeins skipta þegar BÆÐI hlutar eru gildir íslenskir orðstofnar samkvæmt BÍN (bein fletting EÐA samsetning).** Notar sömu kóðafléttu og vídd 8 (`islenska`-pakka Miðeindar), fangar ekta íslensk samskeyti („forvörnumEins") en heldur enskum vörumerkjum og vísindalegum skammstöfunum ósnortnum. **Valið.**

4. **Notkun token-greiningar `tokenizer`-pakkans eingöngu.** Tokenizer-pakkinn þekkir ekki þetta sérstaka mynstur (samskeyti án bils eru einn tóki fyrir honum). Yrði þurft að bæta við eftirvinnslu sem er í grunninn sama reglan og valkostur 3, svo ekkert sparast.

**Ákvörðun:** Valkostur 3. Bætt við `split_concatenated_tokens(text: str, bin_lookup, cache=None) -> tuple[str, int]` í `scripts/preprocess_llm_output.py` og fella inn í `clean_llm_text`-pípuna á milli markdown-fjarlægingar og endurtekningargreiningar.

**Útfærsluákvarðanir:**

- **Þrír regex-mynstur:** (i) `[íslenskur-lágstafur][íslenskur-hástafur]` — aðgreind aðeins ef BÁÐIR hlutar eru gildir íslenskir orðstofnar í BÍN (bein fletting EÐA samsetning með bandstriki í `bmynd`); (ii) `[tala][íslenskur-hástafur]` — ALLTAF aðgreind (taka-stór-stafur mörk eru ekki gildir orðtóka); (iii) `[íslenskur-stafur][tala]` — aðgreind aðeins ef undanfarandi stafaruna er ≥4 stafir OG gild í BÍN. (iii) er nauðsynlegt fyrir töflulíkar línur eins og „5 ára2 ára" en má EKKI aðgreina „PGE2", „IL-6", „TNF-alpha".

- **BÍN-fletting:** Sama mynstur og dim8 notar (`_lookup_bin` í `dim8_bin_ratio.py`): reyna upphaflega töku, síðan lágstafrænt form. „Gilt" þýðir að `Bin().lookup(token)` skili minnst einni merkingu EÐA að `bmynd` í einni skilaðri merkingu innihaldi bandstrik (samsetning sundurbrotin af BÍN).

- **Skyndiminni:** Module-level `_BIN_CACHE: dict[str, bool]` svo fletting hvers orðtóka (lágstafrænt form) er gerð EINU SINNI á keyrslu. Fletting er dýr (~5 ms hver) og sama orðið kemur upp oft yfir skrár.

- **Lazy BÍN-instance:** `_BIN_INSTANCE = None` + `_get_bin_singleton()` lazy-load eins og í dim8. Forðast 2 GB minnisnotkun við skráaaðgreiningu þegar forvinnsla gerir ekkert annað.

- **LaTeX-varðveisla:** Áður en regex-aðgreining keyrir er `$$...$$` og `$...$` formúluspretti vistað með staðgengils-merkjum `__MATH_N__` (undirstrik hvorki stafir né tölur, svo mynstur ná þeim ekki). Eftir aðgreining er staðgengill skipt út aftur fyrir upprunalega streng. Þetta tryggir að `E_{eff}` sé ekki aðgreint í „E {eff}" í kringum undirstrikið og að `\int S(\lambda) d\lambda` sé óbreytt.

- **Endurnefning lýstrar lýsingar:** Fall skilar bæði aðgreindum texta og fjölda aðgreiningarsniða (int), svo `clean_llm_text` geti skráð „samskeyti aðgreind: N" í skýrsluna á per-skrá basa og „Samskeyttir tókar aðgreindir: N staðir" í HEILDARSAMANTEKT.

- **Samhljóða forvinnsla á mannlegum textum:** Nýr `--split-concatenated` flagg í `scripts/extract_samples.py` (sjálfgefið SLÖKKT, vegna þess að mannlegir textar hafa ekki þetta vandamál á akademískum og fréttatextum í gagnasafninu, en sama hreinsun verður að vera möguleg til að tryggja samhljóða forvinnslu þegar hún er þörf). Ef kveikt er á henni kallar `extract_samples.py` beint í `split_concatenated_tokens` og `_get_bin_singleton` úr preprocess-mótu.

**Rökstuðningur:**

- **Af hverju BÍN-staðfesting en ekki regex ein sér?** BÍN-staðfesting er eini þekkti einfaldi hafarinn til að aðskilja ekta íslensk samskeyti („forvörnum" + „Eins") frá ensk CamelCase-myndunum („i" + „Phone") án málfræðilegrar þáttunar. Regex ein sér myndi breyta „iPhone" í „i Phone", sem er rangt í íslenskum texta. BÍN-fletting gefur beint „er þetta gilt íslenskt orð?" svar.

- **Af hverju tala→stór stafur ALLTAF?** Þetta mynstur kemur upp bara í töflulíkum línum þar sem markdown-tafla var hreinsuð í línutexta („0-2 Lágt" varð „0-2Lágt"). Engin löglegt orðform í íslensku byrjar með tölu, svo regla er örugg: aðgreina alltaf.

- **Af hverju stafur→tala aðeins við 4+ stafa forsögu?** Vísindalegar skammstafnir (PGE2, IL-6, TNF, VEGF) eru oftast 2–3 bókstafir á undan tölu. Gild íslensk orð með tölu beint á eftir (t.d. „ára2") hafa langa stafarunu (≥4 stafir) sem sést í BÍN. Þetta er heuristic sem reyndist réttur á prófi Gemini-skjalsins — engar rangar aðgreiningar á PGE2/IL-6/TNF, rétt aðgreining á eina tilviki í prófskjalinu.

- **Af hverju skyndiminni í module-level en ekki instance-level?** Sami BÍN-instance er endurnýttur þvert á allar skrár í einni keyrslu, og sama á við um skyndiminni: „forvörnum" kemur upp oft í akademískum texta, og endurteknar flettingar sem skyndiminnið sparar rétta upp keyrslutíma margsinnis.

- **Af hverju þetta skref er millistig 3 í clean_llm_text (milli markdown og endurtekningargreiningar)?** Markdown-hausar eru uppspretta (a)-samskeytanna (hausinn er fjarlægður en skilur eftir samskeytu), svo aðgreiningin verður að keyra EFTIR markdown-hreinsun. Endurtekningargreining ber saman orð gegn prompti, og orð sem voru samskeyti fyrir aðgreiningu myndu ekki passa neinu í prompti; því verður aðgreiningin að keyra ÁÐUR en endurtekningargreining.

**Takmarkanir (skjalfestar í docstring):**

- **Heuristic á stafur→tala mörkum (≥4 stafir, BÍN-gilt):** heuristic sem hefur verið prófaður á einu Gemini-skjali og þremur GPT-5-skjölum. Gæti misheppnast á ókunnum LLM-úttökum með nýjum skammstöfunarmynstrum (t.d. 5-bókstafa skammstöfun á undan tölu). Handleiðrétting verður að gera eftir handleitaða skoðun á hreinsuðum úttökum.

- **BÍN-hraði:** Fletting er ~5 ms hver; 10.000-tóka skjal með ~500 einstökum lowercase→uppercase mörkum tekur ~5 s. Í venjulegu akademísku skjali eru slíkir staðir 30–40 á skrá, svo áhrif á heildartíma eru lítil. Skyndiminni yfir skrár heldur þessu niðri.

- **Rangfenging BÍN-fjárhags:** Ef BÍN vantar nýtt hugtak (t.d. „smáforrit", „netvangur") verður það EKKI aðgreint jafnvel þó það sé samsetning frá sjónarhorni íslenskrar málfræði. Þetta er öruggar viðsnúningur en lengra þáttunarkerfi sem væri ekki raunhæft að byggja.

- **Val á tegund falls fyrir `bmynd`-bandstrik:** Samsetning eins og „roðaáhrif" er þekkt af BÍN (bmynd = „roða-áhrif"). Ef framtíðar-BÍN-útgáfa breytir þessu formi (t.d. fjarlægir bandstrik eða fer yfir í annan merkingu), þá breytist hegðun. Prófsamsetning í `tests/test_split_concatenated_tokens.py` grípur þetta tilvik.

**Útkoma:**

- Nýtt fall `split_concatenated_tokens` í `scripts/preprocess_llm_output.py` með bilingual docstring.
- Hjálparföll `_extract_left_token`, `_extract_right_token`, `_bin_is_valid` í sama skjali.
- Module-level `_BIN_INSTANCE`, `_BIN_CACHE`, `_get_bin_singleton()` lazy-singleton.
- LaTeX-vörn gegnum `_PATTERN_LATEX_DISPLAY`, `_PATTERN_LATEX_INLINE`, `_MATH_PLACEHOLDER`.
- Innflettun í `clean_llm_text` sem SKREF 3 (milli markdown og hvítbilsjöfnunar); skilar `concatenated_splits` tölu í `all_stats`-dict.
- Uppfærsla á `print_file_report` (ný lína „samskeyti aðgreind: N" þegar N > 0) og `print_summary` (ný lína „Samskeyttir tókar aðgreindir: N staðir" í HEILDARSAMANTEKT).
- Nýr `--split-concatenated` flagg í `scripts/extract_samples.py` með SKREF 3b-keyrslu á mennskum málsýnum (sjálfgefið SLÖKKT).
- 13 einingaprófanir í `tests/test_split_concatenated_tokens.py` (allar standast) — fylla öll viðurkennd tilvik úr verklýsingu og jaðartilvik (macOS, setningarskil með punkti og stórum staf, margfaldur aðgreining, LaTeX-varðveisla).
- Samþættingarprófun á `gemini_thinking_academic_prompt_004.txt`: 32 samskeyti aðgreind, allar LaTeX-formúlur varðveittar, PGE2/IL-6/TNF-alpha ósnortin.
- Afturför-próf á þremur GPT-5 akademískum skjölum: 0 aðgreiningar (enginn falskur jákvæður).

**Þröngur prófastur:**
Keyra forvinnsluna á öllum LLM-úttökum í `data/experiment/llm_continuations/` og staðfesta að (a) fjöldi aðgreininga per skrá er hóflegur (< ~50 á akademískri skrá, minna á skáldaðri), (b) engin ný vísindaleg skammstöfun er brotin upp (sjónræn yfirferð á handfylli skjala), (c) niðurstöður tókastillingar í dim6, dim10 og dim11 breytast í átt að mannlegum viðmiðum (fækkun rangra „langa" tóka). Ef (c) staðfestist, er áhrif aðgreiningarinnar á B-gildi í `run_Milička.py` næsta skref.


### 030 — 24. apríl 2026 — Le Chat Fast + Balanced samnefnd sem le_chat_free í niðurstöðum

**Ákvörðun:** Le Chat Fast (lagt niður á söfnunartíma) og Le Chat Balanced eru bæði Mistral's free-tier Le Chat á ólíkum tímapunktum; aggregað sem `le_chat_free` til að framleiða eina líkansröð í niðurstöðum. Útfært með `MODEL_ALIASES = {"le_chat_fast": "le_chat_free", "le_chat_balanced": "le_chat_free"}` í `scripts/run_Milička.py` sem er beitt á möppuheiti við söfnun málsýna. Möppuheiti í `data/` og hrár gögn eru ÓBREYTT; aðeins línumerki í CSV-niðurstöðum og samanteknum töflum breytist.


