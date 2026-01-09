import os
import time
from dotenv import load_dotenv
from downloader import download_images_and_create_pdf
from extract_pages import extraire_pages_pdf

# Chargement des variables d'environnement
load_dotenv()

def main():
    print("=== DÉBUT DU TRAITEMENT COMPLET ===")
    
    # --- 1. Récupération des configurations ---
    target_url = os.getenv("TARGET_URL")
    
    # On récupère les valeurs brutes (str) pour gérer le cas "ALL"
    start_page = os.getenv("START_PAGE")
    end_page = os.getenv("END_PAGE")

    if not target_url or not start_page or not end_page:
        print("ERREUR CRITIQUE : Vérifiez TARGET_URL, START_PAGE et END_PAGE dans votre fichier .env")
        return

    # Noms des fichiers
    pdf_complet = "Resultat_Calameo.pdf"
    pdf_final = "Resultat_Final_Clean.pdf"

    # --- 2. Lancement du Téléchargement ---
    print(f"\n[ÉTAPE 1/2] Téléchargement depuis : {target_url[:50]}...")
    
    download_images_and_create_pdf(target_url, pdf_complet)

    # Petite pause pour s'assurer que le fichier est bien libéré
    time.sleep(1)

    if not os.path.exists(pdf_complet):
        print("\nERREUR : Le PDF complet n'a pas été créé. Arrêt du processus.")
        return

    # --- 3. Lancement de l'Extraction ---
    print(f"\n[ÉTAPE 2/2] Traitement des pages ({start_page} à {end_page})...")
    
    extraire_pages_pdf(pdf_complet, pdf_final, start_page, end_page)

    print("\n=== TRAITEMENT TERMINÉ ===")

if __name__ == "__main__":
    main()
