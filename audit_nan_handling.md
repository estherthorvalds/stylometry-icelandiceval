# Audit: NaN-meðferð í v-gildi víddanna / NaN handling in dimension v-values

**Dagsetning:** 24. apríl 2026
**Samhengi:** Lokað í tengslum við ákvörðun 028 (sjá `decisions_log.md`).

Vídd 7 var fyrsta víddin þar sem NaN-áhætta varð raunveruleg vandamál
(skrá án `að`-tengiorða framkallaði deilingu með núlli í eldri
útfærslu). Í kjölfar lagfæringarinnar er pípuviðtaka NaN nú þeyst inn í
`run_milicka.py`. Þessi skýrsla skoðar allar aðrar víddir til að
finna sambærilega áhættu og staðfesta hvort þörf er á samsvarandi
lagfæringum.

**Niðurstaða í stuttu máli:** Engin önnur vídd þarf kóðabreytingu fyrir
núverandi gagnasafn. Allar víddir 1–11 nota deilingu sem er stærðfræðilega
óskilgreind á tómu inntaki, en á 2000-orða skala er enginn raunhæfur
veruleiki sem framleiðir slíka tilfelli í eðlilegum textum (sjá hverja
línu fyrir nánari greiningu). Samt sem áður meðhöndlar pípulagningin
NaN sem sleppur í gegn (frá víddum sem síðar verða bætt við eða frá
gagnabilun) á öruggan hátt — sjá ákvörðun 028, lið um RMS-B.

---

## Vídd 1 — Frumlagsleysi (`dim1_frumlagsnafnfall.py`)

- **Aðal-v:** `n_dropped / n_total` (hlutfall setninga án NP-SBJ).
- **Nefnari:** `n_total` = setningar með sögn sem eru ekki boðháttur.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `n_total == 0`
  ([dim1_frumlagsnafnfall.py:198](scripts/dim1_frumlagsnafnfall.py:198)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin í reynd. Til þess
  þyrfti texta með ENGRI persónubeygðri sögn sem ekki er boðháttur —
  hvorki frásögn, lýsing, ályktun né spurning getur orðið til án
  slíkra setninga á eðlilegri íslensku.
- **Kóðabreyting nauðsynleg?** Nei. Tapar engri upplýsingu á núverandi
  gagnasafni. Ef framtíðargögn fela í sér jaðartilvik (einsetnings
  fyrirsagnaskrá) má bæta NaN-meðferð við í sama stíl og dim7.

## Vídd 2 — Aukasetningar (`dim2_aukasetningar.py`)

- **Aðal-v:** `n_sub / total` (IP-SUB / (IP-MAT + IP-SUB)).
- **Nefnari:** `total` = fjöldi greinda IP-hnúta.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `total == 0`
  ([dim2_aukasetningar.py:161](scripts/dim2_aukasetningar.py:161)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. Texti með 2000 orðum
  án eins einasta IP-hnúts er ógerningur — IceConParse merkir öll
  yfirborðs-setningarbrot sem IP-MAT eða IP-SUB.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 3 — Nafnliðalengd (`dim3_nafnlidalengd.py`)

- **Aðal-v:** `sum(lengths) / n_nps` (meðallengd nafnliða í orðum).
- **Nefnari:** `n_nps` = fjöldi NP-hnúta.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `n_nps == 0`
  ([dim3_nafnlidalengd.py:235](scripts/dim3_nafnlidalengd.py:235)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. Það þyrfti texta án
  eins einasta nafnliðar — útilokað á íslensku.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 4 — Þátíðarhlutfall (`dim4_past_tense.py`)

- **Aðal-v:** `total_past / total_finite` (þátíð / persónubeygt).
- **Nefnari:** `total_finite` = persónubeygt sagnform.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `total_finite == 0`
  ([dim4_past_tense.py:294](scripts/dim4_past_tense.py:294)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Mjög sjaldgæf. Hægt er að
  hugsa sér nafnliðasamsetningar (t.d. uppskriftalisti, smáauglýsingar)
  sem ekki innihalda persónubeygt sagnform — en slíkt er útilokað í
  núverandi gagnaframkalli (academic, blog, news, fiction). Á 2000 orða
  íslensku á samfelldri prósu er finita-form ávalt til staðar.
- **Kóðabreyting nauðsynleg?** Nei á núverandi gagnasafni.

## Vídd 5 — Þriðjupersónufornöfn (`dim5_thirdperson_pronouns.py`)

- **Aðal-v:** `(third_person_count / total_words) * 1000`.
- **Nefnari:** `total_words` = heildarfjöldi orða (laufblaða).
- **Núverandi hegðun við 0:** Skilar `0.0` ef `total_words == 0`
  ([dim5_thirdperson_pronouns.py:348](scripts/dim5_thirdperson_pronouns.py:348)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. Tóm skrá myndi
  framkalla 0 orð, en 2000-orða úrtök eru tryggð á upptökustigi.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 6 — Orðalengd (`dim6_word_length.py`)

- **Aðal-v:** `mean(lengths)` (meðalfjöldi stafa per orð).
- **Nefnari:** `len(values)` í `mean()`-fallinu — fjöldi gildra
  orða eftir síun.
- **Núverandi hegðun við 0:** `mean([])` skilar `0.0`
  ([dim6_word_length.py:233](scripts/dim6_word_length.py:233)),
  þannig að skrá án orða fær `mean_length = 0.0`.
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. Tóm orðalisti
  myndi krefjast tómrar skráar.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 8 — BÍN-þekja (`dim8_bin_ratio.py`)

- **Aðal-v:** `(n_exact + n_compound + n_proper) / total` (`in_bin_ratio`).
- **Nefnari:** `total` = fjöldi tóka eftir tóknun.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `total == 0`
  ([dim8_bin_ratio.py:587](scripts/dim8_bin_ratio.py:587)). Skrá sem
  inniheldur aðeins greinarmerki/númer myndi falla undir þetta tilfelli.
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. 2000 orða úrtök fela
  alltaf í sér tóka eftir tóknun.
- **Kóðabreyting nauðsynleg?** Nei.

Að auki hefur vídd 8 sérstaka pípuhegðun: ef `dim8_bin_summary.csv`
vantar er NaN skilað per skrá ([run_milicka.py:363](scripts/run_milicka.py:363)).
Þessi tilvik eru þegar meðhöndluð af summary-pípulagi (ákvörðun 028).

## Vídd 9 — Trédýpt (`dim9_tree_depth.py`)

- **Aðal-v:** `mean(depths)` (meðal hámarksdýpt þáttunartrjáa).
- **Nefnari:** `total_sentences` = fjöldi gildra trjáa með ≥ 2 svigatóka.
- **Núverandi hegðun við 0:** Skilar `0.0` ef `total_sentences == 0`
  ([dim9_tree_depth.py:309-310](scripts/dim9_tree_depth.py:309)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. 2000 orða gefa
  marga tugi trjáa.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 10 — LIX-læsilegskor (`dim10_lix.py`)

- **Aðal-v:** `mean_sentence_length + pct_long_words`.
- **Nefnari:** `total_sentences` (fyrir mlength) og `total_words`
  (fyrir pct_long).
- **Núverandi hegðun við 0:** Skilar `0.0` ef annaðhvort er 0
  ([dim10_lix.py:225-228](scripts/dim10_lix.py:225)).
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. 2000 orða gefa
  setningar OG orð.
- **Kóðabreyting nauðsynleg?** Nei.

## Vídd 11 — MTLD (`dim11_mtld.py`)

- **Aðal-v:** `final_mtld = (forward_mtld + reverse_mtld) / 2`.
- **Nefnari:** `factor_count` per stefnu.
- **Núverandi hegðun við 0:** Sérstakt jaðartilfelli — ef `factor_count
  == 0` (allir tókar einstakir og TTR fer aldrei undir 0.72) er
  `mtld_value = len(tokens)` skilað ([dim11_mtld.py:280](scripts/dim11_mtld.py:280)).
  Þetta er meðvituð hegðun fyrir mjög stutta texta.
- **Raunhæf NaN-áhætta á 2000-orða skala:** Engin. Á 2000 orða skala
  fer TTR ávallt undir þröskuldinn (0.72) snemma — McCarthy & Jarvis
  greina að MTLD sé óáreiðanleg undir ~100 tókum, en 2000-orða úrtök
  eru langt yfir mörkunum.
- **Kóðabreyting nauðsynleg?** Nei. Núverandi jaðartilvika-meðferð er
  rétt fyrir mjög stutta texta og á ekki við um Milička-pípuna.

---

## Heildarniðurstaða

- **Engin vídd 1–11 (annað en 7) þarf kóðabreytingu fyrir núverandi
  2000-orða gagnasafn.**
- Pípulagningin í `run_milicka.py` meðhöndlar NaN sem berst frá hvaða
  vídd sem er á öruggan hátt (NaN-aware b-vektor + RMS-B yfir gildar
  víddir + summary-skýrsla per samplu). Þetta er framtíðarvöxtur fyrir
  víddir sem síðar bætast við eða gagnabilanir.
- Vídd 7 fékk sérstaka athygli vegna þess að `comp_ratio = sem/(sem+að)`
  er það aðal-v-gildi þar sem nefnarann (sem+að) getur verið 0 á
  réttmætan hátt — texti getur einfaldlega haft engar undirskipun með
  tengiorð. Aðrar víddir hafa nefnara sem væri 0 aðeins við degenerata
  inntak (tóm skrá, engin sögn) sem útilokast af gagnatöku okkar.
- Ef framtíðarvinna bætir við viðmiðum sem geta raunhæft framkallað
  tóma nefnara (t.d. mæling á tilteknum sjaldgæfum mannvirkjum), ætti
  að fylgja sama mynstri og í dim7: skila `float('nan')`, skrá í
  stderr, og treysta á pípulagninguna að útiloka víddinni úr B
  fyrir þá samplu.
