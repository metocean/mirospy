from os.path import *
import datetime

import pytest
import xarray as xr

from ..parsers import df038, df022

HERE = dirname(abspath(__file__))

def test_read_df038():
    data = df038.ParseDF038(join(HERE,'data/MIR_LD1_NOW.DF038'))
    assert isinstance(data.spec2d, xr.DataArray)

def test_read_df022_header():
    data = df022.ParseDF022(join(HERE,'data/MIR_All_NOW.DF022'))
    assert isinstance(data.header['datetime'], datetime.datetime)
    assert data.header['data_format'] == 'DF022'
    assert data.header['site'] == '1095'

def test_read_df022_blocks():
    data = df022.ParseDF022(join(HERE,'data/MIR_All_NOW.DF022'))
    assert len(data.data_blocks['WM']) == 2
    for vals in data.data_blocks['WM']:
        assert len(vals) == 43
    assert data.data_blocks['CV'][0][1] == None
    assert data.data_blocks['CV'][1][0] == 0.04

def test_get_available_blocks():
    data = df022.ParseDF022(join(HERE,'data/MIR_All_NOW.DF022'))
    assert data.available_blocks.keys() == data.data_blocks.keys()

def test_get_param():
    data = df022.ParseDF022(join(HERE,'data/MIR_All_NOW.DF022'))
    assert data.get_param('Air Temperature (1 min. mean)') == [2.94]
    assert data.get_param('Average Heading') == [-125.66, -121.72, None, -122.94]
    assert data.get_param('Air Temperature (1 min. mean)') == [2.94]
    assert data.get_param('Cloud Level 1 (lowest cloud) (2min)',True) == ([1331.26],'m/s')