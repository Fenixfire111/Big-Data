# Converter
The utility is designed to convert from csv to parquet and convert from parquet to csv

## Functions
- csv to parquet conversion mode
- parquet to csv conversion mode
- getting file schema (list of attributes and their types)

## Tech
- The converter uses the following additional libraries:
- **pandas** is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,built on top of the Python programming language
- **fastparquet** is a Python interface to the Parquet file format.

## Installation
To install the required libraries run the following command
```sh
pip install -r requirements.txt
```

## Usage
For csv to parquet conversion mode:
```sh
python3 converter.py --csv2parquet <src-filename> <dst-filename>
```
 For parquet to csv conversion mode:
```sh
python3 converter.py --parquet2csv <src-filename> <dst-filename>
```
For getting file schema:
```sh
python3 converter.py --get-schema <filename>
```
For displaying help:
```sh
python3 converter.py --help
```

