import os
import shutil
import requests
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def download_images_and_create_pdf(url, output_pdf_name="document_final.pdf"):
    if not url:
        print("Error: No URL provided. Check your .env file (TARGET_URL).")
        return

    # Create temporary folder
    download_folder = "images_temp"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Enhanced headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Referer': 'https://calameo.pdf-downloader.com/' 
    }

    print(f"Connecting to URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    print(f"{len(img_tags)} images found. Starting download and verification...")

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
            
            # --- IMAGE VERIFICATION ---
            try:
                image_data = BytesIO(img_response.content)
                test_img = Image.open(image_data)
                test_img.verify() # Verify file integrity
            except (IOError, UnidentifiedImageError):
                print(f"⚠️  Skipped image (Invalid file or not an image): {img_url}")
                continue
            
            # Save valid image
            filename = f"Image {counter}.jpg"
            filepath = os.path.join(download_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            downloaded_files.append(filepath)
            print(f"✅ Downloaded: {filename}")
            counter += 1
            
        except Exception as e:
            print(f"❌ Error on {img_url}: {e}")

    if not downloaded_files:
        print("No valid images downloaded.")
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)
        return

    print("\nConverting images to PDF...")
    
    images_objects = []
    # Numeric sort
    downloaded_files.sort(key=lambda x: int(os.path.basename(x).split('Image ')[1].split('.')[0]))

    for file in downloaded_files:
        try:
            img = Image.open(file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images_objects.append(img)
        except Exception as e:
            print(f"Error processing image {file} for PDF: {e}")

    if images_objects:
        try:
            images_objects[0].save(
                output_pdf_name, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=images_objects[1:]
            )
            print(f"\nSuccess! File '{output_pdf_name}' created.")
            
            for img in images_objects:
                img.close()
                
            print(f"Deleting temporary folder '{download_folder}'...")
            shutil.rmtree(download_folder)
            print("Temporary folder deleted.")
            
        except Exception as e:
            print(f"Error saving PDF or cleaning up: {e}")
    else:
        print("No valid images to convert to PDF.")
        if os.path.exists(download_folder):
            shutil.rmtree(download_folder)

if __name__ == "__main__":
    target_url = os.getenv("TARGET_URL")
    download_images_and_create_pdf(target_url, "Resultat_Calameo.pdf")
