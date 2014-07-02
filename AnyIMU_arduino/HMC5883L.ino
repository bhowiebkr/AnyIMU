#include <Wire.h>
#define HMC5883L 0x1E 

// ---------------------------------------------------------------------------------------
void setupMag()
{
  Wire.beginTransmission(HMC5883L); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
}

// ---------------------------------------------------------------------------------------
void readMag()
{
  //Tell the HMC5883L where to begin reading data
  Wire.beginTransmission(HMC5883L);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();
  
  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(HMC5883L, 6);
  if(6<=Wire.available())
  {
    sensorData.magX = Wire.read()<<8;
    sensorData.magX |= Wire.read(); //X lsb
    sensorData.magY = Wire.read()<<8; //Z msb
    sensorData.magY |= Wire.read(); //Z lsb
    sensorData.magZ = Wire.read()<<8; //Y msb
    sensorData.magZ |= Wire.read(); //Y lsb
  }
}
