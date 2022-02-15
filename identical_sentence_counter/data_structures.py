# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <konstantinos.stavrop@gmail.com>
# For License information, see corresponding LICENSE file.
"""This file provides functions that compare whether two lists of words (strings) are identical or nearly identical, 
as well as a function that better formats a list of lists for faster retrieval."""

import os
import sys
from typing import List, Dict, Tuple, Any

from collections import Counter

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))


def get_duplicate_free_list_of_subtuples(tpl: Tuple[Any]) -> List[Tuple[Any]]:
    """Generates a duplicate-free list of all subtuples of the input tuple that are
    smaller by exactly one element.

    Args:
        tpl (Tuple[Any]): the input tuple

    Returns:
        List[Tuple[Any]]: the duplicate-free list of subtuples smaller by one
    """
    return list(dict.fromkeys(tpl[:i] + tpl[i + 1 :] for i in range(len(tpl))))


def create_cardinality_dict_for_doc_sentences(
    list_of_tuples: List[Tuple[str]],
) -> Dict[Tuple[str], int]:
    """Creates a dictionary with the elements of the input list of tuples
    as keys and their cardinalities inside the list as values.

    Args:
        list_of_tuples (List[Tuple[str]]): A list of tuples (of strings)

    Returns:
        Dict[Tuple[str], int]: The cardinality dictionary of the elements of the list
    """
    return Counter(list_of_tuples)


def create_cardinality_dict_for_smaller_doc_sentences(
    list_of_tuples: List[Tuple[str]],
) -> Dict[Tuple[str], int]:
    """Creates a dictionary with all possible smaller-by-one subtuples of elements of the input list of tuples
    as keys and the numbers of their supertuples inside the list as values.

    Args:
        list_of_tuples (List[Tuple[str]]): A list of tuples (of strings)

    Returns:
        Dict[Tuple[str], int]: A dictionary of smaller-by-one subtuples of elements of the list
            whose values are the number of supertuples inside list_of_tuples from which they can
            be obtained by the removal of one word.
    """
    list_of_smaller_tuples_by_one = []
    for tpl in list_of_tuples:
        # this is the only thing one needs to be careful:
        # not to doublecount eg "hello world" from "hello hello world"
        # as the former can be obtained in two ways from the latter
        duplicate_free_list_of_subtuples = get_duplicate_free_list_of_subtuples(tpl)
        list_of_smaller_tuples_by_one += duplicate_free_list_of_subtuples
    return Counter(list_of_smaller_tuples_by_one)
