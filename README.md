# Lyrics Melody Analyzer

## Calculate Word Matched Rate
```
$ python alm/main.py -w -mp 'MusicXML Path' -tp 'Timespan Tree XML Path'
```

## Calculate Word Matched Rates
```
$ python alm/main.py -ws -md 'MusicXML dir' -td 'Timespan Tree XML dir'
```

## Calculate Tree Similarity by subtree count
```
$ python alm/main.py -t -mp 'MusicXML Path' -tp 'Timespan Tree XML Path'
```

## Calculate Tree Similarity by parent child
```
$ python alm/main.py -tpc -mp 'MusicXML Path' -tp 'Timespan Tree XML Path'
```

## Calculate Tree Similarities by subtree count
```
$ python alm/main.py -ts -md 'MusicXML dir' -td 'Timespan Tree XML dir'
```

## Calculate Tree Similarities by parent child
```
$ python alm/main.py -tspc -md 'MusicXML dir' -td 'Timespan Tree XML dir'
```

## Get Spotify popularity
```
$ python alm/main.py -sp -i 'Spotify Track ID'
```

## Get Spotify popularities
```
$ python alm/main.py -sps -c 'CSV Path'
```

## Merge CSV
```
$ python alm/main.py -mc -cl 'CSV Paths'
```

## t-test
```
$ python alm/main.py -ttest -c 'CSV File Path'
```