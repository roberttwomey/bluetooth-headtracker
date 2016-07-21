# myo-osc-relay

Relays data from Thalmic Labs Myo armband to Supercollider (or any other program) via OSC. 

Compiles on OS X with Xcode. 

Versions and dependencies are described below. 

Developed for UW Center for Digital Arts and Experimental Media (DXARTS), July 2016

Robert Twomey - roberttwomey.com

# Usage

after building, the executable can be found in:
```
myo-osc-relay/DerivedData/myo-osc-relay/Build/Products/Debug
```

Parameters are set by command line options: 
```
 -v, verbose text output
 -a ADDR, OSC destination address
 -p PORT, OSC destination port
 -emg, send EMG data
 -pose, send pose data
 -quat, send orientation quaternion
 -accel, send acceleration
 -gyro, send gyroscope
 -linaccel, send linear acceleration
```

 example: 

```./myo-osc-relay -v -emg -pose -quat -accel -gyro -linaccel```

# Versions

## OS X / Xcode
xcode Version 7.3 (7D175)

os x 10.11.5

## Myo

myo connect Version 1.0.1 https://s3.amazonaws.com/thalmicdownloads/mac/1.0.1/MyoConnect.dmg

myo firmware is 1.5.1970

## oscpack

oscpack http://www.rossbencina.com/code/oscpack

