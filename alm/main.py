import sys
import argparse
import pandas as pd
from alm.lyrics import grammar_parser as gp
from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.comparator import evaluator
from alm.utils import io
from alm.api import spotify
from alm.analyzer import ttest

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

    parser.add_argument(
        '-w1', '--weight1',
        action='store_true'
    )
    parser.add_argument(
        '-w2', '--weight2',
        action='store_true'
    )
    parser.add_argument(
        '-w3', '--weight3',
        action='store_true'
    )
    parser.add_argument(
        '-w4', '--weight4',
        action='store_true'
    )
    parser.add_argument(
        '-w5', '--weight5',
        action='store_true'
    )
    parser.add_argument(
        '-w6', '--weight6',
        action='store_true'
    )
    parser.add_argument(
        '-w7', '--weight7',
        action='store_true'
    )
    parser.add_argument(
        '-w8', '--weight8',
        action='store_true'
    )
    parser.add_argument(
        '-w9', '--weight9',
        action='store_true'
    )
    parser.add_argument(
        '-w10', '--weight10',
        action='store_true'
    )
    parser.add_argument(
        '-w11', '--weight11',
        action='store_true'
    )
    parser.add_argument(
        '-w12', '--weight12',
        action='store_true'
    )
    parser.add_argument(
        '-w13', '--weight13',
        action='store_true'
    )
    parser.add_argument(
        '-w14', '--weight14',
        action='store_true'
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

    # t検定を行う
    if args.ttest:
        res = None

        if args.word_matched_rate:
            res = ttest.ttest_word_matched_rate(args.csv)
        if args.tree_similarity:
            res = ttest.ttest_tree_similarity(args.csv)

        if res != None:
            print(f"youtube:{res[0]}")
            print(f"spotify:{res[1]}")

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

    weighting_func = evaluator.weight0
    if args.weight1:
        weighting_func = evaluator.weight1
    elif args.weight2:
        weighting_func = evaluator.weight2
    elif args.weight3:
        weighting_func = evaluator.weight3
    elif args.weight4:
        weighting_func = evaluator.weight4
    elif args.weight5:
        weighting_func = evaluator.weight5
    elif args.weight6:
        weighting_func = evaluator.weight6
    elif args.weight7:
        weighting_func = evaluator.weight7
    elif args.weight8:
        weighting_func = evaluator.weight8
    elif args.weight9:
        weighting_func = evaluator.weight9
    elif args.weight10:
        weighting_func = evaluator.weight10
    elif args.weight11:
        weighting_func = evaluator.weight11
    elif args.weight12:
        weighting_func = evaluator.weight12

    # 複数の分析を一度に行う
    if args.word_matched_rates:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, wmrc.calc_word_matched_rate, evaluator.weight0, args.output)
        return
    if args.tree_similarities:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, tsc.calc_tree_similarity, evaluator.weight0, args.output)
        return
    if args.tree_similarities_by_parent_child:
        evaluator.evaluate(args.mscx_dir, args.tstree_dir, tsc.calc_tree_similarity_by_parent_child, weighting_func, args.output)
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
        similarity = tsc.calc_tree_similarity_by_parent_child(args.mscx_path, args.tstx_path, grammar_parser, weighting_func)
        similarity.print()

if __name__ == "__main__":
    sys.exit(main())
