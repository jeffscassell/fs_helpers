import pytest

from fs_helpers.filename import Filename

INCORRECT_SAMPLE = "[a tag] a title"
CORRECT_SAMPLE = "[a_tag]_a_title"


@pytest.fixture
def filename():
   return Filename(INCORRECT_SAMPLE)


def testTag(filename):
   assert filename.tag == "a tag"


def testNewTag(filename):
   assert filename.newTag == "a_tag"


def testTitle(filename):
   assert filename.title == "a title"


def testNewTitle(filename):
   assert filename.newTitle == "a_title"


def testGetNewFilename(filename):
   assert filename.newFilename == CORRECT_SAMPLE


def testClean():
   sample = "here-is a name"
   sampleCleaned = "here-is_a_name"
   assert Filename.clean(sample) == sampleCleaned
   assert Filename(sample).newFilename == sampleCleaned

   illegal = "some illegal (':'^') characters"
   illegalCleaned = "some_illegal_(''')_characters"
   assert Filename.clean(illegal) == illegalCleaned
