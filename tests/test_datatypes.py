import unittest

from rolodex.datatypes import Fields, Entry, EntryList

class FieldsTest(unittest.TestCase):
    def test_access(self):
        values = []
        for f in Fields:
            values.append(f)
       

class EntryTest(unittest.TestCase):
    def test_creation(self):
        e = Entry()

        for f in Fields:
            self.assertEqual(e[f], '')

    def test_creation_via_dict(self):
        e = Entry(**{Fields.NAME:'bob',
                        Fields.ADDRESS:'123 Somewhere',
                        Fields.PHONE:'555-555-5555'})

        self.assertEqual(e[Fields.NAME], 'bob')
        self.assertEqual(e[Fields.ADDRESS], '123 Somewhere')
        self.assertEqual(e[Fields.PHONE], '555-555-5555')

        e = Entry()
        e[Fields.NAME] = 'bob'
        self.assertEqual(e[Fields.NAME], 'bob')

    def test_creation_via_bydict(self):
        e = Entry.from_dict({Fields.NAME:'bob',
                    Fields.ADDRESS:'123 Somewhere'})
        self.assertEqual(e[Fields.NAME], 'bob')
        self.assertEqual(e[Fields.ADDRESS], '123 Somewhere')
        self.assertEqual(e[Fields.PHONE], '')

    def test_keyerror(self):
        e = Entry()
        with self.assertRaises(KeyError):
            e['invalid_key_here'] = 'nope'

class EntryListTest(unittest.TestCase):
    def test_creation(self):
        e = Entry()
        e_list = EntryList()
        self.assertEqual(e_list, [])

        e_list = EntryList([Entry(), Entry(), Entry()])
        self.assertEqual(len(e_list), 3)

        e_list = EntryList()
        e1 = Entry(**{Fields.NAME:'bob',
                        Fields.ADDRESS:'123 Somewhere',
                        Fields.PHONE:'555-555-5555'})
        e2 =  Entry(**{Fields.NAME:'alice',
                        Fields.ADDRESS:'123 Somewhere',
                        Fields.PHONE:'555-123-4567'})    
        self.assertNotEqual(e1, e2)

        e_list.append(e1)
        e_list.extend([e2])

        epop1 = e_list.pop()
        self.assertEqual(e2, epop1)

        epop2 = e_list.pop()
        self.assertEqual(e1, epop2)

    def test_filter(self):
        e_list = EntryList([
                        Entry.from_dict({Fields.NAME:'bob',
                                        Fields.PHONE:'555-555-5555',
                                        Fields.ADDRESS: '123 Somewhere Ville'}),
                        Entry.from_dict({Fields.NAME:'alice',
                                        Fields.PHONE: '555-123-4567',
                                        Fields.ADDRESS: '456 Somewhere Ville'}),
                        ])
        
        f_list = e_list.filter({Fields.NAME:'alice'})
        self.assertIn(e_list[1], f_list)
        self.assertEqual(len(f_list), 1)

        f_list = e_list.filter({Fields.PHONE:'123'})
        self.assertIn(e_list[1], f_list)
        self.assertEqual(len(f_list), 1)

        f_list = e_list.filter({Fields.NAME: 'bob', Fields.ADDRESS: 'Somewhere Ville'})
        self.assertIn(e_list[0], f_list)
        self.assertEqual(len(f_list), 1)




if '__main__' == __name__:
    unittest.main()        




