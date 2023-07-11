# Script for recording pose snapshots of a specific condition
# 
# To use, specify the condition name and recording duration (in seconds)
# as the first two arguments.
# 
# Ex: "python3 record_poses.py left 30" will record data for the left 
# condition during 30 seconds, and save it in the file fire.pkl in the 
# data folder.
#
# Created by Marco Simões (msimoes@dei.uc.pt)


# pose format: timestamp, skeleton_id, x, y, z for each joint (25 joints)

import numpy as np
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import sys
import pickle
import time

#from configs import MY_SKELETON_ID, LOCALHOST, POSE_SERVER_PORT, POSE_DATA_PATH

# set up osc server
ATARI_SERVER_IP = "127.0.0.1"
ATARI_SERVER_PORT = 5555

SOUND_SERVER_IP = "127.0.0.1"
SOUND_SERVER_PORT = 6666

LOCALHOST = "localhost"
POSE_SERVER_PORT = 12345

MY_SKELETON_ID = 0

POSE_DATA_PATH = 'data/pose'
POSE_MODELS_PATH = 'models/pose'

EMG_DATA_PATH = 'data/emg'
EMG_MODELS_PATH = 'models/emg'

    
BITALINO_ADDRESS = "/dev/tty.BITalino-BD-37-Bluetoot" # "98:D3:91:FD:40:4D"

BITALINO_ACQ_CHANNELS = [0] # record A1 
BITALINO_SRATE = 1000




pose_data = []



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


def record_pose(address, *args):
    ''' records a pose snapshot sent via OSC '''
    global pose_data
    
    if args[0] == MY_SKELETON_ID:
        # skip skeleton id
        pose = args[1:]
        pose_data.append(pose)
        
    print('num of recorded poses: ', len(pose_data))


def save_pose_data(condition):
    ''' writes pose data to file '''
    global pose_data
    pose_data = np.vstack(pose_data)
    
    # saves data to file
    with open('%s/%s.pkl' % (POSE_DATA_PATH, condition), 'wb') as f:
        pickle.dump(pose_data, f) 


def init_server(condition, running):

    dispatcher = Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/pose", record_pose)
    
    server = ThreadingOSCUDPServer((LOCALHOST, POSE_SERVER_PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    


def main():
    ''' run in the format record_poses.py condition duration_in_secs'''

    condition = 'left'
    if len(sys.argv) > 1:
        condition = sys.argv[1]

    running_time = 30
    if len(sys.argv) > 2:
        running_time = int(sys.argv[2])

    # countdown of 3 seconds before recording start
    print("\n\nwill record '%s' for %d seconds!\n\nGet ready!" % (condition, running_time))
    for eta in range(3, 0, -1):
        print("will start in %d seconds"% eta)
        time.sleep(1)
    
    init_server(condition, running_time)



if __name__ == "__main__":
    main()  