from twelve_tone.composer import Composer

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

def send_msg(client, note, msg=None, sleep=0.5):
    """
    sends an OSC message to the
    /weather address
    """
    client.send_message('/weather', note, )
    time.sleep(sleep)

def generate_tone_melody(client, notes, num):
    """
    Selects the tone row length
    depending on the rainfall value
    and then sends each to be
    sent over OSC
    """
    for i in range(num):
        if i > 11:
            i = i - 11
        send_msg(client, int(notes[i]))

def send_eod_signal(client):
    """
    Send note 24 to
    signal the end of a day
    """
    client.send_message('/weather', 24)
    time.sleep(.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=6449,
      help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port) # osc client.

    with open('data/data.txt') as data:
            content = data.readlines()
            c = Composer()
            for row in content:
                for x in range(2, 25):
                    c.compose() # create new tone row matrix
                    notes = c.matrix[0] # get tones from top row
                    num = int(row.split()[x]) # get each hour's rain data
                    print(num)
                    if num == 0:
                        send_msg(client, 0, sleep=0.1)
                        continue
                    elif num > 12:
                        # if more than 12, the tone 
                        # will be the difference of the two.
                        num = num - 12
                    generate_tone_melody(client, notes, num)
                send_eod_signal(client)
                # end of day
