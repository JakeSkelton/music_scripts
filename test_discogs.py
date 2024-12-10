'''
File: test_discogs.py
Created Date: 10 Dec 2024
Author: Jake Skelton
Date Modified: Tue Dec 10 2024
Copyright (c): 2024 Jake Skelton
'''

import pandas as pd
import discogs_client as dc
import time

songs = pd.read_csv('../songs.csv', delimiter=',', on_bad_lines='warn')
noalbum = songs[pd.isna(songs.Album)]

with open('token.txt', 'r', newline='\n') as tokenfile:
    token = tokenfile.readline().rstrip()

cli = dc.Client('JakeSearch', user_token=token)

# For example
for i in range(len(noalbum)):
    entry = noalbum.iloc[i]
    res = cli.search(track=entry.TrackTitle,
                     artist=entry.TrackArtist,
                     type='master').page(1)
    numresults = len(res)
    if numresults:
        first = res[0].main_release
        album = first.title
    else:
        album = '-'

    print("%-50s : %50s"%(entry.TrackArtist + ' - ' + entry.TrackTitle, album))

    time.sleep(1)
