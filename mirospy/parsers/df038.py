import re
import datetime as dt

import numpy as np
import xarray as xr
from wavespectra.specarray import SpecArray
from wavespectra.specdataset import SpecDataset


__version__ = '1.0'
__author__ = 'MetOcean Solutions Ltd.'

class ParseDF038(object):
    """
    Read spectra from Shell format DF038:
        classInstance = SpectraShell(filename)
    - filename: Name of spectra file to read
    - TODO improve description
    - TODO generalize for multiple times (array)
    """
    def __init__(self, filename):
        
        self.filename = filename        
        self._file2dict() # generate dictionary 'dictshell'
        self.nfreq = int(self.dictshell['Number_Of_Frequencies'])
        self.ifreq = float(self.dictshell['Start_Frequency'])
        self.dfreq = float(self.dictshell['Frequency_Resolution'])
        self.freqs = np.arange(self.ifreq,self.nfreq*self.dfreq,self.dfreq)
        self.ndirs = int(self.dictshell['Number_Of_Directions'])
        self.dirs = np.arange(0,360,360./ self.ndirs)
        # set of methods to extract dimensions and spectra
        self._get_times()
        self._get_lonlat()
        self._get_spectra()

    def _file2dict(self):
        fid = open(self.filename, 'r')
        FileContent = fid.read().splitlines() # list with file FileContent
        indicesH = [i for i, s in enumerate(FileContent) if '=' in s] # indices of header values, defined with '='
        # dictionary with all header info and data
        self.dictshell = dict([(FileContent[i].split("=")[0],FileContent[i].split("=")[1]) for i in indicesH])        
        indiceD = FileContent.index('[DATA]')+1 # Indice of 'Data' in FileContent list
        self.dictshell.update(dict([('DATA', FileContent[indiceD])]))

    def _get_times(self):
        content = self.dictshell['DATA']
        # get time valuer from file
        year,month,day,hour,minu,sec = re.split(' |-|:', content[:content.find("Z")])[:-1]
        self.times = dt.datetime(int(year), int(month), int(day), int(hour), int(minu), int(sec))

    def _get_lonlat(self):
        content = self.dictshell['DATA']
        coordstr = re.split(' |,| ', content[-20:])
        self.lon = float(coordstr[2][0:3])+(float(coordstr[2][3:])/60)
        self.lon = -self.lon if coordstr[3] is 'W' else self.lon
        self.lat = float(coordstr[0][0:2])+(float(coordstr[0][2:])/60)
        self.lat = -self.lat if coordstr[3] is 'S' else self.lat
    
    def _get_spectra(self):
        content = self.dictshell['DATA']
        specs = np.fromstring(content[content.find("Z")+1:content.find("1-------")],sep=' ') # remove time
        dirscopy = self.dirs + 180 # correct direction to "coming from" 
        dirscopy[dirscopy>=360] = dirscopy[dirscopy>=360]-360
        idirs = dirscopy.argsort() 
        spec = specs[self.nfreq:].reshape(1, 1, 1, self.ndirs, self.nfreq).transpose(0,1, 2, 4, 3)
        # convert spectra to DataArray:
        self.spec2d = xr.DataArray(spec[:,:,:,:,idirs], coords={'time': [self.times], 'lat': [self.lat], 'lon': [self.lon], \
                                                 'freq': self.freqs, 'dir': self.dirs}, \
                                                  dims=('time', 'lat', 'lon', 'freq', 'dir'))

    def shell2swan(self):
        ds = self.spec2d.to_dataset(name='efth')
        ds.spec.to_swan(self.filename.split('/')[-1]+'.spec') # write SWAN spec file in pwd

if __name__ == '__main__':
    filename = './Example_files/MIR_LD1_NOW.DF038'
    shell = ShellDF038(filename)