import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import requests
from difflib import get_close_matches

# Chargement des données (remplacez "df" par le chemin correct de votre fichier)
input_file = "df"  # Remplacez cette ligne par le chemin réel de votre fichier .parquet
df = pd.read_parquet(input_file)

# Liste des caractéristiques utilisées pour le modèle
feature = [
    'runtimescaler', 'note_moyennescaler', 'budgetscaler', 'popularityscaler', 'revenuescaler',
    'first_country_product_fact', 'original_language_fact', 'movie', 'short', 'tvMovie', 'tvShort',
    'genre1fact', 'decadefact'
]

# Modèle des plus proches voisins avec pondération
weights = np.array([0.7, 0.7, 0.5, 0.7, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
X = df[feature]
X_weighted = X * weights
k = 5
nn = NearestNeighbors(n_neighbors=k + 1, metric='euclidean')  # +1 pour inclure le film lui-même
nn.fit(X_weighted)

# Fonction pour récupérer la description, le poster et la bande-annonce
def get_movie_details(imdb_id):
    url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key=1efc9bac137c809078181e5c2c13cafc&language=fr&external_source=imdb_id'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('movie_results'):
            movie = data['movie_results'][0]
            description = movie.get('overview', 'Description non disponible')
            trailer_key = None
            poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None

            trailers = requests.get(f'https://api.themoviedb.org/3/movie/{movie["id"]}/videos?api_key=1efc9bac137c809078181e5c2c13cafc')
            trailer_data = trailers.json()
            if trailer_data.get('results'):
                trailer_key = trailer_data['results'][0]['key']

            return description, trailer_key, poster_url
    return None, None, None

# Fonction pour afficher un film
def display_movie(movie):
    col1, col2 = st.columns([1, 2])
    with col1:
        description, trailer_key, poster_url = get_movie_details(movie['imdb_id'])
        if poster_url:
            st.image(poster_url, use_container_width=True)
    with col2:
        st.markdown(f"### 🎬 {movie['original_title']}")
        st.markdown(f"**Note moyenne :** {movie['note moyenne']}/10")
        st.markdown(f"**Durée :** {movie['runtimeMinutes']} minutes")
        st.markdown(f"**Année de sortie :** {movie['startYear']}")
        st.markdown(f"**Pays de production :** {movie['country_product_first']}")
        st.markdown(f"**Genres :** {movie['genres_x']}")
        if description:
            st.markdown(f"**Description :** {description}")
        if trailer_key:
            trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
            st.markdown(f"**Bande-annonce :** [Voir sur YouTube]({trailer_url})")

# Fonction pour recommander des films similaires
def recommend_movies(film_title):
    film_data = df[df['original_title'] == film_title]
    if film_data.empty:
        st.error(f"Aucun film trouvé avec le titre : {film_title}")
        return pd.DataFrame()  # Retourner un DataFrame vide si aucun film similaire trouvé
    distances, indices = nn.kneighbors(film_data[feature])
    similar_df = df.iloc[indices[0]]
    similar_df = similar_df[similar_df['original_title'] != film_title]
    return similar_df

# Fonction pour rechercher des films par correspondance partielle
def find_partial_movie(movie_name):
    titles = df['original_title'].tolist()
    matching_titles = [title for title in titles if movie_name.lower() in title.lower()]
    return matching_titles

# Fonction principale
def main():
    st.title("🎬 Recommandation de films basées sur votre film préféré")

    movie_name = st.text_input("Entrez le titre d'un film", placeholder="Exemple : Inception")

    if movie_name:
        # Recherche des films correspondants
        film_data = df[df['original_title'].str.contains(movie_name, case=False, na=False)]

        if not film_data.empty:
            # Si plusieurs films sont trouvés, afficher une liste déroulante pour sélectionner le film
            if len(film_data) > 1:
                selected_movie_title = st.selectbox("Plusieurs films trouvés. Veuillez choisir celui que vous voulez", film_data['original_title'].tolist())
                film_data = film_data[film_data['original_title'] == selected_movie_title]
            
            st.markdown("### Détails du film recherché :")
            display_movie(film_data.iloc[0])  # Afficher les détails du film choisi
            selected_movie_title = film_data.iloc[0]['original_title']  # Le film choisi pour l'exclure de la recherche partielle
        else:
            st.error(f"Aucun film trouvé correspondant à : {movie_name}")

        # Recherche de films similaires via KNN
        if st.button("Rechercher des films similaires"):
            similar_movies = recommend_movies(film_data['original_title'].values[0])

            if similar_movies.empty:
                st.warning(f"Aucun film similaire trouvé pour : {movie_name}.")
                matching_titles = find_partial_movie(movie_name)
                if matching_titles:
                    st.markdown("### Films correspondants par recherche partielle :")
                    # Exclure le film déjà choisi de la liste
                    matching_titles = [title for title in matching_titles if title != selected_movie_title]
                    for title in matching_titles:
                        film_data = df[df['original_title'] == title]
                        display_movie(film_data.iloc[0])  # Afficher les détails du film trouvé
                else:
                    st.error(f"Aucun film trouvé correspondant à : {movie_name}")
            else:
                st.markdown("### Ces films pourraient aussi vous plaire :")
                for _, similar_movie in similar_movies.iterrows():
                    display_movie(similar_movie)  # Afficher les films similaires trouvés

       

if __name__ == "__main__":
    main()
