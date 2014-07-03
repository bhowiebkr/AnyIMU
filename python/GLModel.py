from OpenGL import GL
import math

class GLModel():
  def __init__(self):
    self.objFile = None

  def loadObj(self, objFile):
    print 'objFile is:', objFile

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
 
  # ---------------------------------------------------------------------------------------
  def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
    GL.glColor(0.5, 0.5, 0.5)
 
    GL.glVertex3d(x1, y1, -0.05)
    GL.glVertex3d(x2, y2, -0.05)
    GL.glVertex3d(x3, y3, -0.05)
    GL.glVertex3d(x4, y4, -0.05)
 
    GL.glVertex3d(x4, y4, +0.05)
    GL.glVertex3d(x3, y3, +0.05)
    GL.glVertex3d(x2, y2, +0.05)
    GL.glVertex3d(x1, y1, +0.05)

  # ---------------------------------------------------------------------------------------
  def extrude(self, x1, y1, x2, y2):
    GL.glColor(0.3, 0.3, 0.3)
 
    GL.glVertex3d(x1, y1, +0.05)
    GL.glVertex3d(x2, y2, +0.05)
    GL.glVertex3d(x2, y2, -0.05)
    GL.glVertex3d(x1, y1, -0.05)
                               
