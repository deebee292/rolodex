# Rolodex

Rolodex is a very simple in-memory toy database that seeks to look at:

* Implementing a Factory Pattern via Interfaces (Protocol) for reading file formats
  * CSV
  * JSON
  * YAML
* Implementing a Factory Pattern via Interfaces (Protocol) for writing file formats
  * CSV
  * JSON
  * YAML

The code based leans to a more functional data structure development style. It is simple, but should offer flexibilty for simple expansion and maintenence.


## Dev Environment

* Linux (Debian 12)
* Python (3.11)
  * requirements.txt file for any additions (ex: yaml)
  * unittest
    * "run_tests.sh" for easy test runs
  * venv
    * "run_setup_venv.sh" for setup
* UnitTesting (unittest)

## Command-line Usage

Various examples of using the commandline

```
# Create a one entry file myfile.csv
./rdex.sh --file_out myfile.csv --add name='bob' address='123 Somewhere' phone_number='555-123-4567'

# Read from then write to myfile.csv adding an entry for 'alice'
./rdex.sh --file_in myfile.csv --file_out myfile.csv --add name='alice' address='345 Somewhere' phone_number='555-555-5555'

# Display data within the myfile.csv
./rdex.sh --file_in myfile.csv --display

# Display data within the myfile.csv as a yaml
./rdex.sh --file_in myfile.csv --display --display_format yaml

# Preform a filter and display the result (note: this does nothing to the loaded file)
./rdex.sh --file_in myfile.csv --filter name='bob' --display

# Preform a file format conversion CSV->YAML
./rdex.sh --file_in myfile.csv --file_out myfile.yaml

# Preform a filter operation and write that to myfile_filtered.yaml
./rdex.sh --file_in myfile.csv --file_out myfile_filtered.yaml --filter name="alice"

# Get some information on the fields supported by both ADD and FILTER
./rdex.sh info --fields
```

## Author / Other
The code is provided AS-IS and is not intended for anything other than demonstration / learning.
Please feel free to give comment or feedback.

Find me at deebee262 on github
