
// ---------------------------------------------------------------------------------------
void printData()
{
  // BMA180 
  Serial.print(sensorData.accelX);
  Serial.print(",");
  Serial.print(sensorData.accelY);
  Serial.print(",");
  Serial.print(sensorData.accelZ);
  Serial.print(",");
  
  // L3G4200D
  Serial.print(sensorData.gyroX);
  Serial.print(",");
  Serial.print(sensorData.gyroY);
  Serial.print(",");
  Serial.print(sensorData.gyroZ);
  Serial.print(",");

  
  // HMC5883L
  Serial.print(sensorData.magX);
  Serial.print(",");
  Serial.print(sensorData.magY);
  Serial.print(",");
  Serial.print(sensorData.magZ);
  Serial.print(",");

  
  // BMP085
  Serial.print(sensorData.temperature);
  Serial.print(",");
  Serial.print(sensorData.pressure);
  Serial.print(",");
  Serial.println(sensorData.altitude);
}
