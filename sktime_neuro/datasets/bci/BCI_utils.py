import pandas as pd

def process_dataset(dataset):
    raw_data = dataset["cnt"].astype(float)
    fs = int(dataset["nfo"]["fs"][0][0][0][0])

    event_onsets = dataset["mrk"][0][0][0][0] * (1 / fs)
    event_description = dataset["mrk"][0][0][1][0]
    annotation_pandas = pd.DataFrame(columns=["onset", "duration", "description"])

    annotation_pandas["onset"] = event_onsets
    annotation_pandas["description"] = event_description

    channel_names = [s[0] for s in dataset["nfo"]["clab"][0][0][0]]

    return fs, raw_data, annotation_pandas, channel_names

def test_balls():
    from sktime_neuro.datasets.bci.BCIDownloader import fetch_datasets_from_contest

    raw = fetch_datasets_from_contest("BCICIV_1_mat.zip", ["BCICIV_calib_ds1d.mat"])
    fs, data_train, annotation_train = process_dataset(raw)
