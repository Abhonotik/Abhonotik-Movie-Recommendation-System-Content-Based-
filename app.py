import os
import zipfile
import pickle
import streamlit as st
import pandas as pd

# Step 1: Extract the ZIP file only if simmilarity.pkl doesn't exist
if not os.path.exists('simmilarity.pkl'):
    with zipfile.ZipFile('simmilarity.zip', 'r') as zip_ref:
        zip_ref.extractall()

# Step 2: Load similarity matrix and movie dictionary
with open('simmilarity.pkl', 'rb') as f:
    simmilarity = pickle.load(f)

with open('movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# Step 3: Define the recommendation function
def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = simmilarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]]["title"])
    return recommended_movies

# Step 4: Streamlit UI
st.title(" 🎬 Movie Recommender System")

Selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    recommendations = recommend(Selected_movie_name)
    st.subheader("Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
