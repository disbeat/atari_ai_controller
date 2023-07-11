#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script for training model to classify conditions based on features

To use, specify the model to use (svm, logistic_regression, etc)

Ex: "python3 train_model.py --type 'pose' --model 'svm'" will train an SVM model for pose files

Additional, to evaluate the performance of the model, add the parameter 
--train_and_evaluate set to True

Ex: "python3 train_model.py --type 'emg' --model 'svm' --train_and_evaluate True"
will train and evaluate an SVM model for EMG files

Created by Marco Simoes (msimoes@dei.uc.pt) and Nuno Lourenco (naml@dei.uc.pt)
'''

import numpy as np
import argparse
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn import svm, linear_model
from requests import post
from configs import EMG_DATA_PATH, POSE_DATA_PATH, EMG_MODELS_PATH, POSE_MODELS_PATH

data_path = ''
models_path = ''


def train_model(data, model):
    ''' Trains a model based on the data in the file features.pkl, labels are in the last column '''
    
    # separates features from labels
    features  = data[:,:-1]
    actions = data[:,-1]
    
    # trains the model
    model.fit(features, actions)
    
    return model


def train_and_evaluate(data, model):
    ''' Trains and evaluates a model based on the data in the file features.pkl, labels are in the last column'''
    
    
    # separates features from labels
    features  = data[:,:-1]
    actions = data[:,-1]

    # plots feature_1 vs feature_2 in a scatter plot, different classes represented by different colors
    rel = sns.scatterplot(x=features[:,0], y=features[:,1], hue=actions)
    rel.set(title='Data Distribution')
    
    
    # splits data into training and test sets
    features_train, features_test, actions_train, actions_test = train_test_split(features, actions, train_size = 0.7, test_size = 0.3, random_state = 100)

    # trains the model
    model.fit(features_train, actions_train)
    
    # evaluates the model on the training data
    predictions = model.predict(features_train)
    cm = confusion_matrix(actions_train, predictions)
    #disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    #post('http://127.0.0.1:8050/matrix/predict', data={'data': json.dumps(cm.tolist())})
    
    # evaluates the model on the test data
    predictions = model.predict(features_test)
    cm = confusion_matrix(actions_test, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    #post('http://127.0.0.1:8050/matrix/test', data={'data': json.dumps(cm.tolist())})
    return model


def load_dataset():
    ''' Loads the dataset from the file features.pkl '''
    
    with open('%s/features.pkl' % data_path, 'rb') as f:
        data = pickle.load(f)
    #post('http://127.0.0.1:8050/features', data={'data': json.dumps([data[:,0].tolist(), data[:,1].tolist(), data[:,2].tolist()]), 'mode': 'batch'})
    
    return data




def main():
    ''' Trains an svm or logistic regression model based on the data in the file features.pkl '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, required=True, const='emg', default='emg', nargs='?')
    parser.add_argument('--model', type=str, required=True, const='svm', default='svm', nargs='?')
    parser.add_argument('--train_and_evaluate', type=bool, required=False, const=False, default=False, nargs='?')
    
    # Parse the argument
    args = parser.parse_args()
    
    if args.type == 'emg':
        data_path = EMG_DATA_PATH
        models_path = EMG_MODELS_PATH
    else:
        data_path = POSE_DATA_PATH
        models_path = POSE_MODELS_PATH


    if args.model == 'svm':
        model = svm.SVC()
    else:
        model = linear_model.LogisticRegression()


    
    # loads dataset from file
    dataset = load_dataset()
    
    if args.train_and_evaluate:
         model = train_and_evaluate(dataset, model)
    
    # trains the model
    model = train_model(dataset, model)
    
    

    # saves the model to file
    with open('%s/%s.pkl' % (models_path, args.model), 'wb') as f:
        pickle.dump(model,f)


if __name__ == '__main__':
    main()