'''
File: discogs_id3_completer.py
Created Date: 30 Dec 2024
Author: Jake Skelton
Date Modified: Mon Dec 30 2024
Copyright (c): 2024 Jake Skelton
'''
import pandas as pd
import discogs_client as dc
import time


songs = pd.read_csv('../songs.csv', delimiter=',', on_bad_lines='warn')
noalbum = songs[pd.isna(songs.Album) * pd.notna(songs.TrackTitle)]

with open('token.txt', 'r', newline='\n') as tokenfile:
    token = tokenfile.readline().rstrip()

cli = dc.Client('JakeSearch', user_token=token)
cli.backoff_enabled = True

idxs = noalbum.index
for idx in idxs:
    entry = songs.loc[idx]
    res = cli.search(track=entry.TrackTitle,
                     artist=entry.TrackArtist,
                     type='master').page(1)
    numresults = len(res)
    if numresults:
        first = res[0].main_release
        # Album
        album = first.title
        albumartist = first.artists[0].name  # TODO: Right choice?
        songs.loc[idx, ['Album', 'AlbumArtist']] = [album, albumartist]
        # Year (in none already)
        if pd.isna(entry.Year):
            songs.loc[idx, 'Year'] = first.year
        # Genre
    else:
        album = '-'

    # TODO: Add progress counter
    print("%4d/%-4d %-50s : %-s"%(
        idx, len(songs), entry.TrackArtist + ' - ' + entry.TrackTitle, album))

    time.sleep(2)
