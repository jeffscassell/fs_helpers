from pathlib import Path
from zipfile import ZipFile, is_zipfile



def zipDirectory(
    source: str | Path,
    name: str | None = None,
    destination: str | Path | None = None,
    useCwd: bool = False
) -> Path:
    """ Create a ZIP file from the `source` directory with the `name` name
    in the `destination` directory. If `name` is not specified, use the
    directory's name with a .zip extension. If `destination` is not specified,
    use the same parent directory as `source` (default), or set `useCwd` to
    True to use the current working directory. """

    source = Path(source)

    if not source.exists():
        raise ValueError(f"Path does not exist: {source}")
    if not source.is_dir():
        raise TypeError(f"Path not a directory: {source}")
    
    if not name:
        name = source.stem + ".zip"
    elif not name.endswith(".zip"):
        name += ".zip"
    
    if destination:
        destination = Path(destination)
    if not destination\
        or not destination.is_dir():
        destination = source.parent if not useCwd else Path.cwd()
    
    zip = destination / name
    with ZipFile(zip, "w") as archive:
        for path in source.rglob("*"):
            archive.write(path, arcname=path.relative_to(source))
    return zip


def unzip(
    file: str | Path,
    unzippedDirectory: str | Path | None = None,
) -> None:
    """ Unzip a ZIP `file` and extract to the `unzippedDirectory`. """
    
    file = Path(file)
    if not file.exists():
        raise FileNotFoundError(f"Path is not a file: {file}")
    if not is_zipfile(file):
        raise TypeError(f"File is not a ZIP: {file}")
    
    if unzippedDirectory:
        unzippedDirectory = Path(unzippedDirectory)
    if not unzippedDirectory:
        unzippedDirectory = file.with_suffix("")
    elif unzippedDirectory.is_dir():
        raise IsADirectoryError(f"Destination exists: {unzippedDirectory}")
    elif not unzippedDirectory.is_absolute():
        unzippedDirectory = file.parent / unzippedDirectory
    
    with ZipFile(file) as archive:
        archive.extractall(unzippedDirectory)