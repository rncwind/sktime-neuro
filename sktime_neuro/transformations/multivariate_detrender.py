import sktime.datasets
from sktime.forecasting.compose import ColumnEnsembleForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.transformations.series.detrend import Detrender
from typing import *

import pandas as pd

"""
Unfortunatley, EEG data is multivariate. SKTime used to support this out of the box
with it's detrender class, but that was removed in favor of the forecasting compositors.

As such, this class aims to implement detrending via these forecasting compositors,
rather than backporting the old detrender behaviour.
"""

class ColumnEnsembleDetrender:
    """
    Fancy new version of the detrender that uses the ColumnEnsemble class in order
    to apply trendforecasters.
    """

    def __init__(self, dataset : Union[pd.Series, pd.DataFrame], forecaster=None):
        self.forecaster = forecaster
        self.forecasters = []
        self.dataset = dataset
        self.fh = self.dataset.shape[1]
        if forecaster is None:
            self.forecaster = PolynomialTrendForecaster()

        self.dup_forecasters()

    def dup_forecasters(self):
        for i in range(0, self.fh):
            name = f"forecaster{i}"
            tup = (name, self.forecaster, i)
            self.forecasters.append(tup)
        print(f"Created {i} forecasters")

    def detrend(self):
        fc = ColumnEnsembleForecaster(forecasters=self.forecasters)
        fc.fit(self.dataset, fh=list(range(1, self.fh)))
        return fc.predict()

class DumbDetrender:
    """Just apply detrend to each column on it's own!"""
    def __init__(self, dataset: Union[pd.Series, pd.DataFrame], forecaster = None):
        self.dataset = dataset
        if forecaster is None:
            self.forecaster = PolynomialTrendForecaster(degree=1)
        else:
            self.forecaster = forecaster

    def detrend(self):
        transformed = pd.DataFrame()
        transformer = Detrender(forecaster=self.forecaster)
        for name, values in self.dataset.items():
            detrendcol = transformer.fit_transform(values)
            transformed = pd.concat([transformed, detrendcol], axis=1)

        return transformed
