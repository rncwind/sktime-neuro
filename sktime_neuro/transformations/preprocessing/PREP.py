"""
This is a wrapper around pyprep that handles the general usecase for PREP
As of 2022-05-02, this module REQUIRES the git version of pyprep. If you are using
the pipenv files I wrote, this will be done by default.
"""

import mne
import numpy as np
from pyprep import PrepPipeline
from typing import *


def do_prep(rawDataset, prep_params: dict, montageKind: str = "standard_1005"):
    """
    Apply the prep pipeline to a raw dataset from MNE.
    Returns the preprocessed dataset
    """
    montage = mne.channels.make_standard_montage(montageKind)
    rc = rawDataset.copy()
    prep = PrepPipeline(rc, prep_params, montage)
    prep.fit()
    return prep.EEG_new


def build_prep_params(mains_frequency: float, sample_rate: float, ref_channel: str, reref_channel: Optional[str]):
    """
    A simple builder function that builds a rather standard set of prep parameters. The only one not covered
    is the max-iterations value, as this will generally be unchanging from the default 4.
    """
    if reref_channel is None:
        reref_channel = ref_channel
    pp = {
        "ref_chs": ref_channel,
        "reref_chs": reref_channel,
        "line_freqs": np.arange(mains_frequency, sample_rate / 2, mains_frequency)
    }
    return pp


def prep_dataset(raw, params, outputPath, overwrite = False):
    processed = do_prep(raw, params)
    # This is horrible, BUT it's the only thing we can do if we wish to preserve
    # the metadata of the structure.
    raw._data = processed
    raw.save(outputPath + ".fif", overwrite=overwrite)


if __name__ == "__main__":
    datapath = mne.datasets.eegbci.load_data(subject=4, runs=1, update_path=True)
    fname_test_file = datapath[0]

    # Load in the data
    raw = mne.io.read_raw_edf(fname_test_file, preload=True)
    mne.datasets.eegbci.standardize(raw)
    pp = build_prep_params(60.0, raw.info["sfreq"], "eeg", None)
    prep_dataset(raw, pp, "test")

    # processed = do_prep(raw, pp)
    # print("A")
    # raw._data = processed
    # raw.save("test.fif")
    # print("A")
