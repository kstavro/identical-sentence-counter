# Identical Sentence Counter
The purpose of this package is to showcase some of Python's best practices.

## Contents

* [Introduction](#introduction)

* [Install](#install)

* [Functionality Walkthrough](#functionality-walkthrough)

* [Tests](#tests)

* [Changelog](#changelog)

## Introduction

This package provides a way to count the number of `identical` and `nearly identical` sentences in a lower case document with only periods `.` counting as punctuation separating the sentences. Identical and nearly identical sentences are defined as follows:

- Two sentences are identical if they have the same words in the order.
- Two sentences are nearly identical if we can remove one word from one sentence and they become identical.

## Install

To install the package, choose one of the following:

1. Simply `pip install git+https://github.com/kstavro/identical-sentence-counter.git`

2. If you want to further develop the package at the same time, then
- git clone the repo
- navigate to the folder of the package
- run `python setup.py install` for a simple installation or `python setup.py develop` for a development mode.

## Functionality Walkthrough

The following snippet shows how to easily calculate the number of `identical` and `nearly identical` sentences of a document to a `sentence`.

```
from identical_sentence_counter.sentence_counter import SentenceCounter

sentence_counter = SentenceCounter(<path_to_document>)

sentence_counter.query(sentence)
```

Notice that the `SentenceCounter` class can accept both strings corresponding to absolute paths, as well as `pathlib.Path` objects.

## Unittests

If the CI pipeline is not yet installed inside the repository for unittest automation, you can still run them yourself.

To run the unittests yourself, follow option 2. from 
[Install](#install) and once inside the package's folder, do the following:

```
pip install -r requirements.txt # only the first time required
pytest -v --cov=identical_sentence_counter --cov-report=term-missing
```

## Changelog

* 0.0.2: 
- [X] Updated class data structures for faster queries.

* 0.0.1: 
- [X] Initial implementation of the package.
