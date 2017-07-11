#!/usr/bin/env python3
'''Imports artwork for astists in specified source directory.
'''

import per_tools as pt
import discogs_client as dc
from discogs_client.exceptions import HTTPError
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, error
import webbrowser
import sys
import os
import re

def run():
    # AUTHENTICATION
    consumer_key = 'you_consumer_key'
    consumer_secret = 'you_consumer_secret'
    # You will receive these when registring an application on the discogs
    # website
    user_agent = 'get_artwork/1.0'

    ds = dc.Client(user_agent)
    ds.set_consumer_key(consumer_key, consumer_secret)
    token, secret, url = ds.get_authorize_url()

    webbrowser.open_new(url)

    oauth_verifier = input('Verification code: ')
    try:
        access_token, access_secret = ds.get_access_token(oauth_verifier)
    except HTTPError:
        print('Unable to authenticate.')
        sys.exit(1)

    # AUTHENTICATION END


    # Scan files from input
    os.chdir(source_dir)
    files = [f for f in os.listdir('.') if f[-4:] == ".mp3"]

    # Set up progress bar
    print("Preparing for file image writing ...")
    iteration = 0
    pt.print_progress_bar(iteration, len(files))

    for file in files:
        tmp_file = MP3(file, ID3=ID3)

        # try add missing tags
        try:
            tmp_file.add_tags()
        except error:
            pass

        # Get artist name
        artist = re.split(' - ', file)[0].strip()
        artist = re.split(' x ', artist)[0].strip()
        artist = re.split(',', artist)[0].strip()
        artist = re.split('&', artist)[0].strip()
        artist = re.split('\(', artist)[0].strip()
        artist = re.split('ft.', artist)[0].strip()

        results = ds.search(artist, type='artist')

        try:
            try:
                image = results[0].images[0]['uri']
                _type = image.split('.')[-1]
                content, resp = ds._fetcher.fetch(None, 'GET', image,
                            headers={'User-agent': ds.user_agent})
            except:
                image = results[1].images[0]['uri']
                _type = image.split('.')[-1]
                content, resp = ds._fetcher.fetch(None, 'GET', image,
                            headers={'User-agent': ds.user_agent})
            tmp_file.tags.add(
                APIC(
                    encoding=3,
                    mime='image/'+_type,
                    type=0,
                    desc=u'Cover',
                    data=content
                )
            )
            tmp_file.save()
        except:
            pass

        # Increase progress bar
        iteration += 1
        pt.print_progress_bar(iteration, len(files))

    print('Process complete')


if __name__ == '__main__':
    save_dir = os.getcwd()
    source_dir = "/path/to/music/directory"
    print('Working with source: %s\n' % source_dir)
    run()
    os.chdir(save_dir)
