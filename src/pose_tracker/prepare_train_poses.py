# Script for extracting features from poses for training the classifier
# 
# It expects the existence of a pickle file with the names of each
# condition in the data folder
# 
# To run, provide the window duration for the segmentation (in ms) as argument.
#
# Ex: "python3 prepare_train_emg.py 250" split the signals in segments of 250ms and 
# extract features for each segment
#
# Created by Marco Simões (msimoes@dei.uc.pt)


import numpy as np
import pickle
import sys


# configs
datapath = 'data'

condition_codes = {
    'left': 4,
    'right': 3,
    'up': 2,
    'down': 5
}




def extract_features(poses, cond):
    ''' given a pose, extracts the features for classification '''
    
    # normalize based on joint 0
    for axis in range(3):
        poses[:, axis::3] = poses[:, axis::3] - poses[:, axis]
    
    # all normalized joints will serve as features
    features = poses

     # condition label
    labels = np.ones(shape=[features.shape[0], 1]) * condition_codes[cond]

    # combine features and labels in a table
    features = np.hstack((features, labels))
    return features


def main():
    ''' run in the format prepare_train_poses.py'''
   
    
    features = []

    for condition in condition_codes.keys():
        with open('%s/%s.pkl' % (datapath, condition), 'rb') as f:
            poses = pickle.load(f)

            features.append(extract_features(np.array(poses), condition))
    
    features = np.vstack(features)
    
    print(features)

    # saves features to file
    with open('%s/features.pkl' % datapath, 'wb') as f:
        pickle.dump(features, f)    


if __name__ == '__main__':
    main()