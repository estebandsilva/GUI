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
import numpy as np


class Plot_Sensor:

    def __init__(self, magnitude='temperature', sub_magnitude='outside'):

        self.sensors_plots = {
        'temperature': {'outside':['C1T01A1','C1T02A1'],'inside':['C2T03A1','C2T04A1'],'interior':['C4T05A1','C4T06A1'],'heating':['C5T10A1'],'up':['C1T01A1','C2T03A1','C4T05A1'],'down':['C1T02A1','C2T04A1','C4T06A1'],'all':['C1T01A1','C1T02A1','C2T03A1','C2T04A1','C4T05A1','C4T06A1','C5T10A1']},
        'humidity':    {'outside':['C1H01A2','C1H02A2'],'inside':['C2H03A2','C2H04A2'],'interior':['C4H05A2','C4H06A2'],'heating':['C5H10A2'],'up':['C1H01A2','C2H03A2','C4H05A2'],'down':['C1H02A2','C2H04A2','C4H06A2'],'all':['C1H01A2','C1H02A2','C2H03A2','C2H04A2','C4H05A2','C4H06A2','C5H10A2']},
        'pressure_atm':{'outside':['C1P01A3','C1P02A3'],'inside':['C2P03A3','C2P04A3'],'interior':['C4P05A3','C4P06A3'],'heating':['C5P10A3'],'up':['C1P01A3','C2H03A2','C4P05A3'],'down':['C1P02A3','C2P04A3','C4P06A3'],'all':['C1P01A3','C1P02A3','C2P03A3','C2P04A3','C4P05A3','C4P06A3','C5P10A3']},
        'pressure_abs':{'outside':['C1P01B0','C1P02B0'],'inside':['C2P03B0','C2P04A3'],'interior':['C4P05A3','C4P06B0'],'heating':['C5P10B0'],'up':['C1P01B0','C2P03B0','C4P05B0'],'down':['C1P02B0','C2P04B0','C4P06B0'],'all':['C1P01B0','C1P02B0','C2P03B0','C2P04B0','C4P05B0','C4P06B0','C5P10B0']},
        'velocity':{'wind':['C3W08X1','C3Y08X2'],'air':['C3V07X0','C5V09X0'],'all':['C3V07X0','C5V09X0', 'C3W08X1']},
        'solar':{'radiation':['C3S11X0']},
        'camera':{'image':['E1T13A0'],'areas':['E1T13A0_A'],'sub_matrix':['E1T13A0_SUB'],'temperature':['T1','T2','T3','T4','T5'],'image_temperature':['E1T13A0_IT']}
        }

        self.sensors_dict = {
        'C3V07X0':['Velocity [m/s]','Air Outside Up'], 'C5V09X0':['Velocity [m/s]','Air Heating'],
        'C3W08X1':['Velocity [m/s]','Wind Outside Up'],'C3Y08X2':['Direction [º]','Wind Outside Up'],
        'C3S11X0':['Solar Radiation [W/m^2]','Outside Up'],
        'C1T01A1':['Temperature [ºC]','Outside Up'],   'C1H01A2':['Relative Humidity [%]','Outside Up'],   'C1P01A3':['Pressure Atm [Pa]','Outside Up'],   'C1P01B0':['Pressure Abs [Pa]','Outside Up'],
        'C1T02A1':['Temperature [ºC]','Outside Down'], 'C1H02A2':['Relative Humidity [%]','Outside Down'], 'C1P02A3':['Pressure Atm [Pa]','Outside Down'], 'C1P02B0':['Pressure Abs [Pa]','Outside Down'],
        'C2T03A1':['Temperature [ºC]','Inside Up'],    'C2H03A2':['Relative Humidity [%]','Inside Up'],    'C2P03A3':['Pressure Atm [Pa]','Inside Up'],    'C2P03B0':['Pressure Abs [Pa]','Inside Up'],
        'C2T04A1':['Temperature [ºC]','Inside Down'],  'C2H04A2':['Relative Humidity [%]','Inside Down'],  'C2P04A3':['Pressure Atm [Pa]','Inside Down'],  'C2P04B0':['Pressure Abs [Pa]','Inside Down'],
        'C4T05A1':['Temperature [ºC]','Interior Up'],  'C4H05A2':['Relative Humidity [%]','Interior Up'],  'C4P05A3':['Pressure Atm [Pa]','Interior Up'],  'C4P05B0':['Pressure Abs [Pa]','Interior Up'],
        'C4T06A1':['Temperature [ºC]','Interior Down'],'C4H06A2':['Relative Humidity [%]','Interior Down'],'C4P06A3':['Pressure Atm [Pa]','Interior Down'],'C4P06B0':['Pressure Abs [Pa]','Interior Down'],
        'C5T10A1':['Temperature [ºC]','Heating'],      'C5H10A2':['Relative Humidity [%]','Heating'],      'C5P10A3':['Pressure Atm [Pa]','Heating'],      'C5P10B0':['Pressure Abs [Pa]','Heating'],
        'T1': ['Temperature [ºC]', 'T_1'],'T2': ['Temperature [ºC]', 'T_2'],'T3': ['Temperature [ºC]', 'T_3'],'T4': ['Temperature [ºC]', 'T_4'],'T5': ['Temperature [ºC]', 'T_5'],
        }

        self.camera_dict={'E1T13A0':['Temperature [ºC]','Camera'], 'E1T13A0_T':['Temperature [ºC]','Areas']}

        self.columns_to_keep = ["sensor_identifier", "magnitude", "unit", "value", "sampled_at", "formula_key", "formula_offset"]  # Replace with the column names you want to keep
        self.past_minutes = 2

        # Get the absolute path of the current script
        self.script_dir = os.path.abspath(os.path.dirname(__file__))

        # Create an empty DataFrame to store merged and selected data
        self.file_timestamps = {}
        self.df = pd.DataFrame()

        #self.setup(magnitude = 'temperature', type = 'outside')
        self.setup(magnitude=magnitude, sub_magnitude=sub_magnitude)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)


    def setup(self,magnitude= 'temperature', sub_magnitude = 'outside'):
        self.sensors_to_keep = self.sensors_plots[magnitude][sub_magnitude]
        self.folder_to_copy ='ad' # default

        if bool(set(self.sensors_to_keep).intersection(set(list(self.sensors_dict.keys())))):
            self.folder_to_copy = 'ad' # Sensores
        if bool(set(self.sensors_to_keep).intersection({'T1'})):
            self.folder_to_copy = 'tc'  # Temperaturas Matrices
        if set(self.sensors_to_keep).intersection({'E1T13A0'}):
            self.folder_to_copy = 'tc_matrix' # Temperaturas Camera

        self.sensors_dict.update(self.camera_dict)

        # Get the absolute path of the current script
        self.folder_path = os.path.join(self.script_dir, "DATA", self.folder_to_copy)
        self.output_folder = self.folder_path


    def process_csv_file(self,csv_file):
        try:
            file_path = os.path.join(self.folder_path, csv_file)
            df = pd.read_csv(file_path, usecols=self.columns_to_keep)

            if len(self.sensors_to_keep) > 0:
                selected_rows = df[df['sensor_identifier'].isin(self.sensors_to_keep)]
            else:
                selected_rows = df

            return selected_rows
        except Exception as e:
            print(f"Error processing file {csv_file}: {str(e)}")
            return None

    def formula_apply(self, row):
        key = row['formula_key']
        value = row['value']
        offset = row['formula_offset']
        gain = 1.0

        if key == '1A':
            return gain * (6.25 * (16 * value / 65536 + 4) - 65) - offset
        elif key == '1B':
            return gain * (6.25 * (16 * value / 65536 + 4) - 55) - offset
        elif key == '2':
            return gain * (6.25 * (16 * value / 65536 + 4) - 25) - offset
        elif key == '3':
            return gain * (6250 * (16 * value / 65536 + 4) - 15000) - offset
        elif key == '4':
            return gain * (12500 * (16 * value / 65536 + 4) - 50000) - offset
        elif key == '5':
            return gain * (1.25 * (16 * value / 65536 + 4) - 5) - offset
        elif key == '6':
            return gain * (125 * (16 * value / 65536 + 4) - 500) - offset
        elif key == '7':
            return gain * (22.5 * (16 * value / 65536 + 4) - 90) - offset
        elif key == '8':
            return gain * (2.5 * (16 * value / 65536 + 4) - 10) - offset
        else:
            return value

    def update_df(self):
        #global df, folder_path, past_minutes

        # List CSV files in the folder
        self.csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]

        # Filter out files that are new or modified
        self.updated_csv_files = []
        for csv_file in self.csv_files:
            self.file_path = os.path.join(self.folder_path, csv_file)
            self.current_timestamp = os.path.getmtime(self.file_path)
            if csv_file not in self.file_timestamps or self.file_timestamps[csv_file] != self.current_timestamp:
                self.updated_csv_files.append(csv_file)
                self.file_timestamps[csv_file] = self.current_timestamp

        if not self.updated_csv_files:
            # print("No new or modified CSV files found.")
            return False
        else:
            # print(updated_csv_files)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit tasks for processing updated CSV files
                futures = [executor.submit(self.process_csv_file, csv_file) for csv_file in self.updated_csv_files]
                # Wait for tasks to complete and collect results
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result is not None:
                        result['sampled_at'] = result['sampled_at'].str.replace('T', ' ')
                        result['value_unit'] = result.apply(self.formula_apply, axis=1)
                        result['sampled_at'] = pd.to_datetime(result['sampled_at'],format='%Y-%m-%d %H:%M:%S.%f%z') + pd.to_timedelta('2 hours')
                        self.df = pd.concat([self.df, result], ignore_index=True)

            self.df = self.df.sort_values(by='sampled_at', ascending=True)
            self.df = self.df[self.df['sampled_at'] >= self.df['sampled_at'].iloc[-1] - timedelta(minutes=self.past_minutes)]
            self.df = self.df.drop_duplicates(keep='last')
            self.df = self.df.reset_index(drop=True)

            return True
            # print(df)

    def save_df(self):
        # Save the merged and selected DataFrame to a new CSV file in the output folder
        output_file_path = os.path.join(self.output_folder, 'merged_and_selected_data.csv')
        self.df.to_csv(output_file_path, index=False)
        print(f"Merged and selected data saved to {output_file_path}")




    # Function to update the data and plot
    def update_plot(self):
        if self.update_df():
            ax = self.figure.add_subplot(111)
            ax.clear()

            for key in self.sensors_to_keep:
                subset = self.df[self.df['sensor_identifier'] == key]

                ax.scatter(subset['sampled_at'], subset['value_unit'], alpha=0.33, s=2)
                line = ax.plot(subset['sampled_at'], subset['value_unit'].rolling(window=3).mean().ewm(span=3).mean(), label=self.sensors_dict[key][1])
                last_value = subset['value_unit'].iloc[-1]
                last_time = subset['sampled_at'].iloc[-1]
                ax.text(last_time, last_value, f'{last_value:.2f}', color=line[0].get_color(), va='bottom', ha='center')

            ax.set_xlabel('Time')
            ax.set_ylabel(self.sensors_dict[key][0])
            ax.set_title(self.sensors_dict[key][0] + ' Evolution - ' + str(self.df['sampled_at'].iloc[-1].strftime('%d/%m/%y - %H:%M:%S')))
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
            ax.grid(True)
            ax.legend(loc='upper left')
            self.canvas.draw()