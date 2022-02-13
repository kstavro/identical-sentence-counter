# Identical Sentence Counter
This is a playground package.

## Contents

* [Introduction](#introduction)

* [Install](#install)

* [Functionality Walkthrough](#functionality-walkthrough)

* [Additional attributes for Spacy](#additional-attributes-for-spacy)

* [Details](#details)

* [Changelog](#changelog)

## Introduction

This package provides a way to count the number of `identical` and `nearly identical` sentences in a lower case document with only periods `.` counting as punctuation separating the sentences. Identical and nearly identical sentences are defined as follows:

- Two sentences are identical if they have the same words in the order.
- Two sentences are nearly identical if we can remove one word from one sentence and they become identical.

## Install

To install the package, choose one of the following:

1. Simply `pip install 

2. If you want to further develop the package at the same time, then
- git clone the repo
- navigate to the folder of the package
- run `python setup.py install` for a simple installation or `python setup.py develop` for a development mode.

## Functionality Walkthrough

## Details

This section is reserved to describe more in detail what each function in the whole code does. To be updated in the
future.

## Changelog

* 0.0.1: 
- [X] Initial implementation of the pachage.