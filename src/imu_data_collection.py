#purpose of this file is to extract IMU data into a .bag file for a specified duration in seconds
#the user should be able to properly name the .bag file and specify the duration.
#interfacing should be done through the command line.
#First, will work on the launching/killing of processes for the desired amount of time, then
#we will implement the command line interfacing

from subprocess import Popen, PIPE
import time
import os
import signal
import re

def collectData(fileName, duration=5):
    print("Launching imu.launch")
    proc = Popen(['roslaunch', 'axis_mapping_web_app', 'imu.launch'])
    #give process 1s to initialize
    time.sleep(1)
    collectIMUData(fileName, duration)
    print("Killing imu.launch process")
    os.kill(proc.pid, signal.SIGINT)

def collectIMUData(filename, duration):
    cwd = os.getcwd()
    data_path = cwd + "/../data/"
    ext = ".bag"
    if not os.path.exists(data_path):
        os.mkdir(data_path)
        print("Directory: ", data_path, " created")
    else:
        print("Directory: ", data_path, " already exists.")
    print("Recording data to: ", data_path + filename)
    data_file = data_path + filename + ext
    bagger_proc = Popen(['rosbag', 'record', '/imu/raw', '--duration=' + str(duration), '-o', data_file])
    bagger_proc.wait()

def checkFileName(fileName):
    #perform string checking here
    if re.match("^[a-zA-Z0-9_]*$", fileName):
        return True
    else:
        print("Filename must not contain special characters or an extension.")
        return False

def checkDuration(duration):
    #perform int checking here
    try:
        d = int(duration)
        if d > 30 or d < 3:
            print("Duration must be within 3 and 30 seconds (inclusive)")
            return False
        else:
            return True
    except ValueError:
        print("Duration must be a numeric!")
        return False

def main():
    while True:
        print("Please enter the name of the file")
        fileName = raw_input()
        print("Please enter the duration (default is 5s)")
        duration = raw_input()
        if checkFileName(fileName) and checkDuration(duration):
            break
    if duration == "":
        collectData(fileName)
    else:
        collectData(fileName, int(duration))

if __name__ == '__main__':
    main()
