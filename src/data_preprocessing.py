import pandas as pd
import os
import json
import glob
from datetime import datetime

def load_raw_data(data_type):
    raw_data_path = os.path.join(os.path.dirname(__file__), f"../data/raw/{data_type}_*.json")

    latest_file = max(glob.glob(raw_data_path), key=os.path.getctime)

    with open(latest_file, "r") as file:
        data = json.load(file)

    return data

def preprocess_user_data(user_info):
    user_data = {
        "display_name": user_info.get("display_name", ""),
        "email": user_info.get("email", ""),
        "followers": user_info.get("followers", {}).get("total", 0),
        "country": user_info.get("country", ""),
        "user_id": 1
    }

    return user_data

def preprocess_liked_songs_data(liked_songs_data):
    liked_songs_list = []
    for item in liked_songs_data.get("items", []):
        track_info = item.get("track", {})
        added_at = item.get("added_at", "")
        liked_songs_list.append({
            "user_id": 1,
            "track_id": track_info.get("id", ""),
            "added_at": added_at,
            "track_name": track_info.get("name", ""),
            "artist_name": track_info.get("artists", [{}])[0].get("name", ""),
            "album_name": track_info.get("album", {}).get("name", ""),
            "release_date": track_info.get("album", {}).get("release_date", ""),
            "duration_ms": track_info.get("duration_ms", 0),
            "popularity": track_info.get("popularity", 0)
        })

    return liked_songs_list

def load_and_preprocess_liked_songs_data():
    liked_songs_data = load_raw_data("liked_songs")

    processed_liked_songs_data = preprocess_liked_songs_data(liked_songs_data)

    return processed_liked_songs_data
 
def save_processed_data(user_data, liked_songs_data):
    processed_data_path = os.path.join(os.path.dirname(__file__), "../data/processed/")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    user_data_df = pd.DataFrame([user_data])
    user_data_df.to_csv(os.path.join(processed_data_path, f"user_data_{timestamp}.csv"), index=False)

    liked_songs_data_df = pd.DataFrame(liked_songs_data)
    liked_songs_data_df.to_csv(os.path.join(processed_data_path, f"liked_songs_data_{timestamp}.csv"), index=False)

if __name__ == "__main__":
    user_info = load_raw_data("user_data")

    user_data = preprocess_user_data(user_info)

    processed_liked_songs_data = load_and_preprocess_liked_songs_data()

    save_processed_data(user_data, processed_liked_songs_data)
