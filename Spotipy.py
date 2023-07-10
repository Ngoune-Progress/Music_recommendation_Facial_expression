import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

auth_manager = SpotifyClientCredentials('468151ea05dc423c94782a959f709ad1','58e07aa5ec8b4a979d56b488de19e7f5')
sp = spotipy.Spotify(auth_manager=auth_manager,requests_timeout=20, retries=20)

def getTrackAngry(val):
    track_ids = []
    audio_url = []

    playlist = sp.search(q=val,type=['track'],limit=40)
    # print(playlist)
    for item in playlist['tracks']['items']:
        # track = item['track']
        track_ids.append(item['id'])
        audio_url.append(item['external_urls']['spotify'])

    # for item in playlist['audiobooks']['items']:
    #     # track = item['track']
    #     audio_url.append(item['external_urls'])
    return track_ids,audio_url

def getTrackIDs(user, playlist_id):
    track_ids = []
    audio_url = []

    playlist = sp.search(q='year:2017',type=['track'],limit=40)
    # print(playlist)
    for item in playlist['tracks']['items']:
        # track = item['track']
        track_ids.append(item['id'])
        audio_url.append(item['external_urls']['spotify'])
        
    # for item in playlist['audiobooks']['items']:
    #     # track = item['track']
    #     audio_url.append(item['external_urls'])
    return track_ids,audio_url

def getTrackFeatures(id,uri):
    track_info = sp.track(id)

    name = track_info['name']
    album = track_info['album']['name']
    artist = track_info['album']['artists'][0]['name']
    url = uri[0]
    # release_date = track_info['album']['release_date']
    # length = track_info['duration_ms']
    # popularity = track_info['popularity']

    track_data = [name, album, artist,url] #, release_date, length, popularity
    return track_data

# Code for creating dataframe of feteched playlist

emotion_dict = {0:"Angry",1:"Disgusted",2:"Fearful",3:"Happy",4:"Neutral",5:"Sad",6:"Surprised"}
music_dist={0:"0l9dAmBrUJLylii66JOsHB?si=e1d97b8404e34343",1:"1n6cpWo9ant4WguEo91KZh?si=617ea1c66ab6446b ",2:"4cllEPvFdoX6NIVWPKai9I?si=dfa422af2e8448ef",3:"0deORnapZgrxFY4nsKr9JA?si=7a5aba992ea14c93",4:"4kvSlabrnfRCQWfN0MgtgA?si=b36add73b4a74b3a",5:"1n6cpWo9ant4WguEo91KZh?si=617ea1c66ab6446b",6:"37i9dQZEVXbMDoHDwVN2tF?si=c09391805b6c4651"}

'''
Code can def be modularised into a function but i tried to write it when i was extremely sleepy so thought screw it and repeated code block

Uncomment for fetching updated playlists
'''


track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=angry')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url'])
    df.to_csv('songs/angry.csv')
print("CSV Generated")

track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=disgusted')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/disgusted.csv')
print("CSV Generated")


track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=fearful')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/fearful.csv')
print("CSV Generated")

track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=happy')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/happy.csv')
print("CSV Generated")

track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=neutral')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/neutral.csv')
print("CSV Generated")

track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=sad')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/sad.csv')
print("CSV Generated")

track_ids,uri = getTrackAngry(val='remaster%2520track%3ADoxy%2520&genre=surprised')
track_list = []
for i in range(len(track_ids)):
    time.sleep(.6)
    track_data = getTrackFeatures(track_ids[i],uri=uri)
    track_list.append(track_data)
    df = pd.DataFrame(track_list, columns = ['Name','Album','Artist','Url']) # ,'Release_date','Length','Popularity'
    df.to_csv('songs/surprised.csv')
print("CSV Generated")