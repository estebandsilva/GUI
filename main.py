#########Jere Modificaciones

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
from Plot_Sensor import *
from Plot_Camera import *

########################################################################
##   MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    #Graphics
        #self.setup_heatmap()

        # SETUP -->
        self.setup_plots()

        # UPDATE -->
       # self.plots_dict['temperature']['inside'][0].update_plot()



        #self.temp_inside = Plot_GUI(magnitude_='temperature', type_='inside')
        #layout = QVBoxLayout(self.ui.g1)  # Use the layout of the QGraphicsView
        #layout.addWidget(self.temp_inside.canvas)

        # UPDATE -->
        #self.temp_inside.update_plot()

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


        #self.ui.t1.clicked.connect(lambda: self.update_plot(magnitude='temperature',sub_magnitude='outside'))

        # Create a timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000)  # Update every second

    def setup_keys(self,magnitude='temperature',sub_magnitude='outside'):
        self.magnitude = magnitude
        self.sub_magnitude = sub_magnitude
        print(self.magnitude, self.sub_magnitude)
#plot
    def connect_button(self, button, magnitude, sub_magnitude):
        button.clicked.connect(lambda: self.setup_keys(magnitude=magnitude, sub_magnitude=sub_magnitude))

    def setup_plots(self):

        self.plots_dict = {
            'temperature': {'outside':  [None,'g1'],  'inside': [None,'g2'],  'interior': [None,'g3'],  'heating': [None,'g4'],  'up': [None,'g5'],  'down': [None,'g6'],  'all': [None,'g7']},
            'pressure_abs': {'outside': [None,'g1_2'],'inside': [None,'g2_2'],'interior': [None,'g3_2'],'heating': [None,'g4_2'],'up': [None,'g5_2'],'down': [None,'g6_2'],'all': [None,'g7_2']},
            'pressure_atm': {'outside': [None,'g1_3'],'inside': [None,'g2_3'],'interior': [None,'g3_3'],'heating': [None,'g4_3'],'up': [None,'g5_3'],'down': [None,'g6_3'],'all': [None,'g7_3']},
            'humidity':     {'outside': [None,'g1_4'],'inside': [None,'g2_4'],'interior': [None,'g3_4'],'heating': [None,'g4_4'],'up': [None,'g5_4'],'down': [None,'g6_4'],'all': [None,'g7_4']},
            'velocity': {       'wind': [None,'g1_5'],   'air': [None,'g2_5'],     'all': [None,'g3_5']},
            'solar': {     'radiation': [None,'g1_6']},
            'camera': {        'image': [None,'g1_7'], 'areas': [None,'g2_7'],'sub_matrix': [None,'g3_7'], 'temperature': [None,'g4_7'], 'image_temperature': [None,'g5_7']}
        }

        for key1 in self.plots_dict:
            for key2 in self.plots_dict[key1]:
                if key1 != 'camera' or key1 == 'camera' and key2 == 'temperature':
                    self.plots_dict[key1][key2][0] = Plot_Sensor(magnitude=key1, sub_magnitude=key2)

                else:
                    self.plots_dict[key1][key2][0] = Plot_Camera(magnitude=key1, sub_magnitude=key2)

                fig = self.plots_dict[key1][key2][0]
                x = self.plots_dict[key1][key2][1]
                layout = QVBoxLayout(getattr(self.ui, x))
                layout.addWidget(fig.canvas)
                # fig.update_plot()
                button = getattr(self.ui, x.replace('g', 't'))
                self.connect_button(button, key1, key2)


        self.magnitude = 'temperature'
        self.sub_magnitude = 'outside'
    def update_plots(self):
        self.plots_dict[self.magnitude][self.sub_magnitude][0].update_plot()

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