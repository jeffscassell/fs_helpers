import pytest
from pathlib import Path
import shutil

from fs_helpers.work import (
    cleanFilename,
    size,
    zipDirectory,
    unzip,
)



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


class TestZip:

    ZIPPED_FILE_NAME = "new_name"
    UNZIPPED_DIR_NAME = "unzipped_dir"

    @pytest.fixture
    def zipDir(self, resources: Path):
        yield resources / "zip_dir"
        zippedFile = resources / f"{self.ZIPPED_FILE_NAME}.zip"
        if zippedFile.is_file():
            zippedFile.unlink()
    
    @pytest.fixture
    def zipFile(self, resources: Path):
        zip = resources / "zip_file.zip"
        yield zip
        unzippedDir = zip.with_name(self.UNZIPPED_DIR_NAME)
        if unzippedDir.is_dir():
            shutil.rmtree(unzippedDir)


    def test_zip_directory(self, zipDir: Path):
        assert zipDir.is_dir()
        zipFile = zipDirectory(zipDir, self.ZIPPED_FILE_NAME)
        assert zipFile == zipDir.with_name(f"{self.ZIPPED_FILE_NAME}.zip")
        assert zipFile.is_file()

    def test_unzip_file(self, zipFile: Path):
        assert zipFile.is_file()
        unzip(zipFile, self.UNZIPPED_DIR_NAME)
        assert zipFile.with_name(self.UNZIPPED_DIR_NAME).is_dir()