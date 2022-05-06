from sktime_neuro.transformations.multivariate_detrender import ColumnDetrender
from sktime_neuro.transformations.series_to_panel.eeg_epoching import epoch
from sktime_neuro.utils.mne_processing import create_annotation
from sktime_neuro.utils.pickle_wrapper import *
from mne_bids import BIDSPath, read_raw_bids
from argparse import ArgumentParser

PROBLEMNAME = "matchingpennies"
PENNIES_ONSET_LABELS = ["raised-right/match-true", "raised-right/match-false",
                        "raised-left/match-true", "raised-left/match-false"]

def get_bids_wrapper(subjectNumber, root, taskname, suffix = "eeg", datatype = "eeg"):
    bidspath = BIDSPath(
        subject=subjectNumber, task=taskname, suffix=suffix, datatype=datatype, root=root
    )
    return read_raw_bids(bids_path=bidspath, verbose=False)

def get_root():
    return get_cache_dir() / "eeg_matchingpennies"

def format_subject_number(subjectNumber):
    return format(f"{subjectNumber:02}")

def get_raw(subjectNumber: int):
    root = get_root()
    sn = format_subject_number(subjectNumber)
    raw = get_bids_wrapper(sn, root, PROBLEMNAME)
    return raw

def get_all_raw():
    raws = []
    for i in range(5,12):
        raws.append(get_raw(i))
    return raws

def get_as_data(subjectNumber: int, dontTranspose: bool = False):
    root = get_root()
    sn = format_subject_number(subjectNumber)
    raw = get_bids_wrapper(sn, root, PROBLEMNAME)
    if dontTranspose is True:
        data = raw.get_data()
        return data
    else:
        data = raw.get_data()
        return data.transpose()


def detrend(data, n_jobs=1):
    dt = ColumnDetrender(data)
    result = dt.detrend(n_jobs=n_jobs)
    del dt
    return result


def prep_for_pickle(sid):
    """noun: To perserve something, typically by canning or pickling"""
    raw = get_raw(sid)
    sf = raw.info['sfreq']

    annot = create_annotation(raw)
    data = raw.get_data().transpose()
    detrended = detrend(data, -1)
    return (annot, detrended, sf)


def detrend_and_pickle_data():
    for i in range(5,12):
        # Data is pickled as a list of [labels, dataset, sampleRate]
        topickle = prep_for_pickle(i)
        name = f"matchingpennies_detrended_{i}"
        serialise(topickle, name)

def detrend_epoch_pickle():
    for i in range(5, 12):
        # Data is pickled as a list of [labels, dataset, sampleRate]
        topickle = prep_for_pickle(i)
        topickle = epoch_dataset(topickle)
        name = f"matchingpennies_epoched_{i}"
        serialise(topickle, name)


def load_pickles(subset):
    rootname = f"matchingpennies_{subset}"
    datasets = []
    for i in range(5,12):
        picklename = f"{rootname}_{i}"
        datasets.append(deserialise_if_exists(picklename))

    return datasets

def epoch_dataset(dataset):
    epochs, labels = epoch(dataset[1], dataset[0], PENNIES_ONSET_LABELS, [-0.5, 0.5], sfreq=dataset[2])
    return (epochs, labels)

def epoch_all(datasets):
    epoched = []
    for dataset in datasets:
        epoched.append(epoch_dataset(dataset))
    return epoched

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-pd", "--pickledetrend", metavar='pickledetrend', type=bool, help="Detrend data and pickle it",
                    default=False, required=False)
    parser.add_argument("-pe", "--pickleepoched", metavar="pickleepochs", type=bool, help="Detrend, Epoch, and Pickle",
                        default=False, required=False)
    args = parser.parse_args()

    if args.pickledetrend is True:
        detrend_and_pickle_data()
    elif args.pickleepoched is True:
        detrend_epoch_pickle()
