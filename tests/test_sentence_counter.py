import os
import sys
import logging
import unittest
from pathlib import Path
import pkg_resources

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from sentence_counter.sentence_counter import SentenceCounter

logger = logging.getLogger(__name__)

TEST_FILES_PATH = Path(pkg_resources.resource_filename("tests", "files"))


sentences = [
    "hello world",
    "this is incai",
    "hello",
    "hello great world",
    "hello world championship",
    "this is a very different sentence",
    "Hello woRld."
]
expected_results = [(1, 0), (1, 0), (0, 2), (0, 1), (0, 1), (0, 0), (1,0)]


# document here given as path
# "hello world. hello universe. this is incai."
sentence_counter_for_text = SentenceCounter(TEST_FILES_PATH / "test_document.txt")

# the following text is to check that we process the following bad input
# as if it were correct, i.e. same as "hello world. hello universe. this is incai."
weird_text = "hello woRld .  heLlo    Universe. this is incai. .  "
# document given directly as text
sentence_counter_for_weird_text = SentenceCounter(weird_text, doc_input_is_path=False)
target_sentence_list = [
    ["hello", "world"],
    ["hello", "universe"],
    ["this", "is", "incai"],
]


class TestSentenceCounter(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(TypeError):
            SentenceCounter(123)
        with self.assertRaises(TypeError):
            SentenceCounter(weird_text, 123, 1)
        with self.assertRaises(TypeError):
            SentenceCounter(weird_text, True, "abc")
        with self.assertRaises(ValueError):
            SentenceCounter(weird_text, False, 1)

    def test_query(self):
        # check that error raises appropriately
        with self.assertRaises(TypeError):
            sentence_counter_for_text.query(123)

        for i, sentence in enumerate(sentences):
            self.assertEqual(
                sentence_counter_for_text.query(sentence), expected_results[i]
            )

        for i, sentence in enumerate(sentences):
            self.assertEqual(
                sentence_counter_for_weird_text.query(sentence), expected_results[i]
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG
    )
    unittest.main()
