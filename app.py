import pandas as pd
import requests
import streamlit as st
import pickle

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  1:6]  # it will sort the similarities btw movies in descending order without loosing the index of each value by using enumerate function, and also gives the top 5 results.....

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API..
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Popcorn Picks')

selected_movie_name = st.selectbox(
    "Tell us a movie you liked, and we’ll find more you’ll love.",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], caption=names[0], use_container_width=True)

    with col2:
        st.image(posters[1], caption=names[1], use_container_width=True)

    with col3:
        st.image(posters[2], caption=names[2], use_container_width=True)
    with col4:
        st.image(posters[3], caption=names[3], use_container_width=True)
    with col5:
        st.image(posters[4], caption=names[4], use_container_width=True)






