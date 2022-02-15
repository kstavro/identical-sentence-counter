import os
import sys
import logging
import unittest

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from identical_sentence_counter.data_structures import (
    get_duplicate_free_list_of_subtuples,
    create_cardinality_dict_for_doc_sentences,
    create_cardinality_dict_for_smaller_doc_sentences,
)

logger = logging.getLogger(__name__)

sentences_list = [
    ("hello", "world"),
    ("hello", "universe"),
    ("this", "is", "incai"),
    ("hello", "world")
]
target_cardinality_dict_for_sentences = {('hello', 'world'): 2, ('hello', 'universe'): 1, ('this', 'is', 'incai'): 1}
target_cardinality_dict_for_smaller_sentences = {('hello',): 3, ('world',): 2, ('universe',): 1, ('is', 'incai'): 1, ('this', 'incai'): 1, ('this', 'is'): 1}

test_wordtuple = ("hello", "hello", "world")
target_subtuple_list = [('hello', 'world'), ('hello', 'hello')]

class TestComparisonUtils(unittest.TestCase):
    def testget_duplicate_free_list_of_subtuples(self):
        self.assertEqual(
            get_duplicate_free_list_of_subtuples(test_wordtuple), target_subtuple_list
        )

    def test_create_cardinality_dict_for_doc_sentences(self):
        self.assertEqual(
            create_cardinality_dict_for_doc_sentences(sentences_list), target_cardinality_dict_for_sentences
        )

    def test_create_cardinality_dict_for_smaller_doc_sentences(self):
        self.assertEqual(
            create_cardinality_dict_for_smaller_doc_sentences(sentences_list), target_cardinality_dict_for_smaller_sentences
        )

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG
    )
    unittest.main()
