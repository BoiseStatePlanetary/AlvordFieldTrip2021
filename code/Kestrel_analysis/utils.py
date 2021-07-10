import numpy as np
import pandas as pd

from astropy import units as u
from astropy.coordinates import Angle

import glob

names_to_use = ['DateTime','Temp','Wet_Bulb_Temp','Rel_Hum','Baro','Altitude','Station_P',
                'Wind_Speed','Heat_Index','Dew_Point','Dens_Alt','Crosswind','Headwind','Mag_Dir',
                'True_Dir','Wind_Chill']

# The GPS locations for the Kestrel loggers
logger_locations = {'730': (Angle('42d30m21.492s'), Angle('-118d31m47.028s')),
                    '422': (Angle('42d30m21.42s'), Angle('-118d31m46.59s')),
                    '516': (Angle('42d30m22.248s'), Angle('-118d31m43.158s')),
                    '160': (Angle('42d30m24.468s'), Angle('-118d31m43.77s')),
                    '115': (Angle('42d30m24.378s'), Angle('-118d31m44.1s')),
                    '49': (Angle('42d30m25.02s'), Angle('-118d31m47.088')),
                    '50': (Angle('42d30m23.682s'), Angle('-118d31m48.192')),
                    '48': (Angle('42d30m24.72s'), Angle('-118d31m47.832')),
                    '51': (Angle('42d30m24.942s'), Angle('-118d31m47.118'))}

logger_names = ['730', '422', '516', '160', '115', '49', '50', '48', '51']

# Calculate mean lat/long
mean_lat = 0.
mean_long = 0.
for logger in logger_locations:
    mean_lat += logger_locations[logger][0]
    mean_long += logger_locations[logger][1]

mean_lat /= len(logger_locations)
mean_long /= len(logger_locations)
logger_locations['mean'] = (Angle(mean_lat), Angle(mean_long))

def read_kestrel_data(filename=None, logger_name=None):
    """
    Read in and process (if needed) Kestrel data files

    Args:
        filename (str): name of data file
        logger_name (str): name of logger whose data file you want

    Returns:
        pandas DataFrame: meteorological data

    """

    if((filename is None) and (logger_name is None)):
        raise ValueError("filename or logger_name must be given!")

    if(filename is None):
        filename = glob.glob("*" + logger_name + "_*.csv")[0]

    data = np.genfromtxt(filename, delimiter=',', skip_header=11, 
                         names=names_to_use, 
                         dtype=None)
    # Convert first two columns into datetime
    datatime = pd.to_datetime(data['DateTime'].astype(str))
    dataframe = pd.DataFrame(data[names_to_use[1:]])

    dataframe.insert(0, 'DateTime', datatime) 
    
    return dataframe

def plot_kestrel_timeseries(timeseries_name, ls=None):
    """
    Read in and plot desired time-series

    Args:
        timeseries_name (str): which time-series to plot
        ls (list of str): which data file names; if None, plot all
        "WEATHER*.csv" files

    """

    if(ls is None):
        # Read in all file names
        ls = glob.glob("WEATHER*.csv")

    # Read in and process Kestrel data
    filename = ls[0]
    data1 = read_kestrel_data(filename)
    ax1 = data1.plot(x='DateTime', y=timeseries_name, ls='', marker='.', figsize=(10,10), label=filename)

    fig = ax1.get_figure()

    if(len(ls) > 1):

        for filename in ls[1:]:
            data = read_kestrel_data(filename)
            data.plot(x='DateTime', y=timeseries_name, ls='', marker='.', ax=ax1, label=filename)

    ax1.legend()

    return fig, ax1
