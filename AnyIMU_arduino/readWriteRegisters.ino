
// ---------------------------------------------------------------------------------------
void writeRegister(int device, byte address, byte val) 
{
  Wire.beginTransmission(device);
  Wire.write(address);
  Wire.write(val);
  Wire.endTransmission();
}

// ---------------------------------------------------------------------------------------
int readRegister(int device, byte address, int num, byte buff[])
{
   int value;
   Wire.beginTransmission(device);
   Wire.write(address);
   Wire.endTransmission();
   
   Wire.requestFrom(device, num);

   int i=0;
   while(Wire.available())
   {
     buff[i] =Wire.read();
     i++;
   }
   Wire.endTransmission();
}


