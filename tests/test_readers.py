import unittest
import os
import io

from rolodex.datatypes import Fields, Entry, EntryList
import rolodex.readers as readers

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), 'resources')

class ReadersTest(unittest.TestCase):
    def test_getwriter(self):
        for wt in readers.get_reader_types():
            readers.get_reader(wt)
        
        for wt in readers.ReaderTypes:
            readers.get_reader(wt)

    @unittest.expectedFailure
    def test_load_null(self):
        e_list = EntryList([Entry()])
        
        # test a read that should fail from os.devnull
        with open(os.devnull, 'r') as fp:
            for rt in readers.ReaderTypes:
                r = readers.get_reader(rt)
                e_list = r.load(fp)

    def test_load_file(self):
        csv_file = os.path.join(RESOURCE_PATH, 'dataset.csv')
        with open(csv_file, 'r') as fp:
            e = Entry.from_dict({Fields.NAME:'alice',
                                    Fields.PHONE: '555-123-4567',
                                    Fields.ADDRESS: '456 Somewhere Ville'})
            r = readers.get_reader(readers.ReaderTypes.CSV)
            e_list = r.load(fp)

            self.assertIn(e, e_list)

        valid_list = EntryList([
                                Entry.from_dict({Fields.NAME:'bob',
                                                Fields.PHONE:'555-555-5555',
                                                Fields.ADDRESS: '123 Somewhere Ville'}),
                                Entry.from_dict({Fields.NAME:'alice',
                                                Fields.PHONE: '555-123-4567',
                                                Fields.ADDRESS: '456 Somewhere Ville'}),
                                ])
        json_file = os.path.join(RESOURCE_PATH, 'dataset.json')
        e_list = readers.load_from_file(json_file)
        for vl, el in zip(valid_list, e_list):
            self.assertEqual(vl, el)

            
                


            



        '''
        # test to a string buffer
        e = Entry()
        e[Fields.NAME] = 'bob'
        e_list = EntryList([e])

        for wt in reader.ReaderTypes:
            buf = io.StringIO()
            w = reader.get_writer(wt)
            w.dump(e_list, buf)

            self.assertNotEqual(buf.getvalue(), '')
        '''
        
        
        



if '__main__' == __name__:
    unittest.main()

