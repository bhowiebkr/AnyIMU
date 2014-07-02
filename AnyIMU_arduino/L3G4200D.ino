#include <Wire.h>

#define CTRL_REG1 0x20
#define CTRL_REG2 0x21
#define CTRL_REG3 0x22
#define CTRL_REG4 0x23
#define CTRL_REG5 0x24

#define L3G4200D 105  //address of the accelerometer

int scale = 2000;

// ---------------------------------------------------------------------------------------
void setupGyro()
{
  // Enable x, y, z and turn off power down:
  writeRegister(L3G4200D, CTRL_REG1, 0b00001111);
  
  // If you'd like to adjust/use the HPF, you can edit the line below to configure CTRL_REG2:
  writeRegister(L3G4200D, CTRL_REG2, 0b00000000);
  
  // Configure CTRL_REG3 to generate data ready interrupt on INT2
  // No interrupts used on INT1, if you'd like to configure INT1
  // or INT2 otherwise, consult the datasheet:
  writeRegister(L3G4200D, CTRL_REG3, 0b00001000);
  
  // CTRL_REG4 controls the full-scale range, among other things:
  if(scale == 250)
  {
    writeRegister(L3G4200D, CTRL_REG4, 0b00000000);
  }
  else if(scale == 500)
  {
    writeRegister(L3G4200D, CTRL_REG4, 0b00010000);
  }
  else
  {
    writeRegister(L3G4200D, CTRL_REG4, 0b00110000);
  }
  
  // CTRL_REG5 controls high-pass filtering of outputs, use it
  // if you'd like:
  writeRegister(L3G4200D, CTRL_REG5, 0b00000000);
  
}

void readGyro(){

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
