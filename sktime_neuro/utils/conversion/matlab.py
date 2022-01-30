"""
Lots of datasets are in matlab .MAT files.
Thankfully we can use scipy for this.
"""

import scipy.io
import pandas as pd


def load_matlab_mat(mat_file: str) -> dict:
    """
    A simple wrapper that laods a matlab .mat file and converts them to a pandas
    dataframe.
    """
    mat = scipy.io.loadmat(mat_file)

if __name__ == '__main__':
    mat_to_dataframe("CLA-SubjectJ-170508-3St-LRHand-Inter.mat")
