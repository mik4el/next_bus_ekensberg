# Next Bus Ekensberg
Application to find and visualize time for the next SL bus leaving from Ekensberg station, Stockholm, Sweden. 

# Todos
1. Tests for visualization
1. Make provisioning script installing e.g. vnc
1. Deploy to raspi with external screen
1. Make case for screen

# Nice to have features
1. Blinka ett tecken varje sekund eller liknande
1. “.” om datan är ok
1. “?” om fel med datan
1. “Zzz” istället för “X min” när “no bus"

Visa nästa buss när tiden kvar är 3 min

# Installing hardware
Download latest robopeak raspbian image from http://www.robopeak.com/docs/doku.php?id=product-rpusbdisp-downloads, then follow http://www.raspberrypi.org/documentation/installation/installing-images/mac.md

Insert the card, plugin an ethernet cable. Attach the screen. Power on the raspi and wait a few seconds.

Find the raspi in your network. Go to terminal and input:

nmap 10.0.0.1/24

Nmap can take a few minutes. Download from http://nmap.org/download.html#macosx

There are probably many devices in your network. If one device has port 22 open only it's probably the raspi.

Go to terminal and input with the ip you found:

ssh pi@10.0.0.14

password: raspberry

Don't run apt-get upgrade, it will overwrite the rpusbdisp support.

Install and setup your wifi: https://www.modmypi.com/blog/how-to-set-up-the-ralink-rt5370-wifi-dongle-on-raspian

Then for convenience, setup key based auth:

On the raspi:

cd ~

mkdir .ssh

chmod 700 .ssh

On your mac:

scp ~/.ssh/id_rsa.pub pi@10.0.0.14:~/.ssh/authorized_keys

On your raspi again:

chmod 600 .ssh/authorized_keys