import tflearn
import tensorflow as tf
import numpy as np
import os
import pandas as pd
import random
import helpers

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

    docs, words, classes = helpers.preprocessing(dataset)
    X, y = helpers.bag_of_words(docs, words, classes)

    # Shuffling the data so that the model doesn't overfit
    random.shuffle(X)
    random.shuffle(y)
    X = np.array(X)
    y = np.array(y)

    # TensorFlow for building and training the classifier
    # Clearing any data from previous graphs
    tf.reset_default_graph()
    # Building the NN
    nn = tflearn.input_data(shape=[None, len(X[0])])
    nn = tflearn.fully_connected(nn, 10, activation='relu') 
    nn = tflearn.dropout(nn, 0.2)
    nn = tflearn.fully_connected(nn, 10, activation='sigmoid')
    # Dropout so that the neural network don't memorize the data and prevent overfitting
    nn = tflearn.fully_connected(nn, 10, activation='relu')
    # Output layer, softmax as activation function (best for classification)
    nn = tflearn.fully_connected(nn, len(y[0]), activation='softmax')
    # Applys linear or logistic regression to the input
    nn = tflearn.regression(nn, optimizer='adam', loss='categorical_crossentropy')

    # Defining the deep neural network model and setting up the tensorboard
    model = tflearn.DNN(nn, tensorboard_dir='data/tflearn_logs')
    # Training using adam as optmizer and crossentropy loss function
    # Using 70% for training and 30% for validation(testing)
    model.fit(X, y, validation_set=0.3, batch_size=12, n_epoch=500, show_metric=True)
    # Saving the trained model that ill be used for testing later
    model.save('model/model.tflearn')

if __name__ == '__main__':
    main()
