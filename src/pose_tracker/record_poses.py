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
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import sys
import pickle

MY_SKELETON_ID = 0

pose_data = []

datapath = 'data'

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
    
    if args[1] == MY_SKELETON_ID:
        # skip timestamp and skeleton id
        pose = args[2:]
        pose_data.append(pose)
        
        print('num of recorded poses: ', len(pose_data))


def save_pose_data(condition):
    ''' writes pose data to file '''
    global pose_data
    pose_data = np.vstack(pose_data)
    
    # saves data to file
    with open('%s/%s.pkl' % (datapath, condition), 'wb') as f:
        pickle.dump(pose_data, f) 

dispatcher = Dispatcher()
dispatcher.map("/pose", record_pose)

ip = "127.0.0.1"
port = 6666

async def loop(duration=30):
    """Example main loop that only waits duration time before finishing"""
    
    await asyncio.sleep(duration)


async def init_main(condition, running_time):
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop(running_time)  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

    save_pose_data(condition)


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
    
    asyncio.run(init_main(condition, running_time))



if __name__ == "__main__":
    main()  