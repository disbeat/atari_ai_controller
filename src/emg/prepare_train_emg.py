#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script for extracting features from EMG signals for training the classifier

It expects the existence of a pickle file with the names of each
condition in the data folder

To run, provide the window duration for the segmentation (in ms) as argument.

Ex: "python3 prepare_train_emg.py 250" split the signals in segments of 250ms and 
extract features for each segment

Created by Marco Simões (msimoes@dei.uc.pt)
'''

import numpy as np
import pickle
import sys
from configs import EMG_DATA_PATH, EMG_SEGMENTATION_WINDOW
from ai.talento import extract_features_from_emg_segment


condition_codes = {
    'rest': 0,
    'fire': 1
}




def extract_features(signal, cond, winlen):
    ''' Gets the signal of a specific condition, preprocesses it, 
    segments it into windows of length winlen, and extracts the features for each one. 
    It returns a table with the samples in the lines and features in the columns, plus a last column
    with the condition label '''

    n = signal.shape[0]

    # segmentation
    signal = np.reshape(signal, [n//winlen, winlen])
    
    # feature extraction (mean value for each segment)
    features = []
    for s in range(signal.shape[0]):
        features.append(extract_features_from_emg_segment(signal[s, :]))

    features = np.array(features)

    # condition label
    labels = np.ones(shape=[features.shape[0],1]) * condition_codes[cond]

    # combine features and labels in a table
    features = np.hstack((features, labels))

    return features


def main():
    ''' Run in the format prepare_train_emg.py window_size (in ms)'''
    
    window = EMG_SEGMENTATION_WINDOW
    if len(sys.argv) > 0:
        window = int(sys.argv[1])

    
    features = []

    for condition in condition_codes.keys():
        with open('%s/%s.pkl' % (EMG_DATA_PATH, condition), 'rb') as f:
            signal = pickle.load(f)

            features.append(extract_features(np.array(signal), condition, window))
    
    features = np.vstack(features)
    
    print(features)

    # saves features to file
    with open('%s/features.pkl' % EMG_DATA_PATH, 'wb') as f:
        pickle.dump(features, f)    


if __name__ == '__main__':
    main()