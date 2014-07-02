// sample code from www.geeetech.com

#include <Wire.h>

#define BMA180 0x40  //address of the accelerometer
#define RESET 0x10   
#define PWR 0x0D
#define BW 0X20
#define RANGE 0X35
#define DATA 0x02

// ---------------------------------------------------------------------------------------
void setupAccel()
{
  byte temp[1];
  byte temp1;

  writeRegister(BMA180,RESET,0xB6);
  
  //wake up mode
  writeRegister(BMA180,PWR,0x10);
  
  // low pass filter,
  readRegister(BMA180, BW,1,temp);
  temp1=temp[0]&0x0F;
  writeRegister(BMA180, BW, temp1);   
  
  // range +/- 2g 
  readRegister(BMA180, RANGE, 1 ,temp);  
  temp1=(temp[0]&0xF1) | 0x04;
  writeRegister(BMA180,RANGE,temp1);
}

// ---------------------------------------------------------------------------------------
void readAccel()
{
  // read in the 3 axis data, each one is 14 bits 
  // print the data to terminal 
  int n=6;
  byte result[5];
  readRegister(BMA180, DATA, n , result);
 
  sensorData.accelX = (( result[0] | result[1]<<8)>>2);
  sensorData.accelY = (( result[2] | result[3]<<8 )>>2);
  sensorData.accelZ = (( result[4] | result[5]<<8 )>>2);
}
