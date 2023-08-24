import yaml

from rolodex.datatypes import EntryList

class YamlWriter:
    def dump(self, elist: EntryList, ostream) -> None:
        output = [e.to_dict() for e in elist]
        yaml.dump(output, ostream)        