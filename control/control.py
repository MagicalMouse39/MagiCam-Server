import notifier
from socket import *
import subprocess
from time import sleep
from threading import Thread
from gpiozero import OutputDevice
import json
import logging

logging.basicConfig(level=logging.INFO)

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
    logging.info(f'Connection accepted: [{info}]')
    try:
        data = json.loads(client.recv(1024).decode())
        if 'command' in data.keys():
            logging.info(f'Received {data["command"]} {data["args"]} from {info}')
            code = parse_cmd(data['command'], data['args'])
            client.send(json.dumps({'response': code}).encode())
    except Exception as e:
        logging.warning(f'An error has occurred whilst reading client data: {e}')


def start_control_server():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 6969))
        sock.listen()
        logging.info('Listening for clients...')
        while True:
            client, info = sock.accept()
            Thread(target=client_handler, args=(client, info)).start()


if __name__ == '__main__':
    Thread(target=start_notify, args=()).start()
    while True:
        logging.info('Awaiting phone hotspot...')
        await_connection()
        logging.info('Connected to phone hotspot!')
        logging.info('Starting control server...')
        start_control_server()
