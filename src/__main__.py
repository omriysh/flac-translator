from importlib.resources import path
import os
import shutil
from googletrans import Translator
from mutagen.flac import FLAC
from tqdm import tqdm


TAGS_TO_TRANSLATE = ["TITLE", "ALBUM", "ARTIST"]


def get_albums(path='.'):
    '''
    Return relative paths to directories containing songs.
    '''
    is_album = True

    albums = []
    current_dir = [os.path.join(path, entry) for entry in os.listdir(path)]
    for entry in current_dir:
        if os.path.isdir(entry):
            albums += get_albums(entry)
            is_album = False

    if is_album:
        albums += [path]
    
    return albums

def translate_song_metadata(path):
    '''
    Receive a path to a song, and translates its FLAC metadata.
    '''
    song = FLAC(path)
    t = Translator()

    for t in TAGS_TO_TRANSLATE:
        if t in song.tags:
            for i in range(len(song[t])):
                song[t][i] = t.translate(song[t][i])
    
    song.save()

def translate_album(path):
    '''
    Creates a new directory that will contain the translated album.
    '''
    t = Translator()

    # start by creating the new directory
    album_name = os.path.basename(path)
    album_location = os.path.dirname(path)
    translated_album_name = t.translate(album_name).text
    translated_path = os.path.join(album_location, translated_album_name)
    os.mkdir(translated_path)

    # now fill the directory with translated songs
    print("> Translating", album_name, "into", translated_album_name)
    for song in tqdm(os.listdir(path)):
        translated_song_path = os.path.join(translated_path, t.translate(song).text)
        shutil.copy(os.path.join(path, song), translated_song_path)
        translate_song_metadata(translated_song_path)

def main():
    print("getting albums..")
    albums = get_albums()

    print ("translating albums...")
    for album in tqdm(albums):
        translate_album(album)
    

if __name__ == "__main__":
    main()