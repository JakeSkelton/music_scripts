'''
File: discogs_associate.py
Created Date: 30 Dec 2024
Author: Jake Skelton
Date Modified: Mon Dec 30 2024
Copyright (c): 2024 Jake Skelton
'''
import numpy as np
import pandas as pd
import discogs_client as dc
import time


def RobustPageFetch(results: list) -> dc.models.Release:
    try:
        return results[0].main_release
    except IndexError:
        return None
    except dc.exceptions.HTTPError:
        return RobustPageFetch(results[1:])


infile = '../songs.csv'
outfile = '../songs_with_ids.csv'

songs = pd.read_csv(infile, delimiter=',', dtype="string", on_bad_lines='warn')
hastags = songs[pd.notna(songs.TrackTitle)]
idxs = hastags.index
songs = songs.join(pd.Series(np.nan, songs.index, name="ID", dtype="Int64"))

with open('token.txt', 'r', newline='\n') as tokenfile:
    token=tokenfile.readline().rstrip()

cli = dc.Client('JakeSearch', user_token=token)
cli.backoff_enabled=True


for idx in idxs:
    print("\r%4d/%-4d"%(idx, len(songs)), end='')

    entry = hastags.loc[idx]
    res = cli.search(track=entry.TrackTitle,
                     artist=entry.TrackArtist,
                     type='master').page(1)
    first = RobustPageFetch(res)

    if first:
        # Not None, empty, etc
        songs.loc[idx, 'ID'] = first.id
    else:
        continue

    # Write to outfile every 20 entries
    if not (idx%20):
        songs.iloc[:idx].to_csv(outfile)

    time.sleep(2)
