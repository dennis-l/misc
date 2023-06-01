'''
    calibrator.py
'''

import datetime
import tempfile
import pathlib
import urllib.request
import numpy as np
import pandas as pd

class AMAPOLAFile(object):
    def __init__(self):
        self._load_file()

    def _load_file(self):
        """ load the amapola file """

        def download_file(url="https://www.alma.cl/~skameno/AMAPOLA/amapola.txt") -> str:
            path = pathlib.Path(tempfile.mkdtemp())
            destination_path = path / "amapola.txt"
            urllib.request.urlretrieve(url, destination_path)
            return str(destination_path)
        
        amapola_file_path = download_file() 
        self.amapola_data = pd.read_csv(amapola_file_path, delimiter='\t')
        self.amapola_data['Date'] = pd.to_datetime(self.amapola_data['Date'])
        self.amapola_data['polpercentage'] = 100 * np.sqrt(self.amapola_data['Q']**2 + self.amapola_data['U']**2) / self.amapola_data['I']
        self.amapola_data['p'] =  self.amapola_data['P'] / self.amapola_data['I']
        self.amapola_data['polangle'] = np.arctan2(self.amapola_data['U'], self.amapola_data['Q'])
        self.amapola_data['rotatedpolangle'] = np.arctan2(self.amapola_data['U'], self.amapola_data['Q']) + (np.pi / 2)

    def get_latest_value(self, calibrator_name: str, freq_ghz: float):
        """
        calib_band_6 = calib.loc[calib['Freq'] == 233].copy()
        calib_band_7 = calib.loc[calib['Freq'] == 343.45].copy()
        """
        
        calib = self.amapola_data.loc[self.amapola_data['Src'] == calibrator_name].copy()
        calib_freq = calib.loc[calib['Freq'] == freq_ghz].copy()
        return calib_freq.sort_values(by='Date')[-1:]
        

    def get_recent_values(self, calibrator_name: str, freq_ghz: float, lookback_days: int):
        calib = self.amapola_data.loc[self.amapola_data['Src'] == calibrator_name].copy()
        calib_freq = calib.loc[calib['Freq'] == freq_ghz].copy().sort_values(by='Date')
        calib_freq_recent = calib_freq.loc[calib_freq['Date'] >= datetime.datetime.today() - datetime.timedelta(days=lookback_days)]
        return calib_freq_recent
    


def download_file(url="https://www.alma.cl/~skameno/AMAPOLA/amapola.txt") -> str:
    """Retrieve amapola file"""

    path = pathlib.Path(tempfile.mkdtemp())
    destination_path = path / "amapola.txt"
    urllib.request.urlretrieve(url, destination_path)

    return str(destination_path)

if __name__ == "__main__":

    # load file
    amapola = AMAPOLAFile()

    # get the latest value of that calibrator at that frequency
    _ = amapola.get_latest_value(calibrator_name="J1331+3030 ", freq_ghz=233)
    _ = amapola.get_latest_value(calibrator_name="J1331+3030 ", freq_ghz=343.45)

    # get the latest values of that calibrator at that frequency
    _ = amapola.get_recent_values(calibrator_name="J1331+3030 ", freq_ghz=233, lookback_days=30)
    _ = amapola.get_recent_values(calibrator_name="J1331+3030 ", freq_ghz=343.45, lookback_days=30)

    
 