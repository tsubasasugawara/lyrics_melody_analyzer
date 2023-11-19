import sys
import argparse
from alm.lyrics import grammar_parser as gp
from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.analyzer import analyzer

def main():
    parser = argparse.ArgumentParser(description='This program calc word matched rates and tree similarities.')

    parser.add_argument(
        '-t', '--tree_simiarity',
        action='store_true'
    )
    parser.add_argument(
        '-w', '--word_match-_ate',
        action='store_true'
    )

    parser.add_argument(
        '-mp', '--mscx_path',
        help='MusicXML Path'
    )
    parser.add_argument(
        '-tp', '--tstx_path',
        help='Timespan Tree XML Path'
    )

    #TODO: t検定のオプション追加
    #TODO: spotifyのpopularity取得オプション追加

    args = parser.parse_args()

    grammar_parser = gp.GrammarParser("ja_ginza")
    if args.tree_similarity:
        similarity = tsc.calc_tree_similarity(args.mscx_path, args.tstx_path, grammar_parser)
        similarity.print()
    elif args.word_matched_rate:
        word_matched_rate = wmrc.calc_word_matched_rate(args.mscx_path, args.tstx_path, grammar_parser)
        word_matched_rate.print()

if __name__ == "__main__":
    sys.exit(main())
