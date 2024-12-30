'''
File: discogs_id3_completer.py
Created Date: 30 Dec 2024
Author: Jake Skelton
Date Modified: Mon Dec 30 2024
Copyright (c): 2024 Jake Skelton
'''
import numpy as np
import pandas as pd
import discogs_client as dc
import time
from difflib import SequenceMatcher


def FuzzyMatch(s1: str, s2: str, threshold: float = 0.8) -> float:
    return (SequenceMatcher(None, s1, s2).ratio() > threshold)


def GetTrackNum(tracklist: list[dc.models.Track], tracktitle: str) -> int:
    for i in range(len(tracklist)):
        # TODO: Fuzzy match?
        if FuzzyMatch(tracklist[i].title, tracktitle):
            return i + 1
    raise ValueError("Input track title not found in tracklist")


infile = '../songs_with_ids.csv'

songs = pd.read_csv(infile, delimiter=',', index_col=0, on_bad_lines='warn',
                    dtype={'TrackArtist':'string',
                           'TrackTitle':'string',
                           'Album':'string',
                           'AlbumArtist':'string',
                           'TrackNum':'string',
                           'Year':'Int64',
                           'Genre':'string',
                           'Location':'string',
                           'ID':'Int64'})
hasid = songs[pd.notna(songs.ID)]
newentries = hasid.copy()
# TODO: Parse tracknums. Something like 3/4 should -> 3

with open('token.txt', 'r', newline='\n') as tokenfile:
    token = tokenfile.readline().rstrip()

cli = dc.Client('JakeSearch', user_token=token)
cli.backoff_enabled = True

idxs = hasid.index
for idx in idxs:
    print("\r%4d/%-4d"%(idx, len(songs)), end='')

    entry = songs.loc[idx]
    hit = cli.release(entry.ID)

    try:
        tracknum = str(GetTrackNum(hit.tracklist, entry.TrackTitle))
    except ValueError as err:
        print(err)
        # Can't match track title to release tracklist, skip
        newentries.loc[idx, 'ID'] = np.nan
        continue

    newentries.loc[
        idx, ['Album', 'AlbumArtist', 'TrackNum', 'Year', 'Genre']] = \
        [hit.title, hit.artists[0].name, tracknum, hit.year, hit.genres[0]]

    time.sleep(2)
