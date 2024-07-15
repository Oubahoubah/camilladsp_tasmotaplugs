#!/usr/bin/python3

from websocket import create_connection
import requests
import json
from time import sleep
from cdspmon_lib import tasmota_plug, camilladsp_api

short_sleep = 2
long_sleep = 240

def camilladspmonitor():
    plug1 = tasmota_plug('192.168.0.1', name='plug1')
    plug2 = tasmota_plug('192.168.0.2', name='plug2')
    tasmota_plugs = [ plug1, plug2 ]

    print('configuring plugs...')
    print('- PowerOnState = OFF')
    for plug in tasmota_plugs:
        plug.setPowerOnState('OFF')

    print('- Pulsetime = 260 (4 minutes and 20 seconds)')
    for plug in tasmota_plugs:
        # 20 is the extra time to receive a power on request before switching off
        plug.setPulseTime(long_sleep + 20) 

    cdsp = camilladsp_api()
    while not cdsp.connect():
        print('Trying to reconnect to CamillaDSP API entry point.')
        sleep(short_sleep)

    while True:
        if cdsp.getStateRunning():
            print('CamillaDSP is running here!')
            for plug in tasmota_plugs:
                plug_r = plug.setPower('on')
                if len(plug_r) > 0:
                    print(plug_r)
            sleep(long_sleep)
        else:
            print('CamillaDSP is down :(')
            for plug in tasmota_plugs:
                plug_r = plug.setPower('off')
                if len(plug_r) > 0:
                    print(plug_r)
            sleep(short_sleep)

    cdsp.close()

if __name__ == "__main__":
    camilladspmonitor()

