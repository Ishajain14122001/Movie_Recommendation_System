import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide")


def fetch_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2e475cbd2d58a0046b0f93be52d7156c&language=en-US'.format(id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True,
                        key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(id))

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0],width=150)
    with col2:
        st.write(names[1])
        st.image(posters[1],width=150)

    with col3:
        st.write(names[2])
        st.image(posters[2],width=150)
    with col4:
        st.write(names[3])
        st.image(posters[3],width=150)
    with col5:
        st.write(names[4])
        st.image(posters[4],width=150)
