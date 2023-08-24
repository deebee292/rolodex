"""
writers

This is a basic factory idea.

Formats that are supported for read are defined within "WriterTypes".
Every WriterType has its own python file which implements the Writer(Protocol)

Basic Usage Example:

    e_list = EntryList([Entry()])
    w = get_writer(WriterTypes.JSON)
    with open("somefile.json", 'w') as fp:
        e_list = w.dump(e_list, fp)
        
"""
from enum import StrEnum
from typing import Protocol, IO

import os.path

from rolodex.datatypes import EntryList

from .csv import CsvWriter
from .json import JsonWriter
from .yaml import YamlWriter

class WriterTypes(StrEnum):
    """Defines what formats are supported by the writer factory"""
    CSV = 'csv'
    JSON = 'json'
    YAML = 'yaml'

class Writer(Protocol):
    def dump(elist: EntryList, ostream: IO) -> None:
        """Takes an EntryList and writes to the IO stream

        Args:
            elist (EntryList):
            ostream (IO): An Output Stream, supports write
        """        

# Lookup Dictionary, populate with all known Writers
_factory_dict = {
                WriterTypes.CSV: CsvWriter,
                WriterTypes.JSON: JsonWriter,
                WriterTypes.YAML: YamlWriter
                }

def get_writer_types() -> WriterTypes:
    return WriterTypes
    
def get_writer(wtype: WriterTypes) -> Writer:
    _obj =  _factory_dict.get(wtype)
    return _obj()


def dump_to_file(fname: str, elist: EntryList, wtype: WriterTypes = None) -> None:
    """Convience wrapper to allow easy writes to a file.
    Will auto-detect the needed writer based upon the file extension.
    The writer type can be passed explicitly.

    Args:
        fname (str): Path to a file on disk to be writen (over-writes!!)
        wtype (WriterTypes, optional): Allow to specify which writer to use. Defaults to None.

    """
    _wt  = wtype
    if not _wt:
        p, ext = os.path.splitext(fname)
        _wt = WriterTypes(ext.strip('.').lower())
    
    w = get_writer(_wt)
    with open(fname, 'w') as fp:
        result = w.dump(elist, fp)
    
    return result

