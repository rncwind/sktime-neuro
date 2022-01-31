# A brainvision EEG reading contaisn 3 sepperate files.
# A .vhdr contains metadata, text marer vmrk contains labels, and eeg contains
# the actual voltage values
# For full spec see https://www.brainproducts.com/productdetails.php?id=21&tab=5

import mne

def load_brainvision(path):
    mne.io.read_raw_brainvision(path)
