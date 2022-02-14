# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <k.stavropoulos@oxolo.com>
# For License information, see corresponding LICENSE file.
"""This file provides functions that compare whether two lists of words (strings) are identical or nearly identical, 
as well as a function that better formats a list of lists for faster retrieval."""

import os
import sys
from typing import List, Dict

from itertools import groupby
from copy import copy

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))


def sort_list_of_lists_lengthwise(
    list_of_lists: List[List[str]],
) -> Dict[int, List[str]]:
    """Reorganizes a list of lists (of strings) into a dictionary where each key is a (integer) list length
    and its respective value is the list of all the lists inside the input with length equal to the key.

    Args:
        list_of_lists (List[List[str]]): The input list of lists of strings

    Returns:
        Dict[int, List]: A dictionary with {key: value} where
            - key is an integer denoting a possible list length.
            - value is the list of all the elements of list_of_lists
                whose length matches the key."""

    # create the dictionary (unsorted)
    new_data_structure = dict(
        (length, list(lst)) for length, lst in groupby(list_of_lists, key=len)
    )
    # sort dict by key
    new_data_structure = dict(sorted(new_data_structure.items()))
    return new_data_structure


# sentences will already be split into words, hence the name of the function
def wordlists_are_identical(wordlist1: List[str], wordlist2: List[str]) -> bool:
    """Checks if two lists of words are identical.

    Two lists of words are identical if they have the same words in the same
    order."""

    return wordlist1 == wordlist2


def wordlists_are_nearly_identical(wordlist1: List[str], wordlist2: List[str]) -> bool:
    """Checks if wordlist1 is nearly identical to wordlist2,
    assuming len(wordlist1) == len(wordlist2) + 1.

    Two lists of words are nearly identical if we can remove one word from one
    list and they become identical."""

    len_wordlist1 = len(wordlist1)
    len_wordlist2 = len(wordlist2)

    # can be removed if we are 100% certain from outside
    # of the method that the lengths of the lists are appropriate.
    assert (
        len_wordlist1 == len_wordlist2 + 1
    ), "The length of {} must be 1 more than the length of {}.".format(
        wordlist1, wordlist2
    )

    # in case wordlist1 has only one word we can directly return True
    if len_wordlist1 == 1:
        return True

    # find the first index where the elements of the lists disagree
    index_of_first_different_element = 0
    while (
        wordlist1[index_of_first_different_element]
        == wordlist2[index_of_first_different_element]
    ):
        # if we get to the last element of the first list
        # we know the lists are nearly identical and can return True
        if (
            index_of_first_different_element == len_wordlist1 - 2
        ):  # this is the second to last element
            return True
        index_of_first_different_element += 1

    # pop the first different element from the first list
    # be careful to pop it from a copy not spoil the original list
    wordlist1_copy = copy(wordlist1)
    wordlist1_copy.pop(index_of_first_different_element)

    return wordlists_are_identical(wordlist1_copy, wordlist2)
