from pathlib import Path
import re
from typing import Iterable, TypeVar, Iterator

import requests

from .size import sizes



T = TypeVar("T")


def cleanFilename(filename: str) -> str:
    """
    Sanitizes and validates a filename, then returns the result.
    
    :param str filename: Expects a string.
    :return (str) filename: A sanitized filename.
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


def confirm(
    message: str | None = None,
) -> bool:
    
    if not message:
        message = "Continuing"
    
    print(message)

    confirm = ""
    while confirm not in ("y", "n"):
        confirm = input(f"Accept? [Y/n]: ").lower() or "y"

    if confirm == "n":
        return False

    return True


def progressBar(
    iterable: Iterable[T],
    chunkSize: int | None = None,
    fileSize: int | None = None,
    prefix: str = "Progress",
    suffix: str = "Complete",
    barLength: int = 80,
    filledCharacter: str = "#",
    emptyCharacter: str = "-",
) -> Iterator[T]:
    """
    Accepts an Iterable and yields each element, printing progress as each
    element is yielded. If used to download a file, use the `chunkSize` and
    `fileSize` parameters so that the progress bar fills appropriately, as
    there is no way (that I currently know of) to dynamically determine this
    information.
    
    .. Usage::
        ```
        for element in progressBar(iterator):
            # Do work.
        ```
        
    .. Usage::
        ```
        with requests.get(url, stream=True) as response:
            fileSize = int(response.headers["Content-length"])
        
            with open(file, "wb") as outfile:
                chunkSize = 8192
                
                for chunk in progressBar(
                    response.iter_content(chunk_size=chunkSize),
                    chunkSize=chunkSize,
                    fileSize=fileSize
                ):
                    outfile.write(chunk)
        ```
    
    :param Iterable (required) iterable: Object to iterate through until completion.
    :param int chunkSize: Intended to be used when downloading a file.\
        The amount that each iteration will account for on the progress bar.\
        `Note: must be used in conjunction with the 'fileSize' parameter if\
        used.`
    :param int fileSize: Intended to be used when downloading a file. Used\
        so the bar will fill appropriately. `Note: must be used in conjunction\
        with the 'chunkSize' parameter if used.`
    :param str prefix: The text displayed behind the progress bar's rendering.
    :param str suffix: The text displayed in front of the progress bar's\
        rendering.
    :param int barLength: The amount of characters the bar should occupy on\
        the CLI.
    :param str filledCharacter: The character used to indicate a filled\
        portion of the progress bar.
    :param str emptyCharacter: The character used to indicate an empty\
        portion of the progress bar.
    """
    
    if fileSize and not chunkSize:
        fileSize = None
    
    if chunkSize and not fileSize:
        chunkSize = None
    
    if fileSize:
        total = fileSize
    else:
        total = sum(1 for _ in iterable)
    
    # Subtract the length of each component included within the progress bar.
    barLength = barLength - (len(prefix) + 3) - 9 - len(suffix)
    
    def printProgressBar(iteration, full: bool = False) -> None:
        # Percent will always occupy at least 5 spaces, with 1 trailing digit.
        percent = "{0:5.1f}".format(100 * (iteration) / float(total))

        # Address a bug I'm too lazy to investigate where bar never fills to
        # 100% at the end.
        if full:
            filledLength = barLength
            percent = 100.0
        else:
            filledLength = int(barLength * iteration // total)

        wholeBar = filledCharacter * filledLength + emptyCharacter * \
            (barLength - filledLength)
        print(f"{prefix}: |{wholeBar}| {percent}% {suffix}", end="\r")
    
    # Create starting progress bar.
    printProgressBar(0)
    
    # Update progress bar and return items as work is completed.
    for i, item in enumerate(iterable):
        yield item
        
        if chunkSize:
            i *= chunkSize
        printProgressBar(i + 1)
    
    # Fix bug so that bar fills 100%
    printProgressBar(0, full=True)
    
    # Print a newline at progress completion.
    print()


def _extractFilenameFromUrl(url: str) -> str:
    """ Extract the filename (last segment) of a URL; e.g.,
    `.../some/path/<with.file.name.ext>` """

    # Remove trailing slash if there is one.
    if url[-1] == "/":
        url = url[:-1]
    filename = url.split("/")[-1]
    return filename


def _extractName(filename: str) -> str:
    return Path(filename).stem


def _extractExtension(filename: str) -> str:
    ext = Path(filename).suffix
    if "?" in ext:
        ext, *_ = ext.split("?")
    return ext


def downloadFile(
    url: str,
    filename: str | None = None,
    location: Path | str | None = None,
    session: requests.Session | None = None,
    headers: dict[str, str | bytes | None] | None = None,
) -> None:
    """
    Download a file at the specified URL, with an optional filename. If no
    filename is given, the filename from the URL is used. The filename is
    automatically sanitized and validated. The location to save the file
    can also be specified.
    
    .. Example::
        url=`https://www.domain.com/path/to/a_file.mp4`,
        filename=`some new name`\n
        The file that will be saved is: `some_new_name.mp4`
    
    .. Example::
        url=`https://www.domain.com/path/to/a_file.mp4`\n
        The file that will be saved is: `a_file.mp4`
    
    :param str url: Takes the form: `https://www.domain.com/path/to/a_file.mp4`
    :param str (optional) filename: `filename` will be converted automatically\
        to the relevant extension based on the file's extension in the URL,\
        e.g., `filename.mp4`.
    :param str | Path (optional) location: `location` refers to the location\
        that the file will be saved after download. Must be a directory.
    """
    
    if not session:
        handler = requests
    else:
        handler = session
    
    if not headers:
        headers = {}
    
    extractedFilename = _extractFilenameFromUrl(url)
    urlFilename = _extractName(extractedFilename)
    ext = _extractExtension(extractedFilename)
    
    # Use the URL's filename if one was not provided at function call.
    if not filename:
        filename = urlFilename
    filename = cleanFilename(filename)
    
    # Validate and build file save location.
    if not location:
        location = Path.cwd()
    else:
        location = Path(location)
        if not Path(location).is_dir():
            print("Invalid save location. Defaulting to current directory...")
            location = Path.cwd()
    
    # Prompt for overwrite if file exists.
    saveLocation = location / f"{filename}{ext}"
    if saveLocation.exists():
        
        confirm = "n"
        while confirm != "y":
            confirm = input(
                f"File exists: {saveLocation}\n"
                f"Overwrite? [Y/n]: "
            ).lower() or "y"
            
            if confirm == "n":
                return
        print()
    
    
    try:
        with handler.get(url, timeout=5, stream=True, headers=headers) as response:
            
            try:
                fileSize = int(response.headers["Content-length"])
            except ValueError:
                fileSize = 0

            if not fileSize >= 0:
                raise ValueError("URL points to empty file.")

            with open(saveLocation, "wb") as outfile:
                
                for chunk in progressBar(
                    response.iter_content(chunk_size=8192),
                    chunkSize=8192,
                    fileSize=fileSize,
                    suffix=sizes(fileSize),
                ):
                    outfile.write(chunk)

                # shutil.copyfileobj(response.raw, outfile)
                print(saveLocation)
    except KeyboardInterrupt:
        saveLocation.unlink()
        print()
