import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import requests


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

            # Récupérer la bande-annonce si disponible
            trailers = requests.get(f'https://api.themoviedb.org/3/movie/{movie["id"]}/videos?api_key=1efc9bac137c809078181e5c2c13cafc')
            trailer_data = trailers.json()
            if trailer_data.get('results'):
                trailer_key = trailer_data['results'][0]['key']

            return description, trailer_key, poster_url
    return None, None, None

# Fonction pour afficher un film
def display_movie(movie, is_similar=False):
    col1, col2 = st.columns([1, 2])
    with col1:
        # Détails via l'API
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

    if is_similar:
        st.write("---")

# Fonction pour recommander des films similaires
def recommend_movies(film):
    film_data = df[df['original_title'] == film]
    if film_data.empty:
        st.error(f"Aucun film trouvé avec le titre : {film}")
        return

    # Trouver les indices des films similaires
    distances, indices = nn.kneighbors(film_data[feature])
    similar_df = df.iloc[indices[0]]

    # Exclure le film choisi des recommandations
    similar_df = similar_df[similar_df['original_title'] != film]

    # Afficher les films similaires
    st.markdown("### Ces films pourraient aussi vous plaire :")
    for _, similar_movie in similar_df.iterrows():
        display_movie(similar_movie, is_similar=True)

# Fonction pour trouver un film par recherche approximative
def find_closest_movie(movie_name):
    titles = df['original_title'].tolist()
    closest_matches = get_close_matches(movie_name, titles, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Fonction principale
def main():
    st.title("🎬 Recommandation de films basées sur votre film préféré")

    # Demander à l'utilisateur de saisir un titre de film
    movie_name = st.text_input("Entrez le titre d'un film", placeholder="Exemple : Inception")

    if movie_name:
        # Rechercher le titre le plus proche
        closest_match = find_closest_movie(movie_name)

        if closest_match:
            with st.spinner("Chargement des informations du film..."):
                st.markdown("## 📝 Détails du film choisi :")
                film_data = df[df['original_title'] == closest_match]
                display_movie(film_data.iloc[0])

            st.success(f"Très bon choix ! 🎉 (Saviez-vous que vous cherchiez peut-être : {closest_match}?)")

            # Bouton pour trouver des films similaires
            if st.button("Afficher les films similaires"):
                with st.spinner("Recherche des films similaires..."):
                    recommend_movies(closest_match)
        else:
            st.error(f"Aucun film trouvé correspondant à : {movie_name}")

# Lancement de l'application
if __name__ == "__main__":
    main()
