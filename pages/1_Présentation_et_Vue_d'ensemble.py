import streamlit as st

def main():
    # Configurer Streamlit pour l'affichage large
    st.set_page_config(layout="wide", page_title="Tableau de bord Power BI et PowerPoint")

    # Titre de l'application avec un emoji
    st.title("📊 Tableau de bord Power BI et PowerPoint")

    # Ajouter une image d'illustration dans le sidebar
    st.sidebar.image("https://www.jeveuxetredatascientist.fr/wp-content/uploads/2021/04/power-bi-logo.jpg", width=150)
    st.sidebar.image("https://tse2.mm.bing.net/th?id=OIP.iDTOWshVxOYz6x11vEZ7dwHaHa&pid=Api&P=0&h=180", width=150)

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
        ppt_link = "https://onedrive.live.com/personal/6a73f71480a4fc8e/_layouts/15/Doc.aspx?sourcedoc=%7B2f9cb413-5d8c-41b6-a9ea-c16cc414ac10%7D&action=default&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy82YTczZjcxNDgwYTRmYzhlL0VSTzBuQy1NWGJaQnFlckJiTVFVckJBQm1HM05xanJYVWhoRTdTSG51TFRNVWc_ZT1xZGo4bWI&slrid=beed73a1-20ad-a000-ec05-4ce9fd3161fc&originalPath=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy82YTczZjcxNDgwYTRmYzhlL0VSTzBuQy1NWGJaQnFlckJiTVFVckJBQm1HM05xanJYVWhoRTdTSG51TFRNVWc_cnRpbWU9eHRpMmJnY3MzVWc&CID=9d616f74-24bb-4867-b2ca-10508f450fce&_SRM=0:G:57&file=Etude%20de%20march%c3%a9_Projet%202%20(1).pptx"

        # Lien pour afficher le PowerPoint
        st.subheader("📑 **Présentation PowerPoint**")
        st.markdown(f"### PowerPoint : [Cliquez ici pour voir le PowerPoint]( {ppt_link} )", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
