'''
Module for talento students to implement their AI

Functions are called from other modules

created by Marco Simoes (msimoes.dei.uc.pt)
'''
import numpy as np

def extract_features_from_pose(pose):
    ''' Given a pose, extracts the features for classification '''
    
    # preprocess pose
    pose = np.reshape(pose, [25, 3])
    
    # feature 1 - distance between hands
    f1 = np.linalg.norm(pose[4, :] - pose[7, :])

    # feature 2 - distance between left hand and left foot
    f2 = np.linalg.norm(pose[4, :] - pose[22, :])

    # feature 3 - distance between right hand and right foot
    f3 = np.linalg.norm(pose[7, :] - pose[19, :])
    
    # feature 4 - distance between left hand and head
    f4 = np.linalg.norm(pose[4, :] - pose[3, :])

    # feature 5 - distance between right hand and head
    f5 = np.linalg.norm(pose[7, :] - pose[3, :])

    features = [f1, f2, f3, f4, f5]
    return features

def extract_features_from_emg_segment(segment):
    ''' Given a segment of EMG signal, extracts the features for classification'''
    # feature 1 - mean value
    f1 = np.mean(segment)

    # feature 2 - standard deviation
    f2 = np.std(segment)

    features = [f1, f2]
    return features




def preprocess_signal(signal):
    ''' Centers the signal around zero and rectifies the wave so all 
    values are positive'''

    # zero center
    signal = signal - 512

    # wave rectifier
    signal = np.abs(signal)

    return signal


def predict_from_emg_features(features, model):
    ''' Given a set of features, predicts the class using the model '''

    prediction = int(model.predict(features)[0])

    return prediction


def predict_from_pose_features(features, model):
    ''' Given a set of features, predicts the class using the model '''

    prediction = int(model.predict(features)[0])

    return prediction