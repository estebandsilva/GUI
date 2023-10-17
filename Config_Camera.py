import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib import gridspec
import json
import math
import os
import h5py

def get_mean_temp_camera(directory_camera,filename_camera, file_name_area, plot_figures=False, save_figure=False):
    # plot_figures=True --> Plots the different images to see how is working
    # save_figure=True --> Save the selected areas of the polygons as a matrix on the directory_camera path
    # As a result it gives a dictionary of the different mean temperatures of the areas.

    # Join the components to create a full path
    full_path = os.path.join(directory_camera, filename_camera)

    if full_path.endswith('.h5'):
        # Load HDF5 file using h5py
        with h5py.File(full_path, 'r') as hf:
            dataset = hf['data']  # Replace 'your_dataset_name' with the actual dataset name
            data = dataset[()]  # Load the entire dataset into a NumPy array
    elif full_path.endswith('.txt'):
        # Load text file using np.loadtxt
        data = np.loadtxt(full_path)
    else:
        raise ValueError("Unsupported file format")


    with open(file_name_area, "r") as json_file:
        area = json.load(json_file)

    mean_temperatures = {}

    if plot_figures:
        plt.figure(2)
        num_cols = math.ceil(math.sqrt(len(area)))
        num_rows = math.ceil(len(area) / num_cols)
        gs = gridspec.GridSpec(num_rows, num_cols)

    for i, item in enumerate(area):
        #Clockwise points and dimensions (starting up-left)
        positions = item['positions']
        new_width_top = item['dimensions'][0]
        new_height_right = item['dimensions'][1]
        new_width_bottom = item['dimensions'][2]
        new_height_left = item['dimensions'][3]

        new_rectangle = np.array([[0, 0], [new_width_top - 1, 0], [new_width_bottom - 1, new_height_right - 1], [0, new_height_left - 1]], dtype=np.float32)
        perspective_matrix = cv2.getPerspectiveTransform(np.float32(positions), new_rectangle)
        perspective_corrected_image = cv2.warpPerspective(data, perspective_matrix, (int((new_width_bottom+new_width_top)/2), int((new_height_right+new_height_left)/2)))
        mean_temperature=np.mean(perspective_corrected_image)
        mean_temperatures['T'+str(i)]=mean_temperature

        if save_figure:
            full_file = os.path.join(directory_camera, 'A'+str(i)+'__'+filename_camera)
            np.savetxt(full_file, perspective_corrected_image, delimiter=' ', fmt='%f')

        if plot_figures:
            # Create a grid for Subplots 2 to 7 on the right
            ax = plt.subplot(gs[i])
            ax.imshow(perspective_corrected_image, cmap='jet', aspect='auto', interpolation='gaussian')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('A {:d}'.format(i)+'- T={:.1f}'.format(mean_temperature)+'ºC')
            ax.axis('off')  # Turn off axes for empty subplots
            plt.tight_layout()

    if plot_figures:
        # Create a figure with two subplots
        plt.figure(1)
        # Subplot 1: Temperature Heatmap with Polygon Overlay
        #plt.imshow(data, cmap='inferno', aspect='auto', interpolation='gaussian')
        plt.imshow(data,  aspect='auto', interpolation='gaussian')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Temperature Heatmap [ºC]')

        for i, item in enumerate(area):
            x, y = map(list, zip(*item['positions']))
            # Draw the polygon perimeter on top of the image
            plt.plot(x + [x[0]], y + [y[0]], color='black', linewidth=1)
            # Annotate the plot with the label "A_0" at the centroid
            plt.text(np.mean(x), np.mean(y), r'$A{:}'.format(i) +'$', fontsize=9, color='black', ha='center', va='center')
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    return mean_temperatures






# Directory where the matrix camera file
directory_camera = 'DATA/tc_matrix'
# Filename of the matrix camera file
filename_camera = 'matrix_camera.txt'
# Specify the path to the JSON file of the vertex points of the areas to analyze (polygons)
file_name_area = "CONFIG/area.json"

temperatures = get_mean_temp_camera(directory_camera,filename_camera, file_name_area, plot_figures=True, save_figure=False)
# plot_figures=True --> Plots the different images to see how is working
# save_figure=True --> Save the selected areas of the polygons as a matrix on the directory_camera path
# As a result it gives a dictionary of the different mean temperatures of the areas.

print(temperatures)

