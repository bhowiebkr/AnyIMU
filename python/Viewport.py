from PySide.QtGui import QWidget, QColor
from PySide.QtCore import Qt, SIGNAL, QSize
from PySide.QtOpenGL import QGLWidget
from OpenGL import GL
from GLModel import *
# -----------------------------------------------------------------------------------------
class Viewport(QGLWidget):
  def __init__(self, parent=None):
    super(Viewport, self).__init__()

    self.black = QColor(Qt.black)
    self.gray = QColor(Qt.gray)
    self.model = GLModel()

    self.object = 0
    self.xRot = 0
    self.yRot = 0
    self.zRot = 0

  # ---------------------------------------------------------------------------------------
  def updateView(self, eulerAngles):
    self.setXRotation(eulerAngles[0])
    self.setYRotation(eulerAngles[1])
    self.setZRotation(eulerAngles[2])            

  # ---------------------------------------------------------------------------------------
  def xRotation(self):
    return self.xRot
 
  # ---------------------------------------------------------------------------------------
  def yRotation(self):
    return self.yRot
 
  # ---------------------------------------------------------------------------------------
  def zRotation(self):
    return self.zRot

  # ---------------------------------------------------------------------------------------
  def initializeGL(self):
    self.qglClearColor(self.black)

    self.object = self.model.makeObject() # makes a glGenList
    print self.object

    GL.glShadeModel(GL.GL_FLAT)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_CULL_FACE)

  # ---------------------------------------------------------------------------------------
  def paintGL(self):
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glTranslated(0.0, 0.0, -10.0)
    GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
    GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
    GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
    GL.glCallList(self.object)

  # ---------------------------------------------------------------------------------------
  def setXRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.xRot:
      self.xRot = angle
      self.emit(SIGNAL("xRotationChanged(int)"), angle)
      self.updateGL()
 
  # ---------------------------------------------------------------------------------------
  def setYRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.yRot:
      self.yRot = angle
      self.emit(SIGNAL("yRotationChanged(int)"), angle)
      self.updateGL()
 
  # ---------------------------------------------------------------------------------------
  def setZRotation(self, angle):
    angle = self.normalizeAngle(angle)
    if angle != self.zRot:
      self.zRot = angle
      self.emit(SIGNAL("zRotationChanged(int)"), angle)
      self.updateGL()

  # ---------------------------------------------------------------------------------------
  def normalizeAngle(self, angle):
    while angle < 0: angle += 360 * 16
    while angle > 360 * 16: angle -= 360 * 16
    return angle

  # ---------------------------------------------------------------------------------------
  def minimumSizeHint(self):
    return QSize(50, 50)

  # ---------------------------------------------------------------------------------------
  def sizeHint(self):
    return QSize(500, 500)

  # ---------------------------------------------------------------------------------------
  def resizeGL(self, width, height):
    side = min(width, height)
    GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
 
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)

  # ---------------------------------------------------------------------------------------
     
