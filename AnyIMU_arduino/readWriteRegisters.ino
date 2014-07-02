
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

// ---------------------------------------------------------------------------------------
int readRegisterGyro(int deviceAddress, byte address){

    int v;
    Wire.beginTransmission(deviceAddress);
    Wire.write(address); // register to read
    Wire.endTransmission();

    Wire.requestFrom(deviceAddress, 1); // read a byte

    while(!Wire.available()) {
        // waiting
    }

    v = Wire.read();
    return v;
}
