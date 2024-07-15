#!/usr/bin/python3

from websocket import create_connection
import requests
import json

class tasmota_plug:
    def __init__(self, ipv4, port = 80, name =''):
        self.ipv4 = ipv4
        self.port = port
        self.name = name
        self.url = f'http://{self.ipv4}:{self.port}/'

    def _send_command(self, command):
        r = requests.get(self.url + f'cm?cmnd={command}')
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            return ''

    def getStatus(self):
        return self._send_command(f'Status')

    def getPower(self, id = 1):
        return self._send_command(f'Power{id}')

    def setPower(self, value, id = 1):
        # value is 'on' or 'off'
        return self._send_command(f'Power{id}%20{value}')

    def getPulseTime(self, id = 1):
        return self._send_command(f'PulseTime{id}')

    def setPulseTime(self, seconds, id = 1):
        value = seconds + 100
        return self._send_command(f'PulseTime{id}%20{value}')

    def getPowerOnState(self):
        return self._send_command(f'PowerOnState')

    def setPowerOnState(self, value):
        # 0/OFF, 1/ON, 2/TOGGLE, 3 = last saved state, 4 = turn on and disable, 5 = after Pulsetime turns power on
        return self._send_command(f'PowerOnState{id}%20{value}')

class camilladsp_api:
    def __init__(self, ipv4 = '127.0.0.1', port = 1234):
        self.ipv4 = ipv4
        self.port = port
        self.url = f'ws://{self.ipv4}:{self.port}'
        self.ws = None

    def connect(self):
        try:
            self.ws = create_connection(self.url)
            return True
        except Exception as e:
            print('FailedConn')
            return False

    def getStateRunning(self):
        command='GetState'
        value='value'
        if self.ws is None:
            self.connect()

        if not self.ws is None:
            self.ws.send(json.dumps(command))
            retjson = json.loads(self.ws.recv())
            return retjson[command][value] == 'Running'
        else:
            return False

    def close(self):
        if not self.ws is None:
            self.ws.close()

