import streamlit as st

def main():
    # Configurer Streamlit pour l'affichage large
    st.set_page_config(layout="wide", page_title="Tableau de bord Power BI et PowerPoint")

    # Titre de l'application avec un emoji
    st.title("📊 Tableau de bord Power BI et PowerPoint")

  
    # Texte du rapport affiché dans la sidebar avec un style
    texte_rapport = """
    ### Rapport de Marché du Cinéma
    
    Dans notre rapport, nous avons analysé le marché du cinéma de **1930 à 2024** à partir des données IMDB et TMDB.
    Au total sur **114 126 films**, on peut noter que le budget moyen est de **2,24M**. On recense **282 153 acteurs** 
    avec une note moyenne des films de **5,99**. Les films les plus populaires incluent **"The Pope's Exorcist"** et **"Avatar: The Way of Water"**. 
    Le drame et la comédie sont les genres les plus présents.
    """
    st.sidebar.markdown(texte_rapport, unsafe_allow_html=True)

    # Séparateur de contenu principal
    st.markdown("---")

    # Option de sélection
    option = st.selectbox("🔍 **Choisissez ce que vous souhaitez afficher** :", 
                          ["Power BI", "PowerPoint"], index=0, help="Sélectionnez une option pour voir le contenu")

    if option == "Power BI":
        # URL publique du tableau de bord Power BI
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiYWRlM2ZmYzMtNjlhOS00NzgyLTk5NTEtNjA5ODEyNWJkNjczIiwidCI6IjM3NmIxOTc2LTQxZmEtNDc4OC05NWIzLWFmZGY3MDFlNzkyNyJ9"

        # Affichage du Power BI
        st.subheader("📊 **Tableau de bord Power BI**")
        if st.button("Afficher le Dashboard Power BI", help="Cliquez pour afficher le tableau de bord Power BI"):
            st.markdown(
                f"""
                <iframe src="{powerbi_url}" 
                        width="100%" 
                        height="800px" 
                        style="border:none; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                </iframe>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.write("Cliquez sur le bouton ci-dessus pour afficher le tableau de bord Power BI.")
    
    elif option == "PowerPoint":
        # Lien vers le PowerPoint
        ppt_link = "https://onedrive.live.com/:p:/g/personal/6A73F71480A4FC8E/EQF8omnMvCxKvnPvUyYLtlUBHCocwCihzKFSEcUrVQX4Eg?resid=6A73F71480A4FC8E!s69a27c01bccc4a2cbe73ef53260bb655&ithint=file%2Cpptx&e=dVtWzc&migratedtospo=true&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy82YTczZjcxNDgwYTRmYzhlL0VRRjhvbW5NdkN4S3ZuUHZVeVlMdGxVQkhDb2N3Q2loektGU0VjVXJWUVg0RWc_ZT1kVnRXemM"

        # Lien pour afficher le PowerPoint
        st.subheader("📑 **Présentation PowerPoint**")
        st.markdown(f"### PowerPoint : [Cliquez ici pour voir le PowerPoint]( {ppt_link} )", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
