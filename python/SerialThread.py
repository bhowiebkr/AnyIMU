from PySide.QtCore import QThread, Signal, QMutex, QWaitCondition
import serial, time
# -----------------------------------------------------------------------------------------
class SerialThread(QThread):
  progress = Signal(str)

  def __init__(self, parent=None):
    super(SerialThread, self).__init__(parent)
    self.serial = None
    self.mutex = QMutex()
    self.condition = QWaitCondition()
    self.abort = False

  def serialConn(self, inPort, rate):
    self.serial = serial.Serial(port=inPort, baudrate=rate)
    if self.serial.isOpen():
      print 'Connected to serial'
      time.sleep(0.1)

  def stop(self):
    self.abort = True
    self.wait()
    self.serial.close()

  def run(self):
    while True:
      if self.abort:
        return
      line = str(self.serial.readline())
      self.progress.emit(line)    
    self.deleteLater()                 
