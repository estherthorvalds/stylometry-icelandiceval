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
- Lesa Jangra et al. og LCTG Bench þegar tími gefst.