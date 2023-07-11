# Script for running the pose controller to control the plain movement in River Raid
# 
# To use, specify the model to use (previously trained in the models folder)
# 
# Ex: "python3 run_pose_controller.py --model 'svm'" will load the 
# svm model and evaluate each pose to send a new command to the 
# ATARI emulator server via OSC 
# 
#
# Created by Marco Simoes (msimoes@dei.uc.pt)

# pose format: timestamp, skeleton_id, x, y, z for each joint (25 joints)

import numpy as np
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import sys
import pickle
import argparse

MY_SKELETON_ID = 0


datapath = 'data'
models_path = 'models'


client = None
model = None
previous_pred = 0


def load_model(file_name):
    ''' loads a model from the models folder '''
    with open(f'{models_path}/{file_name}.pkl', 'rb') as f:
        return pickle.load(f)


def establish_atari_connection():
    ''' establishes the connection with the ATARI emulator server via OSC'''
    client = udp_client.SimpleUDPClient(ATARI_SERVER_IP, ATARI_SERVER_PORT)
    
    return client



def extract_features(pose):
    ''' given a pose, extracts the features for classification '''
    # preprocess pose
    pose = np.array(pose)

    # normalize based on joint 0
    for axis in range(3):
        pose[axis::3] = pose[axis::3] - pose[axis]
    
    # all normalized joints will serve as features
    features = pose
    return features

def send_action(prediction, client):
    ''' sends "FIRE" command to atari server via OSC'''
    client.send_message("/action", prediction)
    print("fire!")


def read_pose(address, *args):
    ''' records a pose snapshot sent via OSC '''
    global previous_pred
    
    if args[1] == MY_SKELETON_ID:
        # skip timestamp and skeleton id
        pose = args[2:]
        
        features = extract_features(pose)
        
        prediction = model.predict(features)[0]
        if prediction != previous_pred:
            send_action(prediction, client)
            previous_pred = prediction
            print("action = ", prediction)


dispatcher = Dispatcher()
dispatcher.map("/pose", read_pose)

ip = "127.0.0.1"
port = 6666

async def loop_forever():
    """Example main loop that only waits duration time before finishing"""
    while True:
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop_forever()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint




def main():
    ''' main function for running the pose controller, run as "python3 run_pose_controller.py --model 'svm'" '''
    global model, client

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--debug', type=bool, required=False, default=False)
    # Parse the argument
    args = parser.parse_args()
    model = load_model(args.model_name)
    
    if not args.debug:
        client = establish_atari_connection()
   
    asyncio.run(init_main())



if __name__ == "__main__":
    main()