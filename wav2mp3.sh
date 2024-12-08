#!/bin/bash

for file in *.wav; do
	echo "$file"
	new="${file// /_}"
	new="${new//wav/mp3}" 
	ffmpeg -i "$file" -vn -ar 44100 -ac 2 -b:a 320k "$new"
	rm "$file"
done
