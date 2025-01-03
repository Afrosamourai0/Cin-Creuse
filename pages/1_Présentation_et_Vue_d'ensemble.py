import streamlit as st

def main():
    # Configurer Streamlit pour l'affichage large
    st.set_page_config(layout="wide", page_title="Tableau de bord Power BI")

    # Titre de l'application
    st.title("📊 Tableau de bord Power BI")

    # URL publique du tableau de bord Power BI
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiMGYyODQ5YjYtYjU0YS00ZjkwLWI4ZTItZDNhZjkyMjhlZjJhIiwidCI6IjM3NmIxOTc2LTQxZmEtNDc4OC05NWIzLWFmZGY3MDFlNzkyNyJ9"

    # Bouton pour afficher le tableau de bord
    if st.button("Afficher le Dashboard"):
        # Affichage du tableau dans une iframe
        st.markdown(
            f"""
            <iframe src="{powerbi_url}" 
                    width="100%" 
                    height="800px" 
                    style="border:none;">
            </iframe>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("Cliquez sur le bouton ci-dessus pour afficher le tableau de bord.")

if __name__ == "__main__":
    main()

