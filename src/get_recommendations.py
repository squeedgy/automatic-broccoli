import os
import pandas as pd
from surprise import Dataset, Reader, SVD
import joblib
import glob
 
def load_latest_data():
    processed_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

    user_data_files = glob.glob(os.path.join(processed_data_path, "user_data_*.csv"))
    if not user_data_files:
        raise FileNotFoundError("No user data CSV files found.")
    latest_user_data_file = max(user_data_files, key=os.path.getctime)
    user_data_df = pd.read_csv(latest_user_data_file)

    liked_songs_files = glob.glob(os.path.join(processed_data_path, "liked_songs_data_*.csv"))
    if not liked_songs_files:
        raise FileNotFoundError("No liked songs data CSV files found.")
    latest_liked_songs_file = max(liked_songs_files, key=os.path.getctime)
    liked_songs_data = pd.read_csv(latest_liked_songs_file)

    merged_data = pd.merge(liked_songs_data, user_data_df, how="inner", on="user_id")

    return merged_data

def load_collaborative_filtering_model():
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    cf_model_path = os.path.join(models_dir, "collaborative_filtering_model.pkl")
    
    if not os.path.exists(cf_model_path):
        raise FileNotFoundError(f"Collaborative Filtering model not found at {cf_model_path}")

    return joblib.load(cf_model_path)

def get_new_recommendations(model, user_data):
    liked_track_ids = user_data["track_id"].unique()

    all_track_ids = user_data["track_id"].unique()

    new_track_ids = [track_id for track_id in all_track_ids if track_id not in liked_track_ids]

    recommendations = []
    for track_id in new_track_ids:
        prediction = model.predict(user_id=1, item_id=track_id)
        recommendations.append((track_id, prediction.est))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations

if __name__ == "__main__":
    merged_data = load_latest_data()
    cf_model = load_collaborative_filtering_model()

    new_recommendations = get_new_recommendations(cf_model, merged_data)

    if new_recommendations:
        print("New Recommendations:")
        for track_id, estimated_popularity in new_recommendations:
            print(f"Track ID: {track_id}, Estimated Popularity: {estimated_popularity}")
    else:
        print("No new recommendations found.")
