import os
import sys
import logging
import unittest

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from sentence_counter.comparison_utils import (
    wordlists_are_identical,
    wordlists_are_nearly_identical,
)

logger = logging.getLogger(__name__)

test_wordlist = ["hello", "world"]
candidates_for_identical = [
    (["hello", "world"], True),
    (["world", "hello"], False),
    (["hello", "universe"], False),
]
candidates_for_nearly_identical = [
    (["this", "is", "incai"], False),
    (["hello", "great", "world"], True),
    (["hello", "world", "championship"], True),
]


class TestComparisonUtils(unittest.TestCase):
    def test_wordlists_are_identical(self):
        for sentence, ground_truth in candidates_for_identical:
            self.assertEqual(
                wordlists_are_identical(sentence, test_wordlist), ground_truth
            )

    def test_wordlists_are_nearly_identical(self):
        # check that error raises appropriately
        with self.assertRaises(ValueError):
            wordlists_are_nearly_identical("hello", test_wordlist)

        # check specific case of list of length 1 vs empty list
        self.assertTrue(wordlists_are_nearly_identical(["hello"], []))

        for sentence, ground_truth in candidates_for_nearly_identical:
            self.assertEqual(
                wordlists_are_nearly_identical(sentence, test_wordlist), ground_truth
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG
    )
    unittest.main()
