import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from sklearn.metrics import mean_squared_error
import joblib
import os
import glob 

def load_data():
    processed_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    
    liked_songs_files = glob.glob(os.path.join(processed_data_path, "liked_songs_data_*.csv"))
    if not liked_songs_files:
        raise FileNotFoundError("No liked songs data CSV files found.")
    
    latest_liked_songs_file = max(liked_songs_files, key=os.path.getctime)

    liked_songs_data = pd.read_csv(latest_liked_songs_file)

    reader = Reader(rating_scale=(0, 100))
    data = Dataset.load_from_df(liked_songs_data[["user_id", "track_id", "popularity"]], reader)

    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    return trainset, testset

def evaluate_collaborative_filtering_model(model, testset):
    predictions = model.test(testset)

    predicted_ratings = [pred.est for pred in predictions]
    actual_ratings = [pred.r_ui for pred in predictions]

    mse = mean_squared_error(actual_ratings, predicted_ratings)
    rmse = mse**0.5

    return mse, rmse

if __name__ == "__main__":
    cf_model_path = "models/collaborative_filtering_model.pkl"
    cf_model = joblib.load(cf_model_path)

    trainset, testset = load_data()

    mse, rmse = evaluate_collaborative_filtering_model(cf_model, testset)

    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
