#!/usr/bin/python3

from time import sleep
from isthme_lib import tasmota_plug, camilladsp_api

short_sleep = 2
long_sleep = 240

def camilladspshutdown():
    plug1 = tasmota_plug('192.168.0.1', name='plug1')
    plug2 = tasmota_plug('192.168.0.2', name='plug2')
    tasmota_plugs = [ plug1, plug2 ]

    print('shutting down plugs...')
    print('- PowerOnState = OFF')
    for plug in tasmota_plugs:
        plug.setPower('off')
        sleep(short_sleep)

if __name__ == "__main__":
    camilladspshutdown()

