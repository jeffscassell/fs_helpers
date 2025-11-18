import pytest
from pathlib import Path

from fs_helpers.work import cleanFilename, size



@pytest.fixture
def resources():
    return Path(__file__).parent / "_resources"

@pytest.fixture
def emptyFile(resources):
    return resources / "empty.txt"

@pytest.fixture
def smallFile(resources):
    return resources / "bytes.txt"

@pytest.fixture
def mediumFile(resources):
    return resources / "megabytes.bin"


def test_clean_filename():
    filename = "here-is a name"
    assert cleanFilename(filename) == "here-is_a_name"
    
    filename = "some illegal (':'^') characters"
    assert cleanFilename(filename) == "some_illegal_(''')_characters"


def test_size(emptyFile: Path, smallFile: Path, mediumFile: Path):
    assert size(emptyFile) == "0 bytes"
    assert size(emptyFile, pretty=False) == 0
    assert size(smallFile) == "29 bytes"
    assert size(smallFile, pretty=False) == 29
    assert size(mediumFile) == "2.10 MiB"
    assert size(mediumFile, pretty=False) == 2200676