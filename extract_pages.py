from pypdf import PdfReader, PdfWriter
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

def extraire_pages_pdf(input_path, output_path, start_page, end_page):
    print(f"Traitement du fichier : {input_path}")
    print(f"Extraction demandée : Page {start_page} à {end_page}")
    
    if not os.path.exists(input_path):
        print(f"ERREUR : Le fichier '{input_path}' n'existe pas. Lancez d'abord downloader.py.")
        return

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        print(f"Le document contient {total_pages} pages au total.")

        # Conversion en index (0-based)
        start_index = start_page - 1
        end_index = end_page 

        if start_page < 1 or end_page > total_pages:
            print(f"Erreur : Les pages demandées ({start_page}-{end_page}) sont hors des limites (1-{total_pages}).")
            return

        for i in range(start_index, end_index):
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Succès ! Les pages {start_page} à {end_page} ont été extraites vers '{output_path}'.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    fichier_source = "Resultat_Calameo.pdf"
    fichier_sortie = "Résultat_Lead_Vichy_Clean.pdf"
    
    # Récupération des pages depuis le fichier .env
    try:
        debut = int(os.getenv("START_PAGE"))
        fin = int(os.getenv("END_PAGE"))
        
        extraire_pages_pdf(fichier_source, fichier_sortie, debut, fin)
    except TypeError:
        print("ERREUR : Assurez-vous que START_PAGE et END_PAGE sont bien définis dans le fichier .env")
    except ValueError:
        print("ERREUR : START_PAGE et END_PAGE doivent être des nombres entiers dans le fichier .env")
