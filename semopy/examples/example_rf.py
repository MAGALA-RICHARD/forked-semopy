#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An example of dataset with random effects.

Correct parameter estimates:
       lval  op  rval     Value
    0    x2   ~  eta1  2.008729
    1  eta2   ~  eta1  2.879663
    2    x1   ~  eta1 -2.292444
    3  eta1  =~    y2  2.974733
    4  eta2  =~    y4 -1.246382
Notice that get_data() returns tuple: dataset and K matrix.
"""
import pandas as pd
import os

__desc = '''eta1 =~ y1 + y2
eta2 =~ y3 + y4
x2 ~ eta1
eta2 ~ eta1
x1 ~ eta1'''

__folder = os.path.dirname(os.path.abspath(__file__))
__filename = '%s/example_rf_data.csv' % __folder
__filename_k = '%s/example_rf_kinship.csv' % __folder


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
    Retrieve dataset and kinship matrix.

    Returns
    -------
    pd.DataFrame
        Dataset and K matrix.

    """
    data = pd.read_csv(__filename, index_col=0)
    data['group'] = data.index
    k = pd.read_csv(__filename_k, index_col=0)
    k.columns = list(map(int, k.columns))
    return data, k
