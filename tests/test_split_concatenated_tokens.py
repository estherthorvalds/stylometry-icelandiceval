#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_split_concatenated_tokens.py — Einingaprófanir fyrir BÍN-staðfesta
aðgreiningu samskeyttra tóka í forvinnslu (ákvörðun 029).

Prófin krefjast `islenska` pakkanum (þegar háð dim8).
"""

import sys
import unittest
from pathlib import Path

# Gera scripts/ innflutningsmöguleg
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / 'scripts'))

from islenska import Bin  # noqa: E402

from preprocess_llm_output import split_concatenated_tokens  # noqa: E402


class TestSplitConcatenatedTokens(unittest.TestCase):
    """Prófa split_concatenated_tokens á ýmsum textamynstrum."""

    @classmethod
    def setUpClass(cls) -> None:
        """Hlaða BÍN einu sinni fyrir alla prófin."""
        cls.bin_lookup = Bin()

    # --------------------------------------------------------------
    # GRUNNTILFELLI / BASIC CASES
    # --------------------------------------------------------------

    def test_lower_upper_both_valid_bin_words_gets_split(self) -> None:
        """„forvörnumEins" → „forvörnum Eins" (bæði gild í BÍN)."""
        text, n = split_concatenated_tokens(
            "forvörnumEins", self.bin_lookup
        )
        self.assertEqual(text, "forvörnum Eins")
        self.assertEqual(n, 1)

    def test_iphone_left_not_in_bin_left_unchanged(self) -> None:
        """„iPhone" → óbreytt (i er ekki í BÍN)."""
        text, n = split_concatenated_tokens("iPhone", self.bin_lookup)
        self.assertEqual(text, "iPhone")
        self.assertEqual(n, 0)

    def test_macos_left_not_in_bin_unchanged(self) -> None:
        """„macOS" → óbreytt (mac er ekki gilt íslenskt orð)."""
        text, n = split_concatenated_tokens("macOS", self.bin_lookup)
        self.assertEqual(text, "macOS")
        self.assertEqual(n, 0)

    def test_compound_word_split(self) -> None:
        """„roðaáhrifaÚtfjólublá" → „roðaáhrifa Útfjólublá"
        (roðaáhrif er samsetning, útfjólublá er gilt)."""
        text, n = split_concatenated_tokens(
            "roðaáhrifaÚtfjólublá", self.bin_lookup
        )
        self.assertEqual(text, "roðaáhrifa Útfjólublá")
        self.assertEqual(n, 1)

    # --------------------------------------------------------------
    # STAFI-TALA OG TALA-STAFI / DIGIT-LETTER BOUNDARIES
    # --------------------------------------------------------------

    def test_digit_upper_always_splits(self) -> None:
        """„0-2Lágt" → „0-2 Lágt" (tala-stór stafur regla)."""
        text, n = split_concatenated_tokens("0-2Lágt", self.bin_lookup)
        self.assertEqual(text, "0-2 Lágt")
        self.assertEqual(n, 1)

    def test_short_letter_sequence_before_digit_not_split(self) -> None:
        """„PGE2" → óbreytt (of stutt stafaruna, ekki í BÍN)."""
        text, n = split_concatenated_tokens("PGE2", self.bin_lookup)
        self.assertEqual(text, "PGE2")
        self.assertEqual(n, 0)

    def test_abbreviation_with_hyphen_unchanged(self) -> None:
        """„IL-6" → óbreytt (enginn stafur beint á undan tölu)."""
        text, n = split_concatenated_tokens("IL-6", self.bin_lookup)
        self.assertEqual(text, "IL-6")
        self.assertEqual(n, 0)

    # --------------------------------------------------------------
    # LATEX-VARÐVEISLA / LATEX PRESERVATION
    # --------------------------------------------------------------

    def test_inline_latex_preserved_verbatim(self) -> None:
        """LaTeX $...$ á að vera óbreytt stafur-fyrir-staf."""
        src = r"Formúlan $E_{eff} = \int S(\lambda) d\lambda$ er notuð."
        text, _ = split_concatenated_tokens(src, self.bin_lookup)
        self.assertIn(r"$E_{eff} = \int S(\lambda) d\lambda$", text)

    def test_display_latex_preserved_verbatim(self) -> None:
        """LaTeX $$...$$ á að vera óbreytt."""
        src = r"Skrá: $$E = mc^2$$ endir."
        text, _ = split_concatenated_tokens(src, self.bin_lookup)
        self.assertIn(r"$$E = mc^2$$", text)

    def test_split_around_latex_still_works(self) -> None:
        """Aðgreining í kringum LaTeX á samt að virka."""
        src = r"forvörnumEins $E = mc^2$ roðaáhrifaÚtfjólublá"
        text, n = split_concatenated_tokens(src, self.bin_lookup)
        self.assertIn("forvörnum Eins", text)
        self.assertIn("roðaáhrifa Útfjólublá", text)
        self.assertIn(r"$E = mc^2$", text)
        self.assertEqual(n, 2)

    # --------------------------------------------------------------
    # MARGFALDUR AÐGREININGUR / MULTI-SPLITS
    # --------------------------------------------------------------

    def test_multiple_boundaries_in_one_run(self) -> None:
        """Fleiri en ein aðgreining í sama texta."""
        # "forvörnumEins" og "roðaáhrifaÚtfjólublá" eiga bæði að aðgreinast.
        src = "Upphaf forvörnumEins í miðju og roðaáhrifaÚtfjólublá endi."
        text, n = split_concatenated_tokens(src, self.bin_lookup)
        self.assertIn("forvörnum Eins", text)
        self.assertIn("roðaáhrifa Útfjólublá", text)
        self.assertGreaterEqual(n, 2)

    def test_no_boundaries_returns_unchanged(self) -> None:
        """Texti án lower-upper eða talna-marka er óbreyttur."""
        src = "Þetta er venjulegur texti með engum samskeytum."
        text, n = split_concatenated_tokens(src, self.bin_lookup)
        self.assertEqual(text, src)
        self.assertEqual(n, 0)

    def test_setning_hefst_med_storum_staf_ekki_split(self) -> None:
        """Venjulegt setningarskil „...er. Þetta..." á ekki að aðgreinast."""
        # punktur + bil + stór stafur — engin lower-upper snerting í staf.
        src = "Endir. Upphaf."
        text, n = split_concatenated_tokens(src, self.bin_lookup)
        self.assertEqual(text, src)
        self.assertEqual(n, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
