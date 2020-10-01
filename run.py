import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv
from urilist import uri_list

client_id = 'your-client-id-here'
client_secret = 'your-client-secret-here'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#establish dataframe

schema = {'URI':[],'playlist_title':[],'track_title':[],'artist_name':[]}
tracker = pd.DataFrame(schema)

#run the code

for URI in uri_list:
    p_list = sp.playlist(URI)
    p_list_title = p_list['name']
    p_list_tracks = sp.playlist_tracks(URI)
    p_list_items = p_list_tracks['items']
    track_no = list(range(0,len(p_list_items)))

    for x in track_no:
        track_title = p_list_items[x]['track']['name']
        artist_name = ''

        if len(p_list_items[x]['track']['artists']) > 1:
            artist_no = list(range(0,len(p_list_items[x]['track']['artists'])))
            for y in artist_no:
                if y == 0:
                    artist_name = p_list_items[x]['track']['artists'][y]['name']
                else:
                    artist_name = artist_name + ', ' + p_list_items[x]['track']['artists'][y]['name']
        else:
            artist_name = p_list_items[x]['track']['artists'][0]['name']

        newdata = {'URI':URI,'playlist_title':p_list_title,'track_title':track_title,'artist_name':artist_name}
        tracker = tracker.append(newdata, ignore_index = True)

#export dataframe

tracker.to_csv('playlist-contents.csv', index=False)
