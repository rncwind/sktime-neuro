import shutil

import requests
from requests.auth import HTTPBasicAuth
import tempfile
import zipfile
import io
from typing import *


def authenticated_fetch(url: str, userpassPair: Tuple[str, str]):
    r = requests.get(url, allow_redirects=True, auth=userpassPair)
    return r.content


def fetch(url: str):
    r = requests.get(url, allow_redirects=True)
    return r.content


def createTempFileName(filename: str):
    return str(tempfile.gettempdir()) + filename


def writeFile(path, data):
    file = open(path, "wb")
    file.write(data)
    file.close()


def extract(savePath, extractTo: str):
    shutil.unpack_archive(savePath, extractTo)


def fetch_dataset(url: str, savePath: str, requiresAuth: bool, userpassPair: Optional[Tuple[str,str]] = None, extractArchive = False, extractTo = Optional[str]):
    fetched = None
    if requiresAuth is True:
        fetched = authenticated_fetch(url, userpassPair)
    else:
        fetched = fetch(url)

    file = open(savePath, "wb")
    file.write(fetched)
    file.close()
    if extractArchive is True:
        extract(savePath, extractTo)


if __name__ == "__main__":
    tempDir = tempfile.gettempdir()
    fetch_dataset("https://ftp.cngb.org/pub/gigadb/pub/10.5524/100001_101000/100295/mat_data/s01.mat", createTempFileName("test.mat"), False)