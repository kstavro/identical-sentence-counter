import os
import sys
import logging
import unittest
from pathlib import Path
import pkg_resources

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from identical_sentence_counter.sentence_counter import SentenceCounter

logger = logging.getLogger(__name__)

TEST_FILES_PATH = Path(pkg_resources.resource_filename("tests", "files"))


sentences = [
    "hello world",
    "this is incai",
    "hello",
    "hello great world",
    "hello world championship",
    "this is a very different sentence",
    "Hello woRld.",
]
expected_results = [
    (1, 1),
    (1, 0),
    (0, 2),
    (0, 1),
    (0, 1),
    (0, 0),
    (1, 1),
]

# "hello world. hello universe. this is incai."
sentence_counter_for_text = SentenceCounter(TEST_FILES_PATH / "test_document.txt")

# "hello woRld .  heLlo    Universe. this is incai. .  "
# This is to check that we process the above bad input
# as if it were correct, i.e. same as "hello world. hello universe. this is incai."
sentence_counter_for_weird_text = SentenceCounter(
    TEST_FILES_PATH / "weird_test_document.txt"
)

target_sentence_list = [
    ("hello", "world"),
    ("hello", "hello", "world"),
    ("hello", "universe"),
    ("this", "is", "incai"),
]
target_sentence_dict = {('hello', 'world'): 1, ('hello', 'hello', 'world'): 1, ('hello', 'universe'): 1, ('this', 'is', 'incai'): 1}
target_smaller_sentence_dict = {('hello',): 2, ('world',): 1, ('hello', 'world'): 1, ('hello', 'hello'): 1, ('universe',): 1, ('is', 'incai'): 1, ('this', 'incai'): 1, ('this', 'is'): 1}


class TestSentenceCounter(unittest.TestCase):
    def test_init_errors(self):
        with self.assertRaises(TypeError):
            SentenceCounter(123)
        with self.assertRaises(TypeError):
            SentenceCounter(TEST_FILES_PATH / "test_document.txt", "abc")
        with self.assertRaises(ValueError):
            SentenceCounter(TEST_FILES_PATH / "test_document.txt", 1)

    def test_sentencize(self):
        # sentencize normal text

        self.assertEqual(
            sentence_counter_for_text._sentencize(sentence_counter_for_text.text),
            target_sentence_list,
        )

        # sentencize weird text

        self.assertEqual(
            sentence_counter_for_weird_text._sentencize(
                sentence_counter_for_weird_text.text
            ),
            target_sentence_list,
        )

    def test_data_structures(self):
        # test dict structures
        self.assertEqual(sentence_counter_for_text.cardinality_dict_for_doc_sentences, target_sentence_dict)

        self.assertEqual(sentence_counter_for_text.cardinality_dict_for_smaller_doc_sentences, target_smaller_sentence_dict)

    def test_query(self):
        # check that error raises appropriately
        with self.assertRaises(TypeError):
            sentence_counter_for_text.query(123)

        # tests for normal text
        for i, sentence in enumerate(sentences):
            self.assertEqual(
                sentence_counter_for_text.query(sentence), expected_results[i]
            )

        # tests for weird text
        for i, sentence in enumerate(sentences):
            self.assertEqual(
                sentence_counter_for_weird_text.query(sentence), expected_results[i]
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG
    )
    unittest.main()
