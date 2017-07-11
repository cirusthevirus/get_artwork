# get_artwork.py
## Desription
Small script that uses the discogs client API to download artist artwork to use as covers for mp3 files. Note that the script does not search for the actual cover of the song but rather only for the 'profile picture' of the primary artist. This is due to the fact that most of my songs are remixes that are never officially released and hence do not have cover art stored on discogs. Moreover, note that to obtain the name of the primary artist, the file name is split according to the format 'artist - song_name.mp3'. This is to conform with my other music handling scripts. Moreover, if the artist name contains an ampersand or comma, it will be split.
In order to save the artwork as ID3 tags, the mutagen module is used.
