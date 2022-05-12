from typing import *
import mne
import numpy as np
import pandas as pd
from sktime_neuro.utils.mne_processing import create_annotation

"""
Throughout development, we often encoutnered re-implementing this structure
as a tuple. In order to make this a bit more correct we defined a formal
structure for our dataset repr
"""

class DataContainer:
    def __init__(self, dataset: Union[np.ndarray, mne.io.Raw],
                 annotations: Union[np.ndarray, None],
                 samplerate: Union[float, None],
                 lazy_load_data: bool):
        """
        Parameters
        ----------
        dataset : Union[np.ndarray, mne.io.Raw] / type dataset is (np.ndarray, mne.io.Raw)
            Can be either a numpy ndarray or a mne raw. If ndarray samplerate MUST be passed

        annotations : Union[np.ndarray, None] / Maybe np.ndarray
            the annotatons that were derived from create_annotation(), if none passed then
            annotations will be derived from the dataset if possible.

        samplerate : Union[float, None] / Maybe float
            The samplerate of the dataset. If none, dataset MUST be an mne.io.Raw

        lazy_load_data : bool
            If set to true, data will be lazy loaded upon first call to get_data().
            Otherwise, data will be loaded at instantiation
        """

        # Load the dataset, if user opted in to data duplication,
        # duplicate the data and set required flags
        self.dataset = dataset
        if lazy_load_data is True is True:
            self.rawdata = None
        else:
            self.rawdata = dataset.get_data()

        # Lazy load annotations if we can.
        if annotations is None:
            self.annotations = None
        else:
            self.annotations = annotations

        # Derive samplerate if not given
        if samplerate is None:
            if isinstance(dataset, mne.io.Raw):
                self.samplerate = dataset.info["sfreq"]
            else:
                raise TypeError("No samplerate given, and we cannot derive samplerate from an ndarray")
        else:
            self.samplerate = samplerate

    def get_as_data(self, transpose=True) -> np.ndarray:
        """
        By default, the data will be transposed, as this is what we want
        most of the time for sktime and sklearn
        """
        # We set lazyload on initialize, load it now.
        if self.rawdata is None:
            self.rawdata = self.dataset.get_data()
        if transpose is True:
            return self.rawdata.T
        else:
            return self.rawdata

    def get_annotations(self) -> np.ndarray:
        """
        Get annotation set in the format that we use for sktime and sklearn.
        """
        if self.annotations is None:
            self.annotations = create_annotation(self.dataset)
            return self.annotations
        else:
            return self.annotations

    def load_data(self):
        if isinstance(self.dataset, mne.io.Raw):
            self.dataset.load_data()
        else:
            raise TypeError("Cannot call load_data on np.ndarray")