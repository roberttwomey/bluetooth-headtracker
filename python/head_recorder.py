#!/usr/bin/env python
"""
head_recorder.py

Simple program to read from MPU6050 attached to one arduino
Write pan-tilt values to pan-tilt servo system on second arduino
And save values to a text file.

Robert Twomey 2013 - rtwomey@uw.edu

"""
import serial
from time import sleep
import binascii
import struct
from math import atan2, asin, pi
import datetime
import time

def decode_float(inString):
    # http://stackoverflow.com/questions/4315190/single-precision-big-endian-float-values-to-pythons-float-double-precision-bi
    if (len(inString) == 8):
        res = struct.unpack('<f',binascii.unhexlify(inString))[0]
        return res


def quaternion_to_euler(q):
    euler = [0, 0, 0]
    
    # psi, theta, phi
    euler[0] = atan2(2 * q[1] * q[2] - 2 * q[0] * q[3], 2 * q[0]*q[0] + 2 * q[1] * q[1] - 1)
    euler[1] = -asin(2 * q[1] * q[3] + 2 * q[0] * q[2])
    euler[2] = atan2(2 * q[2] * q[3] - 2 * q[0] * q[1], 2 * q[0] * q[0] + 2 * q[3] * q[3] - 1)

    return euler


def quat_conjugate(q):
    conj = [0, 0, 0, 0]

    conj[0] = q[0]
    conj[1] = -q[1]
    conj[2] = -q[2]
    conj[3] = -q[3]

    return conj


def quat_prod(a, b):
    res = [0, 0, 0, 0]

    res[0] = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
    res[1] = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
    res[2] = a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1]
    res[3] = a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]

    return res

def remap(n, start1, stop1, start2, stop2):

    res = (((n-start1)/(stop1-start1))*(stop2-start2))+start2
    minres = min(start2, stop2)
    maxres = max(start2, stop2)
    if res < minres:
        res = minres
    if res > maxres:
        res = maxres
    return res


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

# on os x
#imuPort = serial.Serial('/dev/tty.usbmodem1d1171', 115200, timeout=1)
#servoPort = serial.Serial('/dev/tty.usbmodem1d1161', 115200, timeout=0.1)

# on beaglebone
imuPort = serial.Serial("/dev/ttyACM1", 115200, timeout=1)
servoPort = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)

# wait a second and send init to IMU
sleep(0.1)
imuPort.write("1")

count = 0
hq = None
calibrated = False

q = [0., 0., 0., 0.]
hq = [0., 0., 0., 0.]

outfname = timeStamped("headrecord.txt")
outf = open(outfname, 'w')

startTime = time.time()

print "=== Head Tracking ==="
print "face forward and press Ctrl-C to store home position"
print "press Ctrl-C twice to exit"
print "logging data to",outfname

try:
    while True:

        try:
            inData = imuPort.readline() #(37) # up to newline char
            # size of data packets

            if(len(inData) >= 37):
                vals = inData.split(",")
                #print vals

                if len(vals) == 5:
                    q = [decode_float(v) for v in vals[:4]]
                    #print q

                    if calibrated:
                        euler = quaternion_to_euler(quat_prod(hq, q))
                    else:
                        euler = quaternion_to_euler(q)

                    # write to file
                    now = time.time() - startTime
                    outf.write('%s\t%s\t%s\t%s\n' % (euler[0], euler[1], euler[2], now))

                    #print euler
                    d1 = int(remap(float(euler[0]), -pi/2.0, pi/2.0, 550., 2300.))
                    d2 = int(remap(float(euler[1]), -pi/2., pi/2., 800., 2100.))

                    #print d1, d2
                    servoPort.write("2, 0, %s\n" % d1)
                    servoPort.write("2, 1, %s\n" % d2)
                    servoPort.flushInput()
                    
            #sleep(0.01)                

        except (KeyboardInterrupt):
            print "\nStoring home:"
            hq = quat_conjugate(q)
            print hq
            calibrated = True
            sleep(0.5)
                

except (KeyboardInterrupt):
    print "exiting..."
    pass


servoPort.close()
imuPort.close()
outf.close()
