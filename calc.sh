#!/bin/sh

python alm/main.py -ws -md xmls/mscx/ヨルシカ/ -td xmls/tstree/ヨルシカ -o "csv/ヨルシカ_wmr_20231119.csv"
python alm/main.py -ts -md xmls/mscx/ヨルシカ/ -td xmls/tstree/ヨルシカ -o "csv/ヨルシカ_ts_20231119.csv"
python alm/main.py -tspc -md xmls/mscx/ヨルシカ/ -td xmls/tstree/ヨルシカ -o "csv/ヨルシカ_tspc_20231119.csv"

python alm/main.py -ws -md xmls/mscx/GReeeeN/ -td xmls/tstree/GReeeeN -o "csv/GReeeeN_wmr_20231119.csv"
python alm/main.py -ts -md xmls/mscx/GReeeeN/ -td xmls/tstree/GReeeeN -o "csv/GReeeeN_ts_20231119.csv"
python alm/main.py -tspc -md xmls/mscx/GReeeeN/ -td xmls/tstree/GReeeeN -o "csv/GReeeeN_tspc_20231119.csv"

for i in `seq 1 14`
do
    python alm/main.py -tspc -md xmls/mscx/ヨルシカ/ -td xmls/tstree/ヨルシカ -o "csv/ヨルシカ_tspc_w"$i"_20231119.csv" -w$i
    python alm/main.py -tspc -md xmls/mscx/GReeeeN/ -td xmls/tstree/GReeeeN -o "csv/GReeeeN_tspc_w"$i"_20231119.csv" -w$i
done
