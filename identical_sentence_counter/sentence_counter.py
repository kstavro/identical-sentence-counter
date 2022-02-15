# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <konstantinos.stavrop@gmail.com>
# For License information, see corresponding LICENSE file.

"""This file contains a class that given a text document that contains only lower case alphabet, space and .
(punctuation) character, it provides a method that calculates the number of identical and nearly identical sentences
inside the document to a queried sentence."""

import logging
from typing import Tuple, List, Union
from pathlib import Path

from identical_sentence_counter.data_structures import (
    get_duplicate_free_list_of_subtuples,
    create_cardinality_dict_for_doc_sentences,
    create_cardinality_dict_for_smaller_doc_sentences,
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
                a string or Path object that denotes a file path.
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

        # get text's sentences as a list of tuples of words
        sentences = self._sentencize(self.text)

        # check if the text is too long in terms of number of sentences
        self.max_number_sentences = max_number_sentences
        if len(sentences) > self.max_number_sentences:
            raise ValueError(
                "Input Document has more than {} sentences. Please replace it with a smaller document.".format(
                    self.max_number_sentences
                )
            )

        # create cardinality dictionaries of original document sentences and document sentences missing one word
        # (with tuples of words as keys)
        self.cardinality_dict_for_doc_sentences = (
            create_cardinality_dict_for_doc_sentences(sentences)
        )
        self.cardinality_dict_for_smaller_doc_sentences = (
            create_cardinality_dict_for_smaller_doc_sentences(sentences)
        )

        logger.info("Document and sentence data structures loaded")

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
    def _sentencize(text: str) -> List[Tuple[str]]:
        """Splits the instantiated text to sentences in the form of tuple of words.
        Returns a list of tuples of words."""
        sentences = [
            tuple(sentence.split())
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

    def _get_number_identical_wordtuples(self, wordtuple: Tuple[str]) -> int:
        """Returns the number of identical lists of words of the document to the input wordtuple"""
        return (
            self.cardinality_dict_for_doc_sentences.get(wordtuple, 0)
            # if wordtuple in self.cardinality_dict_for_doc_sentences.keys()
            # else 0
        )

    def _get_number_smaller_identical_wordtuples(self, wordtuple: Tuple[str]) -> int:
        """Returns the number of smaller nearly identical tuples of words of the document to the input wordtuple"""
        return sum(
            self.cardinality_dict_for_doc_sentences.get(smaller_tuple, 0)
            for smaller_tuple in get_duplicate_free_list_of_subtuples(wordtuple)
        )

    def _get_number_larger_identical_wordtuples(self, wordtuple: Tuple[str]) -> int:
        """Returns the number of nearly identical tuples of words of the document to the input wordtuple
        (only looking inside the sentences from self.sentence_dict that have length one more that the input's length)"""

        return self.cardinality_dict_for_smaller_doc_sentences.get(wordtuple, 0)

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

        queried_sentence_wordtuple = self._sentencize(sentence)[0]

        number_identical_wordtuples = self._get_number_identical_wordtuples(
            queried_sentence_wordtuple
        )

        number_smaller_nearly_identical_wordtuples = (
            self._get_number_smaller_identical_wordtuples(queried_sentence_wordtuple)
        )
        number_larger_nearly_identical_wordtuples = (
            self._get_number_larger_identical_wordtuples(queried_sentence_wordtuple)
        )

        # total number of nearly identical
        number_nearly_identical_wordtuples = (
            number_smaller_nearly_identical_wordtuples
            + number_larger_nearly_identical_wordtuples
        )
        return number_identical_wordtuples, number_nearly_identical_wordtuples
