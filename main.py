
import time
import board
import csv
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

import adafruit_mpl3115a2

# while True:
#     print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
#     print("")
#     time.sleep(0.5)

def main():
    
    IMUSuccess = False
    altimeterSuccess = False
    initDone = False

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
    
    altimeter.sealevel_pressure = 103040


    epoch = time.time()

    #Loop through everything and collect data
    while True:
        with open("data.csv", 'a') as csvFile:
            try:
                IMUData = "IMU, " + str(time.time()-epoch) + ", " + str(IMU.acceleration[0]) + ", " + str(IMU.acceleration[1]) + ", " + str(IMU.acceleration[2]) + ", " + str(IMU.gyro[0]) + ", " + str(IMU.gyro[1]) + ", " + str(IMU.gyro[2]) + '\n'
                csvFile.write(IMUData)
            except Exception as e:
                print("Failed to write IMU Data: ")
                #print(e)
        with open("data.csv", 'a') as csvFile:
            try:
                altimeterData = "Altimeter, " + str(altimeter.pressure) + ", " + str(altimeter.altitude) + '\n'
                csvFile.write(altimeterData)
            except:
                print("Failed to write altimeter data")
                

main()


         
    
