from socket import *
import struct
from time import sleep
import json

MAGICAM_ID = 'MagiCam!'

def get_gateway():
    with open('/proc/net/route', 'rt') as fin:
        for line in fin.readlines()[1:]:
            gateway = line.split()[2]
            if gateway == '00000000': continue
            return inet_ntoa(struct.pack('<L', int(gateway, 16)))


ip = get_gateway()


def handshake():
    with socket(AF_INET, SOCK_STREAM) as s:
        while True:
            try:
                s.connect((ip, 6968))
                s.send(MAGICAM_ID.encode())
                break
            except:
                sleep(2.5)


def send_data(name: str, *values):
    values = list(map(lambda x: str(x), values))
    with socket(AF_INET, SOCK_STREAM) as s:
        try:
            s.connect((ip, 6969))
            s.send(json.dumps({'name': name, 'values': values}).encode())
        except Exception as e:
            print(f'An error occurred whilst sending data: {name} {values}')
            print(e)


def update_lights_state(state: bool):
    send_data('lights_state', state)
