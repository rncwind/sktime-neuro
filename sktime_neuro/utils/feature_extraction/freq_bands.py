import numpy as np
from mne.time_frequency import psd_welch
from sklearn.pipeline import *
from sklearn.preprocessing import FunctionTransformer


def __eeg_power_band(epochs):
    bands = {"d": [0.5,4.5],
             "t": [4.5,8.5],
             "a": [8.5,11.5],
             "s": [11.5,15.5],
             "b": [15.5,30]}
    psd, freq = psd_welch(epochs, picks='eeg', fmin=0.5, fmax=30.)
    psd /= np.sum(psd, axis=-1, keepdims=True)
    x = []
    for fmin, fmax in bands.values():
        pb = psd[:,:, (freq >= fmin) & (freq < fmax)].mean(axis=-1)
        x.append(pb.reshape(len(psd), -1))
    np.concatenate(x, axis=1)


def powerband_pipeline(classifier):
    return make_pipeline(FunctionTransformer(__eeg_power_band, validate=False),
                         classifier)
