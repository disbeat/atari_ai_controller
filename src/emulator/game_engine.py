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
from pythonosc import osc_message_builder
import asyncio
from pythonosc import udp_client
import argparse
import random
import time
from configs import ATARI_SERVER_IP, ATARI_SERVER_PORT, SOUND_SERVER_IP, SOUND_SERVER_PORT, ROM_FILE

# global variables
action = 0
reward = 0


def process_command(address, *args):
    ''' Every time a new OSC message is received in the /action address,
        it saves the action in the global variable action, which is read in the main loop'''

    global action

    action = args[0]
    #print("action = ", action)

def sendRam(client, ram):
    ''' Sends the RAM values of interest via OSC to the sound server'''
    msg = osc_message_builder.OscMessageBuilder(address = '/ram')
    for i in ram:
        msg.add_arg(i, arg_type='i')
    client.send(msg.build())



async def run_atari(sound_client, rom_file):
    ''' Launches the ATARI emulator and enters the main loop that acts on the emulator every time a new action is received'''

    global action

    # initialize ATARI emulator
    ale = ALEInterface()

    # get & set the desired settings
    ale.setInt("random_seed", 123)

    # check if we can display the screen
    if SDL_SUPPORT:
        # deactivate sound
        ale.setBool("sound", False)
        ale.setBool("display_screen", True)

    # Load the ROM file
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
        #ram size = 128
        sendRam(sound_client, ram)
        await asyncio.sleep(0.005)


async def init_main(atari_ip, atari_port, sound_port, rom_file):
    ''' Set up OSC server and initializes atari'''

    # create dispatcher that listens for messages on /action
    dispatcher = Dispatcher()
    dispatcher.map("/action", process_command)

    # initialize OSC server
    server = AsyncIOOSCUDPServer((atari_ip, atari_port), dispatcher, asyncio.get_event_loop())

    # initialize OSC sound client
    sound_client = udp_client.SimpleUDPClient(SOUND_SERVER_IP, sound_port)

    transport, protocol = await server.create_serve_endpoint()

    await run_atari(sound_client, rom_file)  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


def main():
    ''' Reads rom from file and initializes the main loop'''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", default=ROM_FILE, required=False,
        help="ROM game file to load in the emulator")
    parser.add_argument("--atari_ip", default=ATARI_SERVER_IP, required=False,
        help="The IP address for read commands (ATARI server)")
    parser.add_argument("--atari_port", default=ATARI_SERVER_PORT, required=False,
        help="The port for read commands (ATARI server)")
    parser.add_argument("--sound_port", default=SOUND_SERVER_PORT, required=False,
        help="The port for read commands (ATARI server)")
    args = parser.parse_args()


    


    asyncio.run(init_main(args.atari_ip, args.atari_port, args.sound_port, args.rom))

if __name__ == "__main__":
    main()