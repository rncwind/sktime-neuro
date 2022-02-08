import requests
import tempfile
import zipfile
import io
from typing import *


def authenticated_fetch(url, userpassPair):
    return None


def fetch(url):
    r = requests.get(url, allow_redirects=True)
    return r.content


def createTempFileName(filename):
    return str(tempfile.gettempdir()) + filename


def writeFile(path, data):
    file = open(path, "wb")
    file.write(data)
    file.close()


def fetch_dataset(url: str, savePath: str, requiresAuth: bool, userpassPair: Optional[Tuple[str,str]] = None, extractArchive = False, archiveFormat = Optional[str], extractTo = Optional[str]):
    fetched = None
    if requiresAuth == True:
        fetched = authenticated_fetch(url, userpassPair)
    else:
        fetched = fetch(url)

    else:
        file = open(savePath, "wb")
        file.write(fetched)
        file.close()
        return None


if __name__ == "__main__":
    tempDir = tempfile.gettempdir()
    fetch_dataset("https://ftp.cngb.org/pub/gigadb/pub/10.5524/100001_101000/100295/mat_data/s01.mat", createTempFileName("test.mat"), False)