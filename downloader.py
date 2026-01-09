import os
import shutil
import requests
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

def download_images_and_create_pdf(url, output_pdf_name="document_final.pdf"):
    if not url:
        print("Erreur : Aucune URL fournie. Vérifiez votre fichier .env (TARGET_URL).")
        return

    # Création d'un dossier temporaire pour les images
    download_folder = "images_temp"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Headers améliorés pour ressembler encore plus à un vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Referer': 'https://calameo.pdf-downloader.com/' 
    }

    print(f"Connexion à l'URL : {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'accès à la page : {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    print(f"{len(img_tags)} images trouvées. Début du téléchargement et de la vérification...")

    downloaded_files = []
    
    counter = 1
    for img in img_tags:
        img_url = img.get('src')
        
        if not img_url:
            continue

        if not img_url.startswith('http'):
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            else:
                continue 

        try:
            img_response = requests.get(img_url, headers=headers, timeout=10)
            img_response.raise_for_status()
            
            # --- VÉRIFICATION DE L'IMAGE ---
            # On essaie de lire l'image en mémoire avant de l'enregistrer
            try:
                image_data = BytesIO(img_response.content)
                test_img = Image.open(image_data)
                test_img.verify() # Vérifie que le fichier n'est pas corrompu
            except (IOError, UnidentifiedImageError):
                print(f"⚠️  Image ignorée (Fichier invalide ou non-image) : {img_url}")
                continue
            
            # Si on arrive ici, l'image est valide. On l'enregistre.
            filename = f"Image {counter}.jpg"
            filepath = os.path.join(download_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            downloaded_files.append(filepath)
            print(f"✅ Téléchargé : {filename}")
            counter += 1
            
        except Exception as e:
            print(f"❌ Erreur sur {img_url} : {e}")

    if not downloaded_files:
        print("Aucune image valide n'a été téléchargée.")
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)
        return

    print("\nConversion des images en PDF...")
    
    images_objects = []
    # Tri numérique
    downloaded_files.sort(key=lambda x: int(os.path.basename(x).split('Image ')[1].split('.')[0]))

    for file in downloaded_files:
        try:
            img = Image.open(file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images_objects.append(img)
        except Exception as e:
            print(f"Erreur lors du traitement de l'image {file} pour le PDF : {e}")

    if images_objects:
        try:
            images_objects[0].save(
                output_pdf_name, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=images_objects[1:]
            )
            print(f"\nSuccès ! Le fichier '{output_pdf_name}' a été créé.")
            
            for img in images_objects:
                img.close()
                
            print(f"Suppression du dossier temporaire '{download_folder}'...")
            shutil.rmtree(download_folder)
            print("Dossier temporaire supprimé.")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du PDF ou du nettoyage : {e}")
    else:
        print("Aucune image valide à convertir en PDF.")
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)

if __name__ == "__main__":
    target_url = os.getenv("TARGET_URL")
    download_images_and_create_pdf(target_url, "Resultat_Calameo.pdf")
