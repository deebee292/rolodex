"""
Allows Creation, Storage, Filter, Conversion of a simple Rolodex style database

# Create a one entry file myfile.csv
rdex.py --file_out myfile.csv --add name='bob' address='123 Somewhere' phone_number='555-123-4567'

# Read from then write to myfile.csv adding an entry for 'alice'
rdex.py --file_in myfile.csv --file_out myfile.csv --add name='alice' address='345 Somewhere' phone_number='555-555-5555'

# Display data within the myfile.csv
rdex.py --file_in myfile.csv --display

# Display data within the myfile.csv as a yaml
rdex.py --file_in myfile.csv --display --display_format yaml

# Preform a filter and display the result (note: this does nothing to the loaded file)
rdex.py --file_in myfile.csv --filter name='bob' --display

# Preform a file format conversion CSV->YAML
rdex.py --file_in myfile.csv --file_out myfile.yaml

# Preform a filter operation and write that to myfile_filtered.yaml
rdex.py --file_in myfile.csv --file_out myfile_filtered.yaml --filter name="alice"

# Get some information on the fields supported by both ADD and FILTER
rdex.py info --fields
"""

from argparse import ArgumentParser
from rolodex.datatypes import Fields, Entry, EntryList
import rolodex.readers as rolo_readers
import rolodex.writers as rolo_writers

import sys
import re

def setup_argparse() -> ArgumentParser:
    parser = ArgumentParser(prog='rdex')
    parser.add_argument('-i', '--file_in', help="Input Database file, Read-Only from disk")
    parser.add_argument('-o', '--file_out', help="Output Database File, Over-Writes to disk")
    parser.add_argument('-d', '--display', action='store_true', help="Terminal Output")
    parser.add_argument('-df', '--display_format', help="Format desired for terminal output")

    add_help_str = 'Any combination of <field>="<string>", run "rdex info --fields"  for detailed field names'
    parser.add_argument('--add', nargs='+', action='append', help=add_help_str)
    
    filter_help_str = 'Any combination of <field>="<string>", run "rdex info --fields"  for detailed field names'
    parser.add_argument('--filter', nargs='+', help=filter_help_str)
    

    sub_parser = parser.add_subparsers(title='Additional Arguments')
    
    info_parser = sub_parser.add_parser('info')
    info_parser.add_argument('--fields', action='store_true', help='Display the valid Field names')
    info_parser.call = run_display_flags

    return parser

def run_display_flags() -> None:
    for f in Fields:
        print(f, '<string>')

def main(args: dict)->None:
    def _get_fields_dict(src: list) -> dict:
        """Creates a valid <Fields>:<Value> key value based upon a ['<field_name>=<string>',.. ]"""
        src_str = ' ' + ' '.join(src)
        src_parts = re.split(r'( \w+=)', src_str)

        f_dict = {}
        for k,v in zip(src_parts[1::2], src_parts[2::2]):
            f = Fields(k.strip(' ='))
            f_dict.update({f:v})
       
        return f_dict

    # The in-memory database, it will be replaced should a file_in or filter be processed
    database = EntryList()

    # -- File In --
    # Reads an already existing database from disk (based upon a FileOut)
    fname = args.get('file_in')
    if fname:
        database = rolo_readers.load_from_file(fname)
    
    # -- Add --
    # Functions on the in-memory database only
    add_args = args.get('add')
    if add_args:
        for add_arg in add_args:
            try:
                add_dict = _get_fields_dict(add_arg)
            except ValueError as e:
                print('Add Error: ', e)
                exit()

            entry = Entry.from_dict(add_dict)
            entry.get(Fields.PHONE)
            database.append(entry)

    # -- Filter --
    # Replaces the current in-memory database with the newly filtered database
    filter_args = args.get('filter')
    if filter_args:
        try:
            filter_dict = _get_fields_dict(filter_args)
        except ValueError as e:
            print('Filter Error: ', e)
            exit()
        database = database.filter(filter_dict)
                
    # -- Display --
    # Uses sys.stdout for stream output
    display = args.get('display')
    if display:
        display_format = args.get('display_format') or 'csv'
        wr = rolo_writers.get_writer(rolo_writers.WriterTypes(display_format))
        wr.dump(database, sys.stdout)

    # -- File Out --
    # This is destructive. It will over-write any already existing files.
    # FileOut needs to be used should any ADD(s) want to be preserved
    fw_name = args.get('file_out')
    if fw_name:
        wr = rolo_writers.dump_to_file(fw_name, database)

     
if "__main__" == __name__:
    parser = setup_argparse()
    
    args = parser.parse_args()

    arg_dict = vars(args)

    if arg_dict.get('fields'):
        run_display_flags()
    else:
        main(arg_dict)