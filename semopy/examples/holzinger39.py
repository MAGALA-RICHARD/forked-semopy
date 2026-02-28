# -*- coding: utf-8 -*-
"""
Holzinger-Swineford 1939 dataset and CFA model.

The classic Holzinger and Swineford (1939) dataset consists of mental ability
test scores of seventh- and eighth-grade children from two different schools
(Pasteur and Grant-White). 
"""
import pandas as pd
import os

__desc = '''visual =~ x1 + x2 + x3
textual =~ x4 + x5 + x6
speed =~ x7 + x8 + x9'''

__filename = '%s/holzinger_swineford39_data.csv' % \
             os.path.dirname(os.path.abspath(__file__))


def get_model():
    """
    Retrieve model description in semopy syntax.

    Returnsunivariate_regression
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
    return pd.read_csv(__filename, index_col=0, sep=',')
