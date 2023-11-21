import os
import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD
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

def train_and_save_model(data):
    data = data[~data["track_id"].isin(data["track_id"].unique())]

    reader = Reader(rating_scale=(0, 100))
    data = Dataset.load_from_df(data[["user_id", "track_id", "popularity"]], reader)

    trainset = data.build_full_trainset()

    cf_model = SVD()
    cf_model.fit(trainset)

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    cf_model_path = os.path.join(models_dir, "collaborative_filtering_model.pkl")
    joblib.dump(cf_model, cf_model_path)

    print("Collaborative Filtering model trained and saved successfully!")

if __name__ == "__main__":
    merged_data = load_latest_data()

    train_and_save_model(merged_data)
