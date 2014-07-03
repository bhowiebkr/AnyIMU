#include <Wire.h>

#define CTRL_REG1 0x20
#define CTRL_REG2 0x21
#define CTRL_REG3 0x22
#define CTRL_REG4 0x23
#define CTRL_REG5 0x24

#define L3G4200D 105  //address of the accelerometer

// ---------------------------------------------------------------------------------------
void setupGyro()
{
  writeRegister(L3G4200D, CTRL_REG1, 0b00001111); // Enable x, y, z and turn off power down:
  writeRegister(L3G4200D, CTRL_REG2, 0b00011001); // Use the HPF
  writeRegister(L3G4200D, CTRL_REG3, 0b00000000); // Generate data ready interrupt on INT2
  writeRegister(L3G4200D, CTRL_REG4, 0b10110000); // full-scale range 2000
  writeRegister(L3G4200D, CTRL_REG5, 0b00010011); // Controls high-pass filtering of outputs
}

void readGyro()
{
  byte xMSB = readRegisterGyro(L3G4200D, 0x29);
  byte xLSB = readRegisterGyro(L3G4200D, 0x28);
  sensorData.gyroX = ((xMSB << 8) | xLSB);

  byte yMSB = readRegisterGyro(L3G4200D, 0x2B);
  byte yLSB = readRegisterGyro(L3G4200D, 0x2A);
  sensorData.gyroY = ((yMSB << 8) | yLSB);

  byte zMSB = readRegisterGyro(L3G4200D, 0x2D);
  byte zLSB = readRegisterGyro(L3G4200D, 0x2C);
  sensorData.gyroZ = ((zMSB << 8) | zLSB);
}

// ---------------------------------------------------------------------------------------
int readRegisterGyro(int deviceAddress, byte address)
{
  int v;
  Wire.beginTransmission(deviceAddress);
  Wire.write(address); // register to read
  Wire.endTransmission();

  Wire.requestFrom(deviceAddress, 1); // read a byte

  while(!Wire.available()) { // waiting 
  }

  v = Wire.read();
  return v;
}
