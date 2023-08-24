import yaml
import enum
from rolodex.datatypes import Fields, Entry, EntryList

class YamlReader:
    def load(self, istream) -> EntryList:
        result = EntryList()

        jobj = yaml.safe_load(istream)
        result.extend([Entry.from_dict(j) for j in jobj])  
        
        return result      
