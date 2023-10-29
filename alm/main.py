import sys
import argparse
from alm.lyrics import grammar_parser as gp
from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc

def main():
    parser = argparse.ArgumentParser(description='This program calc word matched rates and tree similarities.')
    parser.add_argument(
        'mode',
        help="'word-matched-rate' or 'tree-similarity'"
    )
    parser.add_argument(
        'mscx_path',
        help='MusicXML Path'
    )
    parser.add_argument(
        'tstx_path',
        help='Timespan Tree XML Path'
    )
    args = parser.parse_args()

    grammar_parser = gp.GrammarParser("ja_ginza")
    if args.mode == 'tree-similarity':
        similarity = tsc.calc_tree_similarity(args.mscx_path, args.tstx_path, grammar_parser)
        similarity.print()
    elif args.mode == 'word-matched-rate':
        word_matched_rate = wmrc.calc_word_matched_rate(args.mscx_path, args.tstx_path, grammar_parser)
        word_matched_rate.print()

if __name__ == "__main__":
    sys.exit(main())
