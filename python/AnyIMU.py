from PySide.QtGui import QMainWindow, QApplication, QGridLayout, QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton
import sys, os

from SensorDisplay import *
from Viewport import *
from SerialThread import *
from DCM import *

# -----------------------------------------------------------------------------------------
class AnyIMU_window(QMainWindow):
  def __init__(self, parent=None):
    super(AnyIMU_window, self).__init__(parent)
    self.setWindowTitle('AnyIMU')
    self.resize(450, 700)
    os.system('cls')
    self.dcm = DCM()

    self.accDataCurr = None
    self.gyrDataCurr = None
    self.magDataCurr = None
    self.barDataCurr = None
    self.serialThread = None
    self.skipDataCount = 5

    # The plot widget
    self.accPlotWidget = SensorDisplay(name='Accelerometer')
    self.gyrPlotWidget = SensorDisplay(name='Gyroscope')
    self.magPlotWidget = SensorDisplay(name='Magnetometer')
    self.barPlotWidget = SensorDisplay(name='Barometer')

    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='int', dataName='X')
    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='int', dataName='Y')
    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='int', dataName='Z')

    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='int', dataName='X')
    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='int', dataName='Y')
    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='int', dataName='Z')

    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='int', dataName='X')
    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='int', dataName='Y')
    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='int', dataName='Z')

    self.barPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='float', dataName='TEMP')
    self.barPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='float', dataName='PRS')
    self.barPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='float', dataName='ALT')
                                                                                      
    # the main layout and widgets
    self.mainWidget = QWidget()
    self.setCentralWidget(self.mainWidget)
    self.mainLayout = QGridLayout()
    self.mainWidget.setLayout(self.mainLayout)
    connectionLayout = QHBoxLayout()

    # widgets
    serialLab = QLabel('Serial Port:')
    self.serialLine = QLineEdit('COM3')
    self.serialLine.setFixedWidth(100)
    baudRateLab = QLabel('Baud Rate:')
    self.baudRateCombo = QComboBox()
    for baud in [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]: self.baudRateCombo.addItem(str(baud))
    default = self.baudRateCombo.findText('9600')
    self.baudRateCombo.setCurrentIndex(default)  
    self.viewport = Viewport()

    # Debugging stuff----------------------------------
    debugLayout = QHBoxLayout()

    # these are used to offset the the rotation
    self.xAdd = QSpinBox()
    self.yAdd = QSpinBox()
    self.zAdd = QSpinBox()

    for each in [self.xAdd, self.yAdd, self.zAdd]:
      each.setMinimum(-180)  # min
      each.setMaximum(180)   # max
      each.setSingleStep(90) # change this to a small value if need be

    # these are used for inverting the rotations
    self.xMult = QCheckBox()
    self.yMult = QCheckBox()
    self.zMult = QCheckBox()

    self.xAdd.setValue(0)
    self.yAdd.setValue(90)  # in my case I need to offset by 90 in the Y axis
    self.zAdd.setValue(0)
    self.xMult.setChecked(False)
    self.yMult.setChecked(True)   # in my case I need to invert the Y axis on the acc
    self.zMult.setChecked(False)

    for each in [self.xAdd, self.yAdd, self.zAdd, self.xMult, self.yMult, self.zMult]:
      debugLayout.addWidget(each)

    # Debugging stuff----------------------------------
    
    self.serialBtn = QPushButton('Connect')

    # add widgets to layout
    connectionLayout.addWidget(serialLab)
    connectionLayout.addWidget(self.serialLine)
    connectionLayout.addWidget(baudRateLab)
    connectionLayout.addWidget(self.baudRateCombo)
    connectionLayout.addWidget(self.serialBtn)
    connectionLayout.addStretch()

    self.mainLayout.addLayout(connectionLayout, 0,0,1,2)
    self.mainLayout.addWidget(self.viewport, 1,0,1,2)
    self.mainLayout.addWidget(self.accPlotWidget, 2,0,1,1)
    self.mainLayout.addWidget(self.gyrPlotWidget, 2,1,1,1)
    self.mainLayout.addWidget(self.magPlotWidget, 3,0,1,1)
    self.mainLayout.addWidget(self.barPlotWidget, 3,1,1,1)
    self.mainLayout.addLayout(debugLayout, 4,0,1,2)


    self.serialBtn.clicked.connect(self.serialBtnCmd)

    self.serialBtnCmd()

  # ---------------------------------------------------------------------------------------
  def setupSerialThread(self):
    portVal = self.serialLine.text()
    baudRate = int(self.baudRateCombo.currentText())

    self.serialThread = SerialThread()
    self.serialThread.serialConn(portVal, baudRate)
    self.serialThread.progress.connect(self.update, Qt.QueuedConnection)
    
    if not self.serialThread.isRunning():
      self.serialThread.start()       

  # ---------------------------------------------------------------------------------------
  def update(self, line):
    if self.skipDataCount: # skip the first couple lines of data, because there could be some junk
      self.skipDataCount-=1
      return

    try:
      data = map(float, line.split(','))
      dataChunks =[data[x:x+3] for x in xrange(0, len(data), 3)]
    except ValueError, e:
      print 'ERROR', e
      return

    self.accDataCurr = map(int, dataChunks[0])
    self.gyrDataCurr = map(int, dataChunks[1])
    self.magDataCurr = map(int, dataChunks[2])
    self.barDataCurr = dataChunks[3]

    self.accPlotWidget.update(self.accDataCurr)
    self.gyrPlotWidget.update(self.gyrDataCurr)
    self.magPlotWidget.update(self.magDataCurr)
    self.barPlotWidget.update(self.barDataCurr)

    eulerAngles = self.dcm.update(self.accDataCurr, self.gyrDataCurr, self.magDataCurr)
    self.viewport.updateView(eulerAngles)

  # ---------------------------------------------------------------------------------------
  def serialBtnCmd(self):
    self.setupSerialThread()
   
# -----------------------------------------------------------------------------------------
def startAnyIMU():
  app = QApplication(sys.argv)
  window = AnyIMU_window()
  window.show()
  r = app.exec_()
  window.serialThread.stop()
  sys.exit(r)

startAnyIMU()
