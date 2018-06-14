from nltk import tokenize
from nltk.stem.rslp import RSLPStemmer
import tflearn
import tensorflow as tf
import numpy as np
import os
import json
import pandas as pd
import random

# stemmer for portugues language
stemmer = RSLPStemmer()

def bag_of_words(docs, words, classes):
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


def main():
    # Preprocessing
    # Reading the crawled data
    df = pd.read_csv('magazine_products.csv', usecols=['Titulo', 'category'])

    # Creating the dataset
    dataset = []
    for category, title in zip(df['category'], df['Titulo']):
        # classes only geladeira/refrigerador and lavadora
        # replace frigobar with geladeira/refrigerador
        category = category.replace('/ ', '/').split(' ')[0].lower()
        if(category not in ('acessórios')):
            if(category in ('frigobar')): category = 'geladeira/refrigerador'
            dataset.append({'categoria': category, 'titulo': title})

    docs, words, classes = preprocessing(dataset)
    X, y = bag_of_words(docs, words, classes)

    # Shuffling the data so that the model doesn't overfit
    random.seed(a=12)
    random.shuffle(X)
    random.shuffle(y)
    X = np.array(X)
    y = np.array(y)

    # TensorFlow for building and training the classifier
    # Building the NN
    nn = tflearn.input_data(shape=[None, len(X[0])])
    nn = tflearn.fully_connected(nn, 10, activation='sigmoid')
    # Dropout so that the neural network don't memorize the data
    nn = tflearn.dropout(nn, 0.3)
    nn = tflearn.fully_connected(nn, 10, activation='sigmoid')
    nn = tflearn.fully_connected(nn, 10, activation='relu')    
    # Dropout so that the neural network don't memorize the data
    
    # Output layer, softmax as activation function (best for classification)
    nn = tflearn.fully_connected(nn, len(y[0]), activation='softmax')
    # Applys linear or logistic regression to the input
    nn = tflearn.regression(nn, optimizer='adam', loss='categorical_crossentropy')

    # Defining the deep neural network model and setting up the tensorboard
    model = tflearn.DNN(nn, tensorboard_dir='tflearn_logs')
    # Training using adam as optmizer and crossentropy loss function
    # Using 70% for training and 30% for validation(testing)
    model.fit(X, y, validation_set=0.3, batch_size=8, n_epoch=1000, show_metric=True)
    # Saving the trained model that ill be used for testing later
    model.save('model.tflearn')

if __name__ == '__main__':
    main()
