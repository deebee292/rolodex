import json
import enum
from rolodex.datatypes import Entry, EntryList

class JsonReader:
    def load(self, istream) -> EntryList:
        result = EntryList()

        jobj = json.load(istream)
        result.extend([Entry.from_dict(j) for j in jobj])

        return result