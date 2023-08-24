import unittest
import os
import io

from rolodex.datatypes import Fields, Entry, EntryList
import rolodex.writers as writers

class WritersTest(unittest.TestCase):
    def test_getwriter(self):
        for wt in writers.get_writer_types():
            writers.get_writer(wt)
        
        for wt in writers.WriterTypes:
            writers.get_writer(wt)

    def test_dump(self):
        e_list = EntryList([Entry()])
        
        # test a dump to os.devnull
        with open(os.devnull, 'w') as fp:
            for wt in writers.WriterTypes:
                w = writers.get_writer(wt)
                w.dump(e_list, fp)

        # test to a string buffer
        e = Entry()
        e[Fields.NAME] = 'bob'
        e_list = EntryList([e])

        for wt in writers.WriterTypes:
            buf = io.StringIO()
            w = writers.get_writer(wt)
            w.dump(e_list, buf)

            self.assertNotEqual(buf.getvalue(), '')
        
        
        



if '__main__' == __name__:
    unittest.main()

