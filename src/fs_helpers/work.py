import shutil
from pathlib import Path
import re
from typing import Iterable, Any

import requests



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


def confirmFilename(filename: str) -> str:
    confirm = ""
        
    while confirm.lower() != "y":
        confirm = input(
            f"Proposed file name: {filename}\n"
            f"Accept name? [Y/n]: "
        ).lower() or "y"

        if confirm == "n":
            filename = input(f"Enter new file name: ")
            print()

    return filename


def progressBar(
    iterable: Iterable[Any],
    chunkSize: int | None = None,
    fileSize: int | None = None,
    prefix: str = "Progress",
    suffix: str = "Complete",
    decimals: int = 1,
    length: int = 80,
    empty: str = "-",
    fill: str = "#",
):
    """
    Accepts an Iterable and yields each element, printing progress as each
    element is yielded. If used to download a file, use the `chunkSize` and
    `fileSize` parameters so that the progress bar fills appropriately, as
    there is no way (that I currently know of) to dynamically determine this
    information.
    
    :param (Iterable) iterable: Object to iterate through until completion.
    :param (int) chunkSize: Intended to be used when downloading a file.\
        The amount that each iteration will account for on the progress bar.\
        `Note: must be used in conjunction with the 'fileSize' parameter if\
        used.`
    :param (int) fileSize: Intended to be used when downloading a file. The\
        
    """
    
    if fileSize and not chunkSize:
        fileSize = None
    
    if chunkSize and not fileSize:
        chunkSize = None
    
    if fileSize:
        total = fileSize
        sizes = "KiB MiB GiB".split()
        
        # Change the suffix to the file's actual size.
        for i in range(3):  # Example fileSize: 121291539
            size = fileSize / 1024**(i+1)  # 121291539 / 1024 = 118448.768...
            if len(f"{size:.0f}") < 4:  # if [118448].768... < 4 characters
                suffix = f"{size:.2f} {sizes[i]}"
                break
    else:
        total = sum(1 for _ in iterable)
    
    length = length - (len(prefix) + 3) - (len(suffix) + 7)
    
    def printProgressBar(iteration) -> None:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration) / float(total))
        filledBar = int(length * iteration // total)
        wholeBar = fill * filledBar + empty * (length - filledBar)
        print(f"{prefix}: |{wholeBar}| {percent}% {suffix}", end="\r")
    
    # Create starting progress bar.
    printProgressBar(0)
    
    # Update progress bar and return items as work is completed.
    for i, item in enumerate(iterable):
        yield item
        
        if chunkSize:
            i *= chunkSize
        printProgressBar(i + 1)
    
    # Print a newline at progress completion.
    print()
    ...


def downloadFile(
    url: str,
    filename: str | None = None,
    location: Path | str | None = None,
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
    :param str (optional) filename: `filename` will be converted automatically
    to the relevant extension based on the file's extension in the URL, e.g., `filename.mp4`.
    :param str (optional) location: `location` refers to the location that the
    file will be saved after download. Must be a directory.
    """
    
    if not url:
        raise ValueError("Missing URL to download file")
    
    if not isinstance(url, str):
        raise TypeError("URL is not of string type")
    
    # Extract the last segment of the URL (".../path/<some.file.name.ext>")
    urlFilename = url.split("/")[-1]
    # Separate out the file parts (["some", "file", "name"], "ext")
    *urlFilename, ext = urlFilename.split(".")
    urlFilename = "_".join(urlFilename)
    
    if ext:
        ext = "." + ext
    else:
        ext = ""
    
    # Get the filename from the passed argument if it exists, or use the URL's
    if not filename:
        filename = urlFilename
    filename = cleanFilename(filename)
    
    # Validate and build file save location
    if not location:
        location = Path.cwd()
    else:
        location = Path(location)
        if not Path(location).exists() or not Path(location).is_dir():
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
        with requests.get(url, timeout=5, stream=True) as response:
            
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
                    fileSize=fileSize
                ):
                    outfile.write(chunk)

                # shutil.copyfileobj(response.raw, outfile)
                print(saveLocation)
    except KeyboardInterrupt:
        saveLocation.unlink()
        print()
