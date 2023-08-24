import json

from rolodex.datatypes import EntryList

class JsonWriter:    
    def dump(self, elist: EntryList, ostream) -> None:
        output = [e.to_dict() for e in elist]
        json.dump(output, ostream)
