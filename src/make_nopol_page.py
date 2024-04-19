'''
    calibrator.py
'''

import datetime
import tempfile
import pathlib
import urllib.request
import numpy as np
import pandas as pd
import jinja2
from utils import write_html_file

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
        return calib_freq_recent.sort_values(by='Date', ascending=False)



def download_file(url="https://www.alma.cl/~skameno/AMAPOLA/amapola.txt") -> str:
    """Retrieve amapola file"""

    path = pathlib.Path(tempfile.mkdtemp())
    destination_path = path / "amapola.txt"
    urllib.request.urlretrieve(url, destination_path)

    return str(destination_path)

if __name__ == "__main__":

    # load file
    amapola = AMAPOLAFile()

    # datetimeid
    dtts = datetime.datetime.today().timestamp()

    # folders of relevance
    templates_dir   = './src/templates/'

    # load templates
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    templateEnv     = jinja2.Environment(loader=template_loader)

    # get the right template
    tmplt = templateEnv.get_template('nopol.html')

    band_6 = amapola.get_recent_values(calibrator_name="    Pallas ", freq_ghz=233, lookback_days=360)
    band_7 = amapola.get_recent_values(calibrator_name="    Pallas ", freq_ghz=343.45, lookback_days=360)

    obs_list_233 = []
    for _, row in band_6.iterrows():
        I = f"{(row['I']):0.3f} +/- {(row['eI']):0.3f}"
        Q = f"{(row['Q']):0.3f} +/- {(row['eQ']):0.3f}"
        U = f"{(row['U']):0.3f} +/- {(row['eU']):0.3f}"
        polperc = f"{(row['P']/row['I'] * 100):0.1f} +/- {(np.mean([row['P'] - row['eP_lower'], row['eP_upper']- row['P']])/row['I'] * 100):0.1f}"
        evpa = f"{np.rad2deg(row['EVPA']):0.1f} +/- {np.rad2deg(row['eEVPA']):0.1f}"
        obs = dict(date=row['Date'].strftime('%Y-%m-%d'),I=I, polperc=polperc, evpa=evpa, Q=Q, U=U)
        obs_list_233.append(obs)
    obs_list_343 = []
    for _, row in band_7.iterrows():
        I = f"{(row['I']):0.3f} +/- {(row['eI']):0.3f}"
        Q = f"{(row['Q']):0.3f} +/- {(row['eQ']):0.3f}"
        U = f"{(row['U']):0.3f} +/- {(row['eU']):0.3f}"
        polperc = f"{(row['P']/row['I'] * 100):0.1f} +/- {(np.mean([row['P'] - row['eP_lower'], row['eP_upper']- row['P']])/row['I'] * 100):0.1f}"
        evpa = f"{np.rad2deg(row['EVPA']):0.1f} +/- {np.rad2deg(row['eEVPA']):0.1f}"
        obs = dict(date=row['Date'].strftime('%Y-%m-%d'),I=I, polperc=polperc, evpa=evpa, Q=Q, U=U)
        # strftime('%Y-%m-%d %H:%M:%S')
        obs_list_343.append(obs)

    # payload
    payload = dict()
    payload['dtts'] = dtts
    payload['last_observation_str'] = pd.to_datetime(str(amapola.amapola_data.sort_values(by='Date')['Date'].values[-1])).strftime('%Y-%m-%d %H:%M:%S')
    payload['obs_list_233'] =  obs_list_233
    payload['obs_list_343'] =  obs_list_343

    write_html_file(
        tmplt.render(payload),
        'index.html',
        './docs/nopol/',
        subfolder=None
    )
