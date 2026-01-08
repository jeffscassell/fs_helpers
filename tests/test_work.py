import pytest

from fs_helpers.work import (
    cleanFilename,
    _extractFilenameFromUrl,
    _extractName,
    _extractExtension,
)



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
