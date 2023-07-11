# Script for recording EMG signals of a specific condition
# 
# To use, specify the condition name and recording duration (in seconds)
# as the first two arguments.
# 
# Ex: "python3 record_emg.py fire 30" will record data for the forward 
# condition during 30 seconds, and save it in the file fire.pkl in the 
# data folder.
#
# Created by Marco Simões (msimoes@dei.uc.pt)


from math import ceil
import time
from bitalino import BITalino
#from requests import post
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
import json

from ..configs import EMG_DATA_PATH, BITALINO_MAC_ADDRESS, BITALINO_ACQ_CHANNELS, BITALINO_SRATE


nSamples = 1000

def record(device, condition, running_time, plot=True):
    ''' performs the EMG recording for 'running_time' seconds
    and saves it in a pickle file'''
    
    signal = [] 

    # Start Acquisition
    device.start(BITALINO_SRATE, BITALINO_ACQ_CHANNELS)

    print("RECORDING STARTED!")

    start = time.time()
    current = time.time()
    while (current - start) < running_time:
        
        # Read samples
        r = np.array(device.read(nSamples))
        
        # add samples read for each arm
        signal.extend(r[:, -1].tolist())
        

        current = time.time()

        print('remaining: %d s' % ceil(running_time - (current - start)))

    
    # stops acquisition
    device.stop()
    print("RECORDING STOPPED!")
    
    # saves data to file
    with open('%s/%s.pkl' % (EMG_DATA_PATH, condition), 'wb') as f:
        pickle.dump(signal, f)    

    # plots the data
    if plot:
        plt.plot(range(len(signal)), signal)
        plt.show()


def main():
    ''' run in the format record_emg.py condition duration_in_secs'''


    condition = 'fire'
    if len(sys.argv) > 1:
        condition = sys.argv[1]

    running_time = 30
    if len(sys.argv) > 2:
        running_time = int(sys.argv[2])

    # Connect to BITalino
    device = BITalino(BITALINO_MAC_ADDRESS)

    # countdown of 3 seconds before recording start
    print("\n\nwill record '%s' for %d seconds!\n\nGet ready!" % (condition, running_time))
    for eta in range(3, 0, -1):
        print("will start in %d seconds"% eta)
        time.sleep(1)
    

    # record data
    record(device, condition, running_time)
        
    
    # Close connection
    device.close()

    

if __name__ == '__main__':
    main()