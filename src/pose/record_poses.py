#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script for recording pose snapshots of a specific condition

To use, specify the condition name and recording duration (in seconds)
as the first two arguments.

Ex: "python3 record_poses.py --condition left --duration 30 --skel 0" will record data for the left 
condition during 30 seconds from skeleton 0, and save it in the file fire.pkl in the 
data folder.

Created by Marco Simões (msimoes@dei.uc.pt)
'''

# pose format: timestamp, skeleton_id, x, y, z for each joint (25 joints)

import argparse
import numpy as np
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import sys
import pickle
import time
import socket
from configs import MY_SKELETON_ID, SERVER_LOCALHOST, POSE_SERVER_PORT, POSE_DATA_PATH



pose_data = []
skel_id = None

def record_pose(address, *args):
    ''' Records a pose snapshot sent via OSC '''
    global pose_data
    
    if args[0] == MY_SKELETON_ID:
        # skip skeleton id
        pose = args[1:]
        pose_data.append(pose)
        
    print('num of recorded poses: ', len(pose_data))


def save_pose_data(condition):
    ''' Writes pose data to file '''
    global pose_data
    pose_data = np.vstack(pose_data)
    
    # saves data to file
    with open('%s/%s.pkl' % (POSE_DATA_PATH, condition), 'wb') as f:
        pickle.dump(pose_data, f) 


async def loop(duration=30):
    """ Runs the main loop for duration seconds"""
    
    await asyncio.sleep(duration)


async def init_main(condition, duration):
    ''' Inits OSC server and runs main loop for running_time seconds'''
    
    dispatcher = Dispatcher()
    dispatcher.map("/pose", record_pose)
    
    server = AsyncIOOSCUDPServer((SERVER_LOCALHOST, POSE_SERVER_PORT), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    
    await asyncio.sleep(duration)  # Wait for duration seconds for data to be recorded

    transport.close()  # Clean up serve endpoint

    save_pose_data(condition) # Save data to file


def main():
    ''' Run in the format record_poses.py condition duration_in_secs'''

    global skel_id

    parser = argparse.ArgumentParser()
    parser.add_argument('--condition', type=str, required=True)
    parser.add_argument('--duration', type=int, required=False, default=30)
    parser.add_argument('--skel', type=int, required=False, default=MY_SKELETON_ID)
    
    # Parse the argument
    args = parser.parse_args()
    skel_id = args.skel
    condition = args.condition
    running_time = args.duration
    
    # countdown of 3 seconds before recording start
    print("\n\nwill record '%s' for %d seconds using skel_id %d!\n\nGet ready!" % (condition, running_time, skel_id))
    for eta in range(3, 0, -1):
        print("will start in %d seconds"% eta)
        time.sleep(1)
    
    asyncio.run(init_main(condition, running_time))



if __name__ == "__main__":
    main()  