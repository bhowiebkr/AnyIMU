import serial
from PySide.QtGui import *
from PySide.QtCore import *
import numpy as np
from scipy import signal
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys, time

# -----------------------------------------------------------------------------------------
class SensorDisplay(QWidget):
  def __init__(self, name=None):
    super(SensorDisplay, self).__init__()
    self.graph = pg.PlotWidget(name=name)
    self.plots = []
    title = QLabel(name)
    title.setStyleSheet('color: white; background-color: black')
    title.setAlignment(Qt.AlignCenter)

    mainLayout = QVBoxLayout()
    mainLayout.setContentsMargins(0,0,0,0)
    mainLayout.setSpacing(0)
    self.setLayout(mainLayout)
    self.dataLayout = QHBoxLayout()
    self.dataLayout.setContentsMargins(0,0,0,0)
    self.dataLayout.setSpacing(0)

    mainLayout.addWidget(title)
    mainLayout.addWidget(self.graph)
    mainLayout.addLayout(self.dataLayout)

  # ---------------------------------------------------------------------------------------
  def addPlot(self, fillLevelIn, brushIn, penIn, dataType='float', dataName=None):
    data = np.array([0], dtype=dataType)

    plot = self.graph.plot(fillLevel=fillLevelIn, brush=brushIn, pen=penIn)

    dataWidget = QLabel(dataName)
    dataWidget.dataName = dataName
    dataWidget.setStyleSheet('color: rgb' + str(penIn) + '; background-color: black')

    dataWidget.setAlignment(Qt.AlignCenter)
    self.dataLayout.addWidget(dataWidget)

    self.plots.append({'plot':plot, 'data':data, 'widget':dataWidget})

  # ---------------------------------------------------------------------------------------
  def update(self, rawData):
    try:
      dataList = map(float, rawData.split(' ')[1:])
    except ValueError:
      print 'raw data is no good:', rawData
      return

    for i in range(len(dataList)):
      self.plots[i]['data'] = np.append(self.plots[i]['data'], dataList[i]) 
      self.plots[i]['plot'].setData(self.plots[i]['data'])

      dataName = self.plots[i]['widget'].dataName
      self.plots[i]['widget'].setText(dataName + ' ' + str(dataList[i]))

    if len(self.plots[0]['data']) > 200:
      for plot in self.plots:
        plot['data'] = plot['data'][1:]

# -----------------------------------------------------------------------------------------
class AnyIMU_window(QMainWindow):
  def __init__(self, parent=None):
    super(AnyIMU_window, self).__init__(parent)
    self.setWindowTitle('AnyIMU')
    self.resize(700, 500)

    self.serial = None
    self.toggleSerial = False

    # The plot widget
    self.accPlotWidget = SensorDisplay(name='Accelerometer')
    self.gyrPlotWidget = SensorDisplay(name='Gyroscope')
    self.magPlotWidget = SensorDisplay(name='Magnetometer')
    self.altPlotWidget = SensorDisplay(name='Barometer')

    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='float', dataName='X')
    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='float', dataName='Y')
    self.accPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='float', dataName='Z')

    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='int', dataName='X')
    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='int', dataName='Y')
    self.gyrPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='int', dataName='Z')

    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='int', dataName='X')
    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,200,0,100), penIn=(0,255,0), dataType='int', dataName='Y')
    self.magPlotWidget.addPlot(fillLevelIn=0, brushIn=(0,0,200,100), penIn=(0,0,255), dataType='int', dataName='Z')

    self.altPlotWidget.addPlot(fillLevelIn=0, brushIn=(200,0,0,100), penIn=(255,0,0), dataType='float', dataName='ALT')
                                                                                      
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
    
    self.serialBtn = QPushButton('Connect')

    # add widgets to layout
    connectionLayout.addWidget(serialLab)
    connectionLayout.addWidget(self.serialLine)
    connectionLayout.addWidget(baudRateLab)
    connectionLayout.addWidget(self.baudRateCombo)
    connectionLayout.addWidget(self.serialBtn)
    connectionLayout.addStretch()


    self.mainLayout.addLayout(connectionLayout, 0,0,1,2)
    self.mainLayout.addWidget(self.accPlotWidget, 1,0,1,1)
    self.mainLayout.addWidget(self.gyrPlotWidget, 1,1,1,1)
    self.mainLayout.addWidget(self.magPlotWidget, 2,0,1,1)
    self.mainLayout.addWidget(self.altPlotWidget, 2,1,1,1)

    self.timer = QTimer()
    self.timer.timeout.connect(self.update)

    self.serialBtn.clicked.connect(self.serialBtnCmd)
    self.serialBtnCmd()
  # ---------------------------------------------------------------------------------------
  def update(self):
    if not self.toggleSerial: return

    line = str(self.serial.readline())

    if 'ACC:' in line: self.accPlotWidget.update(line)
    elif 'GYR:' in line: self.gyrPlotWidget.update(line)
    elif 'MAG:' in line: self.magPlotWidget.update(line)
    elif 'ALT:' in line: self.altPlotWidget.update(line)
    else: pass


  # ---------------------------------------------------------------------------------------
  def serialBtnCmd(self):
    if self.toggleSerial:
      self.serialDisconnect()
      self.serialBtn.setText('Connect')
    else:
      self.serialConnect()
      self.serialBtn.setText('Disconnect')

  # ---------------------------------------------------------------------------------------
  def serialConnect(self):
    portVal = self.serialLine.text()
    baudRate = int(self.baudRateCombo.currentText())
#    self.serial = serial.Serial( port='COM3', baudrate=115200)
    self.serial = serial.Serial( port=portVal, baudrate=baudRate)

    if self.serial.isOpen():
      print 'Connected to Arduino'
      time.sleep(1)
    self.toggleSerial = True
    self.timer.start(0)

  # ---------------------------------------------------------------------------------------
  def serialDisconnect(self):
    self.serial.close()
    self.toggleSerial = False
    print 'Disconnected from Arduino'

# -----------------------------------------------------------------------------------------

def startAnyIMU():
  app = QApplication(sys.argv)
  window = AnyIMU_window()
  window.show()
  sys.exit(app.exec_())

startAnyIMU()
