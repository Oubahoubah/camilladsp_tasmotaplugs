# camilladsp.monitor
CamillaDSP.monitor probes CamillaDSP status through its websocket to switch on Tasmota plugs to turn on your amplifiers when "Running". It can be installed as a systemd service using very little resources in the background so not to compromise the audio playback quality.

## Dependencies
Code has been kept as basic as possible:

      websocket
      requests
      json

## camilladsp.monitor.py
### Configuration
The '''camilladspmonitor()''' function begins with the declaration of the Tasmota plugs with their IP addresses, optionally with names (default = '') and port number (default = 80).

      # add/remove plugs here and set their IP addresses.
      plug1 = tasmota_plug('192.168.0.1', name='plug1')
      plug2 = tasmota_plug('192.168.0.2', name='plug2')
      tasmota_plugs = [ plug1, plug2 ]

If you add more plugs, don't forget to add them in the tasmota_plugs list. I'm sure I can make it simpler to set up :)

### Execution
Simply run camilladsp.monitorstatus.py from the console or a systemd service script.

    $ /usr/bin/python3 camilladsp.monitorstatus.py
    [...]

### Internals
A websocket is opened and kept alive to the CamillaDSP daemon and '''requests''' are issued to the Tasmota plugs (check out the cdspmon_lib.py file which contains '''tasmota_plug''' and '''camilladsp_api''' objects.

When starting, the Tasmota plugs will be configured :
- Pulsetime set to 260 seconds (4 minutes and 20 seconds)
- PowerOnState set to OFF (so the amps don't get powered up when mains are back after a failure).

Then a first loop will iterate every few seconds (2) to connect to CamillaDSP daemon.
Once connected, the next loop checks the status of CamillaDSP:
- if it is not '''Running''', every 2 seconds and plugs are switched off.
- if CamillaDSP is '''Running''' (processing audio), the tasmota plugs are switched on and a delay of 240 seconds is started. Switching on the Tasmota plugs will reset their Pulsetime timers to their initial value and won't expire.

## camilladsp.shutdown.py
### Configuration
The '''camilladspshutdown()''' function begins with the declaration of the Tasmota plugs with their IP addresses, optionally with names (default = '') and port number (default = 80).

    # add/remove plugs here and set their IP addresses.
    plug1 = tasmota_plug('192.168.0.1', name='plug1')
    plug2 = tasmota_plug('192.168.0.2', name='plug2')
    tasmota_plugs = [ plug1, plug2 ]

If you add more plugs, don't forget to add them in the tasmota_plugs list. I'm sure I can make it simpler to set up :)

### Execution
Simply run camilladsp.shutdown.py from the console or a systemd service script to SWITCH OFF your tasmota plugs. This script does not act as a daemon !!!

## camillamonitor.service
The configuration should reflect your system for:

    User=oubah
    ExecStart=~/bin/camilladsp.monitorstatus.py
    ExecStop=~/bin/camilladsp.shutdown.py
