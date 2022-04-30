from sktime_neuro.utils.get_cache_dir import get_cache_dir
from mne_bids import BIDSPath, read_raw_bids

PROBLEMNAME = "matchingpennies"

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