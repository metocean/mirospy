# -*- coding: utf-8 -*-

import datetime
import re

class ParseDF022(object):
    """docstring for ParseDF022"""
    def __init__(self, filename, 
                 missing_values=('-999.99','-999.88','-999.77')):
        super(ParseDF022, self).__init__()
        self.filename = filename
        self.missing_values = missing_values
        self.raw_lines = []
        self.header = {}
        self.data_blocks = {}
        self.block_id_re = re.compile(r"^\w\w\w-\d{3}")
        self.blocks_metadata = {
            'title' : {
                'CL': 'Cloud Level Data',
                'CV': 'Current from Miros Wave Radar',
                'PT': 'Precipitation Data',
                'PW': 'Weather and Visibility',
                'TH': 'Air Temperature Humidity Pressure Data',
                'VB': 'Vessel Position',
                'VG': 'Vessel Heading True',
                'VH': 'Vessel Heading',
                'VM': 'Vessel Motion (general data)',
                'VN': 'Vessel Motion (location dependant data)',
                'WA': 'Wind Data (polar averaging)',
                'WM': 'Wave parameters from wave spectrum',


            },
            'params': {
                'CL': ['Cloud Level 1 (lowest cloud) (2min)',
                    'Cloud Level 2 (2min)',
                    'Cloud Level 3 (2min)',
                    'Vertical Visibility (ALCH) (2min)',
                    'Cloud Level 1 (lowest cloud) (10min)',
                    'Cloud Level 2 (10min)',
                    'Cloud Level 3 (10min)',
                    'Vertical Visibility (ALCH) (10min)',
                    'Laser Status',
                    'Receiver Status',
                    'Window Status',
                    'Other Status',
                    'Cloud Cover Layer 1 (30min)',
                    'Cloud Height Layer 1 (30min)',
                    'Cloud Cover Layer 2 (30min)',
                    'Cloud Height Layer 2 (30min)',
                    'Cloud Cover Layer 3 (30min)',
                    'Cloud Height Layer 3 (30min)',
                    'Cloud Cover Layer 4 (30min)',
                    'Cloud Height Layer 4 (30min)'],
                'PT': ['Precipitation last fixed 3 hours'],
                'PW': ['Cumulative Snow Sum Last 1 minute',
                       'Cumulative Water Sum Last 1 minute',
                       'Precipitation Water Intensity Last 1 min Average',
                       'Cumulative Snow Sum Last 1 Hour',
                       'Cumulative water sum, last 1 Hour',
                       'One Hour Present Weather Code',
                       '15 minutes Present Weather Code',
                       'Instant Present Weather Code',
                       'Visibility 1 minutes Average (MOR)',
                       'Visibility 10 minutes Average (MOR)',
                       'Instant Weather (Metar Codes - GR1)',
                       'Recent Weather (Metar Codes - GR1)',
                       'Instant Weather (Metar Codes - GR2)',
                       'Recent Weather (Metar Codes - GR2)',
                       'Instant Weather (Metar Codes - GR3)',
                       'Recent Weather (Metar Codes - GR3)',
                       'Background Luminance',
                       'Crossarm Temperature',
                       'Hardware Error',
                       'Hardware Warning',
                       'Runway Light Intensity',
                       'Visibility 1 minutes Average (RVR)',
                       'Visibility 10 minutes Average (RVR)'],

                'TH': [ 'Air Temperature (1 min. mean)',
                        'Air Dewpoint Temperature (1 min. mean)',
                        'Air Humidity (1 min. mean)',
                        'Air Pressure at sensor level (1 min. mean)',
                        'Air Pressure QFE (1 min. mean)',
                        'Air Pressure QNH (1 min. mean)',
                        'Air Pressure QFF (1 min. mean)',
                        'Air Pressure 3 Hour Trend (1 min. mean)'],
                'VB': ['Latitude','Longitude'],
                'VG': ['Observation/ Averaging period',
                        'Vessel Heading True - Average',
                        'Vessel Heading True - Max Starboard',
                        'Vessel Heading True - Max Port',
                        'Vessel Heading True - RMS',
                        'Vessel Heading True - Start',
                        'Vessel Heading True - End'],
                'VH': ['Vessel Heading 1 min mean'],
                'VM': ['Observation / Averaging period',
                        'List',
                        'Max Roll Starboard',
                        'Max Roll Port',
                        'Trim',
                        'Max Pitch Up',
                        'Max Pitch Down',
                        'Average Heading',
                        'Max Yaw Starboard',
                        'Max Yaw Port',
                        'Max Roll',
                        'Max Pitch',
                        'Max Yaw',
                        'Total Roll',
                        'Total Pitch',
                        'Total Yaw',
                        'Max Static Deck Inclination'],
                'VN':['Location x-coordinate',
                      'Location y coordinate',
                      'Location z coordinate',
                      'Observation period in minutes',
                      'Max Heave - Total (peak to peak)',
                      'Max Surge - Total (peak to peak)',
                      'Max Sway - Total (peak to peak)',
                      'Max Heave Speed',
                      'Max Surge Speed',
                      'Max Sway Speed',
                      'Max Heave Acceleration',
                      'Max Surge Acceleration',
                      'Max Sway Acceleration',
                      'Max Heave- Single (peak to peak)',
                      'Average Heave',
                      'Average Heave Speed',
                      'Average Heave Rate',
                      'Max Average Heave Rate 1',
                      'Max Average Heave Rate 2',
                      'Average Heave Period',
                      'Min Heave Period',
                      'Max Heave Period',
                      'Max Average Heave Rate 3',
                      'Significant Heave Rate'],
                'WA': ['Sensor Height',
                        'Speed Reduction Exponent',
                        'Min. Wind Speed (Lull) True Last 2 min 10m level',
                        'Aver. Wind Speed True Last 2 min 10m level',
                        'Max. Wind Speed (Gust) True Last 2 min 10m level',
                        'Min. Wind Speed (Lull) True Last 10 min 10m level',
                        'Aver. Wind Speed True Last 10 min 10m level',
                        'Max. Wind Speed (Gust) True Last 10 min 10m level',
                        'Min. Wind Speed (Lull) True Last 2 min Sensor level',
                        'Aver. Wind Speed True Last 2 min Sensor level',
                        'Max. Wind Speed (Gust) True Last 2 min Sensor level',
                        'Min. Wind Speed (Lull) True Last 10 min Sensor level',
                        'Aver. Wind Speed True Last 10 min Sensor level',
                        'Max. Wind Speed (Gust) True Last 10 min Sensor level',
                        'Min. Wind Speed (Lull) Relative Last 2 min 10m level',
                        'Aver. Wind Speed Relative Last 2 min 10m level',
                        'Max. Wind Speed (Gust) Relative Last 2 min 10m level',
                        'Min. Wind Speed (Lull) Relative Last 10 min 10m level',
                        'Aver. Wind Speed Relative Last 10 min 10m level',
                        'Max. Wind Speed (Gust) Relative Last 10 min 10m level',
                        'Min. Wind Speed (Lull) Relative Last 2 min Sensor level',
                        'Aver. Wind Speed Relative Last 2 min Sensor level',
                        'Max. Wind Speed (Gust) Relative Last 2 min Sensor level',
                        'Min. Wind Speed (Lull) Relative Last 10 min Sensor level',
                        'Aver. Wind Speed Relative Last 10 min Sensor level',
                        'Max. Wind Speed (Gust) Relative Last 10 min Sensor level',
                        'Min. Wind Direction True Last 2 min',
                        'Aver. Wind Direction True Last 2 min',
                        'Max. Wind Direction True Last 2 min',
                        'Gust Wind Direction True Last 2 min',
                        'Min. Wind Direction True Last 10 min',
                        'Aver. Wind Direction True Last 10 min',
                        'Max. Wind Direction True Last 10 min',
                        'Gust Wind Direction True Last 10 min',
                        'Min. Wind Direction Relative Last 2 min',
                        'Aver. Wind Direction Relative Last 2 min',
                        'Max. Wind Direction Relative Last 2 min',
                        'Gust Wind Direction Relative Last 2 min',
                        'Min. Wind Direction Relative Last 10 min',
                        'Aver. Wind Direction Relative Last 10 min',
                        'Max. Wind Direction Relative Last 10 min',
                        'Gust Wind Direction Relative Last 10 min',
                        'Min. Wind Direction Magnetic Last 2 min',
                        'Aver. Wind Direction Magnetic Last 2 min',
                        'Max. Wind Direction Magnetic Last 2 min',
                        'Gust Wind Direction Magnetic Last 2 min',
                        'Min. Wind Direction Magnetic Last 10 min',
                        'Aver. Wind Direction Magnetic Last 10 min',
                        'Max. Wind Direction Magnetic Last 10 min',
                        'Gust Wind Direction Magnetic Last 10 min'],
                'WM': ['Primary wave spectral density',
                        'Significant wave height',
                        'Maximum wave height',
                        'Wave height of maximum wave period',
                        'Primary wave peak period',
                        'Secondary wave peak period',
                        'Calculated wave peak period',
                        'Significant wave period',
                        'Energy wave period',
                        'Integral wave period',
                        'Mean zero up-crossing period',
                        'Mean period',
                        'Maximum wave period',
                        'Wave period of maximum wave height',
                        'Average wave crest period',
                        'Primary wave peak direction True',
                        'Primary wave mean direction True',
                        'Primary wave directional spread',
                        'Total energy peak direction True',
                        'Total energy mean direction True',
                        'Total energy directional spread',
                        'Spectral band width',
                        'Skewness',
                        'Wave steepness',
                        'Zero order moment',
                        '1st order moment',
                        '2nd order moment',
                        '3rd order moment',
                        '4th order moment',
                        '1st order negative moment',
                        '2nd order negative moment',
                        'Primary wave phase velocity',
                        'Primary wave length ',
                        'Primary wave group velocity',
                        'Secondary wave peak direction True',
                        'Secondary wave mean direction True',
                        'Secondary wave directional spread',
                        'Primary wave peak direction Relative',
                        'Primary wave mean direction Relative',
                        'Secondary wave peak direction Relative',
                        'Secondary wave mean direction Relative',
                        'Total energy peak direction Relative',
                        'Total energy mean direction Relative'],
            },
            'units': {
                'CV': ['m','m','m','m','m','m','m',None,None,None,None,
                       'oktas','m','oktas','m','oktas','m','oktas','m'],
                'CL': ['m/s','m/s','m/s','m/s','m/s','m/s','deg','deg',
                       'm/s','deg','deg','deg','deg','min'],
                'PT': ['mm'],
                'PW': ['mm','mm','mm/h','mm','mm',None,None,None,'m','m',
                       None,None,None,None,None,None,'cd/m2','degC',None,None,
                       'cd','m','m'],
                'TH': [u'°C',u'°C','%RH','hPa','hPa','hPa','hPa','hPa'],
                'VB': ['degmin','degmin'],
                'VG': ['min']+['deg']*6,
                'VH': ['deg'],
                'VM': ['min']+['deg']*16,
                'VN': ['m','m','m','min','m','m','m','m/s','m/s','m/s','m/s2','m/s2',
                        'm/s2','m','m','m/s','m/s','m/s','m/s','s','s','s','m/s',
                       'm/s'],
                'WA': ['m',None]+(['m/s']*24)+(['deg']*24),
                'WM':['m2/Hz']+(['m']*3)+(['s']*11)+(['deg']*6)+[u'ʋ']+([None]*2)+\
                     [u'm²',u'm²/s',u'm²/s²',u'm²/s³',u'm²/s⁴',u'm².s',u'm².s²',
                     'm/s','m','m/s']+['deg']*9,
            },

        }

        
        self._read_raw()
        self._read_header()
        self._read_data_blocks()
        
    def _read_raw(self):
        self.raw_lines = []
        with open(self.filename) as openfile:
            for line in openfile.readlines():
                self.raw_lines.append(line.strip())


    def _read_header(self):
        self.header = {
            'data_format': self.raw_lines[1],
            'site': self.raw_lines[2],
            'datetime': datetime.datetime.strptime(\
                            self.raw_lines[3]+'T'+self.raw_lines[4],
                            '%d-%m-%YT%H:%M')
        }
    
    def _read_data_blocks(self):
        blocks = {}
        for line in self.raw_lines[5:]:
            if self.block_id_re.match(line):
                block_id = line[:2]

                try: block_n = int(line[2])-1
                except: block_n = 0

                if block_id not in blocks:
                    blocks[block_id] = [[]]
                elif (block_n+1) > len(blocks[block_id]):
                    blocks[block_id] += [[]]*((block_n+1)-len(blocks[block_id]))
            elif line == '$$$$$$$':
                pass
            else:
                value = float(line) if line not in self.missing_values else None
                blocks[block_id][block_n].append(value)

        self.data_blocks = blocks

    @property
    def available_blocks(self):
        params = {}
        for key in self.data_blocks.keys():
            params[key]=self.blocks_metadata['title'].get(key,'Unknown')
        return params
    
    def get_param(self, param, units=False):
        for key, values in self.data_blocks.items():
            if key in self.blocks_metadata['params'] and\
               param in self.blocks_metadata['params'][key]:
                try:
                    param_index = self.blocks_metadata['params'][key].index(param)
                    param_values = [v[param_index] for v in values]
                    if units:
                        unit = self.blocks_metadata['units'][key][param_index]
                        return param_values,unit
                    else:
                        return param_values
                except:
                    pass

