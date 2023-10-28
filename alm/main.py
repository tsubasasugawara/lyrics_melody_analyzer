import sys
import argparse
from alm.lyrics import *
from alm.melody import *
from alm.comparator import *
from alm.utils import io

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        'integers',
        metavar='N',
        type=int,
        nargs='+',
        help='an integer for the accumulator'
    )
    parser.add_argument(
        '--sum',
        action='store_true',
        help='sum the integers (default: find the max)'
    )

    args = parser.parse_args()
    if args.sum:
        print(sum(args.integers))
    else:
        print(max(args.integers))

if __name__ == "__main__":
    sys.exit(main())