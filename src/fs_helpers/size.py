from pathlib import Path



def sizei(inputPath: str | Path) -> int:
    """
    Accepts a filesystem path and returns the number of bytes of that path.
    """
    
    path = inputPath
    BAD_INPUT_VALUE = 0
    
    # Determine number of bytes we're working with.
    path = Path(path)
    if path.is_file():
        total = path.stat().st_size
    elif path.is_dir():
        total = 0
        for currentPath, subdirs, files in path.walk():
            for currentFile in files:
                total += (currentPath / currentFile).stat().st_size
    else:
        return BAD_INPUT_VALUE
    
    return total


def sizes(input: int | str | Path) -> str:
    """
    Accepts either a filesystem path or number of bytes and returns a
    human-readable file size string.
    """
    
    if isinstance(input, (str, Path)):
        path = input
        bytes = None
    else:
        path = None
        bytes = input
    
    BAD_INPUT_VALUE = "0 bytes"
    
    # Determine number of bytes we're working with.
    if bytes:
        total = bytes
    elif path:
        total = sizei(path)
    else:
        return BAD_INPUT_VALUE
    
    # Make the output pretty.
    sizes = "bytes KiB MiB GiB TiB".split()
    for i in range(len(sizes)):  # Example fileSize: 121291539
        scaled = total / 1024**i  # 121291539 / 1024 = 118448.768...
        if len(f"{scaled:.0f}") < 4:  # if [118448].768... < 4 characters
            number = f"{scaled:.2f}"
            if number[-3:] == ".00":
                number = number[:-3]
            specifier = sizes[i]
            return f"{number} {specifier}"
    
    return f"{total:,} bytes"