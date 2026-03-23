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