from twelve_tone.composer import Composer

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

def send_msg(client, note, msg=None):
    client.send_message('/weather', note)
    time.sleep(1)

def generate_tone_melody(notes, num):
    for i in range(num):
        send_msg(client, int(notes[i]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=6449,
      help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port) # osc client.

    with open('data.txt') as data:
            content = data.readlines()
            c = Composer()
            for row in content:
                for x in range(2, 25):
                    c.compose() # create new tone row matrix
                    notes = c.matrix[0] # get tones from top row
                    num = int(row.split()[x]) # get each hour's rain data
                    print(num)
                    if num == 0: 
                        # if no rain this hour
                        print('ZERO!!!!!!')
                        continue
                    elif num > 12:
                        # if more than 12, the tone 
                        # will be the difference of the two.
                        num = num - 12
                    generate_tone_melody(notes, num)

                # end of day