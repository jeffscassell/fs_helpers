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
    existsOk: bool = False,
) -> None:
    """
    Unzip a ZIP `file` and extract to the `unzippedDirectory`.
    `unzippedDirectory` can be relative or absolute. If relative, it will be
    unzipped to the same directory as `file`.
    
    :raises FileExistsError: If the `unzippedDirectory` already exists, and
    `existsOk` is `False` (default), raises a `FileExistsError`.
    """

    file = Path(file)
    if not file.exists():
        raise FileNotFoundError(f"Path is not a file: {file}")
    if not is_zipfile(file):
        raise TypeError(f"File is not a ZIP: {file}")

    # Make unzippedDirectory safe to work with first: turn it into a Path.
    if unzippedDirectory:
        unzippedDirectory = Path(unzippedDirectory)
    if not unzippedDirectory:
        unzippedDirectory = file.with_suffix("")

    # Turn it into an absolute path if it isn't yet.
    if not unzippedDirectory.is_absolute():
        unzippedDirectory = file.parent / unzippedDirectory

    # Then work with a fully qualified Path.
    if unzippedDirectory.is_dir() and not existsOk:
        raise FileExistsError(f"Destination exists: {unzippedDirectory}")

    with ZipFile(file) as archive:
        archive.extractall(unzippedDirectory)
