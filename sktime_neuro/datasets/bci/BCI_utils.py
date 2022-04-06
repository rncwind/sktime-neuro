import pandas as pd
from sktime_neuro.utils import mne_processing as utils


def process_dataset_mat(dataset):
    raw_data = dataset["cnt"].astype(float)

    # Samp freq
    fs = int(dataset["nfo"]["fs"][0][0][0][0])

    event_onsets = dataset["mrk"][0][0][0][0] * (1 / fs)
    event_description = dataset["mrk"][0][0][1][0]

    annotation_pandas = pd.DataFrame(columns=["onset", "duration", "description"])
    annotation_pandas["onset"] = event_onsets
    annotation_pandas["description"] = event_description

    #channel_names = [s[0] for s in dataset["nfo"]["clab"][0][0][0]]

    return fs, raw_data, annotation_pandas


def process_dataset_gdf(dataset):
    annotations = utils.create_annotation(dataset)
    data = dataset.pick_types(eeg=True).get_data().transpose()
    fs = dataset.info["sfreq"]
    return fs, data, annotations


def test_mat():
    from sktime_neuro.datasets.bci.BCIDownloader import fetch_datasets_from_contest

    raw = fetch_datasets_from_contest("BCICIV_1_mat.zip", ["BCICIV_calib_ds1d.mat"])
    fs, data_train, annotation_train = process_dataset_mat(raw)
