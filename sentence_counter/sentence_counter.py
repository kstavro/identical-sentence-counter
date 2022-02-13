# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <k.stavropoulos@oxolo.com>
# For License information, see corresponding LICENSE file.

"""This file contains a class that given a text document that contains only lower case alphabet, space and .
(punctuation) character, it provides a method that calculates the number of identical and nearly identical sentences
inside the document to a queried sentence."""

# import os
# import sys
import logging
from typing import Tuple, List, Union
from pathlib import Path

# sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from sentence_counter.comparison_utils import (
    wordlists_are_identical,
    wordlists_are_nearly_identical,
)

logger = logging.getLogger(__name__)


class SentenceCounter:
    """The class that instantiates a document to be processed.
    Contains a query method that returns the number of identical and nearly identical
    sentences inside the document to a queried sentence."""

    def __init__(
        self,
        doc_input: Union[Path, str],
        doc_input_is_path: bool = True,
        max_number_sentences: int = 100_000,
    ):
        """The init function of the class.

        Args:
            doc_input (Union[Path, str]): The input document. Can be given both as
                a string/path object that denotes a file path or directly the input text,
                depending on the value of <doc_input_is_path>.
            doc_input_is_path (str): denotes whether <doc_input> is given as a file path or a
                direct text. Defaults to True.
            max_number_sequences (int): maximum number of sentences the document is allowed to have.
                Defaults to 100.000.
        """

        logger.info("Loading document...")
        self._validate_class_input(doc_input, doc_input_is_path, max_number_sentences)

        if isinstance(doc_input, Path) or doc_input_is_path:
            with open(doc_input) as doc:
                text = doc.read()
        else:
            text = doc_input

        if not text.islower():
            text = text.lower()
            logger.info("Input text is not lowercase. Converted to lowercase.")
        self.text = text.strip()
        self.sentences = self._sentencize(self.text)

        self.max_number_sentences = max_number_sentences
        if len(self.sentences) > self.max_number_sentences:
            raise ValueError(
                "Input Document has more than 100.000 sentences. Please replace it with a smaller document."
            )
        logger.info("Document and list of sentences loaded")

    @staticmethod
    def _validate_class_input(
        doc_input: str, doc_input_is_path: bool, max_number_sentences: int
    ):
        """Validates the format of the input sentence."""
        if not isinstance(doc_input, Path) and not isinstance(doc_input, str):
            raise TypeError(
                "doc_input should be Path or str, while it is {}".format(
                    type(doc_input)
                )
            )
        if not isinstance(doc_input_is_path, bool):
            raise TypeError(
                "doc_input_is_path should be bool, while it is {}".format(
                    type(doc_input_is_path)
                )
            )
        if not isinstance(max_number_sentences, int):
            raise TypeError(
                "max_number should be int, while it is {}".format(
                    type(max_number_sentences)
                )
            )

    @staticmethod
    def _sentencize(text: str) -> List[List[str]]:
        """Splits the instantiated text to sentences in the form of list of words.
        Returns a list of lists of words."""

        sentences = [
            sentence.split()
            for sentence in text.split(".")
            if sentence and not sentence.isspace()
        ]
        print("Split: ", text.split("."))
        return sentences

    # we will already have the sentences as lists of words
    def _compare_wordlist_pair(
        self, wordlist1: str, wordlist2: str
    ) -> Tuple[bool, bool]:
        """Checks if a pair of lists of words is identical or nearly identical.
        1. Two sentences are identical if they have the same words in the same
        order.
        2. Two sentences are nearly identical if we can remove one word from one
        sentence and they become identical.

        Args:
            sentence1 (str): First sentence of the pair
            sentence2 (str): Second sentence of the pair

        Returns:
            bool: denotes whether the sentences are identical
            bool: denoted whether the sentences are nearly identical
        """

        len_difference = len(wordlist1) - len(wordlist2)

        # if the sizes of the lists differ by at least two elements
        # we know directly that the sentences are neither identical nor nearly identical
        if abs(len_difference) > 1:
            return False, False

        # equal lengths means only identical is possible
        if len_difference == 0:
            return wordlists_are_identical(wordlist1, wordlist2), False

        # we now know len_difference is either 1 or -1
        # only nearly identical is possible
        is_nearly_identical = (
            wordlists_are_nearly_identical(wordlist1, wordlist2)
            if len_difference == 1
            else wordlists_are_nearly_identical(wordlist2, wordlist1)
        )
        return False, is_nearly_identical

    @staticmethod
    def _validate_queried_sentence(sentence: str):
        """Validates the format of the input sentence."""
        if not isinstance(sentence, str):
            raise TypeError(
                "Input sentence should be str, while it is {}".format(type(sentence))
            )

    def query(self, sentence: str) -> Tuple[int, int]:
        """Returns the number of identical and nearly identical sentences to the input sentence.

        Args:
            sentence (str): the sentence to compare with

        Returns:
            (int): the number of identical sentences
            (int): the number of nearly identical sentences"""

        self._validate_queried_sentence(sentence)

        if not sentence.islower():
            sentence = sentence.lower()
            logger.info(
                "Input query sentence is not lowercase. Converted to lowercase."
            )

        queried_sentence_wordlist = self._sentencize(sentence)[0]
        truth_list_for_identical, truth_list_for_nearly_identical = list(
            zip(
                *(
                    self._compare_wordlist_pair(
                        queried_sentence_wordlist, sentence_wordlist
                    )
                    for sentence_wordlist in self.sentences
                )
            )
        )
        return sum(truth_list_for_identical), sum(truth_list_for_nearly_identical)
