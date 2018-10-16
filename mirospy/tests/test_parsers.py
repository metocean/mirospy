import pytest

from .. import parsers


def test_read_df038():
    data = parsers.df038.ParseDF038('data/MIR_LD1_NOW.DF038')
    assert data.spec2d