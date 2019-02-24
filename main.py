import spotipy
import os
import sys
import json
import eyed3
import spotipy.util as util
from bottle import route, run, request
from spotipy import oauth2
from eyed3 import id3
from json.decoder import JSONDecodeError
from userCredentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

PORT_NUMBER = 8080
SPOTIPY_REDIRECT_URI = "http://google.com/"
SCOPE = 'playlist-modify-private,playlist-modify-public'
CACHE = '.spotipyoauthcache'


#tag = id3.Tag()
def scrapeDir(dir):
    directory = os.listdir(dir)
    for x in directory:
        audiofile = eyed3.load(dir + "/" + x)
        print(audiofile.tag.artist)
        print(audiofile.tag.title)

#scope = 'user-library-read'
username = ""
while True:
    print()
    print(">>> Welcome to Spotipy!")
    print("Would you like to create a new playlist?")
    print("0 - Yes")
    print("1 - No")
    print()
    choice = input("Your choice: ")
    if choice == "0":
        username = input("Please enter your username: ")
        print()
        dir = input("Ok, enter the directory of your playlist: ")
        print()
        playlistName = input("What would you like to call your playlist?: ")
        print()
        break
    else:
        break




#User ID 1130282094

#Erase cache and prompt
try:
    token = util.prompt_for_user_token(username, client_id = SPOTIPY_CLIENT_ID,
    client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri= SPOTIPY_REDIRECT_URI, scope=SCOPE)

except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI= SPOTIPY_REDIRECT_URI, scope=SCOPE)

#spotify object
sp = spotipy.Spotify(auth=token)

playlist = sp.user_playlist_create(username, playlistName)

uri = playlist["uri"]
index = uri.find("playlist:") + 9
playlistID = uri[index:]

def makePlaylist(dir):
    directory = os.listdir(dir)
    counter = 0
    track = []
    unadded = []
    repetition = len(directory) // 100 + 1
    while counter < repetition:
        idx = 0
        x = 0
        while idx < 100 and x < len(directory):
            audiofile = eyed3.load(dir + "/" + directory[x])
            artist = audiofile.tag.artist.rsplit(";")[0]
            artist = artist.rsplit(",")[0]
            title = audiofile.tag.title
            if "'" in title:
                title = title.replace("'", "")
            query = "artist:" + artist + " track:" + title
            print (title)

            if query.find("(f") != -1:
                temp = query.rsplit("(f")
                query = temp[0]
            elif query.find("(F") != -1:
                temp = query.rsplit("(F")
                query = temp[0]
            elif query.find("feat.") != -1:
                temp = query.rsplit("feat.")
                query = temp[0]
            elif query.find("(Album") != -1:
                temp = query.rsplit("(Album")
                query = temp[0]
            elif query.find("Version") != -1:
                temp = query.rsplit("Version")
                query = temp[0]
            elif query.find("Feat.") != -1:
                temp = query.rsplit("Feat.")
                query = temp[0]
            result= sp.search(q=query, limit = 1, type='track')
            if len(result["tracks"]["items"]) > 0:
                trackID = result["tracks"]["items"][-1]["uri"]
                track.append(trackID)
            else:
                unadded.append(query)
            x += 1
            idx += 1
        sp.user_playlist_add_tracks(username, playlistID, track, position=None)
        directory = directory[100:]
        track= []
        counter += 1
    if len(unadded) != 0:
        print ("These/This " + str(len(unadded)) + " song were/was not added to your playlist")
        print(unadded)
makePlaylist(dir)
