
#pip install PySide2
#pip install PySide6
#pip install Pycairo
#pip install pipwin
#pipwin install cairocffi
#pip install pyqt5

##Generamos el python con PySide2
#pyuic5 -x interface.ui -o ui_interface.py
#lo mismo con resources
#pyrcc5 resources.qrc -o resoruces_rc.py

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


########################################################################
##   MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

         # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)

        ########################################################################
        # SHOW WINDOW
        ########################################################################
        self.show()

########################################################################
## EXECUTE  APP
########################################################################
if __name__ == "__main_3d__":
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