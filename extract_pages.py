from pypdf import PdfReader, PdfWriter
import os
import shutil
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

def extraire_pages_pdf(input_path, output_path, start_page, end_page):
    print(f"Traitement du fichier : {input_path}")
    
    if not os.path.exists(input_path):
        print(f"ERREUR : Le fichier '{input_path}' n'existe pas. Lancez d'abord downloader.py.")
        return

    # --- GESTION DU MODE "ALL" ---
    # Si l'utilisateur a mis "ALL" (insensible à la casse), on garde tout.
    if str(start_page).strip().upper() == "ALL" or str(end_page).strip().upper() == "ALL":
        print("Mode 'ALL' détecté : Le document complet sera conservé.")
        try:
            shutil.copy(input_path, output_path)
            print(f"Succès ! Le fichier complet a été copié vers '{output_path}'.")
            return
        except Exception as e:
            print(f"Erreur lors de la copie du fichier complet : {e}")
            return

    # --- MODE EXTRACTION CLASSIQUE ---
    try:
        # Conversion en entiers maintenant qu'on sait que ce n'est pas "ALL"
        start_page_int = int(start_page)
        end_page_int = int(end_page)
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        print(f"Le document contient {total_pages} pages au total. Extraction demandée : {start_page_int}-{end_page_int}")

        start_index = start_page_int - 1
        end_index = end_page_int 

        if start_page_int < 1 or end_page_int > total_pages:
            print(f"Erreur : Les pages demandées ({start_page_int}-{end_page_int}) sont hors des limites (1-{total_pages}).")
            return

        for i in range(start_index, end_index):
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Succès ! Les pages {start_page_int} à {end_page_int} ont été extraites vers '{output_path}'.")

    except ValueError:
        print(f"ERREUR DE CONFIGURATION : START_PAGE et END_PAGE doivent être des nombres ou 'ALL'. Valeurs reçues : {start_page}, {end_page}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    fichier_source = "Resultat_Calameo.pdf"
    fichier_sortie = "Résultat_Lead_Vichy_Clean.pdf"
    
    try:
        debut = os.getenv("START_PAGE")
        fin = os.getenv("END_PAGE")
        
        extraire_pages_pdf(fichier_source, fichier_sortie, debut, fin)
    except Exception as e:
        print(f"Erreur : {e}")
