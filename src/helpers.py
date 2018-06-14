from nltk import tokenize
from nltk.stem.rslp import RSLPStemmer
import tflearn
import tensorflow as tf
import numpy as np
import os
import json
import pandas as pd
import random

"""
    Helpers including bow model and preprocessing
"""

# stemmer for portugues language
stemmer = RSLPStemmer()

def bag_of_words(docs, words, classes):
    """
        Creates the bag of words for every sentence/title in the docs
        @return:
            data = list of bag of words
            target = list of the target classes per sentece
    """
    # Creating our data
    data = []
    target = []
    # Empty array for the target
    target_empty = [0] * len(classes)

    for doc in docs:
        # Create a bow for each document
        bow = []
        # doc = (tokens, category)
        tokens = doc[0]
        # stemming words
        tokens = [stemmer.stem(word.lower()) for word in tokens]
        # Creating the bag of words
        for word in words:
            bow.append(1) if word in tokens else bow.append(0)
        data.append(bow)

        # Target is a 0 for each class and 1 for the current class
        target_row = list(target_empty)
        target_row[classes.index(doc[1])] = 1
        target.append(target_row)

    return data, target


def preprocessing(dataset):
    """
        Organize the dataset into classes, documents and words.
        @return:
            docs = list(tokens - > category)
            words: list of unique stemmed words
            classes: all unique classes
    """
    # Creating the lists
    classes = []
    docs = []
    words = []

    # Going through the dataset
    for data in dataset:
        # Tokenization of the title in data
        tokens = tokenize.word_tokenize((data['titulo'].replace('-', '')))
        # Adding the tokens to our words list
        words.extend(tokens)
        # For these tokens associate them to the class = document
        docs.append((tokens, data['categoria']))
        # Add the unique classes to our classes list
        if data['categoria'] not in classes:
            classes.append(data['categoria'])

    # Stemming = process of find the root of the word
    # Stem and lower each word also remove duplicates
    # Using list comprehension, it returns a new list
    words = [stemmer.stem(word.lower()) for word in words]
    # Using set to remove all of the duplicates
    words = list(set(words))

    return docs, words, classes