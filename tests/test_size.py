from pathlib import Path

import pytest

from fs_helpers.size import sizei, sizes



@pytest.fixture
def emptyFile(resources):
    return resources / "empty.txt"

@pytest.fixture
def smallFile(resources):
    return resources / "bytes.txt"

@pytest.fixture
def mediumFile(resources):
    return resources / "megabytes.bin"


def test_size(emptyFile: Path, smallFile: Path, mediumFile: Path):
    assert sizei(emptyFile) == 0
    assert sizei(smallFile) == 29
    assert sizei(mediumFile) == 2200676

def test_sizes(emptyFile: Path, smallFile: Path, mediumFile: Path):
    assert sizes(emptyFile) == "0 bytes"
    assert sizes(smallFile) == "29 bytes"
    assert sizes(mediumFile) == "2.10 MiB"
