from PySide.QtGui import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide.QtCore import Qt
import pyqtgraph as pg
import numpy as np
# -----------------------------------------------------------------------------------------
class SensorDisplay(QWidget):
  def __init__(self, name=None):
    super(SensorDisplay, self).__init__()
    self.graph = pg.PlotWidget(name=name)
    self.plots = []
    title = QLabel(name)
    title.setStyleSheet('color: white; background-color: black')
    title.setAlignment(Qt.AlignCenter)
    self.setFixedHeight(150)

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
                                 
