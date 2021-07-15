# -*- coding: utf-8 -*-
__author__ = ["Svea Meyer"]
__all__ = ["SeriesDownsampling"]

from sktime_neuro.transformations.base import _SeriesToSeriesTransformer
from sktime.utils.validation.series import check_series


class SeriesDownsampling(_SeriesToSeriesTransformer):
    """
    Downsample X by factor.

    Parameters
    _________
    factor : int
        downsampling factor
    fs : int or float
        sampling frequency of the recorded data in Hz

    Downsampling keeps only the data in position
    of a multiple of factor.
    So downsampling by a factor 1 keeps all the data,
    downsampling by 2 keeps half the data, etc.
    """

    def __init__(self, factor=2):
        self.factor = factor
        if not isinstance(self.factor, int):
            raise TypeError("Can only downsample by whole integers")
        super(SeriesDownsampling, self).__init__()

    def transform(self, Z, y=None):
        """
        Take every factorth element of a trial.

        Parameters
        _________
        X : np.array
            shape: channels*timepoints

        Returns
        ________
        Xt : np.array,
            Downsampled time series

        """
        self.check_is_fitted()
        z = check_series(Z)

        if self.factor > Z.shape[1]:
            raise ValueError("Factor too high for shape of Series.")

        z = z[:, 0 :: self.factor]
        # do we need a warning about this?
        # print("The new sampling frequency is:" + str(self.fs / self.factor))
        return z