
#pip install PySide2
#pip install PySide6
#pip install Pycairo
#pip install pipwin
#pipwin install cairocffi
#pip install pyqt5

##Generamos el python con PySide2
#pyuic5 -x my_ui.ui -o my_ui.py
#lo mismo con resources
#pyrcc5 resources.qrc -o resources_rc.py

#otros
# pip install QT-PyQt-PySide-Custom-Widgets



import os
import sys

from ui_interface import *
from Custom_Widgets.Widgets import *

########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *
########################################################################
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
        self.ui.Btemperature.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.Bhumidity.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.Bflow.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.Bpressure.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.Btempcam.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.Bsolar.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.B1.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.B2.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())



        # CLOSE CENTER MENU WIDGET SIZE
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())

        # EXPAND RIGHT MENU WIDGET SIZE
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profieMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())

        # CLOSE RIGHT MENU WIDGET SIZE
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())



#plot
    def setup_heatmap(self):

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self.ui.g1)  # Use the layout of the QGraphicsView
        layout.addWidget(self.canvas)

        self.plot_heatmap()
    def plot_heatmap(self):
        # Generate sample data (replace with your data)
        data = np.random.rand(10, 10)

        ax = self.figure.add_subplot(111)
        cax = ax.matshow(data, cmap='viridis')
        self.figure.colorbar(cax)

        self.canvas.draw()




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
########################################################################