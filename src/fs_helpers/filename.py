import re


class Filename:
   # sample filename: [tag]_title_of_file
   # tag: Match.group(2)
   # title_of_file: Match.group(3)
   _PATTERN = re.compile(r"^(\[(.*?)\][_ -]?)?(.*)")
   _filename: str

   def __init__(self, filename: str):
      self._filename = filename

   def __str__(self) -> str:
      return self._filename

   @property
   def tag(self) -> str:
      """ Returns only the original contents of the tag (if it exists). """

      matched = re.search(self._PATTERN, self._filename)
      if not matched or not matched.group(2):
         return ""

      return matched.group(2)

   @property
   def title(self) -> str:
      """ Returns only the original title of the filename, excluding any
      tags or extra whitespace/word separators. """

      matched = re.search(self._PATTERN, self._filename)
      if not matched or not matched.group(3):
         return ""

      return matched.group(3)

   @property
   def newTag(self) -> str:
      """ Returns only the updated version of the tag (if it exists),
      correcting for any erroneous spaces within. """

      rawTag = self.tag
      if not rawTag:
         return ""

      # Fix any erroneous spaces within tag(s).
      # "some space, in_tags" -> "some_space,in_tags"
      tags = rawTag.split(",")  # ["some space", " in_tags"]
      fixedTags = []
      for tag in tags:
         tag = tag.split()  # ["some", "space"]
         fixedTags.append("_".join(tag))  # ["some_space"]
      return ",".join(fixedTags)  # "some_space,in_tags"

   @property
   def newTitle(self) -> str:
      """ Eeturns only the title of the file, excluding any
      tags or extra whitespace/word separators. """

      matched = re.search(self._PATTERN, self._filename)
      if not matched or not matched.group(3):
         return ""

      title = self.title
      return "_".join(title.split())

   @classmethod
   def clean(cls, filename: str) -> str:
      """
      Sanitizes a filename and returns the result.
      
      Removes illegal file system characters, extra spacing between words, and
      converts spaces to underscores.
      """

      illegalCharacters = (
         ":",
         "^",
         "@",
         "<",
         ">",
         "?",
         "*",
         "|",
         "/",
         "\\",
         "\"",
         "/",
      )

      filename = filename.replace(" ", "_")
      filename = re.sub("_{2,}", "_", filename)

      for character in illegalCharacters:
         filename = filename.replace(character, "")

      return filename

   @property
   def newFilename(self) -> str:
      """ Combines both new Tag and new Title to create a new filename in the
      form: [tag]_new_title """

      tag = self.newTag
      title = self.newTitle
      result = ""

      if tag:
         result += f"[{tag}]"

      if tag and title:
         result += f" {title}"
      elif title:
         result += title

      return self.clean(result)
