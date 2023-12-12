#!/bin/sh

for i in `seq 1 14`
do
    python alm/main.py -tspc -md xmls/mscx/ヨルシカ/ -td xmls/tstree/ヨルシカ -o "csv/ヨルシカ_tspc_w"$i"_20231119.csv" -w$i
    python alm/main.py -tspc -md xmls/mscx/GReeeeN/ -td xmls/tstree/GReeeeN -o "csv/GReeeeN_tspc_w"$i"_20231119.csv" -w$i
done
