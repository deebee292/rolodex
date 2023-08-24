from enum import StrEnum
from collections import UserDict, UserList
from typing import Iterator
import re


class Fields(StrEnum):
    NAME = 'name'
    ADDRESS = 'address'
    PHONE = 'phone_number'

class Entry(UserDict):
    """A Dictionary based data structure where each key can only be an enum value from Fields."""    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in [x for x in Fields if x not in self.data.keys()]:
            self.data[f] = ''
        
    def __setitem__(self, key: Fields, value):
        try:
            if key in Fields:
                self.data[key] = value
        except:
            raise KeyError
            
    def to_dict(self) -> dict:
        return {str(k):v for k,v in self.data.items()}

    @staticmethod
    def from_dict(src: dict) -> object:
        return Entry({Fields(k):v for (k,v) in src.items() if Fields(k) in Fields})


class EntryList(UserList):
    """A List of Entry Objects. An EntryList can be thought of as an In-Memory database."""    
    def __setitem__(self, index, value: Entry):
        if not isinstance(value, Entry):
            raise ValueError
        self.data[index] = value

    def append(self, value: Entry):
        if not isinstance(value, Entry):
            raise ValueError
        self.data.append(value)
        

    def iter_filter(self, kwargs: dict) -> Iterator[Entry]:
        """Generator, yields any Entry objects that match the given kwargs 
        Example, {Fields.NAME:"bob"}
        

        Args:
            kwargs (dict): Filter definition where key is a Fields and value is a string (re)
                            Example, {Fields.NAME:".*(bob|mary)"}

        Yields:
            Iterator[Entry]: Yields an Entry object upon a match
        """        
        valid_kwargs = {k:v for (k,v) in kwargs.items() if k in Fields}
        
        for item in self.data:
            match = True
            for k,v in valid_kwargs.items():
                if not re.findall(v, item[k]):
                    match = False
                    break
            if match:
                yield item
    
    def filter(self, kwargs: dict) -> UserList:
        """Generates a Filtered EntryList. Wraps iter_filter.

        Args:
            kwargs (dict): A dictionary where Key -> Fields & Value is String

        Returns:
            EntryList 
        """        
        return EntryList([x for x in self.iter_filter(kwargs)])
            
               

