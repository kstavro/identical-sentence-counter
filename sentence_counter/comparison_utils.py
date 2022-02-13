# %%
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <k.stavropoulos@oxolo.com>
# For License information, see corresponding LICENSE file.
"""This file provides functions that compare whether two lists of words (strings) are identical or nearly identical"""

import os
import sys
from typing import List

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

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

    # these two values might already be precomputed from outside of the method
    # however I chose to not put them as optional arguments in the method for readability and
    # correctness reasons, albeit sacrificing a tiny bit of inference speed.
    len_wordlist1 = len(wordlist1)
    len_wordlist2 = len(wordlist2)

    # this check costs some time and can be removed if we are certain from outside
    # of the method that the lengths of the lists are appropriate.
    if len_wordlist1 != len_wordlist2 + 1:
        raise ValueError(
            f"The length of {wordlist1} must be 1 more than the length of {wordlist2}."
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
    wordlist1.pop(index_of_first_different_element)

    return wordlists_are_identical(wordlist1, wordlist2)
