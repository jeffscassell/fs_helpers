import pytest
from pathlib import Path
import shutil

from fs_helpers.work import (
    cleanFilename,
    size,
    zipDirectory,
    unzip,
    _extractFilenameFromUrl,
    _extractName,
    _extractExtension,
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


def test_clean_filename():
    filename = "here-is a name"
    assert cleanFilename(filename) == "here-is_a_name"
    
    filename = "some illegal (':'^') characters"
    assert cleanFilename(filename) == "some_illegal_(''')_characters"


def test_extractFilename():
    url = "https://www.website.com/a/path/here/with.a_file-name.mp4"
    filename = "with.a_file-name.mp4"
    assert _extractFilenameFromUrl(url) == filename
    assert _extractFilenameFromUrl(url + "/") == filename


problems = (
    "a.file_name-here.mp4",
    "a.file.name.here.mp4",
)
solutions = (
    "a.file_name-here",
    "a.file.name.here",
)
@pytest.fixture(params=zip(problems, solutions))
def filenames(request):
    return request.param

def test_extractName(filenames):
    filename, solution = filenames
    assert _extractName(filename) == solution

def test_extractExtension(filenames):
    filename, _ = filenames
    assert _extractExtension(filename) == ".mp4"
