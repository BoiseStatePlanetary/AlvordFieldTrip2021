import numpy as np
import pandas as pd

def read_kestrel_data(filename):
    """
    Read in and process (if needed) Kestrel data files

    Args:
        filename (str): name of data file

    Returns:
        pandas DataFrame: meteorological data

    """
    names_to_use = ['DateTime','Temp','Wet_Bulb_Temp','Rel_Hum','Baro','Altitude','Station_P',
                    'Wind_Speed','Heat_Index','Dew_Point','Dens_Alt','Crosswind','Headwind','Mag_Dir',
                    'True_Dir','Wind_Chill']
    data = np.genfromtxt(filename, delimiter=',', skip_header=11, 
                         names=names_to_use, 
                         dtype=None)
    # Convert first two columns into datetime
    datatime = pd.to_datetime(data['DateTime'].astype(str))
    dataframe = pd.DataFrame(data[names_to_use[1:]])

    dataframe.insert(0, 'DateTime', datatime) 
    
    return dataframe
