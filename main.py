
import time
import board
import csv
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import busio
import adafruit_gps
import serial
import adafruit_mpl3115a2
import subprocess
import os

# while True:
#     print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
#     print("")
#     time.sleep(0.5)

def initFileStructure():
    if (not os.path.exists('~/video')):
        print("Making video directory")
        os.popen("mkdir video")
    print("video directory already exists")


def main():
    
    IMUSuccess = False
    altimeterSuccess = False
    initDone = False
    GPSSuccess = True

    #Initalize sensors
    for i in range(0,10):
        if initDone:
            break

        i2c = board.I2C()
        if IMUSuccess == False:
            try:
                IMU = LSM6DSOX(i2c)
                IMUSuccess = True
                print("Initialized IMU")
            except Exception as e:
                print("Failed to initialize IMU")
                print(e)
        
        if altimeterSuccess == False:
            try:
                altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
                altimeterSuccess  = True
                print("Initialized Altimeter")
            except Exception as e:
                print("Failed to initialize Altimeter")
                print(e)
        if GPSSuccess == True:
            try:
                uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
                gps = adafruit_gps.GPS(uart, debug=False)
                gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                gps.send_command(b"PMTK220, 500")
            except Exception as e:
                print("Failed to initialize GPS")
                print(e)
    if altimeterSuccess == True:
        altimeter.sealevel_pressure = 103040



    # create video directory and start recording video
    initFileStructure()
    files = os.popen("cd video; ls").read()
    print(type(files))
    for i in range (0,10):
        if ("vid" + str(i)) in files:
            pass
        else:
            filename = "vid" + str(i)  + ".h264"
            break
    subprocess.Popen("libcamera-vid --width 1280 --height 780 --timeout 6000 -o video/" + filename, shell=True)



    epoch = time.time()
    lastTime = time.time()
    #Loop through everything and collect data
    while True:
        print("ReadingData")

        # Read IMU Data
        if IMUSuccess:
            with open("data.csv", 'a') as csvFile:
                try:
                    IMUData = "IMU, " + str(time.time()-epoch) + ", " + str(IMU.acceleration[0]) + ", " + str(IMU.acceleration[1]) + ", " + str(IMU.acceleration[2]) + ", " + str(IMU.gyro[0]) + ", " + str(IMU.gyro[1]) + ", " + str(IMU.gyro[2]) + '\n'
                    csvFile.write(IMUData)
                except Exception as e:
                    print("Failed to write IMU Data: ")
                    #print(e)
        
        # Read altimeter Data
        if altimeterSuccess:
            with open("data.csv", 'a') as csvFile:
                try:
                    altimeterData = "Altimeter, " + str(altimeter.pressure) + ", " + str(altimeter.altitude) + '\n'
                    csvFile.write(altimeterData)
                except:
                    print("Failed to write altimeter data")
        
        # Read GPS Data
        try:
            gps.update()
        except Exception as e:
                    print("Failed to update gps")
                    print(e)

        try:
            if time.time() - lastTime >= 0.5:
                lastTime=time.time()
                if not gps.hasfix():
                    print("Waiting for gps fix")
                    continue
                data = str(time.time() - epoch) + "," + str(gps.timestamp_utc.tm_mon) + "/" + str(gps.timestamp_utc.tm_mday) + "/" + str(gps.timestamp_utc.tm_year) + str(gps.timestamp_utc.tm_hour) + ":" + str(gps.timestamp_utc.tm_min) + ":" + str(gps.timestamp_utc.tm_sec) + ","
                data = data + str(gps.latitude)  + "," + str(gps.latitude_degrees) + "," + str(gps.latitude_minutes) + "," + str(gps.latitude) + "," + str(gps.longitude) + "," + str(gps.longitude_degrees) + "," + str(gps.longitude_minutes) + "," + str(gps.fix_quality) + ","
                if gps.satellites is not None:
                  data = data + "#sats " + str(gps.satellites) + ","
                if gps.altitude_m is not None:
                    data = data + "alt " + str(gps.altitude_m) + ","
                if gps.speed_kmh is not None:
                    data = data + "khm " + str(gps.speed_kmh) + ","
                if gps.track_angle_deg is not None:
                    data = data + "track" + str(gps.track_angle_deg) + ","
                if gps.horizontal_dilution is not None:
                    data = data + "dilution" + str(gps.horizontal_dilution) + ","
                if gps.height_geoid is not None:
                    data = data + "geoid" + str(gps.height_geoid)
                with open("data.csv", 'a') as csvFile:
                    try:
                        csvFile.write(data)
                    except:
                        print("Failed to write gps data")
        except Exception as e:
                    print("Failed to update gps")
                    print(e)


main()


         
    
