# AerospaceEngineeringClub

In Windows run `env\Scripts\Activate.ps1` to source python virtual environment

## Connecting to raspberry pi

1. Start a hotspot with the name and password found in our Google Drive under AV Bay resources. The Raspberry Pi will automatically connect to this.

2. Find the IP address of the raspberry pi. In `Settings->Mobile Hotspot` on Windows 
[IP Address](docs\ip.png)
### To copy video from pi to computer

On your computer run `scp aerospace@IPADDRESS:~/rocket/video/VIDEONAME.h264 LOCALDESTINATION` replacing IPADDRESS with the raspberry pi's IP address, VIDEONAME with the name of the video file, and LOCALDESTINATION with where you want the file to be saved on your machine. Possible video names will be `vid0`, `vid1`, `vid2`, ..., `vid9`