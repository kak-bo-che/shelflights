#!/usr/bin/env python
from __future__ import print_function
from arcadeshelves.util import parse_layout, connect_to_server
from lava_lamp import LavaLamp
from display_off import DisplayOff
import sys
import optparse
import signal

class Daemon(object):
    def __init__(self):
        self.options = self.parse_args()
        self.program_number_file = self.options.program_number_file
        self.change_display = False
        self.coordinates = parse_layout(self.options)
        self.client = connect_to_server(self.options)
        signal.signal(signal.SIGHUP, self.handler)

    def parse_args(self):
        parser = optparse.OptionParser()
        parser.add_option('-l', '--layout', dest='layout',
                            action='store', type='string',
                            help='layout file')
        parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
                            action='store', type='string',
                            help='ip and port of server')
        parser.add_option('-f', '--fps', dest='fps', default=20,
                            action='store', type='int',
                            help='frames per second')
        parser.add_option('-n', '--program_number_file', type='string',
                            help='file with scene index to use, updated with HUP signal')

        options, args = parser.parse_args()

        if not options.layout:
            parser.print_help()
            print('ERROR: you must specify a layout file using --layout')
            sys.exit(1)
        return options

    def clear(self):
        pixels = [(0,0,0)]*len(self.coordinates)
        self.client.put_pixels(pixels, channel=0)

    def handler(self, signum, frame):
        print('Signal handler called with signal', signum)
        self.change_display=True

    def run(self):
        scenes = {
            0: DisplayOff,
            1: LavaLamp,
        }
        # lava_lamp = LavaLamp(self.coordinates, self.client, self.options)
        while True:
            self.change_display = False
            with open(self.program_number_file,'r') as f:
                program_number = int(f.read())
            print("Loading Program {}".format(program_number))
            scene = scenes.get(program_number, DisplayOff)(self.coordinates, self.client, self.options)
            while (self.change_display == False):
                scene.run_once()
            self.clear()

if __name__ == "__main__":
    daemon = Daemon()
    daemon.run()

