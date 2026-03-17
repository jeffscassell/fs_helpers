from pathlib import Path
import shutil

import pytest

from fs_helpers.zip_directory import zipDirectory, unzip



ZIPPED_FILE_NAME = "zipped_file"
UNZIPPED_DIR_NAME = "unzipped_dir"

@pytest.fixture
def zipDir(resources: Path):
    yield resources / "zip_dir"
    zippedFile = resources / f"{ZIPPED_FILE_NAME}.zip"
    if zippedFile.is_file():
        zippedFile.unlink()

@pytest.fixture
def zipFile(resources: Path):
    zip = resources / "zip_file.zip"
    yield zip
    unzippedDir = zip.with_name(UNZIPPED_DIR_NAME)
    if unzippedDir.is_dir():
        shutil.rmtree(unzippedDir)

@pytest.fixture
def existingDirectory(resources: Path):
    directory = resources / "existingDirectory"
    directory.mkdir()
    yield directory
    if directory.is_dir():
        shutil.rmtree(directory)


def testZipDirectory(zipDir: Path):
    assert zipDir.is_dir()
    zipFile = zipDirectory(zipDir, ZIPPED_FILE_NAME)
    assert zipFile == zipDir.with_name(f"{ZIPPED_FILE_NAME}.zip")
    assert zipFile.is_file()

def testUnzipFile(zipFile: Path):
    assert zipFile.is_file()
    unzip(zipFile, UNZIPPED_DIR_NAME)
    assert zipFile.with_name(UNZIPPED_DIR_NAME).is_dir()

def testUnzipToExistingDirectory(zipFile: Path, existingDirectory: Path):
    assert zipFile.is_file()
    assert existingDirectory.is_dir()
    with pytest.raises(FileExistsError):
        unzip(zipFile, existingDirectory)
    unzip(zipFile, existingDirectory, existsOk=True)
