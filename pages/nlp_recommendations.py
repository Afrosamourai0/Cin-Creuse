import streamlit as st
import requests
import spacy

API_KEY = '1efc9bac137c809078181e5c2c13cafc'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'


from spacy.cli import download

try:
    nlp = spacy.load("fr_core_news_md")
except OSError:
    download("fr_core_news_md")  # Télécharge automatiquement le modèle
    nlp = spacy.load("fr_core_news_md")

# Charger le modèle de langue français de spaCy
nlp = spacy.load("fr_core_news_md")

# Fonction pour extraire des mots-clés ou effectuer une analyse NLP sur un texte
def extract_keywords_with_nlp(text):
    doc = nlp(text)
    # Garder les noms, adjectifs, et verbes pour les mots-clés
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"]]
    return keywords

# Fonction pour rechercher des films
@st.cache_data
def recommend_movies(sort_by="popularity.desc", genre=None):
    try:
        url = f"{BASE_URL}/discover/movie"
        params = {"api_key": API_KEY, "language": "fr-FR", "sort_by": sort_by}
        if genre:
            params["with_genres"] = genre
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la recherche de films : {e}")
        return {"results": []}

# Fonction pour effectuer une similarité basée sur les descriptions ou titres
def find_similar_movies(user_input, movies, field="overview"):
    user_doc = nlp(user_input)
    recommendations = []
    
    for movie in movies:
        movie_text = movie.get(field, "")
        if movie_text:
            movie_doc = nlp(movie_text)
            similarity = user_doc.similarity(movie_doc)
            recommendations.append((movie, similarity))
    
    # Trier les films par similarité décroissante
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

# Fonction pour afficher les films recommandés
def display_recommended_movies(recommendations, top_n=10):
    for movie, similarity in recommendations[:top_n]:
        col1, col2 = st.columns([1, 3])
        with col1:
            poster_url = f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else ""
            if poster_url:
                st.image(poster_url, use_container_width=True)

        with col2:
            st.write(f"### **{movie['title']}** ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})")
            st.write(f"**Similarité avec votre idée :** {similarity:.2f}")
            st.write(f"**Résumé :** {movie['overview']}")
            st.write(f"**Genres :** {', '.join([genre['name'] for genre in movie['genres']]) if movie.get('genres') else 'N/A'}")
            st.write(f"**Note moyenne :** {movie['vote_average']}/10")
            st.write("---")

def main():
    st.title("🎬 Recommandation de films basée sur votre idée (NLP)")

    # Demander à l'utilisateur une idée de film
    user_input = st.text_input("💡 Entrez une idée de film ou un thème qui vous intéresse", placeholder="Exemple : Action avec des super-héros")

    # Choix du filtre (popularité, genre, etc.)
    sort_by = st.selectbox("Trier les films par", options=["popularité", "date de sortie"], index=0)
    genre_option = st.selectbox("Choisissez un genre", options=["Tous"] + ["Action", "Comédie", "Drame", "Horreur", "Science-fiction"], index=0)

    if genre_option != "Tous":
        genre_dict = {
            "Action": 28,
            "Comédie": 35,
            "Drame": 18,
            "Horreur": 27,
            "Science-fiction": 878,
        }
        genre = genre_dict.get(genre_option)
    else:
        genre = None

    if st.button("Rechercher des films") and user_input:
        st.write(f"Vous avez entré l'idée : **{user_input}**")

        # Rechercher des films populaires avec un filtre de genre
        movies = recommend_movies(sort_by="popularity.desc", genre=genre)["results"]

        # Comparer avec les descriptions ou les titres
        st.write("🔍 Recherche basée sur les descriptions des films...")
        similar_movies = find_similar_movies(user_input, movies, field="overview")

        if similar_movies:
            st.write(f"**Top {len(similar_movies)} films recommandés :**")
            display_recommended_movies(similar_movies, top_n=10)
        else:
            st.warning("Aucun film similaire trouvé. Essayez une autre idée.")
    elif not user_input:
        st.warning("Veuillez entrer une idée pour commencer la recherche de films.")

if __name__ == "__main__":
    main()
