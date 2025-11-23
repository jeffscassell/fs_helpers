import pytest
from pathlib import Path

from fs_helpers.work import cleanFilename, size, zipDirectory



@pytest.fixture
def resources():
    return Path(__file__).parent / "_resources"


class TestSize:

    @pytest.fixture
    def emptyFile(self, resources):
        return resources / "empty.txt"

    @pytest.fixture
    def smallFile(self, resources):
        return resources / "bytes.txt"

    @pytest.fixture
    def mediumFile(self, resources):
        return resources / "megabytes.bin"


    def test_size(self, emptyFile: Path, smallFile: Path, mediumFile: Path):
        assert size(emptyFile) == "0 bytes"
        assert size(emptyFile, pretty=False) == 0
        assert size(smallFile) == "29 bytes"
        assert size(smallFile, pretty=False) == 29
        assert size(mediumFile) == "2.10 MiB"
        assert size(mediumFile, pretty=False) == 2200676


def test_clean_filename():
    filename = "here-is a name"
    assert cleanFilename(filename) == "here-is_a_name"
    
    filename = "some illegal (':'^') characters"
    assert cleanFilename(filename) == "some_illegal_(''')_characters"


@pytest.fixture
def zipDir(resources):
    return resources / "zip_dir"


def test_zip_directory(zipDir: Path):
    assert zipDir.is_dir()
    name = "new_name"
    zipDirectory(zipDir, name)
    zipFile = zipDir.with_name(f"{name}.zip")
    assert zipFile.is_file()
    zipFile.unlink()