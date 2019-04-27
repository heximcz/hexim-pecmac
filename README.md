# Controller for NCD.io board and Zabbix monitor

## Hardware

- 3-Channel Off-Board 98% Accuracy 100-Amp AC Current Monitor with IoT Interface [link](https://store.ncd.io/product/3-channel-off-board-98-accuracy-100-amp-ac-current-monitor-with-iot-interface/?attribute_pa_amperage=20-amp)
- RPI LCD1602 ADD-ON V1.0 [link](https://www.itead.cc/wiki/RPI_LCD1602_ADD-ON_V1.0)
- Raspberry Pi [link](https://www.raspberrypi.org/products/)

## Python packages

```
pip3 install fire
pip3 install adafruit-circuitpython-charlcd
pip3 install pyyaml
pip3 install smbus2
```

## Prerequisites

- create folder for ram disk where is stored zabbix data file:
```
mkdir /opt/ramdisk
```
- add this line to the /etc/fstab
```
ramdisk  /opt/ramdisk  tmpfs  defaults,size=5M,x-gvfs-show  0  0
```

## Install
```
cd /opt
git clone <this package>
cd ./hexim-pecmac
# print help
python3 ./ncdio.py
```
Important command is:
```
python3 ./ncdio.py run &
```
This command run this on background.
Enjoy!

## Source
[Adafruit character LCD](https://learn.adafruit.com/character-lcds/python-circuitpython)

## Run as service

- create file "ncdio.service" in /etc/systemd/system with this content:
```
[Unit]
Description=NCD.io driver
After=syslog.target

[Service]
User=root
Group=root
ProtectSystem=full
Type=simple
WorkingDirectory=/opt/hexim-pecmac
ExecStart=/usr/bin/python3 ncdio.py run
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
- after save run command:
```
systemctl enable ncdio
systemctl daemon-reload
systemctl start ncdio
```
