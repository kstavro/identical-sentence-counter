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

from identical_sentence_counter.comparison_utils import (
    sort_list_of_lists_lengthwise,
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
        max_number_sentences: int = 100_000,
    ):
        """The init function of the class.

        Args:
            doc_input (Union[Path, str]): The input document. Can be given both as
                a sting or Path object that denotes a file path.
            max_number_sequences (int): maximum number of sentences the document is allowed to have.
                Defaults to 100.000.
        """

        logger.info("Loading document...")
        self._validate_class_input(doc_input, max_number_sentences)

        with open(doc_input) as doc:
            text = doc.read()

        if not text.islower():
            text = text.lower()
            logger.info("Input text is not lowercase. Converted to lowercase.")
        self.text = text.strip()

        # get text's sentences as a list of lists of words
        sentences = self._sentencize(self.text)

        # check if the text is too long in terms of number of sentences
        self.max_number_sentences = max_number_sentences
        if len(sentences) > self.max_number_sentences:
            raise ValueError(
                "Input Document has more than 100.000 sentences. Please replace it with a smaller document."
            )

        # reorganize sentences into a dict according to list (sentence) lengths
        self.sentences_dict = sort_list_of_lists_lengthwise(sentences)

        logger.info("Document and sentence data structure loaded")

    @staticmethod
    def _validate_class_input(doc_input: str, max_number_sentences: int):
        """Validates the format of the input sentence."""
        if not isinstance(doc_input, Path) and not isinstance(doc_input, str):
            raise TypeError(
                "doc_input should be Path or str, while it is {}".format(
                    type(doc_input)
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
        return sentences

    @staticmethod
    def _validate_queried_sentence(sentence: str):
        """Validates the format of the input sentence."""
        if not isinstance(sentence, str):
            raise TypeError(
                "Input sentence should be str, while it is {}".format(type(sentence))
            )

    def get_number_identical_wordlists(self, wordlist: List[str]) -> int:
        """Returns the number of identical lists of words of the document to the input wordlist
        (only looking inside the sentences from self.sentence_dict that match the input's length)"""
        return (
            sum(
                wordlists_are_identical(wordlist, sentence)
                for sentence in self.sentences_dict.get(len(wordlist))
            )
            if len(wordlist) in self.sentences_dict.keys()
            else 0
        )

    def get_number_smaller_identical_wordlists(self, wordlist: List[str]) -> int:
        """Returns the number of nearly identical lists of words of the document to the input wordlist
        (only looking inside the sentences from self.sentence_dict that have length one less that the input's length)"""
        return (
            sum(
                wordlists_are_nearly_identical(wordlist, sentence)
                for sentence in self.sentences_dict.get(len(wordlist) - 1)
            )
            if len(wordlist) - 1 in self.sentences_dict.keys()
            else 0
        )

    def get_number_larger_identical_wordlists(self, wordlist: List[str]) -> int:
        """Returns the number of nearly identical lists of words of the document to the input wordlist
        (only looking inside the sentences from self.sentence_dict that have length one more that the input's length)"""
        return (
            sum(
                wordlists_are_nearly_identical(sentence, wordlist)
                for sentence in self.sentences_dict.get(len(wordlist) + 1)
            )
            if len(wordlist) + 1 in self.sentences_dict.keys()
            else 0
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

        number_identical_wordlists = self.get_number_identical_wordlists(
            queried_sentence_wordlist
        )

        number_smaller_nearly_identical_wordlists = (
            self.get_number_smaller_identical_wordlists(queried_sentence_wordlist)
        )
        number_larger_nearly_identical_wordlists = (
            self.get_number_larger_identical_wordlists(queried_sentence_wordlist)
        )

        # total number of nearly identical
        number_nearly_identical_wordlists = (
            number_smaller_nearly_identical_wordlists
            + number_larger_nearly_identical_wordlists
        )
        return number_identical_wordlists, number_nearly_identical_wordlists