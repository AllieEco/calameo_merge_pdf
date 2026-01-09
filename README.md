# Calameo PDF Downloader & Extractor

This project allows you to automatically download all images from an online document. It has been specifically designed to work with **[Calameo PDF Downloader](https://calameo.pdf-downloader.com/)**.

It downloads the images, converts them into a complete PDF file, and then extracts a specific range of pages into a second, cleaned-up PDF.

## 📋 Prerequisites

- **Python 3** must be installed on your machine.
- An internet connection.

## 🚀 Installation

1. **Open your terminal** in the project folder.
2. **Install the dependencies** using the following command:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

The project uses a configuration file to define the download URL and the pages to keep.

1.  **Copy the example file** `env.example` and rename it to `.env`:
    
    ```bash
    cp env.example .env
    # Or rename it manually
    ```

2.  **Open this `.env` file** with a text editor and modify the values according to your needs:

```env
# The exact URL of the download page where the images are located
TARGET_URL=your_url_here

# The first page to keep in the final PDF
START_PAGE=32

# The last page to keep (inclusive)
END_PAGE=176
```

## 💻 Usage

Once the `.env` file is configured, simply run the main script:

```bash
python main.py
```

The script will automatically:
1.  Download all images.
2.  Create a complete PDF (`Resultat_Calameo.pdf`).
3.  Delete temporary files.
4.  Create the final cleaned PDF with only the selected pages (`Resultat_Final_Clean.pdf`).

*Note: The scripts `downloader.py` and `extract_pages.py` are still available if you need to run a single step manually.*

## ⚠️ Troubleshooting

- **The .env file is not read**: Make sure there is a dot at the beginning of the filename (`.env` and not `env` or `config.env`).
- **Page error**: If you request page 200 on a 100-page document, the extraction script will show an explicit error.
- **Missing images**: If the site changes its structure or requires complex authentication, simple downloading may fail. Check that the URL in `.env` is still valid.
