from pooch import os_cache
from mne_bids import BIDSPath, read_raw_bids
from sktime_neuro.transformations.series.seriesdownsampling import SeriesDownsampling
import matplotlib.pyplot as plt

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

class ColumnDetrender:
    """Just apply detrend to each column on it's own!"""
    def __init__(self, dataset: pd.DataFrame, forecaster = None):
        self.dataset = dataset
        if forecaster is None:
            self.forecaster = PolynomialTrendForecaster(degree=1)
        else:
            self.forecaster = forecaster


    def detrend(self, n_jobs: Optional[int] = 1):
        """
        n_jobs : Number of jobs to run in parallel, default is 4.
        """
        if n_jobs is None:
            n_jobs = 1
        processed_list = Parallel(n_jobs=n_jobs, verbose=10)(delayed(detrend_col)(values, deepcopy(self.forecaster)) for values in self.dataset.T)
        con = np.concatenate(processed_list, axis=1)
        return con

def detrend_col(values, forecaster):
    transformer = Detrender(forecaster=forecaster)
    detrendcol = transformer.fit_transform(values)
    return detrendcol


if __name__ == "__main__":
    root = os_cache("sktime_neuro") / "eeg_matchingpennies"
    bids_path = BIDSPath(
        subject="08", task="matchingpennies", suffix="eeg", datatype="eeg", root=root
    )

    raw = read_raw_bids(bids_path=bids_path, verbose=False)

    # mne assumes shape channels*timepoints;sktime assumes shape timepoints*channels
    data = raw.get_data().transpose()
    print("DAta loaded, downsapmpling...")
    downsampled_data = SeriesDownsampling(2).fit_transform(data)
    print("building enesemble")
    dt = ColumnDetrender(downsampled_data)
    print("Detrending...")
    detrended = dt.detrend(n_jobs=-1)
    plt.figure()
    plt.plot(downsampled_data)
    plt.show()
    plt.figure()
    plt.plot(detrended)
    plt.show()
    print("A")
