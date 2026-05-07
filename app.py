import streamlit as st
from recipe_scrapers import scrape_me

# Configuration de la page
st.set_page_config(page_title="Ma Cuisine Zen", page_icon="🍳")

st.title("🍳 Ma Cuisine Sans Pub")
st.write("Collez l'URL d'une recette (Marmiton, 750g, Cuisine AZ, etc.) pour l'afficher proprement.")

# Barre de recherche
url = st.text_input("Lien de la recette :", placeholder="https://www.marmiton.org/recettes/...")

if url:
    try:
        # Extraction des données
        scraper = scrape_me(url)
        
        # Affichage du titre et de l'image
        st.header(scraper.title())
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(scraper.image(), use_column_width=True)
        
        with col2:
            st.metric("Temps total", f"{scraper.total_time()} min")
            st.metric("Portions", scraper.yields())

        # Affichage des Ingrédients
        st.subheader("🛒 Ingrédients")
        for ingredient in scraper.ingredients():
            st.write(f"- {ingredient}")

        # Affichage des Étapes
        st.subheader("👨‍🍳 Préparation")
        instructions = scraper.instructions().split('\n')
        for i, etape in enumerate(instructions):
            if etape.strip():
                st.info(f"**Étape {i+1}** : {etape}")

    except Exception as e:
        st.error(f"Oups ! Impossible de lire cette recette. Erreur : {e}")
