import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class HeatmapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi('interface.ui', self)
        self.setup_heatmap()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HeatmapApp()
    window.show()
    sys.exit(app.exec_())
