/* -- usage --
SerialPort.devices

// a = ArduinoQuaternion( "/dev/tty.AdafruitEZ-Link3e2f-SPP", 38400)
a = ArduinoQuaternion( "/dev/tty.AdafruitEZ-Link416c-SPP", 38400)

// set the action to be performed with every new
// reading of the sensor. yaw, pitch, and roll are
// passed into your action function
a.action = { |y,p,r| [ y,p,r ].raddeg.postln};

a.setHome
a.clearHome

// post yaw pitch and roll from within parser for debugging
a.parser.postYPR = true
a.parser.postYPR = false

a.close

SerialPort.closeAll

*/

SerialPort.devices

a = ArduinoQuaternion( "/dev/tty.AdafruitEZ-Link3e2f-SPP", 38400);

// a = ArduinoQuaternion( "/dev/tty.AdafruitEZ-Link157f-SPP", 38400);

a.parser.postYPR = true
a.parser.postYPR = false

a.parser.postRaw = true
a.parser.postRaw = false

a.close

SerialPort.closeAll






l = List[ 252, 16, 252, 53, 69, 55, 66, 67, 44, 65, 56, 51, 50, 67, 57, 66, 67, 44, 52, 67, 54, 50, 55, 52, 51, 70, 44 ];

l.collectAs( { |item| item.asAscii }, String).split($,);

collect