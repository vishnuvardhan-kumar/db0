# db0

### A single-table, in-memory, SQL-style database in 75 lines of Python3

[![asciicast](https://asciinema.org/a/305402.svg)](https://asciinema.org/a/305402)

## How to run:

Clone the repository: 

`$ git clone git_url`

Install dependencies:

`$ pip install -r db0/requirements.txt`

Run the db0 shell directly:

`$ python db0/db.py`

Or optionally, expose the db0 connection on a port of your choice:

`$ python db0/db.py 5000`

## Features:
- CLI Shell
- SQL-style command parser
- In-memory datastore
- Fully configurable table schema / datatypes
- Accessible over network if needed
- Pure Python3

## Dependencies:
- [tabulate](https://pypi.org/project/tabulate/) - for printing out the table neatly.

## Disclaimer:
This is purely a proof-of-concept and not a production database. Use it for any tasks at your own risk.