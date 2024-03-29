import sys
import argparse
import pandas as pd
from alm.lyrics import grammar_parser as gp
from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.comparator import evaluator
from alm.utils import io
from alm.api import spotify

def main():
    parser = argparse.ArgumentParser(description='This program calc word matched rates and tree similarities.')

    # 1曲づつの分析
    parser.add_argument(
        '-w', '--word_matched_rate',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--tree_similarity',
        action='store_true'
    )
    parser.add_argument(
        '-tpc', '--tree_similarity_by_parent_child',
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
        '-ws', '--word_matched_rates',
        action='store_true'
    )
    parser.add_argument(
        '-ts', '--tree_similarities',
        action='store_true'
    )
    parser.add_argument(
        '-tspc', '--tree_similarities_by_parent_child',
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
    parser.add_argument(
        '-o', '--output',
        help='output file path.'
    )

    # t検定
    parser.add_argument(
        '-ttest',
        action='store_true'
    )
    
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

    # csvの結合を行う
    parser.add_argument(
        '-mc', '--merge_csv',
        action='store_true'
    )
    parser.add_argument(
        '-cl', '--csv_list',
        help='list of csv path',
        nargs='*'
    )

    parser.add_argument(
        '-c', '--csv',
        help='csv path'
    )

    args = parser.parse_args()

    # csvの結合
    if args.merge_csv:
        merged_data = io.merge_csv_data(args.csv_list)
        merged_data.to_csv(f"merged_{args.csv_list[0]}")
        return

    # spotifyのpopularityを取得
    if args.spotify_popularity:
        res = spotify.get_popularity(args.spotify_id)
        print(res.name, res.popularity)
        return
    
    #spotifyのpopularityを複数取得
    if args.spotify_popularities:
        data = pd.read_csv(args.csv)
        res = spotify.get_popularities(data['spotify_id'])
        for item in res:
            print(item.name, item. popularity)
        return 

    # 複数の分析を一度に行う
    if args.word_matched_rates:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, wmrc.calc_word_matched_rate, args.output)
        return
    if args.tree_similarities:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, tsc.calc_tree_similarity, args.output)
        return
    if args.tree_similarities_by_parent_child:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, tsc.calc_tree_similarity_by_parent_child, args.output)
        return

    # 1曲づつ分析を行う
    grammar_parser = gp.GrammarParser("ja_ginza")

    if args.word_matched_rate:
        word_matched_rate = wmrc.calc_word_matched_rate(args.mscx_path, args.tstx_path, grammar_parser)
        word_matched_rate.print()
    elif args.tree_similarity:
        similarity = tsc.calc_tree_similarity(args.mscx_path, args.tstx_path, grammar_parser)
        similarity.print()
    elif args.tree_similarity_by_parent_child:
        similarity = tsc.calc_tree_similarity_by_parent_child(args.mscx_path, args.tstx_path, grammar_parser)
        similarity.print()

if __name__ == "__main__":
    sys.exit(main())
