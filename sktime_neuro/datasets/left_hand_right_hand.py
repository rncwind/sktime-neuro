import pytest
import scipy.io
import numpy as np
from typing import *

import pooch

lrh_pooch = pooch.create(
    path=pooch.os_cache("sktime_neuro"),
    base_url="https://ftp.cngb.org/pub/gigadb/pub/10.5524/100001_101000/100295/mat_data/",
    registry={
        "s01.mat": "sha256:57f2f10056b3c240adc78324872597d9b06b282df537a7763e98467275efe6db",
        "s02.mat": "sha256:1ad1d82d9e409d85d520837377d88a89c086a4f526dba0ce0fe588b6e6e3659e",
        "s03.mat": "sha256:f2b4e386c501add1bfd5b43767f2d684a7c1fa29f811d3a1876d4e5861377ebc",
        "s04.mat": "sha256:9c4e682deb3d60f9b5f3e77d0b369046674a5ecc0db440975c1ca516fd501840",
        "s05.mat": "sha256:5d25609b80f2d61c7a0698d9443b236dd369e77b41a15355643b85d97c97d902",
        "s06.mat": "sha256:74375f26572b73b6d6caf51705ef355d978e46796ac5d91517a36ab1a0c02e8c",
        "s07.mat": "sha256:59300489a42f04ad304c5f3e74a5984bd1127f473eac4d754ea46679c5b5c8dc",
        "s08.mat": "sha256:be4b73dd6c6d41d9005011f5298e51f4be709c2f5e6d1d0722215df19c7df882",
        "s09.mat": "sha256:fff2e17497211bb70f0050564353108098513398c0836add8e84d85585f9b541",
        "s10.mat": "sha256:1d9638cad324fb12ada1313679c35a54a991fc80939c6502a8bf3102fb137ee8",
        "s11.mat": "sha256:afb8a7e00531149f54af6b597ee171143f60fd114cdd6853bb2193aa747c2091",
        "s12.mat": "sha256:b14c885be9999c108287cdfc6c46bc0fe1b364c971b3c1ddd4d2c645fb1809e7",
        "s13.mat": "sha256:4c9806b3051ccb9ce4ffb19a80cce510d9424d2cf3dc81da2e6969dc2cdd6481",
        "s14.mat": "sha256:d80df4caafa163a62ef9c9533ef5baded9fb6a8aa7ae7ab6ecdb70bf45f05c83",
        "s15.mat": "sha256:95011e9b668784c8dad3c45bb6105232190848db6100eafe53d4ddff55cb35d7",
        "s16.mat": "sha256:d3280d213c723e8623e8364edfb24104ed6dcd035a20f3e1f86c9510b0d947b0",
        "s17.mat": "sha256:8b55f5ce72b983e52617e866fabdf45446376701d9e819c439715b7aba9e055a",
        "s18.mat": "sha256:c875a04e589afef69388702fa293012d35237abbff5240c2ce37488184fc607c",
        "s19.mat": "sha256:cbb9fdf4c063d0dac3e83f6089242f56562775bfe0d952dfc93ba08d7861f658",
        "s20.mat": "sha256:5b91cf6de405b8a23e9c01e70b8955fdf15c6334c18d6335e93d94715a64f64d",
        "s21.mat": "sha256:2c95224bddff358a89cba617bf9eb74a261b8b853790f4ce9c75c5473ced8a18",
        "s22.mat": "sha256:0eac5d10dc674ee5bbf6d35e96e0a44a2d6056ad4a1d3a0a22ff80a2e7027fcf",
        "s23.mat": "sha256:c4a01839bc60d44eff43675492c3056c1338d0202f2cb6c72d37ecaaa95c81b0",
        "s24.mat": "sha256:b28db34626242be4975e19bea742e486d8fd0c4f9eaefd3878077745816f4d35",
        "s25.mat": "sha256:8b7baa831b699fc95527f2a7eb87e920374e87052acb87556790e0277e993a3d",
        "s26.mat": "sha256:479472ff4574d2b54a6653ce129db2f8e36ec5500ece321b2b113d5ce58e0723",
        "s27.mat": "sha256:2e0d2c30ff6df46cb07c5b8563e1012d0d924261b0d062c49be33d7a1cb9a7dc",
        "s28.mat": "sha256:b6c51b130fb2bb349e614fcab23655948c6658fdf782199041cbb03ff7a36dbd",
        "s29.mat": "sha256:bcadd645f161acae0f5b45bfc3f724d6b6e25ed9c9978d3e339a74908bc13f73",
        "s30.mat": "sha256:29d0d8714bb8e59cc9c3718ff84542536f34703eb17f536e7400d39abf5561f8",
        "s31.mat": "sha256:e03f3343b410ddff2584d95e5af0aad8039ceeecbded59f2fcc1e94a91a9e30a",
        "s32.mat": "sha256:79217e2938b36fe29ef040ae34ffe3628ee8f557563771d3601b3c2253ee0ea7",
        "s33.mat": "sha256:fc0ae6795a14bdf112e07812929570ad1bc140718d71e3605e2c99588ccf5d2d",
        "s34.mat": "sha256:8fd506677c43ffdbe7f3cbbb5ed22b9426ab3eb1275595202d88c508df6e240a",
        "s35.mat": "sha256:656951a3620d0ba432e24273d191fff428735e092833491599ca302e9bfcb51d",
        "s36.mat": "sha256:201e2aa49eb2dad84a4738668e0a02db9abebf57376251040c1aa9cf4efcd413",
        "s37.mat": "sha256:82badb54e53e3895f72681d9cf581613573e0675c8cd9a0f578913ef18d846e3",
        "s38.mat": "sha256:2f95a38d9f50492781dd57c0638122f3fb0794b1361f220475bc20700bf75a12",
        "s39.mat": "sha256:26c8a180de81d2671984efb7a9a3655a78e292a289b97a8083b8cc180244ed15",
        "s40.mat": "sha256:94b8d9c933011543251d2075e4575b01c6534ab1fb43ee1406b7fb53f3200d11",
        "s41.mat": "sha256:88d058863f7d1942cb24a32230d39c663f8902057a0e9aaa6063d36e5fc81fdc",
        "s42.mat": "sha256:fe60fdfc6120d9716510b8a5a056c4bf0bf9b77782eed806a3ccf7a50bc040e5",
        "s43.mat": "sha256:7d4d7f93acf84569669ff2655364e0ddf7018d68e7d8b5e2060f0ec479507ea0",
        "s44.mat": "sha256:b0433df98a59f5c354743d97e5ffea422cb9bfa69cf025f828d4e038872d3c7d",
        "s45.mat": "sha256:1d679a6daba9a60160eb080abe7532bab49f78f6ebe7bc79f817512d6b9f855b",
        "s46.mat": "sha256:be33aa595d7a32cf7666758f102f52fd4d71f150a70f7529c7bb86c3c09ea0a8",
        "s47.mat": "sha256:e5d5161a85b645839ec3c23b5ef8e334f423aab132cd6b938d96eccd73ed5137",
        "s48.mat": "sha256:ad01fd29a2f358204b0f528e78dbb909d35ad4304b3fa222dff90e759941a287",
        "s49.mat": "sha256:a1e24e633b20ea4ed3eba5d93f9cf51b8cf24a340ec72b78d7000da5afaf957b",
        "s50.mat": "sha256:b5df79bb64eb585ff01eb77cc176c9a02964c564dd40a4eeec7764b510950d40",
        "s51.mat": "sha256:0c09887cc122d4a0c043d2304af1537a293fe86562b4296ec0e75f5bf2e95fbb",
    },
)


def fetch_dataset(experimentNumber: int, *, only_get_filepaths = False) -> Union[np.ndarray, str]:
    padded = str(experimentNumber).zfill(2)
    path = lrh_pooch.fetch(("s" + padded + ".mat"))
    if only_get_filepaths is False:
        return scipy.io.loadmat(path)["eeg"]
    else:
        return path


def fetch_multiple_datasets(experiment_list: List[int], *, only_get_filepaths=False) -> Union[List[np.ndarray], List[str]]:
    res = []
    for e in experiment_list:
        res.append(fetch_dataset(e))
    return res



def test_fetch():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        lrh_pooch.path = td
        testNum = 2
        fetched = fetch_dataset(testNum)
        assert fetched is not None
        assert(fetched.shape == (1,1))
        assert(len(fetched[0]) == 1)


def test_fetch_multiple():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        lrh_pooch.path = td
        tests = [2,3,5]
        fetched = fetch_multiple_datasets(tests)
        assert(len(fetched) == 3)


def test_fetch_invalid():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        lrh_pooch.path = td
        testnum = 100
        with pytest.raises(ValueError):
            fetched = fetch_dataset(testnum)


def test_fetch_partial_invalid():
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        lrh_pooch.path = td
        tests = [1,100]
        with pytest.raises(ValueError):
            fetch_multiple_datasets(tests)