import streamlit as st
from recipe_scrapers import scrape_me
from duckduckgo_search import DDGS

st.set_page_config(page_title="Ma Cuisine Zen", page_icon="🍳", layout="wide")

st.title("🍳 Moteur de Recherche Culinaire")

# --- ZONE DE RECHERCHE ---
query = st.text_input("Que voulez-vous cuisiner ?", placeholder="Ex: Lasagnes végétariennes, Poulet curry...")

if query:
    # On force la recherche sur des sites compatibles pour garantir l'extraction
    search_query = f"{query} site:marmiton.org OR site:750g.com OR site:cuisineaz.com"
    
    with st.spinner('Recherche des meilleures recettes...'):
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(search_query, max_results=8)]
            
            if not results:
                st.warning("Aucun résultat trouvé.")
            else:
                # Création d'une liste de titres pour la sélection
                titles = [r['title'] for r in results]
                selected_title = st.selectbox("Choisissez une recette à afficher :", ["--- Sélectionnez une recette ---"] + titles)

                if selected_title != "--- Sélectionnez une recette ---":
                    # Récupération de l'URL correspondante
                    selected_url = next(r['href'] for r in results if r['title'] == selected_title)
                    
                    st.divider()
                    
                    # --- EXTRACTION ET AFFICHAGE ---
                    try:
                        scraper = scrape_me(selected_url)
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.image(scraper.image(), use_column_width=True)
                            st.success(f"⏱ {scraper.total_time()} min")
                            st.info(f"👥 {scraper.yields()}")
                        
                        with col2:
                            st.header(scraper.title())
                            
                            tab1, tab2 = st.tabs(["🛒 Ingrédients", "👨‍🍳 Étapes"])
                            
                            with tab1:
                                for ing in scraper.ingredients():
                                    st.write(f"✅ {ing}")
                                    
                            with tab2:
                                instructions = scraper.instructions().split('\n')
                                for i, step in enumerate(instructions):
                                    if step.strip():
                                        st.write(f"**{i+1}.** {step}")
                        
                        st.caption(f"Source originale : [Cliquez ici]({selected_url})")

                    except Exception as e:
                        st.error("Désolé, cette recette est protégée ou mal structurée. Essayez-en une autre !")
        
        except Exception as e:
            st.error(f"Erreur de recherche : {e}")

else:
    st.info("Entrez un plat ou des ingrédients ci-dessus pour commencer.")
