import numpy as np
from sklearn.model_selection import *
from sktime.classification.kernel_based import RocketClassifier
from sktime_neuro.datasets.matching_pennies_util import *
from sktime_neuro.transformations.multivariate_detrender import ColumnDetrender
from sktime_neuro.transformations.series_to_panel.eeg_epoching import epoch
from sktime_neuro.utils.mne_processing import create_annotation
from sktime_neuro.utils.get_cache_dir import get_cache_dir
from sktime_neuro.datasets.matching_pennies_util import PENNIES_ONSET_LABELS, load_pickles
from typing import *


def detrend(data, n_jobs=1) -> np.ndarray:
    dt = ColumnDetrender(data)
    return dt.detrend(n_jobs=n_jobs)

def load_subject(subjectId: int) -> Tuple[np.ndarray, np.ndarray, float]:
    raw = get_raw(subjectId)
    sf = raw.info["sfreq"]
    annotations = create_annotation(raw)
    data = raw.get_data().transpose()
    detrended = detrend(data, -1)
    return annotations, detrended, sf

def load_all_subjects() -> List[Tuple[np.ndarray, np.ndarray, float]]:
    allData = []
    for i in range(5,12):
        allData.append(load_subject(i))
    return allData

def epoch_subject(subjectData: Tuple[np.ndarray, np.ndarray, float]) -> Tuple[np.ndarray, np.ndarray]:
    epochs, annotations = epoch(subjectData[1], subjectData[0], PENNIES_ONSET_LABELS, [-0.5, 0.5], sfreq=subjectData[2])
    return epochs, annotations

def epoch_set(dataset: List[Tuple[np.ndarray, np.ndarray, float]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    epoched = []
    for subj in dataset:
        epoched.append(epoch_subject(subj))
    return epoched

def run_experiment(dataset: List[Tuple[np.ndarray, np.ndarray]], classifier, cv=5):
    results = []
    for i in range(0, len(dataset)):
        scores = cross_val_score(classifier, dataset[i][0], dataset[i][1], cv=cv)
        results.append(scores)
    return results

def write_results(results, prefix):
    i = 0
    for resultset in results:
        fn = f"{prefix}_{i:02d}"
        np.savetxt(fn, resultset, delimiter=",")
        i += 1

if __name__ == "__main__":
    allData = load_pickles("detrended")
    epochedSet = epoch_set(allData)
    rocket = RocketClassifier(n_jobs=16)
    results = run_experiment(epochedSet, rocket)
    write_results(results, str((get_cache_dir() / "detrended_only")))
