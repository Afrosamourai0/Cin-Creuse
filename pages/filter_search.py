import streamlit as st
import requests
import pandas as pd

API_KEY = '1efc9bac137c809078181e5c2c13cafc'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Fonction pour récupérer les genres
@st.cache_data
def get_genres():
    try:
        url = f"{BASE_URL}/genre/movie/list"
        params = {'api_key': API_KEY, 'language': 'fr-FR'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des genres : {e}")
        return {'genres': []}

# Fonction pour rechercher des films par filtres
@st.cache_data
def search_movies_by_filters(genre, min_votes, year):
    try:
        url = f"{BASE_URL}/discover/movie"
        params = {
            'api_key': API_KEY,
            'with_genres': genre,
            'vote_average.gte': min_votes,
            'primary_release_year': year,
            'language': 'fr-FR'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la recherche de films : {e}")
        return {'results': []}

# Fonction pour recommander des films similaires
@st.cache_data
def recommend_movies(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}/recommendations"
        params = {"api_key": API_KEY, "language": "fr-FR"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la recommandation des films : {e}")
        return {"results": []}

# Fonction pour récupérer la bande-annonce du film
@st.cache_data
def get_movie_trailer(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}/videos"
        params = {"api_key": API_KEY, "language": "fr-FR"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        videos = response.json().get('results', [])
        for video in videos:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération de la bande-annonce : {e}")
        return None

def display_movie_details(movie):
    st.write(f"**{movie['title']}** ({movie['release_date'][:4]})")

    # Affichage de l'affiche du film
    poster_url = f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else ""
    if poster_url:
        st.image(poster_url, use_container_width=True)

    # Affichage de la note et du résumé
    st.write(f"**Note :** {movie['vote_average']}/10")
    st.write(f"**Résumé :** {movie['overview'][:200]}...")

    # Affichage de la bande-annonce
    trailer_url = get_movie_trailer(movie['id'])
    if trailer_url:
        st.video(trailer_url)
    st.write("---")

def display_recommendation_details(movies):
    for movie in movies:
        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                poster_url = f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else ""
                if poster_url:
                    st.image(poster_url, width=100)
            with cols[1]:
                st.write(f"**{movie['title']}** ({movie['release_date'][:4]})")
                st.write(f"**Note :** {movie['vote_average']}/10")
                st.write(f"**Résumé :** {movie['overview'][:100]}...")  # Limiter à 100 caractères
                trailer_url = get_movie_trailer(movie['id'])
                if trailer_url:
                    st.markdown(f"[Voir la bande-annonce](https://www.youtube.com/watch?v={trailer_url.split('=')[1]})", unsafe_allow_html=True)
        st.write("---")

def main():
    st.title("🎬 Filtrer les films")

    genres = get_genres()
    genre_options = {genre['name']: genre['id'] for genre in genres.get('genres', [])}
    genre_options['Tous'] = None
    genre = st.sidebar.selectbox("Genre", list(genre_options.keys()))
    min_votes = st.sidebar.slider("Note moyenne minimum", 0.0, 10.0, 5.0)
    year = st.sidebar.slider("Année de sortie", 1900, 2024, 2000)

    if st.sidebar.button("Rechercher"):
        genre_id = genre_options[genre]
        results = search_movies_by_filters(genre_id, min_votes, year)

        if results and 'results' in results:
            movies_df = pd.DataFrame(results['results'])
            for _, movie in movies_df.head(10).iterrows():
                display_movie_details(movie)

                st.write(f"### Recommandations pour **{movie['title']}**")
                recommended_movies = recommend_movies(movie['id'])
                if recommended_movies["results"]:
                    display_recommendation_details(recommended_movies["results"][:5])
                else:
                    st.write("Aucune recommandation trouvée.")
                st.write("----")

if __name__ == "__main__":
    main()
