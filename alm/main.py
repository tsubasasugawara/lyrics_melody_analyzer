import sys
import argparse
import pandas as pd
from alm.lyrics import grammar_parser as gp
from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.api import spotify

def main():
    parser = argparse.ArgumentParser(description='This program calc word matched rates and tree similarities.')

    # 1曲づつの分析
    parser.add_argument(
        '-w', '--word_match_rate',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--tree_similarity',
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
    
    # 複数曲の分析
    parser.add_argument(
        '-ws', '--word_match_rates',
        action='store_true'
    )
    parser.add_argument(
        '-ts', '--tree_similarities',
        action='store_true'
    )
    parser.add_argument(
        '-md', '--mscx_dir',
        help='MusicXML dir'
    )
    parser.add_argument(
        '-td', '--tstree_dir',
        help='Timespan Tree XML dir'
    )

    #TODO: t検定のオプション追加

    #TODO: youtubeの再生回数取得オプション追加

    # spotifyのpopularity取得
    parser.add_argument(
        '-sp', '--spotify_popularity',
        action='store_true'
    )
    parser.add_argument(
        '-i', '--spotify_id',
        help='Track ID'
    )

    # spotifyのpopularityを複数取得
    parser.add_argument(
        '-sps', '--spotify_popularities',
        action='store_true'
    )
    parser.add_argument(
        '-c', '--spotify_id_csv',
        help='Track id csv'
    )

    args = parser.parse_args()

    # spotifyのpopularityを取得
    if args.spotify_popularity:
        res = spotify.get_popularity(args.spotify_id)
        print(res.name, res.popularity)
        return
    
    #spotifyのpopularityを複数取得
    if args.spotify_popularities:
        data = pd.read_csv(args.spotify_id_csv)
        res = spotify.get_popularities(data['spotify_id'])
        for item in res:
            print(item.name, item. popularity)
        return 

    # 複数の分析を一度に行う
    if args.word_match_rates:
        wmrc.calc_word_matched_rates(args.mscx_dir, args.tstree_dir)
        return
    if args.tree_similarities:
        tsc.calc_tree_similarities(args.mscx_dir, args.tstree_dir)
        return

    # 1曲づつ分析を行う
    grammar_parser = gp.GrammarParser("ja_ginza")
    if args.tree_similarity:
        similarity = tsc.calc_tree_similarity(args.mscx_path, args.tstx_path, grammar_parser)
        similarity.print()
    elif args.word_matched_rate:
        word_matched_rate = wmrc.calc_word_matched_rate(args.mscx_path, args.tstx_path, grammar_parser)
        word_matched_rate.print()

if __name__ == "__main__":
    sys.exit(main())
