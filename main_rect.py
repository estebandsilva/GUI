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


###IMPORTS
import os
import sys

from ui_interface import *
    #from PyQt5.QtWidgets import QApplication, QWidget, QLabel
    #IMPORTED ON ui_interface


########################################################################
# IMPORT Custom widgets
from Custom_Widgets.Widgets import *
########################################################################



########################################################################
##   MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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


        #Cambiar el valor de las posiciones por pantalla

        self.step_x = 2
        self.step_y = 2

    def move_rectangle(self):
        rect_position = self.ui.rect_label.pos()
        new_x = rect_position.x() + self.step_x
        new_y = rect_position.y() + self.step_y


        # Cambiar la dirección cuando golpea los límites
        if new_x + self.ui.rect_label.width() > self.ui.label_12.width() or new_x < 0:
            self.step_x = -self.step_x

        if new_y + self.ui.rect_label.height() > self.ui.label_12.height() or new_y < 0:
            self.step_y = -self.step_y

        self.ui.rect_label.move(new_x, new_y)

        self.ui.label_16.setText( str(new_y))
        self.ui.label_17.setText( str(new_x))

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