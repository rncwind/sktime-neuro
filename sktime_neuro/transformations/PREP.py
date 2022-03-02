import mne
import numpy as np
from pyprep import PrepPipeline
from typing import *


def do_prep(rawDataset, sampleRate: float, mainsFrequency: int, prep_params: Optional[dict], montageKind: str = "standard_1005"):
    if prep_params is None:
        prep_params = {
            "ref_chs": "eeg",
            "reref_chs": "eeg",
            "line_freqs": np.arange(mainsFrequency, sampleRate / 2, mainsFrequency),
        }
    montage = mne.channels.make_standard_montage(montageKind)
    rc = rawDataset.copy()
    prep = PrepPipeline(rc, prep_params, montage)
    prep.fit()
    return prep.EEG_new


if __name__ == "__main__":
    datapath = mne.datasets.eegbci.load_data(subject=4, runs=1, update_path=True)
    fname_test_file = datapath[0]

    # Load in the data
    raw = mne.io.read_raw_edf(fname_test_file, preload=True)
    mne.datasets.eegbci.standardize(raw)

    processed = do_prep(raw, raw.info["sfreq"], 60, None)