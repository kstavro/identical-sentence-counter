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
    (1, 0),
    (1, 0),
    (0, 2),
    (0, 1),
    (0, 1),
    (0, 0),
    (1, 0),
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
    ["hello", "world"],
    ["hello", "universe"],
    ["this", "is", "incai"],
]
target_sentence_dict = {
    2: [["hello", "world"], ["hello", "universe"]],
    3: [["this", "is", "incai"]],
}


class TestSentenceCounter(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(TypeError):
            SentenceCounter(123)
        with self.assertRaises(TypeError):
            SentenceCounter(TEST_FILES_PATH / "test_document.txt", "abc")
        with self.assertRaises(ValueError):
            SentenceCounter(TEST_FILES_PATH / "test_document.txt", 1)

    def test_sentencize(self):
        # sentencize normal text

        # test list structure
        self.assertEqual(
            sentence_counter_for_text._sentencize(sentence_counter_for_text.text),
            target_sentence_list,
        )
        # test dict structure
        self.assertEqual(sentence_counter_for_text.sentences_dict, target_sentence_dict)

        # sentencize weird text

        # test list structure
        self.assertEqual(
            sentence_counter_for_weird_text._sentencize(
                sentence_counter_for_weird_text.text
            ),
            target_sentence_list,
        )
        # test dict structure
        self.assertEqual(sentence_counter_for_text.sentences_dict, target_sentence_dict)

    def test_query(self):
        # check that error raises appropriately
        with self.assertRaises(TypeError):
            sentence_counter_for_text.query(123)

        # # tests for normal text
        # for i, sentence in enumerate(sentences):
        #     self.assertEqual(
        #         sentence_counter_for_text.query(sentence), expected_results[i]
        #     )

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
