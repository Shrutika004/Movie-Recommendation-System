
import joblib
import streamlit as st
import requests


def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=5bb5602f"
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Error fetching poster for {movie_title}. Status code: {response.status_code}")
        return None

    data = response.json()
    poster_url = data.get("Poster")
    if poster_url and poster_url != "N/A":
        return poster_url
    else:
        st.warning(f"No poster found for {movie_title}")
        return None



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:  
        movie_title = movies.iloc[i[0]].title
        recommended_movies_name.append(movie_title)
        recommended_movies_poster.append(fetch_poster(movie_title))
    return recommended_movies_name, recommended_movies_poster

st.header("🎬 Movies Recommendation System Using Machine Learning")

movies = joblib.load(open('artificats/movie_list.pkl', 'rb'))
similarity = joblib.load(open('artificats/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)

if st.button('Show recommendation'):
    names, posters = recommend(selected_movie)

    if names:
        st.subheader("Recommended Movies 🎥")
        cols = st.columns(5) 
        for idx, (name, poster) in enumerate(zip(names, posters)):
            with cols[idx % 5]:
                if poster:
                    st.image(poster, use_container_width=True)
                st.caption(name)
