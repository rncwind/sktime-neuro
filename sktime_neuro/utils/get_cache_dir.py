# This may seem simple, but i repeat this a lot, so let's go with it.
from pathlib import Path

def get_cache_dir():
    return Path(__file__).parent.parent.parent / "cache"
