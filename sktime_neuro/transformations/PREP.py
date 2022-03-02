"""
This is a wrapper around pyprep that handles the general usecase,
"""

import mne
import numpy as np
from pyprep import PrepPipeline
from typing import *


def do_prep(rawDataset, prep_params, montageKind: str = "standard_1005"):
    montage = mne.channels.make_standard_montage(montageKind)
    rc = rawDataset.copy()
    prep = PrepPipeline(rc, prep_params, montage)
    prep.fit()
    return prep.EEG_new


def build_prep_params(mains_frequency: float, sample_rate: float, ref_channel: str, reref_channel: Optional[str]):
    if reref_channel is None:
        reref_channel = ref_channel
    pp = {
        "ref_chs": ref_channel,
        "reref_chs": reref_channel,
        "line_freqs": np.arange(mains_frequency, sample_rate / 2, mains_frequency)
    }
    return pp


if __name__ == "__main__":
    datapath = mne.datasets.eegbci.load_data(subject=4, runs=1, update_path=True)
    fname_test_file = datapath[0]
    #pp = build_prep_params(60.0, "eeg", "eeg", None)

    # Load in the data
    raw = mne.io.read_raw_edf(fname_test_file, preload=True)
    mne.datasets.eegbci.standardize(raw)
    pp = build_prep_params(60.0, raw.info["sfreq"], "eeg", None)

    processed = do_prep(raw, pp)
