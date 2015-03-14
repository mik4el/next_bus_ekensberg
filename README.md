# Next Bus Ekensberg
Application to find and visualize time for the next SL bus leaving from Ekensberg station, Stockholm, Sweden. 

# Suggested hardware
Raspberry B+, Wifi USB Nano (WiFi-R-Pi), 2.8 TFT Rpusbdisp (http://www.robopeak.com/data/doc/rpusbdisp/RPUD01-rpusbdisp_datasheet-enUS.1.2.pdf) with 3D printed enclosure (see folder rpusbdisp_enclosure in repo).

# Todos
1. Make numbers little bigger
1. Show the next next bus when time to next bus < 3min
1. Fix bug that next update takes 30min when API shows error, should poll every minute:
```
{u'ExecutionTime': 4254, u'ResponseData': {u'LatestUpdate': u'0001-01-01T00:00:00', u'Buses': [], u'Ships': [], u'StopPointDeviations': [], u'Trams': [], u'DataAge': 0, u'Trains': [], u'Metros': []}, u'Message': u'Could not retrive information for buses, trains or trams.', u'StatusCode': 5322}
```
1. Fix rare bug
```
ValueError: No JSON object could be decoded
    raise ValueError("No JSON object could be decoded")
  File "/usr/lib/python2.7/json/decoder.py", line 383, in raw_decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python2.7/json/decoder.py", line 365, in decode
    return _default_decoder.decode(s)
  File "/usr/lib/python2.7/json/__init__.py", line 326, in loads
    return json.loads(self.text, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/models.py", line 799, in json
    api_result = api_request.json()
  File "/home/pi/source/next_bus_ekensberg/next_bus.py", line 90, in get_data_from_api
    api_result = self.get_data_from_api()
  File "/home/pi/source/next_bus_ekensberg/next_bus.py", line 98, in get_minutes_to_next_bus
    data = self.get_minutes_to_next_bus()
  File "/home/pi/source/next_bus_ekensberg/next_bus.py", line 176, in tick
    self.tick()
  File "/home/pi/source/next_bus_ekensberg/next_bus.py", line 194, in run
    self.run()
  File "/usr/lib/python2.7/threading.py", line 552, in __bootstrap_inner
Traceback (most recent call last):
```

# Installing hardware
Download latest robopeak raspbian image from http://www.robopeak.com/docs/doku.php?id=product-rpusbdisp-downloads, then follow http://www.raspberrypi.org/documentation/installation/installing-images/mac.md

Insert the card, plugin an ethernet cable. Attach the screen. Power on the raspi and wait a few seconds.

Find the raspi in your network. Go to terminal and input:
`nmap 192.168.1.1/24`

Nmap can take a few minutes. Download from http://nmap.org/download.html#macosx

There are probably many devices in your network. If one device has port 22 open only it's probably the raspi.

Go to terminal and input with the ip you found:

```
ssh pi@192.168.1.4
password: raspberry
```

Don't run apt-get upgrade, it will overwrite the rpusbdisp support.

Install and setup your wifi: https://www.modmypi.com/blog/how-to-set-up-the-ralink-rt5370-wifi-dongle-on-raspian

Then for convenience, setup key based auth:

On the raspi:
```
cd ~
mkdir .ssh
chmod 700 .ssh
```

On your mac:
```
scp ~/.ssh/id_rsa.pub pi@192.168.1.4:~/.ssh/authorized_keys
```

On your raspi again:
```
chmod 600 .ssh/authorized_keys
```

Stop text terminals from blanking, change in /etc/kbd/config these two:
```
BLANK_TIME=0
POWERDOWN_TIME=0
```

Stop Xsession from blanking. Add to /etc/X11/xinit/xinitrc:
```
xset s noblank
xset s off
xset -dpms
```

Stop Lightdm from blanking. In lightdm conf /etc/lightdm/lightdm.conf change xserver-command under [SeatDefaults] to:
```
xserver-command=X -s 0 -dpms
```