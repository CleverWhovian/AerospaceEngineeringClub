#!/bin/bash
cd /usr/aerospace/rocket
source env/bin/activate
python3 imu2.py


add to /etc/rc.local
protection 755
/home/pi/startup_runner.sh &
