# Script for running the EMG controller to control the fire mecanism of River Raid
# 
# To use, specify the model to use (previously trained in the models folder), 
# the window size (in ms)
# 
# Ex: "python3 run_emg_controller.py --model 'svm' --window 250" will load the 
# svm model and evaluate the EMG at each 250 ms to send a new command to the 
# ATARI emulator server via OSC 
# 
#
# Created by Marco Simoes (msimoes@dei.uc.pt)


import numpy as np
from bitalino import BITalino
import pickle
import time
import argparse
import sys
import json
#from requests import post
from pythonosc import udp_client
from ..configs import EMG_MODELS_PATH, ATARI_SERVER_IP, ATARI_SERVER_PORT, BITALINO_ADDRESS, BITALINO_ACQ_CHANNELS, BITALINO_SRATE



client = None


def load_model(file_name):
    ''' loads a model from the models folder '''
    with open(f'{EMG_MODELS_PATH}/{file_name}.pkl', 'rb') as f:
        return pickle.load(f)


def establish_atari_connection():
    ''' establishes the connection with the ATARI emulator server via OSC'''
    client = udp_client.SimpleUDPClient(ATARI_SERVER_IP, ATARI_SERVER_PORT)
    
    return client


def send_action(prediction, client):
    ''' sends "FIRE" command to atari server via OSC'''
    client.send_message("/action", prediction)
    print("fire!")


def preprocess_signal(signal):
    ''' centers the signal around zero and rectifies the wave so all 
    values are positive'''

    # zero center
    signal = signal - 512

    # wave rectifier
    signal = np.abs(signal)

    return signal

def get_data(device, window):
    ''' reads a segment of EMG data from the device and returns the features'''
    r = np.array(device.read(window))
   
    # preprocess signal
    signal = preprocess_signal(r[:, -1])
    
    # extract features
    features = [np.mean(signal), np.std(signal)]

    return [features]

def make_predictions(model, device, window, client):
    ''' main loop for the EMG controller: get segments of data --> make prediction --> send action'''
    previous_pred = 0
    print('Acquiring')
    while True:
        data = get_data(device, window)
        prediction = model.predict(data)[0]
        if prediction != previous_pred:
            if prediction == 1:
                # if was rest and now is fire
                send_action(prediction, client)
                #post('http://127.0.0.1:8050/simulator', data={'data': json.dumps([prediction]), 'mode': 'stream'})
            
            previous_pred = prediction
            




def main():
    ''' main function for running the EMG controller, run as "python3 run_emg_controller.py --model 'svm' --window 250" '''

    client = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--window', type=int, required=False, default=250)
    parser.add_argument('--debug', type=bool, required=False, default=False)
    # Parse the argument
    args = parser.parse_args()
    model = load_model(args.model_name)
    
    if not args.debug:
        client = establish_atari_connection()
    
    print('connecing to bitalino')
    # Connect to BITalino
    device = BITalino(BITALINO_ADDRESS)
    print('connected')

    # Start Acquisition
    device.start(BITALINO_SRATE, BITALINO_ACQ_CHANNELS)


    try:
        make_predictions(model, device, args.window, client)
    except KeyboardInterrupt:
        pass
    finally:
        print('Finishing...')
        if client is not None:
            client.disconnect()

        # Close connection
        device.close()

if __name__ == '__main__':
    main()