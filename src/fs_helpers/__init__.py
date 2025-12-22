"""
FS (filesystem) Helpers

A modest library to re-use code I've written for handling common filesystem
operations, like sanitizing filenames and downloading a file from a URL.
"""

from .work import (
    cleanFilename,
    confirm,
    downloadFile,
    progressBar,
    size,
    zipDirectory,
    unzip,
)