import csv
import enum

from rolodex.datatypes import Entry, EntryList

class CsvReader:
    def load(self, istream) -> EntryList:
        result = EntryList()

        reader = csv.DictReader(istream)
        for row in reader:
            e = Entry.from_dict(row)
            result.append(e)

        return result