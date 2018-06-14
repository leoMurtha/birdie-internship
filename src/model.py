from nltk import tokenize
from nltk.stem.rslp import RSLPStemmer
import os
import json
import pandas as pd
import datetime
import numpy as np
stemmer = RSLPStemmer()

#https://machinelearnings.co/text-classification-using-neural-networks-f5cd7b8765c6

def bag_of_words(docs, words, classes):
    # Creating our data
    data = []
    output = []
    # Empty array for the output
    output_empty = np.zeros((1, len(classes)))
    
    for doc in docs:
        # Create a bow for each document
        bow = []
        # doc = (tokens, category)
        tokens = doc[0]
        # stemming words
        tokens = [stemmer.stem(word.lower()) for word in tokens]
        # Creating the bag of words
        bow = [bow.append(1) if word in tokens else bow.append(0) for word in words]
        output_row = list(output_empty)
        output_row[categories.index(doc[1])]
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
        if data['categoria'] not in classes: classes.append(data['categoria'])

    # Stemming = process of find the root of the word
    # Stem and lower each word also remove duplicates
    # Using list comprehension, it returns a new list
    words = [stemmer.stem(word.lower()) for word in words]
    # Using set to remove all of the duplicates
    words = list(set(words))

    return docs, words, classes

def main():
    # Preprocessing
    # Reading the crawled data
    df = pd.read_csv('magazine_products.csv', usecols=['Titulo', 'category'])

    # Creating the dataset
    dataset = []
    for category, title in zip(df['category'], df['Titulo']):
        dataset.append({'categoria': category, 'titulo': title})

    docs, words, classes = preprocessing(dataset)
    X, y = bag_of_words(docs, words, classes)

if __name__ == '__main__':
    main()