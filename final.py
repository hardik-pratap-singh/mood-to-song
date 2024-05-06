import json
import spotipy
import requests
import random
import pygame
import tempfile
import os

#Old
# clientID = '3c46ae9e8c8e4863b2de9c8b261d45e1'
# clientSecret = '2aa36f60e4d348fc8ebd16032dfc2fb6'


#New
clientID = '2cb50359dded48f4b3d7f32d6df3b86c'
clientSecret = '9c932fa3cb784419b641c85ed2c4163d'

redirect_uri = 'http://localhost:8400/'

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)

# this is access token
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

# this is a spotify object 
spotifyObject = spotipy.Spotify(auth=token)

# this will give user information 
user_name = spotifyObject.current_user()

# # To print the JSON response from browser in a readable format (optional)
# print(json.dumps(user_name, sort_keys=True, indent=4))

def get_playlist_by_mood(mood):
    # Search for playlists containing the mood in their name
    results = spotifyObject.search(q='mood:' + mood, type='playlist')
    playlists = results['playlists']['items']
    if playlists:
        playlist = random.choice(playlists)
        playlist_id = playlist['id']
        play_random_track_from_playlist(playlist_id)
    else:
        print("No playlists found for this mood.")

def download_and_play_audio(url):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        response = requests.get(url)
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file_path)
    pygame.mixer.music.play()
    print('Now playing...')
    # Adjust as needed
    pygame.time.wait(10000)  # Let the song play for 30 seconds
    # pygame.mixer.music.stop()
    # os.unlink(temp_file_path)  # Delete the temporary file

def play_random_track_from_playlist(playlist_id):
    # Get tracks from the playlist
    tracks = spotifyObject.playlist_tracks(playlist_id)
    track_items = tracks['items']
    if track_items:
        # Select a random track
        random_track = random.choice(track_items)['track']
        song_url = random_track['preview_url']
        if song_url:
            download_and_play_audio(song_url)
        else:
            print("Selected song does not have a preview available.")
    else:
        print("Playlist is empty.")

while True:
    print("Welcome to the project, " + user_name['display_name'])
    print("0 - Exit the console")
    print("1 - Get Playlist by Mood and Play a Random Song")
    user_input = input("Enter Your Choice: ")
    if user_input == '1':
        mood = input("Enter the mood: ")
        get_playlist_by_mood(mood)
    elif user_input == '0':
        print("Good Bye, Have a great day!")
        break
    else:
        print("Please enter valid user input.")
