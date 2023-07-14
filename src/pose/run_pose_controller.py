#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script for running the pose controller to control the plain movement in River Raid

To use, specify the model to use (previously trained in the models folder)

Ex: "python3 run_pose_controller.py --model svm --skel 0" will load the 
svm model and evaluate each pose from skel 0 to send a new command to the 
ATARI emulator server via OSC 


Created by Marco Simoes (msimoes@dei.uc.pt)
'''

# pose format: skeleton_id, x, y, z for each joint (25 joints)

import numpy as np
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
import asyncio
import sys
import pickle
import argparse
from configs import MY_SKELETON_ID, ATARI_SERVER_IP, ATARI_SERVER_PORT, POSE_MODELS_PATH, POSE_DATA_PATH, SERVER_LOCALHOST, POSE_SERVER_PORT
from ai import talento



client = None
model = None
previous_pred = 0
skel_id = None


def load_model(file_name):
    ''' Loads a model from the models folder '''
    with open(f'{POSE_MODELS_PATH}/{file_name}.pkl', 'rb') as f:
        return pickle.load(f)


def establish_atari_connection():
    ''' Establishes the connection with the ATARI emulator server via OSC'''
    client = udp_client.SimpleUDPClient(ATARI_SERVER_IP, ATARI_SERVER_PORT)
    
    return client




def send_action(prediction, client):
    ''' Sends command to atari server via OSC'''
    client.send_message("/action", prediction)
    print("sent action: ", prediction)


def read_pose(address, *args):
    ''' Records a pose snapshot sent via OSC '''
    global previous_pred
    
    print(args)
    if args[0] == MY_SKELETON_ID:
        # skip timestamp and skeleton id
        pose = args[1:]
        
        features = talento.extract_features_from_pose(pose)
        
        prediction = int(model.predict([features])[0])
        if prediction != previous_pred:
            send_action(prediction, client)
        #else:
        #    send_action(0, client)
        previous_pred = prediction


async def loop_forever():
    ''' Example main loop that runs forever. '''
    while True:
        await asyncio.sleep(1)


async def init_main():
    ''' Initializes OSC server and runs the main loop. '''
    dispatcher = Dispatcher()
    dispatcher.map("/pose", read_pose)
    
    server = AsyncIOOSCUDPServer((SERVER_LOCALHOST, POSE_SERVER_PORT), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop_forever()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint




def main():
    ''' Main function for running the pose controller, run as "python3 run_pose_controller.py --model 'svm'" '''
    global model, client, skel_id

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--debug', type=bool, required=False, default=False)
    parser.add_argument('--skel', type=int, required=False, default=MY_SKELETON_ID)
    
    # Parse the argument
    args = parser.parse_args()
    skel_id = args.skel
    
    model = load_model(args.model)
    
    if not args.debug:
        client = establish_atari_connection()
   
    asyncio.run(init_main())

if __name__ == '__main__':
    main()
