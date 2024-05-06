import notifier
from socket import *
import subprocess
from time import sleep
from threading import Thread
from gpiozero import OutputDevice
import json


lights_relay = OutputDevice(2, active_high=True, initial_value=False)


def await_connection():
    with socket(AF_INET, SOCK_STREAM) as s:
        while True:
            try:
                s.connect(('google.com', 80))
                break
            except:
                pass
            sleep(2.5)


def start_notify():
    while True:
        try:
            notifier.handshake()
        except:
            pass
        sleep(2.5)


def parse_cmd(cmd: str, args: list):
    print(f'Received command: {cmd} {args}')
    if cmd == 'lights_state':
        if args[0] == 'on':
            lights_relay.on()
        elif args[0] == 'off':
            lights_relay.off()
        elif args[0] == 'get':
            pass
        else:
            return -1
        notifier.update_lights_state(lights_relay.value)
        return 0


def client_handler(client, info):
    print(f'Connection accepted: [{info}]')
    try:
        data = json.loads(client.recv(1024).decode())
        if 'command' in data.keys():
            code = parse_cmd(data['command'], data['args'])
            client.send(json.dumps({'response': code}).encode())
    except Exception as e:
        print(e)


def start_control_server():
    print('Starting server...')
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 6969))
        sock.listen()
        print('Listening...')
        while True:
            client, info = sock.accept()
            Thread(target=client_handler, args=(client, info)).start()


if __name__ == '__main__':
    Thread(target=start_notify, args=()).start()
    while True:
        print('Awaiting phone hotspot...')
        await_connection()
        print('Connected to phone hotspot')
        start_control_server()
