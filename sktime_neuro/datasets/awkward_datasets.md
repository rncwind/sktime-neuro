# Awkward Datasets
This is a list of datasets that are in some way, shape, or form
"awkward". Generally this means that pooch won't support them
due to either a custom downloading system, or them making use of
git and git annex, which would in turn require us to write our own git porcelin.

| Name                   | URL                                                   | Why it's Awkward     | Dataset format |
|------------------------|-------------------------------------------------------|----------------------|----------------|
| matchingpennies        | https://gin.g-node.org/sappelhoff/eeg_matchingpennies | Uses GIn / Git Annex | BIDS           |
| All OpenNeuro datasets | https://github.com/OpenNeuroDatasets                  | Git                  | Various        |