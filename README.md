# AerospaceEngineeringClub

In Windows run `env\Scripts\Activate.ps1` to source python virtual environment

### To copy video from pi to computer

On your computer run `scp aerospace@IPADDRESS:~/rocket/video/VIDEONAME.h264 LOCALDESTINATION` replacing IPADDRESS with the raspberry pi's IP address, VIDEONAME with the name of the video file, and LOCALDESTINATION with where you want the file to be saved on your machine. Possible video names will be `vid0`, `vid1`, `vid2`, ..., `vid9`