#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Univariate regression example model."""
import pandas as pd
import os

__desc = 'y ~ x'

__folder = os.path.dirname(os.path.abspath(__file__))
__filename = '%s/univariate_regression_data.csv' % __folder
__filename_p = '%s/univariate_regression_params.csv' % __folder


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
    return pd.read_csv(__filename, index_col=0)


def get_params():
    """
    Retrieve true parameter estimates.

    Returns
    -------
    pd.DataFrame
        Dataset.

    """
    return pd.read_csv(__filename_p, index_col=0)
