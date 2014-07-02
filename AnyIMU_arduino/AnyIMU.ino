#include <Wire.h>

struct sensorDataStruct
{
  int accelX;
  int accelY;
  int accelZ;
  int gyroX;
  int gyroY;
  int gyroZ;
  int magX;
  int magY;
  int magZ;
  short temperature;
  long pressure;
  float altitude;
};

sensorDataStruct sensorData = {0,0,0,0,0,0,0,0,0,0,0,0};

void setup()
{
  Serial.begin(9600);
  //Serial.println();
  //Serial.println("AnyIMU 9DOF + pressure");
  //Serial.println("www.tinlynx.com");
  
  Wire.begin();
  delay(20);
  
  // setup sensors
  setupAccel();
  setupGyro();
  setupMag();
  setupBar();
  
  delay(1500);
}

void loop()
{
  readAccel();
  readGyro();
  readMag();
  readBar();
  
  printData();
}
