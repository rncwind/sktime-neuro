# For debugging and saving us time.
# Pickle some data, with a name, and save it in cache.

import pickle
from pathlib import Path
import os

def get_cache_dir():
    return Path(__file__).parent.parent / "cache"

def get_filename(filename):
    return get_cache_dir() / filename

def serialise(data, filename):
    cachefilename = get_filename(filename)
    with open(cachefilename, "wb") as outfile:
        pickle.dump(data, outfile)

def deserialise(filename):
    cachefilename = get_filename(filename)
    with open(cachefilename, "rb") as infile:
        return pickle.load(infile)

def serialise_if_doesnt_exist(data, filename):
    """
    Only serialises the data, if the file with that filename doesn't exist
    on the disk already.
    """
    cache_filename = get_filename(filename)
    if os.path.isfile(cache_filename) is False:
        serialise(data, filename)

def deserialise_if_exists(filename):
    """
    Deserialise if the file exists.
    """
    cache_filename = get_filename(filename)
    if os.path.isfile(cache_filename) is True:
        return deserialise(filename)
    else:
        return None