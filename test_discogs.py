'''
File: test_discogs.py
Created Date: 10 Dec 2024
Author: Jake Skelton
Date Modified: Mon Dec 23 2024
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
cli.backoff_enabled = True

# For example
idxs = noalbum.index
for idx in idxs:
    entry = noalbum.loc[idx]
    res = cli.search(track=entry.TrackTitle,
                     artist=entry.TrackArtist,
                     type='master').page(1)
    numresults = len(res)
    if numresults:
        first = res[0].main_release
        album = first.title
        albumartist = first.artists[0].name  # TODO: Right choice?
        year = first.year
        # Modify dataframe in-place
        # TODO: Check populated before overwrite?
        noalbum.loc[idx, ['Album', 'AlbumArtist', 'Year']] = \
            [album, albumartist, year]
    else:
        album = '-'

    # TODO: Add progress counter
    print("%-50s : %50s"%(entry.TrackArtist + ' - ' + entry.TrackTitle, album))

    time.sleep(2)
