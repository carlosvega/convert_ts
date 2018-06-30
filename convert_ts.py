#!/usr/bin/python
from __future__ import print_function
import time, datetime, sys, argparse, logging, os, fileinput
from argparse import RawTextHelpFormatter

os.environ['TZ'] = 'GMT' #oddly faster with GMT :-O

date_format = '%d/%m/%Y:%H.%M.%S'

def parse_args():
    global date_format
    description = """
       _~
    _~ )_)_~
    )_))_))_)
    _!__!__!_
    \_______/
  ~~~~~~ ~~~~~~
  ~~ ~~~~  ~~~~
   Carlos Vega
    14/09/17
      v1.0

Timestamp Converter.

Execute with pypy for better performance
"""
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', required=False, default='-', help='Input file. Default: stdin')
    parser.add_argument('-o', '--output', dest='output', required=False, type=argparse.FileType('w'), default=sys.stdout, help='Output file. It will use the same separator. Default stdout')
    parser.add_argument('-s', '--separator', dest='separator', required=False, default=';', help='File Separator. Default: Semicolon ";"')
    parser.add_argument('-t', '--ts_column', dest='ts_column', nargs='+', required=False, type=int, default=[0], help='Number or list of numbers of the columns with timestamps. Default 0.')
    parser.add_argument('-x', '--exclude', dest='exclude', nargs='+',  required=False, type=int, default=[], help='List of numbers starting in 0 of the columns to be excluded. Default: none. If a column appears in both include and exclude it will be excluded')
    parser.add_argument('-z', '--include', dest='include',  nargs='+',  required=False, type=int, default=[], help='List of numbers starting in 0 of the columns to be included. Default all, except those excluded with the parameter -x.')
    parser.add_argument('--start', dest='start', type=int, required=False, default=None, help='Filter output by time range. This parameter indicates the min timestamp IN SECONDS. Default: None')
    parser.add_argument('--main_ts', dest='main_ts', type=int, required=False, default=0, help='Which of the given timestamp columns is the main ts? By the fault it will be the first number provided in option -t.')
    parser.add_argument('--end', dest='end', type=int, required=False, default=None, help='Filter output by time range. This parameter indicates the min timestamp IN SECONDS. Default: None')
    parser.add_argument('-f', '--ts_format', dest='ts_format',  nargs='+',  default=date_format, required=False, help="Indicate the date format. Default: %s" % date_format.replace(r"%", r"%%"))
    parser.add_argument('--ms', dest='ms', default=False, action='store_true', help='Prints the converted timestamps in miliseconds, otherwise are printed in seconds.')
    parser.add_argument('--version', dest='version', default=False, action='store_true', help="Prints the program version.")
    parser.add_argument('--where', dest='where', default='GMT', help="Where the timestamps come from? By default we assume GMT.")

    args = parser.parse_args()

    if args.version:
        logging.info('Timestamp Converter v0.1')
        sys.exit()

    os.environ['TZ'] = args.where

    return args

# Initialization of parameters
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
args = parse_args()

# Returns false if the column is included in the excluded list or if it's included in the included list
#    Returns true if the column is not included in the excluded list or if it's included in the included list
#    Additionally returns true if the both lists are empty
def column_is_included(i, included, excluded):
        if len(excluded) > 0 and i in excluded:
                return False
        if len(included) > 0 and i not in included:
                return False
        return True

# Checks if timestamp is in range. If start and end are None, return True
def timestamp_in_range(ts, start, end):
        if start is not None and start > ts:
                return False
        if end is not None and end < ts:
                return False
        return True

# This function converts the given string to an epoch timestamp in milliseconds
def convert_ts_single(string, date_format):
        return int(time.mktime(datetime.datetime.strptime(string, date_format).timetuple()))

# This function converts the given string to an epoch timestamp in milliseconds trying multiple formats
def convert_ts_multi(string, date_formats):
        for fmt in date_formats:
            try:
               return int(time.mktime(datetime.datetime.strptime(string, fmt).timetuple()))
            except:
                continue
        raise ValueError

# def convert_ts_single(string, date_format):

convert_ts = convert_ts_multi if isinstance(args.ts_format, list) else convert_ts_single

# MAIN PROGRAM
ctr=0
for line in fileinput.input(args.input):
        next_line = False
        o_line = line
        ctr+=1
        line = line.rstrip().split(args.separator)
        # Convert the columns in args.ts_column to timestamp
        try:
            for column in args.ts_column:
                line[column] = convert_ts(line[column], args.ts_format)
                if column == args.ts_column[args.main_ts] and not timestamp_in_range(line[column], args.start, args.end):
                    next_line = True
                elif args.ms:
                    line[column] = line[column]*1000
        except Exception as e:
            logging.warn('Error converting column {} ({}) from line number {}. Ignoring entire line: {}'.format(column, line[column], ctr, o_line))
            continue

        if next_line:
            continue
        # Remove the columns the user wants to exclude and convert to string
        line = [str(c) for i,c in enumerate(line) if column_is_included(i, args.include, args.exclude)]
        line = args.separator.join(line)
        print(line, file=args.output)

