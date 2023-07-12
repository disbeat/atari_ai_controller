#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remote control an OSC server with your keyboard.

This program maps keypresses to OSC messages. Arrows for up, down, left, right and space for fire. R key for reset.

Created by Marco Simoes (msimoes@dei.uc.pt)
"""

import argparse
import sys

from pynput import keyboard
from time import sleep

from pythonosc import udp_client

DEFAULT_IP = "10.6.0.226"
DEFAULT_PORT = 5555
 
client = None

mapping = {"'r'": -1, 'Key.space': 1, 'Key.up': 2, 'Key.right': 3, 'Key.left': 4, 'Key.down': 5} 



def send_command(command):
    ''' Sends the command to the OSC server. '''
    global client
    print("sending command: " + str(command))
    client.send_message("/action", command)


def on_press(key):
    '''Check if key is mapped to a command and send it. '''

    if str(key) in mapping.keys():
        send_command(mapping[str(key)])
    elif key == keyboard.Key.esc:
        sys.exit()

def on_release(key):
    '''Send NOOP command when key is released.'''
    send_command(0)


def main():
    ''' Maps keypresses to OSC commands'''
    global client
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=DEFAULT_IP,
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()