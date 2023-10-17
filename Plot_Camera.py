import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import cv2
from matplotlib import gridspec
import json
import math
import os
import h5py
import os
import pandas as pd
import concurrent.futures
import matplotlib
matplotlib.use('Qt5Agg')  # Use Qt5Agg backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Plot_Camera:

    def __init__(self, magnitude='camera', sub_magnitude='image'):

        self.sensors_plots = {
        'temperature': {'outside':['C1T01A1','C1T02A1'],'inside':['C2T03A1','C2T04A1'],'interior':['C4T05A1','C4T06A1'],'heating':['C5T10A1'],'up':['C1T01A1','C2T03A1','C4T05A1'],'down':['C1T02A1','C2T04A1','C4T06A1'],'all':['C1T01A1','C1T02A1','C2T03A1','C2T04A1','C4T05A1','C4T06A1','C5T10A1']},
        'humidity':    {'outside':['C1H01A2','C1H02A2'],'inside':['C2H03A2','C2H04A2'],'interior':['C4H05A2','C4H06A2'],'heating':['C5H10A2'],'up':['C1H01A2','C2H03A2','C4H05A2'],'down':['C1H02A2','C2H04A2','C4H06A2'],'all':['C1H01A2','C1H02A2','C2H03A2','C2H04A2','C4H05A2','C4H06A2','C5H10A2']},
        'pressure_atm':{'outside':['C1P01A3','C1P02A3'],'inside':['C2P03A3','C2P04A3'],'interior':['C4P05A3','C4P06A3'],'heating':['C5P10A3'],'up':['C1P01A3','C2H03A2','C4P05A3'],'down':['C1P02A3','C2P04A3','C4P06A3'],'all':['C1P01A3','C1P02A3','C2P03A3','C2P04A3','C4P05A3','C4P06A3','C5P10A3']},
        'pressure_abs':{'outside':['C1P01B0','C1P02B0'],'inside':['C2P03B0','C2P04A3'],'interior':['C4P05A3','C4P06B0'],'heating':['C5P10B0'],'up':['C1P01B0','C2P03B0','C4P05B0'],'down':['C1P02B0','C2P04B0','C4P06B0'],'all':['C1P01B0','C1P02B0','C2P03B0','C2P04B0','C4P05B0','C4P06B0','C5P10B0']},
        'velocity':{'wind':['C3W08X1','C3Y08X2'],'air':['C3V07X0','C5V09X0'],'all':['C3V07X0','C5V09X0', 'C3W08X1']},
        'solar':{'radiation':['C3S11X0']},
        'camera':{'image':['E1T13A0'],'areas':['E1T13A0_A'],'sub_matrix':['E1T13A0_SUB'],'temperature':['E1T13A0_T'],'image_temperature':['E1T13A0_IT']}
        }



        self.directory_camera = 'DATA/tc_matrix'
        self.filename_camera = 'matrix_camera.txt'
        self.file_name_area = 'CONFIG/area.json'
        self.plot_figures = True
        self.save_figure = False

        self.full_path = os.path.join(self.directory_camera, self.filename_camera)

        with open(self.file_name_area, "r") as json_file:
            self.area = json.load(json_file)

        self.magnitude = magnitude
        self.sub_magnitude = sub_magnitude

        if self.sub_magnitude == 'sub_matrix':
            self.figure, self.axes = plt.subplots(2, 3)
            self.canvas = FigureCanvas(self.figure)
        else:
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
        self.last_modification = None
        self.mean_temperatures = {}

        self.update_plot()

    def update_df(self):
        new_modification = os.path.getmtime(self.full_path)
        if self.last_modification != new_modification:
            if self.full_path.endswith('.h5'):
                # Load HDF5 file using h5py
                with h5py.File(self.full_path, 'r') as hf:
                    dataset = hf['data']  # Replace 'your_dataset_name' with the actual dataset name
                    self.data = dataset[()]  # Load the entire dataset into a NumPy array
            elif self.full_path.endswith('.txt'):
                # Load text file using np.loadtxt
                self.data = np.loadtxt(self.full_path)
            else:
                raise ValueError("Unsupported file format")

            self.last_modification = new_modification
            return True
        else:
            return False


    def update_plot(self):
        if self.update_df():
            if self.sub_magnitude in ['image','areas']:
                ax = self.figure.add_subplot(111)
                ax.clear()
                ax.imshow(self.data, aspect='auto', interpolation='gaussian')
                #ax.imshow(data, cmap='inferno', aspect='auto', interpolation='gaussian')
                # ax.imshow(data, cmap='jet', aspect='auto', interpolation='gaussian')
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                ax.set_title('Temperature Heatmap [ºC]')
                ax.figure.colorbar(ax.get_images()[0], ax=ax)
                if self.sub_magnitude == 'areas':
                    for i, item in enumerate(self.area):
                        x, y = map(list, zip(*item['positions']))
                        # Draw the polygon perimeter on top of the image
                        ax.plot(x + [x[0]], y + [y[0]], color='black', linewidth=1)
                        # Annotate the plot with the label "A_0" at the centroid
                        ax.text(np.mean(x), np.mean(y), r'$A{:}'.format(i) + '$', fontsize=9, color='black', ha='center',va='center')
                ax.figure.tight_layout()

            elif self.sub_magnitude == 'sub_matrix':

                for i, item in enumerate(self.area):
                    # Clockwise points and dimensions (starting up-left)
                    positions = item['positions']
                    new_width_top = item['dimensions'][0]
                    new_height_right = item['dimensions'][1]
                    new_width_bottom = item['dimensions'][2]
                    new_height_left = item['dimensions'][3]

                    new_rectangle = np.array([[0, 0], [new_width_top - 1, 0], [new_width_bottom - 1, new_height_right - 1], [0, new_height_left - 1]], dtype=np.float32)
                    perspective_matrix = cv2.getPerspectiveTransform(np.float32(positions), new_rectangle)
                    perspective_corrected_image = cv2.warpPerspective(self.data, perspective_matrix, (int((new_width_bottom + new_width_top) / 2), int((new_height_right + new_height_left) / 2)))
                    mean_temperature = np.mean(perspective_corrected_image)
                    self.mean_temperatures['T' + str(i)] = mean_temperature

                    ax = self.axes.flat[i]
                    ax.imshow(perspective_corrected_image, cmap='jet', aspect='auto', interpolation='gaussian')
                    ax.set_xlabel('X-axis')
                    ax.set_ylabel('Y-axis')
                    ax.set_title('A{:d}'.format(i) + '- T={:.1f}'.format(mean_temperature) + 'ºC')
                    ax.axis('off')  # Turn off axes for empty subplots
                    ax.figure.tight_layout()
                print(self.mean_temperatures)

            self.canvas.draw()
