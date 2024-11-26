####REQUIREMENTS
#Entorno Virtual cambiar libreria site-packages
#pip install pipwin
#pipwin install cairocffi
#pip install -r requirements.txt

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

# cairocffi @ file:///C:/Users/esteb/pipwin/cairocffi-1.3.0-cp310-cp310-win_amd64.whl#sha256=44ab832c1aa061ff740bb5ea981c6d1a01bffa71d4068d51aeb65907e29970ca


### MANUAL INSTALATION ON PC
#pipwin install cairocffi


###IMPORTS
import os
import sys

from ui_interface import *
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# IMPORTED ON ui_interface
from PyQt5.QtCore import QTimer

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
        self.timer = QTimer()

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
        #self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        #self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        #self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())

        # CLOSE CENTER MENU WIDGET SIZE
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())

        # CLOSE RIGHT MENU WIDGET SIZE
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())



        ### BOTONES DEL PANEL
        #self.ui.panel_1.clicked.connect(lambda:self.ui.label_4.lower())
        self.ui.iniciar.clicked.connect(self.handle_button_click)
        self.timer.timeout.connect(self.blink_labels)
        self.is_label_1_up_g_visible = True  # Para empezar con label_1_up_g visible

        #self.timer.timeout.connect(lambda: print("time out"))

    def handle_button_click(self):
        print("Button click")
        if self.ui.panel_1.isChecked() == True:
            print("Checkbox 1 está marcado.")

            #self.ui.label_1_up_g.lower()
            #self.ui.label_1_up_g.raise_()
            self.timer.start(2000)


            self.blink_count = 0

            self.ui.close_1.lower()
        else:
            self.ui.close_1.raise_()

        if self.ui.panel_2.isChecked()==True:
            print("Checkbox 2 está marcado.")
            self.ui.close_2.lower()
        else:
            self.ui.close_2.raise_()

    def blink_labels(self):
        print("Blinking")
        #"""Intercambia la visibilidad de los dos labels, poniéndolos uno encima del otro."""
        if self.is_label_1_up_g_visible :
            print("detección de visivilidad")

            self.ui.label_1_up_g.lower()  # Mueve label_1_up_g debajo
            self.ui.label_1_up_w.raise_()  # Mueve label_1_up_w encima
        else:
            self.ui.label_1_up_w.lower()  # Mueve label_1_up_w debajo
            self.ui.label_1_up_g.raise_()  # Mueve label_1_up_g encima

        # Alternar la visibilidad de los labels
        self.is_label_1_up_g_visible = not self.is_label_1_up_g_visible

        # Incrementar el contador de parpadeos
        self.blink_count += 1

        # Detener el parpadeo después de 4 intercambios
        if self.blink_count >= 4:
            self.timer.stop()  # Detener el temporizador después de 4 cambios
            print("Parpadeo terminado.")

        #self.ui.panel_1.checkStateSet().connect(lambda:self.ui.close_1.lower())





        #self.ui.panel_2.clicked.connect(lambda: self.ui.close_2.raise_())

        #self.ui.panel_3.clicked.connect(lambda: self.ui.close_3.raise_())

        #self.ui.panel_4.clicked.connect(lambda: self.ui.close_4.lower())








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