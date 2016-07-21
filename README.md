# bluetooth-headtracker

A simple bluetooth, rechargeable, 10DOF head-tracking device.

For use with the [Ambisonic ToolKit (ATK)](http://www.ambisonictoolkit.net/wiki/tiki-index.php) , motion capture, and [Pan-Tilt](http://wiki.roberttwomey.com/Pan-Tilt) camera systems. 

A hardware, software, and 3d printed enclosure solution.

Developed for UW Center for Digital Arts and Experimental Media (DXARTS), July 2016

Robert Twomey - roberttwomey.com

# Usage

See the software options below. 

# Hardware

Built with simple, ready to order parts from common suppliers. Purchase 1 each of the following:
* Bluefruit EZ-Link - bluetooth modem w/ baud rate detection - http://www.adafruit.com/product/1588
* Arduino Pro Mini 3.3V - https://www.sparkfun.com/products/11114
* Power switch - https://www.sparkfun.com/products/102
* GY-86 - 10 DOF flight control module with MPU6050 + HMC5883L + MS5611 - http://www.amazon.com/Arrela-Control-Ms5611-Hmc5883l-Mpu6050/dp/B00KKJYMO6/
* LiPo Battery - https://www.sparkfun.com/products/731
* LiPo Charger - https://www.sparkfun.com/products/10217 (note you need to cut off the JST connector to fit it in the enclosure)
* Small quantity of stranded ribbon cable.

One of the following, needed to program the arduino. (One use only! Borrow from a friend?)
* FTDI Basic 3.3V - https://www.sparkfun.com/products/9873
* FTDI Cable 3.3V - http://www.adafruit.com/product/70

You can also choose to leave the LiPo charger out of the enclosure for small space savings.

# Arduino

[arduino/FreeIMU_quaternion/FreeIMU_quaternion.ino](arduino/FreeIMU_quaternion/FreeIMU_quaternion.ino)

We are using the straight FreeIMU_quaternion example from FreeIMU v0.4. This reads the attached sensors, calculates the AHRS quaternion, and transmits via serial print.

I've attached a copy of the FreeIMU_quaternion code here with the baud rate set to 38400, the max rate for the Arduino Pro Mini. 


# Processing

[processing/FreeIMU_cube](processing/FreeIMU_cube)

This is the demo app in Processing included with FreeIMU v0.4.

1. With the headtraker powered on, pair your computer with the bluefruit device.
2. Change the serial port screen to match your bluefruit device, for example ''/dev/tty.AdafruitEZ-Link3e2f-SPP'' on my system.
3. Run the example. Press 'h' to store the home position.



# Python
[python/head_through.py](python/head_through.py)

Simple python program to read from the IMU headtracker and record to file. Additionally opens second serial device and feeds values to pan-tilt camera in matching orientation. 


# Supercollider

[supercollider/ArduinoQuaternion/ArduinoQuaternion.sc](supercollider/ArduinoQuaternion/ArduinoQuaternion.sc)

A class based on the Arduino quark that connects to the paired bluetooth device as a serial port, and parses the binary data.

[supercollider/bt_headtrack_test.scd](supercollider/bt_headtrack_test.scd)

A sandbox program to try out the headtrack class.

# Solidworks

[solidworks/realv4/](solidworks/realv4/)

Solid model of enclosures and circuitry.
