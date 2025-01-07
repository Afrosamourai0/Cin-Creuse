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

# Fonction pour afficher les détails d'un film
def display_movie_details(movie):
    cols = st.columns([1, 3])  # Diviser en colonnes
    with cols[0]:
        # Réduction de la taille des images (150px de largeur)
        poster_url = f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else ""
        if poster_url:
            st.image(poster_url, width=150)
    with cols[1]:
        st.markdown(f"### 🎥 **{movie['title']}** ({movie['release_date'][:4]})")
        st.markdown(f"**Note :** ⭐ {movie['vote_average']}/10")
        
        # Affichage complet du résumé
        overview = movie['overview']
        st.markdown(f"<p style='text-align: justify;'>{overview}</p>", unsafe_allow_html=True)

# Fonction principale
def main():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🎬 Découvrez des films exceptionnels</h1>", unsafe_allow_html=True)
    st.sidebar.title("🔍 Filtres")
    
    genres = get_genres()
    genre_options = {genre['name']: genre['id'] for genre in genres.get('genres', [])}
    genre_options['Tous'] = None
    genre = st.sidebar.selectbox("Genre", list(genre_options.keys()))
    min_votes = st.sidebar.slider("Note moyenne minimum", 0.0, 10.0, 5.0)
    year = st.sidebar.slider("Année de sortie", 1900, 2024, 2020)

    if st.sidebar.button("Rechercher"):
        genre_id = genre_options[genre]
        results = search_movies_by_filters(genre_id, min_votes, year)
        st.markdown(f"<h3 style='color: #FFC300;'>Résultats de la recherche :</h3>", unsafe_allow_html=True)
        
        if results and 'results' in results:
            for movie in results['results'][:10]:  # Limiter à 10 résultats
                display_movie_details(movie)
                st.markdown("---")
        else:
            st.warning("Aucun film trouvé pour les critères sélectionnés.")

if __name__ == "__main__":
    main()
