from __future__ import print_function

import json
from arcadeshelves.opc import Client

def parse_layout(options):
    print('    parsing layout file')

    coordinates = []
    for item in json.load(open(options.layout)):
        if 'point' in item:
            coordinates.append(tuple(item['point']))
    return coordinates

def connect_to_server(options):
    client = Client(options.server)
    if client.can_connect():
        print('    connected to %s' % options.server)
    else:
        # can't connect, but keep running in case the server appears later
        print('    WARNING: could not connect to %s' % options.server)
    return client
