import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=yourkey&language=en-US".format(movie_id))

    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']




def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)  
        recommended_movies_poster.append(fetch_poster(movie_id))  
    return recommend_movies, recommended_movies_poster

similarity=pickle.load(open('similarity.pkl','rb'))

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame.from_dict(movies_dict)

st.title('Movie Recommender System')

option = st.selectbox("Choose a movie", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)
    
   
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

