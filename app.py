import pickle
import streamlit as st
import pandas as pd

# Load similarity matrix and movie dictionary
simmilarity = pickle.load(open('simmilarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# Function to recommend movies
def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = simmilarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        #movie_id=i[0]
        #fetch poster from   API
        recommended_movies.append(movies.iloc[i[0]]["title"])
    return recommended_movies


# Streamlit UI
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
