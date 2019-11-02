## Any IMU

Any IMU is a rather old repo of python and arduino code used for reading electronic digital sensors. The gui was written with PySide and pyqtgraph. Also included is c++ code for the arduino (.ino) files. 

Protocols these chips are using are I2C and SPI

The following digital sensors are supported in this framework:

- Gyroscope - L3G4200D (address 0x69)
- Accelerometer - BMA180 (address 0x40
- Magnetometer - HMC5883L (address 0x1E)
- Barometer - BMP085 (address 0x77)

## Below are photos of the prototype board used with this code

![imu v1 board](https://github.com/bhowiebkr/AnyIMU/blob/master/images/IMU-v1-Board.jpg)

![imu v2 board](https://github.com/bhowiebkr/AnyIMU/blob/master/images/IMU-v2-Board.jpg)
