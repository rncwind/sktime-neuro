import sktime.datasets
from sktime.forecasting.compose import ColumnEnsembleForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.forecasting.base._fh import ForecastingHorizon
from sktime.transformations.series.detrend import Detrender
from joblib import Parallel, delayed
from typing import *
from copy import deepcopy

import pandas as pd
import numpy as np

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

    def __init__(self, dataset: np.ndarray):
        self.dataset = dataset
        self.fitted = False
        self.forecasters = []
        for column in range(dataset.shape[1]):
            self.forecasters.append(
                (("trend" + str(column)), PolynomialTrendForecaster(), column)
            )
        self.cef = ColumnEnsembleForecaster(forecasters=self.forecasters)
        self.fh = np.arange(self.dataset.shape[0])

    def fit(self):
        if self.fitted is False:
            self.cef.fit(self.dataset, fh=self.fh)

    def fit_predict(self):
        if self.fitted is False:
            self.cef.fit(self.dataset, fh=self.fh)
        return self.cef.predict()


class DumbDetrender:
    """Just apply detrend to each column on it's own!"""
    def __init__(self, dataset: pd.DataFrame, forecaster = None):
        self.dataset = dataset
        if forecaster is None:
            self.forecaster = PolynomialTrendForecaster(degree=1)
        else:
            self.forecaster = forecaster


    def detrend(self, n_jobs: Optional[int]):
        """
        n_jobs : Number of jobs to run in parallel, default is 4.
        """
        if n_jobs is None:
            n_jobs = 4
        processed_list = []
        if isinstance(self.dataset, np.ndarray):
            print("Ndarray")
            processed_list = Parallel(n_jobs=n_jobs)(delayed(detrend_col)(values, deepcopy(self.forecaster)) for values in self.dataset.T)
        elif isinstance(self.dataset, pd.DataFrame):
            print("Dataframe")
            detrended_cols = Parallel(n_jobs=4)(delayed(detrend_col)(values, self.forecaster) for name, values in self.dataset)

        if isinstance(self.dataset, np.ndarray):
            con = np.empty_like(self.dataset)
            for detrended_col in processed_list:
                np.concatenate(con, detrended_col)
            return con
        elif isinstance(self.dataset, pd.DataFrame):
            raise NotImplementedError("Only numpy arrays for now")



def detrend_col(values, forecaster):
    transformer = Detrender(forecaster=forecaster)
    detrendcol = transformer.fit_transform(values)
    print("Done")
    return detrendcol


def test_dumb_detrender():
    from pooch import os_cache
    from mne_bids import BIDSPath, read_raw_bids
    from sktime_neuro.transformations.series.seriesdownsampling import SeriesDownsampling

    root = os_cache("sktime_neuro") / "eeg_matchingpennies"
    bids_path = BIDSPath(
        subject="08", task="matchingpennies", suffix="eeg", datatype="eeg", root=root
    )

    raw = read_raw_bids(bids_path=bids_path, verbose=False)

    # mne assumes shape channels*timepoints;sktime assumes shape timepoints*channels
    data = raw.get_data().transpose()
    downsampled_data = SeriesDownsampling(2).fit_transform(data)
    dt = DumbDetrender(downsampled_data)
    detrended = dt.detrend(n_jobs=8)
    assert(detrended is not None)

def test_ensemble():
    from pooch import os_cache
    from mne_bids import BIDSPath, read_raw_bids
    from sktime_neuro.transformations.series.seriesdownsampling import SeriesDownsampling

    root = os_cache("sktime_neuro") / "eeg_matchingpennies"
    bids_path = BIDSPath(
        subject="08", task="matchingpennies", suffix="eeg", datatype="eeg", root=root
    )

    raw = read_raw_bids(bids_path=bids_path, verbose=False)

    # mne assumes shape channels*timepoints;sktime assumes shape timepoints*channels
    data = raw.get_data().transpose()
    downsampled_data = SeriesDownsampling(2).fit_transform(data)

    dt = ColumnEnsembleDetrender(downsampled_data)
    detrended = dt.fit_predict()
    print("A")