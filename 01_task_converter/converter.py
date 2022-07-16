import argparse
import os
import sys

import pandas as pd


def create_arg_parser():
    """create a parser to process command line arguments"""
    arg_parser = argparse.ArgumentParser(description='The utility is intended:\n'
                                                     '1) to convert from csv to parquet\n'
                                                     '2) to convert from parquet to csv')
    arg_parser.add_argument('--csv2parquet', nargs=2,
                            metavar=('<src-filename>', '<dst-filename>'),
                            help='converts csv file to parquet file')

    arg_parser.add_argument('--parquet2csv', nargs=2,
                            metavar=('<src-filename>', '<dst-filename>'),
                            help='converts parquet file to csv file')

    arg_parser.add_argument('--get-schema', nargs=1,
                            metavar='<filename>',
                            help='prints the schema of a file')

    return arg_parser


class Parser:

    def csv_to_parquet(self, name_csv, name_parquet):
        """convert from csv to parquet"""
        df = pd.read_csv(name_csv, encoding='utf8')
        df.to_parquet(name_parquet, index=False)

    def parquet_to_csv(self, name_parquet, name_csv):
        """convert from parquet to csv"""
        df = pd.read_parquet(name_parquet, encoding='utf8')
        df.to_csv(name_csv, index=False)

    def get_schema(self, filename):
        """prints the schema of a file"""
        path, file_extension = os.path.splitext(filename)
        if file_extension == '.parquet':
            df = pd.read_parquet(filename, encoding='utf8')
            print(df.dtypes)
        else:
            df = pd.read_csv(filename, encoding='utf8')
            print(df.dtypes)


def execution():
    """selects the correct action depending on the input data"""
    try:
        if args.csv2parquet:
            parser.csv_to_parquet(*args.csv2parquet)
        elif args.parquet2csv:
            parser.parquet_to_csv(*args.parquet2csv)
        elif args.get_schema:
            parser.get_schema(*args.get_schema)
        else:
            arg_parser_.print_help()
    except Exception:
        sys.stderr = open('errors.txt', 'w')
        sys.stderr.write('the program ended incorrectly')
        print('the program ended incorrectly')
        sys.stderr.close()


if __name__ == '__main__':
    arg_parser_ = create_arg_parser()
    args = arg_parser_.parse_args()

    parser = Parser()
    execution()

