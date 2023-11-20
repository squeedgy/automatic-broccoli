import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from datetime import datetime

credentials_path = os.path.join(os.path.dirname(__file__), "../data/raw/spotify_credentials.json")
with open(credentials_path, "r") as file:
    spotify_credentials = json.load(file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_credentials["client_id"],
    client_secret=spotify_credentials["client_secret"],
    redirect_uri="http://localhost:8888/callback",
    scope="user-library-read user-read-recently-played"
))

def get_user_data():
    user_info = sp.current_user()

    liked_songs = sp.current_user_saved_tracks()

    listening_history = sp.current_user_recently_played()

    return user_info, liked_songs, listening_history

def save_data(user_info, liked_songs, listening_history):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    user_data_path = os.path.join(os.path.dirname(__file__), f"../data/raw/user_data_{timestamp}.json")
    liked_songs_path = os.path.join(os.path.dirname(__file__), f"../data/raw/liked_songs_{timestamp}.json")
    tracks_data_path = os.path.join(os.path.dirname(__file__), f"../data/raw/tracks_data_{timestamp}.json")

    with open(user_data_path, "w") as user_data_file:
        json.dump(user_info, user_data_file, indent=4)

    with open(liked_songs_path, "w") as liked_songs_file:
        json.dump(liked_songs, liked_songs_file, indent=4)

    with open(tracks_data_path, "w") as tracks_data_file:
        json.dump(listening_history, tracks_data_file, indent=4)

if __name__ == "__main__":
    user_info, liked_songs, listening_history = get_user_data()
    save_data(user_info, liked_songs, listening_history)
