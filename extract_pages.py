from pypdf import PdfReader, PdfWriter
import os
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extraire_pages_pdf(input_path, output_path, start_page, end_page):
    print(f"Processing file: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"ERROR: File '{input_path}' does not exist. Run downloader.py first.")
        return

    # --- "ALL" MODE HANDLING ---
    if str(start_page).strip().upper() == "ALL" or str(end_page).strip().upper() == "ALL":
        print("'ALL' mode detected: The complete document will be kept.")
        try:
            shutil.copy(input_path, output_path)
            print(f"Success! Complete file copied to '{output_path}'.")
            return
        except Exception as e:
            print(f"Error copying complete file: {e}")
            return

    # --- CLASSIC EXTRACTION MODE ---
    try:
        start_page_int = int(start_page)
        end_page_int = int(end_page)
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        print(f"Document contains {total_pages} pages. Requested extraction: {start_page_int}-{end_page_int}")

        start_index = start_page_int - 1
        end_index = end_page_int 

        if start_page_int < 1 or end_page_int > total_pages:
            print(f"Error: Requested pages ({start_page_int}-{end_page_int}) are out of bounds (1-{total_pages}).")
            return

        for i in range(start_index, end_index):
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Success! Pages {start_page_int} to {end_page_int} extracted to '{output_path}'.")

    except ValueError:
        print(f"CONFIGURATION ERROR: START_PAGE and END_PAGE must be numbers or 'ALL'. Received: {start_page}, {end_page}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fichier_source = "Resultat_Calameo.pdf"
    fichier_sortie = "Résultat_Lead_Vichy_Clean.pdf"
    
    try:
        debut = os.getenv("START_PAGE")
        fin = os.getenv("END_PAGE")
        
        extraire_pages_pdf(fichier_source, fichier_sortie, debut, fin)
    except Exception as e:
        print(f"Error: {e}")
