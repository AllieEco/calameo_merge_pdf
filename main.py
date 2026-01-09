import os
import time
from dotenv import load_dotenv
from downloader import download_images_and_create_pdf
from extract_pages import extraire_pages_pdf

# Load environment variables
load_dotenv()

def main():
    print("=== STARTING FULL PROCESS ===")
    
    # --- 1. Get configuration ---
    target_url = os.getenv("TARGET_URL")
    
    # Get raw values (str) to handle "ALL" case
    start_page = os.getenv("START_PAGE")
    end_page = os.getenv("END_PAGE")

    if not target_url or not start_page or not end_page:
        print("CRITICAL ERROR: Please check TARGET_URL, START_PAGE, and END_PAGE in your .env file.")
        return

    # Filenames
    pdf_complet = "Resultat_Calameo.pdf"
    pdf_final = "Resultat_Final_Clean.pdf"

    # --- 2. Start Download ---
    print(f"\n[STEP 1/2] Downloading from: {target_url[:50]}...")
    
    download_images_and_create_pdf(target_url, pdf_complet)

    # Small pause to ensure file system release
    time.sleep(1)

    if not os.path.exists(pdf_complet):
        print("\nERROR: The complete PDF was not created. Process aborted.")
        return

    # --- 3. Start Extraction ---
    print(f"\n[STEP 2/2] Processing pages ({start_page} to {end_page})...")
    
    extraire_pages_pdf(pdf_complet, pdf_final, start_page, end_page)

    print("\n=== PROCESS COMPLETED ===")

if __name__ == "__main__":
    main()
