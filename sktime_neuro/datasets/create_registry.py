import tempfile
from typing import *
import pooch
from pathlib import Path

"""
This is pureley a function designed to automate the downloading and hashing of datasets to be fed into pooch.
This will generally only be of use for developers of this library, rather than consumers.
"""


def create_registry(base_url: str, names: List[str], problemName: str):
    regpath = "./registries/" + problemName + ".txt"
    with tempfile.TemporaryDirectory() as dir:
        with open(regpath, "w+", 1) as reg:
            for fname in names:
                path = pooch.retrieve(
                    url=base_url + (fname + ".mat"),
                    known_hash=None,
                    fname=fname,
                    path=dir,
                )
                reg.write(f"\"{fname}\": \"sha256:{pooch.file_hash(path)}\",\n")
    print("Done")


if __name__ == "__main__":
    names = ["A01T", "A01E", "A02T", "A02E", "A03T", "A03E", "A04T", "A04E", "A05T", "A05E", "A06T", "A06E", "A07T",
             "A07E", "A08T", "A08E", "A09T", "A09E"]
    create_registry("https://lampx.tugraz.at/~bci/database/001-2014/",
                    names, "Four-class-motor-imagery-001-2014")
