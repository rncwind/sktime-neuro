# This may seem simple, but i repeat this a lot, so let's go with it.
from pathlib import Path

import dotenv
from dotenv import load_dotenv
import os

def get_cache_dir():
    dotenv.load_dotenv()
    return Path(os.getenv("SKT_NEURO_CACHE_DIR"))

def get_result_dir():
    dotenv.load_dotenv()
    return Path(os.getenv("PROJECT_ROOT")) / "experiment_results"