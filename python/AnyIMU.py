#TODO need to close the thread correctly when the UI is closed

import serial, sys, time, math

# -- PyQt --
from PySide.QtGui import *
from PySide.QtCore import *

# -- numbers --
import numpy as np
from scipy import signal

# -- pyqtgraph
import pyqtgraph as pg
import pyqtgraph.opengl as gl

# -- openGL ---
from PySide.QtOpenGL import *
from OpenGL import GL

# -----------------------------------------------------------------------------------------
class SerialThread(QThread):
  progress = Signal(str)

  def __init__(self, parent=None):
    super(SerialThread, self).__init__(parent)
    self.serial = None

  def serialConn(self, inPort, rate):
    self.serial = serial.Serial(port=inPort, baudrate=rate)
    if self.serial.isOpen():
      print 'Connected to serial'
      time.sleep(1)

  def serialDis(self):
    self.serial.clost()

  def run(self):
    while True:
      line = str(self.serial.readline())
      self.progress.emit(line)    


# -----------------------------------------------------------------------------------------
class Viewport(QGLWidget):
  def __init__(self, parent=None):
    super(Viewport, self).__init__()

    self.black = QColor(Qt.black)
    self.gray = QColor(Qt.gray)

    self.object = 0
    self.xRot = 0
    self.yRot = 0
    self.zRot = 0
    self.lastPos = QPoint()

  def xRotation(self):
    return self.xRot
 
  def yRotation(self):
    return self.yRot
 
  def zRotation(self):
    return self.zRot

  def initializeGL(self):
    self.qglClearColor(self.black)
    self.object = self.makeObject()
    GL.glShadeModel(GL.GL_FLAT)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_CULL_FACE)

  def paintGL(self):
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glTranslated(0.0, 0.0, -10.0)
    GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
    GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
    GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
    GL.glCallList(self.object)

  def setXRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.xRot:
      self.xRot = angle
      self.emit(SIGNAL("xRotationChanged(int)"), angle)
      self.updateGL()
 
  def setYRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.yRot:
      self.yRot = angle
      self.emit(SIGNAL("yRotationChanged(int)"), angle)
      self.updateGL()
 
  def setZRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.zRot:
      self.zRot = angle
      self.emit(SIGNAL("zRotationChanged(int)"), angle)
      self.updateGL()

  def normalizeAngle(self, angle):
    while angle < 0: angle += 360 * 16
    while angle > 360 * 16: angle -= 360 * 16
    return angle

  def minimumSizeHint(self):
    return QSize(50, 50)

  def sizeHint(self):
    return QSize(500, 500)

  def resizeGL(self, width, height):
    side = min(width, height)
    GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
 
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)

  def mousePressEvent(self, event):
    self.lastPos = QPoint(event.pos())

  def mouseMoveEvent(self, event):
    dx = event.x() - self.lastPos.x()
    dy = event.y() - self.lastPos.y()
 
    if event.buttons() & Qt.LeftButton:
      self.setXRotation(self.xRot + 8 * dy)
      self.setYRotation(self.yRot + 8 * dx)

    elif event.buttons() & Qt.RightButton:
      self.setXRotation(self.xRot + 8 * dy)
      self.setZRotation(self.zRot + 8 * dx)
 
    self.lastPos = QPoint(event.pos())

  def makeObject(self):
    genList = GL.glGenLists(1)
    GL.glNewList(genList, GL.GL_COMPILE)
 
    GL.glBegin(GL.GL_QUADS)
 
    x1 = +0.06
    y1 = -0.14
    x2 = +0.14
    y2 = -0.06
    x3 = +0.08
    y3 = +0.00
    x4 = +0.30
    y4 = +0.22
 
    self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
    self.quad(x3, y3, x4, y4, y4, x4, y3, x3)
 
    self.extrude(x1, y1, x2, y2)
    self.extrude(x2, y2, y2, x2)
    self.extrude(y2, x2, y1, x1)
    self.extrude(y1, x1, x1, y1)
    self.extrude(x3, y3, x4, y4)
    self.extrude(x4, y4, y4, x4)
    self.extrude(y4, x4, y3, x3)
 
    Pi = 3.14159265358979323846
    NumSectors = 200
 
    for i in range(NumSectors):
      angle1 = (i * 2 * Pi) / NumSectors
      x5 = 0.30 * math.sin(angle1)
      y5 = 0.30 * math.cos(angle1)
      x6 = 0.20 * math.sin(angle1)
      y6 = 0.20 * math.cos(angle1)
 
      angle2 = ((i + 1) * 2 * Pi) / NumSectors
      x7 = 0.20 * math.sin(angle2)
      y7 = 0.20 * math.cos(angle2)
      x8 = 0.30 * math.sin(angle2)
      y8 = 0.30 * math.cos(angle2)
 
      self.quad(x5, y5, x6, y6, x7, y7, x8, y8)
 
      self.extrude(x6, y6, x7, y7)
      self.extrude(x8, y8, x5, y5)
 
    GL.glEnd()
    GL.glEndList()
 
    return genList
 
  def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
    self.qglColor(self.gray)
 
    GL.glVertex3d(x1, y1, -0.05)
    GL.glVertex3d(x2, y2, -0.05)
    GL.glVertex3d(x3, y3, -0.05)
    GL.glVertex3d(x4, y4, -0.05)
 
    GL.glVertex3d(x4, y4, +0.05)
    GL.glVertex3d(x3, y3, +0.05)
    GL.glVertex3d(x2, y2, +0.05)
    GL.glVertex3d(x1, y1, +0.05)

  def extrude(self, x1, y1, x2, y2):
    self.qglColor(self.gray.darker())
 
    GL.glVertex3d(x1, y1, +0.05)
    GL.glVertex3d(x2, y2, +0.05)
    GL.glVertex3d(x2, y2, -0.05)
    GL.glVertex3d(x1, y1, -0.05)

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
  def update(self, dataList):
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
    self.resize(700, 900)

    self.accDataCurr = None
    self.gyrDataCurr = None
    self.magDataCurr = None
    self.barDataCurr = None
    self.serialThread = None

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
    self.viewport.setFixedHeight(500)
    
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

    self.serialBtn.clicked.connect(self.serialBtnCmd)

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

    self.update3d() # whenever we get acc data we refresh the viewport

  # ---------------------------------------------------------------------------------------
  def update3d(self):

    if self.magDataCurr==None: return

    self.viewport.setXRotation(self.magDataCurr[0]*180.0/600.0)
    self.viewport.setYRotation(self.magDataCurr[1]*180.0/600.0)
    self.viewport.setZRotation(self.magDataCurr[2]*180.0/600.0)

  # ---------------------------------------------------------------------------------------
  def serialBtnCmd(self):
    self.setupSerialThread()

# -----------------------------------------------------------------------------------------
def startAnyIMU():
  app = QApplication(sys.argv)
  window = AnyIMU_window()
  window.show()
  sys.exit(app.exec_())

startAnyIMU()
