#!/usr/bin/env python

import serial
from time import sleep
import binascii
import struct
from math import atan2, asin, pi
import datetime
import time
import numpy as np
import platform
import sys

# name appropriate ports for platform
if platform.system() == 'Darwin':
    # os x

    # no hub
##    botPortName = '/dev/tty.usbmodem1d11471'
##    encoderPortName = '/dev/tty.usbmodem1d11461'

    # usb hub
    servoPortName = '/dev/tty.usbmodem1d1151'
    datapath = "/Users/rtwomey/code/pytwomey/drawing_recorder/"

else:
    # angstrom
    servoPortName = '/dev/ttyACM0'
    datapath = "/home/root/code/drawing_recorder/"
    


# open devices and file
servoPort = serial.Serial(servoPortName, 115200, timeout=0.1)
infname = ""



def readHeadData(filename):

    f = open(filename)

    lines = [line.rstrip('\n') for line in f]

    points = []

    print len(lines),"frames in file...",


    for i, l in enumerate(lines):
        fields = np.array(l.split('\t')).astype(np.float)
        if len(fields)<4:
            print i
            break

        e1, e2, e3, seconds = fields

        #print "time",millis,
        
        points.append([e1, e2, e3, seconds])
        
    print "done reading."

    f.close()
    
    return np.array(points)


def remap(n, start1, stop1, start2, stop2):

    res = (((n-start1)/(stop1-start1))*(stop2-start2))+start2
    minres = min(start2, stop2)
    maxres = max(start2, stop2)
    if res < minres:
        res = minres
    if res > maxres:
        res = maxres
    return res

   
def main():

    # check arguments
    if len(sys.argv) > 1:
        infname = sys.argv[1]
    else:
        fname = "2013-05-14-08-40-03_headrecord.txt"
        infname = datapath+fname

    # read recorded head data
    points = readHeadData(infname)
    count = 0   

    startTime = time.time()

    print "=== Headless Playback ==="
    print "reading data from",infname
    print "press Ctrl-C twice to exit"

    try:
        while True:

            try:
                vals = points[count]

                # write to file
                currtime = time.time() - startTime
                
                if(currtime > vals[3]):
                    
                    d1 = int(remap(float(vals[0]), -pi/2.0, pi/2.0, 550., 2300.))
                    d2 = int(remap(float(vals[1]), -pi/2., pi/2., 2300., 700.))

                    print d1, d2
                    servoPort.write("2, 0, {0}\r\n".format(d1))
                    servoPort.write("2, 1, {0}\r\n".format(d2))
                    servoPort.flushInput()

                    count = count + 1
                    if count >= len(points):
                        break

                sys.stdout.write("({0:.2f}, {1}/{2})\r".format(currtime, count, len(points)))
                sys.stdout.flush()
                sleep(0.01)

            except (KeyboardInterrupt):
                sleep(0.5)
                    

    except (KeyboardInterrupt):
        print "exiting..."
        pass

    print "{0:.2f} sec elapsed".format(time.time() - startTime)

    # cleanup
    servoPort.close()

    

if __name__ == "__main__":
    main()
    
