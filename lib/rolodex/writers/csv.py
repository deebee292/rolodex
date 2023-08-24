import csv

from rolodex.datatypes import Fields, Entry, EntryList

class CsvWriter:
    def dump(self, elist: EntryList, ostream) -> None:
        def _header()->list:
            return [str(f) for f in Fields]

        def _to_list(entry: Entry) -> list:
            return [entry[f] for f in Fields]
        
        writer = csv.writer(ostream)

        writer.writerow(_header())
        for e in elist:
            writer.writerow(_to_list(e))
