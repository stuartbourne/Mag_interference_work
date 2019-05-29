import rosbag
import sys
import matplotlib.pyplot as plt
import numpy as np
import math


def checkBagName(bag_name):
    #most checking should be encapsulated by the rosbag try/except
    bag = ""
    try:
        bag = rosbag.Bag(bag_name)
    except IOError:
        print("Supplied .bag file could not be found!")
        exit()
    return bag

def getImuVals(bagFile):
    accelVals, gyroVals, magVals = ([] for i in range(3))
    for topic, msg, t in bagFile.read_messages(topics=['/imu/raw', '/imu/raw/']):
        magVals.append(msg.magnetometers)
        accelVals.append(msg.accelerometers)
        gyroVals.append(msg.gyroscopes)
    return accelVals, gyroVals, magVals

def plotMagnitude(magVals):
    mag_x, mag_y, mag_z, mag_norm = ([] for i in range(4))
    for m in magVals:
        mag_x.append(m.x)
        mag_y.append(m.y)
        mag_z.append(m.z)
        mag_norm.append(math.sqrt(m.x*m.x + m.y*m.y + m.z*m.z))
    plt.subplot(311)
    x_plot, =plt.plot( np.arange(0., len(mag_x), 1), mag_x,'r--', label="mag_x")
    y_plot, =plt.plot( np.arange(0., len(mag_y), 1), mag_y,'b--', label="mag_y")
    z_plot, =plt.plot( np.arange(0., len(mag_z), 1), mag_z,'g--', label="mag_y") #np.arange(0., len(mag_y), 1), mag_y, 'b--', np.arange(0., len(mag_z), 1), mag_z, 'g--', np.arange(0., len(mag_norm), 1), mag_norm)
    mag_plot =plt.plot( np.arange(0., len(mag_norm), 1), mag_norm,'b', label="mag_norm")
    plt.xlabel("Sample #")
    plt.ylabel("Magnetic Values")
    plt.legend()

def plotMean(magVals):
    mag_norm = np.array([])
    for m in magVals:
        mag_norm = np.append(mag_norm, math.sqrt(m.x*m.x + m.y*m.y + m.z*m.z))
    mag_samples = np.arange(0.0, len(mag_norm), 1)
    mean_mag_norm = np.array([np.mean(mag_norm) for i in xrange(len(mag_norm))]) #get mean with same amount of data point as the mag norm data
    plt.subplot(312)
    plt.plot(mag_samples, mag_norm, 'bo')#,
    plt.plot(mag_samples, mean_mag_norm, 'r--', label="mean_mag_norm")
    plt.xlabel("Sample #")
    plt.ylabel("Magnetic Magnitude")
    plt.legend()
    #Now lets plot y variance as a bar graph for easier visualization
    y_var = np.square(mean_mag_norm - mag_norm)   #get y variance
    plt.subplot(313)
    plt.bar(mag_samples, y_var)
    plt.ylabel("Magnetic Variance")
    plt.xlabel("Sample #")

def main():
    if len(sys.argv) <= 1:
        print("Please supply a .bag file!")
        exit()
    #first read in the IMU data into a data array
    bag_name = sys.argv[1]
    bag = checkBagName(bag_name)
    print("Extracting IMU values from: ", bag_name)
    _, _, magVals = getImuVals(bag)
    plt.figure(num=None, figsize=(12, 10), dpi=80)
    plotMagnitude(magVals)
    plt.title("Collected magnetic values")
    plotMean(magVals)
    plt.show()

if __name__ == "__main__":
    main()
