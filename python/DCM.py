import math

class DCM():
  def __init__(self):
    self.accX = None
    self.accY = None
    self.accZ = None

    self.gyrX = None
    self.gyrY = None
    self.gyrZ = None

    self.magX = None
    self.magY = None
    self.magZ = None

  def update(self, accIn=None, gyrIn=None, magIn=None):
    self.accX = accIn[0]
    self.accY = accIn[1]
    self.accZ = accIn[2]

    self.gyrX = gyrIn[0]
    self.gyrY = gyrIn[1]
    self.gyrZ = gyrIn[2]

    self.magX = magIn[0]
    self.magY = magIn[1]
    self.magZ = magIn[2]
   
    # normalize the data
    x = self.accX/4096.0
    y = self.accY/4096.0
    z = self.accZ/4096.0 

    # clamp the data
    x = max(min(1, x), -1)
    y = max(min(1, y), -1)
    z = max(min(1, z), -1)

    Axr = math.acos(x)  #x/R
    Ayr = math.acos(y)  #y/R
    Azr = math.acos(z)  #z/R  

    eulerX = math.degrees(Axr)
    eulerY = math.degrees(Ayr) * -1.0 + 90.0
    eulerZ = math.degrees(Azr)

    return (eulerX, eulerY, eulerZ)


