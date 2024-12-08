#!/bin/bash
outfile="songs.csv"
folder="$(pwd)"

# Check if outfile exists, if not create and add header
if ! [[ -e "$outfile" ]]; then
	printf '%s,%s,%s,%s,%s,%s,%s,%s\n' 'TrackArtist' 'TrackTitle' 'Album' \
	'AlbumArtist' 'TrackNum' 'Year' 'Genre' 'Location' > "$outfile"
fi

numfiles="$(ls *.mp3 | wc -l)"
# Main loop
i=1 
for file in *.mp3; do
	printf "File %4d of %4d" $i $numfiles 
	meta="$(id3v2 -l "$file")"

	trackartist="$(sed -nE 's/^TPE1[^:]+:\s(.*)/\1/p' <<< "$meta")"
	tracktitle="$(sed -nE 's/^TIT2[^:]+:\s(.*)/\1/p' <<< "$meta")"
	album="$(sed -nE 's/^TALB[^:]+:\s(.*)/\1/p' <<< "$meta")"
	albumartist="$(sed -nE 's/^TPE2[^:]+:\s(.*)/\1/p' <<< "$meta")"
	tracknum="$(sed -nE 's/^TRCK[^:]+:\s(.*)/\1/p' <<< "$meta")"
	year="$(sed -nE 's/^TYER[^:]+:\s(.*)/\1/p' <<< "$meta")"
	genre="$(sed -nE 's/^TCON[^:]+:\s(.*)/\1/p' <<< "$meta")"

	if [[ -z "$trackartist" ]]; then
		# ID3 tag empty, use album artist unless various
		if [[ ! -z "$albumartist" ]] && [[ ! "$albumartist" =~ .*arious.* ]]; then
			trackartist="$albumartist"
		else
		# Album artist not suitable, use file name
		trackartist="$(sed -nE 's/(.*)\s[–|-].*/\1/p' <<< "$file")"
		fi
	fi

	if [[ -z "$tracktitle" ]] || [[ "$tracktitle" =~ .*"$albumartist".* ]]; then
		# Track title empty or includes artist name, use file name
		tracktitle="$(sed -nE 's/.*[–|-]\s(.*)\.mp3/\1/p' <<< "$file")"
	fi

	printf '%s,%s,%s,%s,%s,%s,%s,%s\n' "$trackartist" "$tracktitle" "$album" \
	"$albumartist" "$tracknum" "$year" "$genre" "$folder/$file" >> "$outfile"

	printf '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b'
	(( i++ ))
done
