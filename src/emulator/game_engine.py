#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Runs the ATARI emulator receiving commands via OSC messages in the /action 
and sends OSC messages with the RAM values of interest

Created by Marco Simoes (msimoes@dei.uc.pt) and Andre Perrota (avperrota@dei.uc.pt)
'''

import sys
from random import randrange
from ale_py import ALEInterface, SDL_SUPPORT
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
from configs import ATARI_SERVER_PORT, SERVER_LOCALHOST

# global variables
action = 0
reward = 0

# ids of the RAM values of interest for sound play
ram_ids_of_interest = [7, 58, 104, 120, 121, 122, 123]
prev_ram_values = {ram_id: 0 for ram_id in ram_ids_of_interest}



def process_command(address, *args):
    ''' Every time a new OSC message is received in the /action address, 
        it saves the action in the global variable action, which is read in the main loop'''
    
    global action
    
    action = args[0]
    print("action = ", action)



async def run_atari():
    ''' Launches the ATARI emulator and enters the main loop that acts on the emulator every time a new action is received'''

    global action

    # initialize ATARI emulator
    ale = ALEInterface()
    
    # get & set the desired settings
    ale.setInt("random_seed", 123)
    
    # check if we can display the screen
    if SDL_SUPPORT:
        print("with sound")
        ale.setBool("sound", True)
        ale.setBool("display_screen", True)
    
    # Load the ROM file
    rom_file = sys.argv[1]
    ale.loadROM(rom_file)
    
    # Get the list of legal actions
    legal_actions = ale.getLegalActionSet()
    print('legal action set:', legal_actions)
    
    # get the list of available modes
    avail_modes = ale.getAvailableModes()
    print('available modes:', avail_modes)


    # main loop that acts on the emulator every time a new action is received
    while True:
        
        # action == -1 means reset the game
        if action == -1:
            ale.reset_game()
            action = 0
            continue

        # act on the emulator if action != 0
        reward = ale.act(ale.getLegalActionSet()[action])
        
        # get the RAM values
        ram = ale.getRAM()

        # check if any of the RAM values of interest have changed
        for ram_id in ram_ids_of_interest:
            
            # if so, send new value to OSC server
            if ram[ram_id] != prev_ram_values[ram_id]:
                
                # TODO: send OSC message with ram_id and ram[ram_id] to play sound outside of python
                print(ram_id, ram[ram_id])
                prev_ram_values[ram_id] = ram[ram_id]

        await asyncio.sleep(0)


async def init_main():
    ''' Set up OSC server and initializes atari'''
    
    # create dispatcher that listens for messages on /action
    dispatcher = Dispatcher()
    dispatcher.map("/action", process_command)
    
    # initialize OSC server
    server = AsyncIOOSCUDPServer((SERVER_LOCALHOST, 9999), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    
    await run_atari()  # Enter main loop of program
    
    transport.close()  # Clean up serve endpoint


def main():
    ''' Reads rom from file and initializes the main loop'''
    # parse command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} rom_file")
        sys.exit()

    asyncio.run(init_main())

if __name__ == "__main__":
    main()
