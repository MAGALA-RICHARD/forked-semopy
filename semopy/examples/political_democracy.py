#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Political Democracy model and data.

Bollen's Data on Industrialization and Political Democracy.
Dataset set includes four measures of democracy at two points in time, 1960
and 1965, and three measures of industrialization in 1960, for 75 developing
countries.
"""
import pandas as pd
import os

from pathlib import Path

__desc = '''# measurement model
ind60 =~ x1 + x2 + x3
dem60 =~ y1 + y2 + y3 + y4
dem65 =~ y5 + y6 + y7 + y8
# regressions
dem60 ~ ind60
dem65 ~ ind60 + dem60
# residual correlations
y1 ~~ y5
y2 ~~ y4 + y6
y3 ~~ y7
y4 ~~ y8
y6 ~~ y8'''

__folder = Path(os.path.dirname(os.path.abspath(__file__)))
__filename = __folder / "pd_data.csv"
__params_filename = __folder / "pd_lavaan_params.csv"


def get_model():
    """
    Retrieve model description in semopy syntax.

    Returns
    -------
    str
        Model's description.

    """
    return __desc


def get_data():
    """
    Retrieve dataset.

    Returns
    -------
    pd.DataFrame
        Dataset.

    """
    return pd.read_csv(__filename, index_col=0)


def get_params() -> pd.DataFrame:
    """
    Retrieve parameter values estimated by `lavaan` (https://gist.github.com/zuevval/17682e44b4778dc9156a944d306fb8d4)
    """
    return pd.read_csv(__params_filename, index_col=0)
