from typing import *
import pooch
from pathlib import Path

def create_registry(base_url: str, names: List[str], problemName: str):
    userhome = Path.home()
    dir = userhome.joinpath(".cache/sktime_neuro").joinpath(problemName)
    with open(dir.joinpath("registry.txt"), "w") as reg:
        for fname in names:
            path = pooch.retrieve(
                url=base_url + fname, known_hash=None, fname=fname, path=dir, progressbar=True
            )
            reg.write(
                f"{fname} sha256:{pooch.file_hash(path)} {(base_url + fname)}\n"
            )
    print("Done")


def prompted():
    url = input("Enter Base URL > ")
    names = input("Enter filenames seperated by commas > ")
    pn = input("Enter problem name (Files will be saved in a dir with this name) > ")
    create_registry(url, names.split(","), pn)


if __name__ == "__main__":
    prompted()