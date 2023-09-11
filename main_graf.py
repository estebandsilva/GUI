####REQUIREMENTS
#pip install PySide2
#pip install PySide6
#pip install Pycairo
#pip install pipwin
#pipwin install cairocffi
#pip install pyqt5

##Generamos el python con PySide2
#pyuic5 -x interface.ui -o ui_interface.py
#lo mismo con resources
#pyrcc5 resources.qrc -o resources_rc.py

#otros
# pip install QT-PyQt-PySide-Custom-Widgets

#EN RASPBERRYPI
#$ sudo apt-get install --upgrade python3-pyside2.qt3dcore python3-pyside2.qt3dinput python3-pyside2.qt3dlogic python3-pyside2.qt3drender python3-pyside2.qtcharts python3-pyside2.qtconcurrent python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qthelp python3-pyside2.qtlocation python3-pyside2.qtmultimedia python3-pyside2.qtmultimediawidgets python3-pyside2.qtnetwork python3-pyside2.qtopengl python3-pyside2.qtpositioning python3-pyside2.qtprintsupport python3-pyside2.qtqml python3-pyside2.qtquick python3-pyside2.qtquickwidgets python3-pyside2.qtscript python3-pyside2.qtscripttools python3-pyside2.qtsensors python3-pyside2.qtsql python3-pyside2.qtsvg python3-pyside2.qttest python3-pyside2.qttexttospeech python3-pyside2.qtuitools python3-pyside2.qtwebchannel python3-pyside2.qtwebsockets python3-pyside2.qtwidgets python3-pyside2.qtx11extras python3-pyside2.qtxml python3-pyside2.qtxmlpatterns
# export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/python3.9/site-packages/PySide2/plugins/platforms
#sudo pip install QT-PyQt-PySide-Custom-Widgets
# Execute as super user
# sudo ./pruebaqt.sh



### MANUAL INSTALATION ON PC
#pipwin install cairocffi


###IMPORTS
import os
import sys

from ui_interface import *
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# IMPORTED ON ui_interface

from Custom_Widgets.Widgets import *

#GRAPHICS Version 1.0
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


########################################################################
##   MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Graphics
        self.setup_heatmap()
        self.setup_flowmap()
        self.setup_humiditymap()
        self.setup_pressuremap()

        #Rectangle
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_rectangle)
        self.timer.start(50)




         # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)
################
        # SHOW WINDOW
        #######################################################################
        #########################################################
        self.show()

        # EXPAND CENTER MENU WIDGET SIZE
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())

        # CLOSE CENTER MENU WIDGET SIZE
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())

        # EXPAND RIGHT MENU WIDGET SIZE
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profieMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())

        # CLOSE RIGHT MENU WIDGET SIZE
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())

        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())


#####GRAPHICS

    #TEMPERATURE

    def setup_heatmap(self):

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self.ui.heatmapView)  # Use the layout of the QGraphicsView
        layout.addWidget(self.canvas)

        self.plot_heatmap()
    def plot_heatmap(self):
        # Generate sample data (replace with your data)
        data = np.random.rand(10, 10)

        ax = self.figure.add_subplot(111)
        cax = ax.matshow(data, cmap='viridis')
        self.figure.colorbar(cax)

        self.canvas.draw()



    #FLOW
    def setup_flowmap(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self.ui.flow_graphic)  # Use the layout of the QGraphicsView
        layout.addWidget(self.canvas)

        self.plot_flowmap()
    def plot_flowmap(self):
        # Generate sample data (replace with your data)
        data = np.random.rand(20, 20)

        ax = self.figure.add_subplot(111)
        cax = ax.matshow(data, cmap='viridis')
        self.figure.colorbar(cax)

        self.canvas.draw()

    #HUMIDITY
    def setup_humiditymap(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self.ui.humidity_graphic)  # Use the layout of the QGraphicsView
        layout.addWidget(self.canvas)

        self.plot_humiditymap()
    def plot_humiditymap(self):
        # Generate sample data (replace with your data)
        data = np.random.rand(30, 30)

        ax = self.figure.add_subplot(111)
        cax = ax.matshow(data, cmap='viridis')
        self.figure.colorbar(cax)

        self.canvas.draw()


    #PRESSURE
    def setup_pressuremap(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self.ui.pressure_graphic)  # Use the layout of the QGraphicsView
        layout.addWidget(self.canvas)

        self.plot_pressuremap()
    def plot_pressuremap(self):
        # Generate sample data (replace with your data)
        data = np.random.rand(40, 40)

        ax = self.figure.add_subplot(111)
        cax = ax.matshow(data, cmap='viridis')
        self.figure.colorbar(cax)

        self.canvas.draw()

    def move_rectangle(self):
        #QTWidht= 731
        #QTHight= 678

        rect_position = self.ui.rect_label.pos()
        #WITH DATA POSITION
        # new_x = rect_position.x() + self.step_x
        #new_y = rect_position.y() + self.step_y

        x = 0
        y = 0

        new_x = round(self.ui.label_12.width()*(x/100))
        new_y = round(self.ui.label_12.height()*(1-y/100))


        # Cambiar la dirección cuando golpea los límites
        if new_x + self.ui.rect_label.width() > self.ui.label_12.width():
            new_x = self.ui.label_12.width()-self.ui.rect_label.width()
        elif new_x < 0:
            new_x = 0

        if new_y + self.ui.rect_label.height() > self.ui.label_12.height():
            new_y = self.ui.label_12.height()-self.ui.rect_label.height()
        elif new_y < 0:
            new_y = 0

        self.ui.rect_label.move(new_x, new_y)
        self.ui.label_16.setText( str(x))
        self.ui.label_17.setText( str(y))

########################################################################
## EXECUTE  APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ##
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

########################################################################
## END
###########