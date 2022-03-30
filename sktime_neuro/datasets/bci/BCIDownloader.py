from os import environ
import pooch
from pooch import HTTPDownloader
from typing import *
import scipy.io
import mne
import pytest
import logging

bci_pooch = pooch.create(
    path=pooch.os_cache("sktime_neuro"),
    base_url="http://bbci.de/competition/download/competition_iv/",
    registry={
        "BCICIV_1_mat.zip": "sha256:f7acc9420158e6d58629589040ced64b49ffd8e946c4024f85cc77896acdf686",
        "BCICIV_2a_gdf.zip": "sha256:65fe93cb766e4b00ece69a200312d81f54bba17c642406bd922d913a8aedc024",
        "BCICIV_2b_gdf.zip": "sha256:1af1625d8a2c7c793d23236000f49cef2a064a71337194585b4fa353eff62e15",
        "BCICIV_3_mat.zip": "sha256:acc7b24309f953c412948a0eb4a13ec33b4bbf47b7730fb15b78caabbbb90d41",
        "BCICIV_4_mat.zip": "sha256:cf734300ad415f81350b75d1606fea42d9e552543fb42b0a8c09754ea522cbc6",
    },
)

memberLists = {
    # Listings for each zip. This lets people extract induvidual trials if necessary
    "BCICIV_1": [
        "BCICIV_calib_ds1a.mat", "BCICIV_calib_ds1b.mat", "BCICIV_calib_ds1c.mat",
        "BCICIV_calib_ds1d.mat", "BCICIV_calib_ds1e.mat", "BCICIV_calib_ds1f.mat",
        "BCICIV_calib_ds1g.mat", "BCICIV_eval_ds1a.mat", "BCICIV_eval_ds1b.mat",
        "BCICIV_eval_ds1c.mat", "BCICIV_eval_ds1d.mat", "BCICIV_eval_ds1e.mat",
        "BCICIV_eval_ds1f.mat", "BCICIV_eval_ds1g.mat",
    ],
    "BCICIV_2a": [
        "A01E.gdf", "A01T.gdf", "A02E.gdf", "A02T.gdf", "A03E.gdf", "A03T.gdf",
        "A04E.gdf", "A04T.gdf", "A05E.gdf", "A05T.gdf", "A06E.gdf", "A06T.gdf",
        "A07E.gdf", "A07T.gdf", "A08E.gdf", "A08T.gdf", "A09E.gdf", "A09T.gdf",
    ],
    "BCICIV_2b": [
        "B0101T.gdf", "B0102T.gdf", "B0103T.gdf", "B0104E.gdf", "B0105E.gdf",
        "B0201T.gdf", "B0202T.gdf", "B0203T.gdf", "B0204E.gdf", "B0205E.gdf",
        "B0301T.gdf", "B0302T.gdf", "B0303T.gdf", "B0304E.gdf", "B0305E.gdf",
        "B0401T.gdf", "B0402T.gdf", "B0403T.gdf", "B0404E.gdf", "B0405E.gdf",
        "B0501T.gdf", "B0502T.gdf", "B0503T.gdf", "B0504E.gdf", "B0505E.gdf",
        "B0601T.gdf", "B0602T.gdf", "B0603T.gdf", "B0604E.gdf", "B0605E.gdf",
        "B0701T.gdf", "B0702T.gdf", "B0703T.gdf", "B0704E.gdf", "B0705E.gdf",
        "B0801T.gdf", "B0802T.gdf", "B0803T.gdf", "B0804E.gdf", "B0805E.gdf",
        "B0901T.gdf", "B0902T.gdf", "B0903T.gdf", "B0904E.gdf", "B0905E.gdf",
    ],
    "BCICIV_3": ["S1.mat", "S2.mat", "SensorPos.pdf"],
    "BCICIV_4": ["sub1_comp.mat", "sub2_comp.mat", "sub3_comp.mat"],
}

zips = ["BCICIV_1_mat.zip", "BCICIV_2a_gdf.zip", "BCICIV_2b_gdf.zip", "BCICIV_3_mat.zip", "BCICIV_4_mat.zip"]


def fetch_all() -> List[str]:
    '''
    Please note, this will get all datasets, download them to disk and have them ready
    for usage with :func:`fetch_datasets_from_contest`.
    '''
    un, passwd = fetch_un_pw()
    download = HTTPDownloader(auth=(un, passwd))
    fnames = []
    for contest in zips:
        fn = bci_pooch.fetch(contest, downloader=download)
        fnames.append(fn)
    return fnames


def fetch_contest(contest):
    '''
    Please note, this will get a dataset, download it to disk and have it ready
    for usage with :func:`fetch_datasets_from_contest`
    '''
    un, passwd = fetch_un_pw()
    download = HTTPDownloader(auth=(un, passwd))
    fname = bci_pooch.fetch(contest, downloader=download)
    return fname


def fetch_datasets_from_contest(contest, dataset_names: List[str], *, only_get_filepaths = False):
    """
    Fetch a specified dataset file from a BCI contest

    Parameters:
        contest : str
            The zip filename for the BCI contest we want (eg, BCI_CIV1_mat.zip)

        dataset_names : List[str]
            The chosen dataset members we want (eg, BCICIV_calib_ds1a.mat in BCICIV_1)

        only_get_filepaths : bool
            a keyword only variable, if set to true, only the file paths will
            be extracted. By default we will take each dataset, and convert it to a
            dataframe which will be returned

    Returns:
        A list of datasets as ndarrays by default. If only_get_filepaths is set to True, a list of filepaths
    """
    un, passwd = fetch_un_pw()
    download = HTTPDownloader(auth=(un, passwd))
    unpack = pooch.Unzip(members=dataset_names)
    fname = bci_pooch.fetch(contest, downloader=download, processor=unpack)
    if only_get_filepaths is True:
        return fname
    else:
        return extract_datasets(fname)

def extract_datasets(fnames: List[str]):
    datasets = []
    for f in fnames:
        if f.endswith(".gdf"):
            d = mne.io.read_raw_gdf(f)
            datasets.append(d)
        elif f.endswith(".mat"):
            d = scipy.io.loadmat(f)
            datasets.append(d)

    return datasets


def fetch_un_pw():
    try:
        un = environ.get("BCI_USERNAME")
        logging.debug("Found BCI_USERNAME")
        pw = environ.get("BCI_PASSWORD")
        logging.debug("Found BCI_PASSWORD")
    except KeyError:
        print(
            "BCI Requires a registration. Please register at http://bbci.de/competition/iv/ before use"
        )
        print(
            "For faster access. Set BCI_USERNAME and BCI_PASSWORD as environment variables"
        )
        print("Please check your shell, or operating system manual for how to do this.")
        un = input("Enter username")
        pw = input("Enter password")
    return un, pw


def test_fetch_all():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_all()
        assert(fp is not None)


def test_fetch_contest_1():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_contest("BCICIV_1_mat.zip")
        assert(fp is not None)


def test_fetch_contest_2a():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_contest("BCICIV_2a_gdf.zip")
        assert(fp is not None)


def test_fetch_contest_2b():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_contest("BCICIV_2b_gdf.zip")
        assert(fp is not None)


def test_fetch_contest_3():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_contest("BCICIV_3_mat.zip")
        assert(fp is not None)


def test_fetch_contest_4():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        fp = fetch_contest("BCICIV_4_mat.zip")
        assert(fp is not None)

def test_fetch_mat_dataset():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        ds = fetch_datasets_from_contest("BCICIV_4_mat.zip", ["sub1_comp.mat"])
        assert(ds is not None)
        assert(ds[0]["train_data"] is not None)
        assert(ds[0]["train_data"].shape == (400000, 62))

def test_fetch_experiment_from_set_1():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bci_pooch.path = td
        ds = fetch_datasets_from_contest("BCICIV_1_mat.zip", ["BCICIV_calib_ds1d.mat"])
        assert (ds is not None)
