import os
import pickle
import streamlit as st
import pandas as pd
import gdown  # Ensure this is in your requirements.txt

# Ensure the 'data' directory exists
os.makedirs('data', exist_ok=True)

# Google Drive File ID for similarity.pkl
file_id = '1YduzIMdhDLOlKd1o1OmeAQoN3t3HURhD'
output_path = 'data/similarity.pkl'

# Step 1: Download similarity.pkl from Google Drive if not exists
if not os.path.exists(output_path):
    url = f'https://drive.google.com/uc?id={file_id}'
    st.write("📥 Downloading model file...")
    gdown.download(url, output_path, quiet=False)

# Step 2: Load similarity matrix and movie dictionary
with open('data/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

with open('data/movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# Step 3: Define the recommendation function
def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]]["title"])
    return recommended_movies

# Step 4: Streamlit UI
st.title("🎬 Movie Recommender System")

Selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    recommendations = recommend(Selected_movie_name)
    st.subheader("Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
