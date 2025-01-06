import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="🎬 Recommandation de Films", page_icon="🎥", layout="wide")

# API Configuration
API_KEY = '1efc9bac137c809078181e5c2c13cafc'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="

# Fonction pour récupérer les films populaires
@st.cache_data
def get_popular_movies():
    try:
        url = f"{BASE_URL}/movie/popular"
        params = {'api_key': API_KEY, 'language': 'fr-FR'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des films populaires : {e}")
        return {'results': []}

# Fonction pour récupérer les détails d'un film
def get_movie_details(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {'api_key': API_KEY, 'language': 'fr-FR'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des détails du film : {e}")
        return {}

# Fonction pour récupérer la bande-annonce d'un film
def get_movie_trailer(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}/videos"
        params = {'api_key': API_KEY, 'language': 'fr-FR'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        videos = response.json().get("results", [])
        for video in videos:
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"{YOUTUBE_BASE_URL}{video['key']}"
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération de la bande-annonce : {e}")
        return None

# Utilisation de CSS pour personnaliser l'apparence
st.markdown("""
    <style>
        body {
            background-color: #000000;
        }
        .main-title {
            text-align: center;
            color: #ffffff;
            font-size: 48px;
            font-weight: bold;
        }
        .description {
            text-align: center;
            color: #ffffff;
            font-size: 16px;
            margin-top: -10px;
        }
        .subheader {
            font-size: 24px;
            color: #01b4e4;
            font-weight: bold;
            margin-top: 30px;
        }
        .film-card {
            background-color: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
            padding: 15px;
            text-align: left;
            margin: 10px;
        }
        .film-title {
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        }
        .film-note {
            color: #ff6347;
            font-weight: bold;
        }
        .film-details {
            margin-top: 10px;
            font-size: 14px;
            color: #d3d3d3;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 class='main-title'>🎬 Recommandation de Films</h1>", unsafe_allow_html=True)

# Ajouter une image sur la page de présentation
st.markdown("""
<div style="text-align: center;">
    <img src="https://www.cia-france.fr/media/1492/les-films-incontournables-du-cinema-w_1700x595.webp" alt="Image de présentation" style="width:50%; border-radius:10px;">
</div>
""", unsafe_allow_html=True)

# Section de présentation
st.markdown("""
<div class='description'>
    <p>Projet de Recommandation de Films</p>
    <p><strong>Collaborateurs :</strong> Laura, Florent, Lucas</p>
    <h3>Contexte</h3>
    <p>Un cinéma en perte de vitesse situé dans la Creuse nous a contacté pour digitaliser son offre en créant un site internet dédié aux habitants locaux.</p>
    <h3>Challenge</h3>
    <p>Créer un moteur de recommandation de films malgré une situation de cold start.</p>
    <h3>Démarche</h3>
    <ul>
        <li>Analyse de la consommation de cinéma dans la région.</li>
        <li>Étude des bases de données IMDb pour identifier les tendances.</li>
        <li>Création d’un tableau de bord interactif pour illustrer les résultats.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Section des films populaires
st.markdown("<h2 class='subheader'>🎥 Films Populaires</h2>", unsafe_allow_html=True)

# Ajout du spinner pendant le chargement des films populaires
with st.spinner("Chargement des films populaires..."):
    popular_movies = get_popular_movies()

if popular_movies["results"]:
    # Organisation des films en colonnes
    col1, col2, col3 = st.columns(3, gap="medium")
    cols = [col1, col2, col3]
    for i, movie in enumerate(popular_movies["results"][:9]):  # Afficher les 9 premiers films
        with cols[i % 3]:
            poster_path = movie.get("poster_path")
            movie_id = movie.get("id")
            movie_details = get_movie_details(movie_id)
            trailer_url = get_movie_trailer(movie_id)

            st.markdown("<div class='film-card'>", unsafe_allow_html=True)
            
            # Affichage de l'affiche
            if poster_path:
                poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                st.image(poster_url, use_container_width=True)
            
            # Affichage des détails
            st.markdown(f"<p class='film-title'>{movie['title']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Date de sortie : {movie.get('release_date', 'N/A')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='film-note'>⭐ {movie['vote_average']}/10 ({movie['vote_count']} votes)</p>", unsafe_allow_html=True)
            
            # Genres
            genres = [genre['name'] for genre in movie_details.get('genres', [])]
            if genres:
                st.markdown(f"<p class='film-details'>Genres : {', '.join(genres)}</p>", unsafe_allow_html=True)
            
            # Résumé
            overview = movie['overview'] if movie['overview'] else "Résumé non disponible."
            # Limiter la description
            max_chars = 150
            if len(overview) > max_chars:
                overview = overview[:max_chars] + "..."
            st.markdown(f"<p class='film-details'>{overview}</p>", unsafe_allow_html=True)
            
            # Bande-annonce
            if trailer_url:
                st.markdown(f"[🎥 Voir la bande-annonce]({trailer_url})", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.write("Aucun film populaire trouvé pour le moment.")
