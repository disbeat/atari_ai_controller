"""Remote control an OSC server with your keyboard.

This program maps keypresses to OSC messages.
"""
import argparse
import sys

from pynput import keyboard
from time import sleep

from pythonosc import udp_client

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 5555

#[<Action.NOOP: 0>, <Action.FIRE: 1>, <Action.UP: 2>, <Action.RIGHT: 3>, <Action.LEFT: 4>, 
# <Action.DOWN: 5>, <Action.UPRIGHT: 6>, <Action.UPLEFT: 7>, <Action.DOWNRIGHT: 8>, <Action.DOWNLEFT: 9>, <Action.UPFIRE: 10>, <Action.RIGHTFIRE: 11>, <Action.LEFTFIRE: 12>, <Action.DOWNFIRE: 13>, <Action.UPRIGHTFIRE: 14>, <Action.UPLEFTFIRE: 15>, <Action.DOWNRIGHTFIRE: 16>, <Action.DOWNLEFTFIRE: 17>]

client = None

mapping = {'Key.space': 1, 'Key.up': 2, 'Key.right': 3, 'Key.left': 4, 'Key.down': 5}



def send_command(command):
    global client
    print("sending command: " + str(command))
    client.send_message("/action", command)


def on_press(key):

    if str(key) in mapping.keys():
        send_command(mapping[str(key)])
    elif key == keyboard.Key.esc:
        sys.exit()

def on_release(key):
    send_command(0)


def main():
    ''' maps keypresses to OSC commands'''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=DEFAULT_IP,
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    client.send_message("/action", 1)

    
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()