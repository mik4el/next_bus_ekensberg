# Next Bus Ekensberg
Application to find and visualize time for the next SL bus leaving from Ekensberg station, Stockholm, Sweden. 

# Todos
1. Make case for screen

# Nice to have features
1. Show the next next bus when time to next bus < 3min

# Installing hardware
Download latest robopeak raspbian image from http://www.robopeak.com/docs/doku.php?id=product-rpusbdisp-downloads, then follow http://www.raspberrypi.org/documentation/installation/installing-images/mac.md

Insert the card, plugin an ethernet cable. Attach the screen. Power on the raspi and wait a few seconds.

Find the raspi in your network. Go to terminal and input:

nmap 192.168.1.1/24

Nmap can take a few minutes. Download from http://nmap.org/download.html#macosx

There are probably many devices in your network. If one device has port 22 open only it's probably the raspi.

Go to terminal and input with the ip you found:

ssh pi@192.168.1.4

password: raspberry

Don't run apt-get upgrade, it will overwrite the rpusbdisp support.

Install and setup your wifi: https://www.modmypi.com/blog/how-to-set-up-the-ralink-rt5370-wifi-dongle-on-raspian

Then for convenience, setup key based auth:

On the raspi:

cd ~

mkdir .ssh

chmod 700 .ssh

On your mac:

scp ~/.ssh/id_rsa.pub pi@192.168.1.4:~/.ssh/authorized_keys

On your raspi again:

chmod 600 .ssh/authorized_keys

1) Stop text terminals from blanking
Change in /etc/kbd/config these two:
BLANK_TIME=0
POWERDOWN_TIME=0

2) Stop Xsession from blanking
Add to /etc/X11/xinit/xinitrc:
xset s noblank
xset s off
xset -dpms

3) In lightdm conf /etc/lightdm/lightdm.conf change xserver-command under [SeatDefaults] to:
xserver-command=X -s 0 -dpms