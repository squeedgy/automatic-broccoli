# Music Recommendation System

## Overview

This project implements a music recommendation system using collaborative filtering. It explores user listening history to recommend new songs based on their preferences. The recommendation system is trained using a combination of collaborative filtering and content-based filtering approaches.

## Installation

1. Clone the repository:

  ```
   git clone https://github.com/your-username/music-recommendation-system.git
  ```

2. install dependencies

    ```
    pip install -r requirements.txt
    ```
## Usage

1. Data Collection
    data_collection.py to collect user data, liked songs, and listening history

2. Data Preprocessing
    data_preprocessing.py to preprocess the raw data and create CSV files

3. Recommendation Model
    recommendation_model.py to train the collaborative filtering model

4. Evaluation
    MSE and RMSE

5. Get Recommendations
    get_recommendations.py to get new song recommendations

## Recommendation Model
    The recommendation model is implemented using collaborative filtering with the Surprise library.

## Evaluation
    Metrics like Mean Squared Error (MSE) and Root Mean Squared Error (RMSE) are used to evaluate the model's performance.

## Get Recommendations
    get_recommendations.py fetches new song recommendations for the user that are not in the liked songs playlist or the DataFrame.
