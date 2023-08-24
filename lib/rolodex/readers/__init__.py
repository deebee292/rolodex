"""
readers

This is a basic factory idea.
Formats that are supported for read are defined within "ReaderTypes".
Every ReaderType has its own python file which implements the Reader(Protocol)

Basic Usage Example:
    e_list = None
    r = get_reader(ReaderTypes.JSON)
    with open("somefile.json", 'r') as fp:
        e_list = r.load(fp)

"""
from enum import StrEnum
from typing import Protocol, IO

import os.path

from rolodex.datatypes import Entry, EntryList

from .csv import CsvReader
from .json import JsonReader
from .yaml import YamlReader

class ReaderTypes(StrEnum):
    """Defines what formats are supported by the reader factory"""
    JSON = 'json'
    YAML = 'yaml'
    CSV = 'csv'

class Reader(Protocol):
    def load(self, istream: IO) -> EntryList:
        """Load in data from a io stream

        Args:
            istream (io.RawIOBase): An Input Stream, supports "read"

        Returns:
            EntryList
        """

# Lookup Dictionary, populate with all known Readers
_factory_dict = {
                ReaderTypes.CSV: CsvReader,
                ReaderTypes.JSON: JsonReader,
                ReaderTypes.YAML: YamlReader
                }

def get_reader_types() -> ReaderTypes:
    return ReaderTypes

def get_reader(rtype: ReaderTypes) -> Reader:
    _obj = _factory_dict.get(rtype)
    return _obj()

def load_from_file(fname: str, rtype: ReaderTypes = None) -> EntryList:
    """Convience wrapper to allow easy loads from an existing file.
    Will auto-detect the needed reader based upon the file extension.
    The reader type can be passed explicitly.

    Args:
        fname (str): Path to a file on disk
        rtype (ReaderTypes, optional): Allow to specify which reader to use. Defaults to None.

    Returns:
        EntryList
    """
    result = EntryList()
    
    _rt  = rtype
    if not _rt:
        p, ext = os.path.splitext(fname)
        _rt = ReaderTypes(ext.strip('.').lower())
    
    r = get_reader(_rt)
    with open(fname, 'r') as fp:
        result = r.load(fp)
    
    return result
