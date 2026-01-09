# Calameo PDF Downloader & Extractor

Sometimes, on [Calaméo](https://www.calameo.com/), some publications cannot be downloaded directly to your computer. Users often try to use third-party tools like [Calameo PDF Downloader](https://calameo.pdf-downloader.com/), but the "Download as PDF" button is frequently broken or unreliable.

![Broken Download Button](broken_download_button.png)

**This project provides a "crafted" solution to this problem.** It allows you to automatically retrieve the pages displayed by the downloader service, even if the final download button fails, and reconstruct the PDF yourself.

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

2.  **Open this `.env` file** with a text editor and modify the values.

    **⚠️ IMPORTANT - How to get the `TARGET_URL`:**
    1.  Go to [Calameo PDF Downloader](https://calameo.pdf-downloader.com/index.php).
    2.  Paste the link of the Calaméo publication you want.
    3.  Click "Download" and wait for the page to load the document preview.
    4.  **Copy the URL from your browser's address bar** (it should look like `https://calameo.pdf-downloader.com/download.php?documentId=...`).
    5.  Paste this URL into `TARGET_URL` below.

```env
# The URL of the page where the document pages are displayed
TARGET_URL=your_url_here

# The first page to keep in the final PDF (or set to "ALL" to keep everything)
START_PAGE=32

# The last page to keep (inclusive) (or set to "ALL" to keep everything)
END_PAGE=176
```

## 💻 Usage

Once the `.env` file is configured, simply run the main script:

```bash
python main.py
```

The script will automatically:
1.  Download all images.
2.  Create a complete PDF (`calameo_result.pdf`).
3.  Delete temporary files.
4.  Create the final cleaned PDF with only the selected pages (`calameo_clean.pdf`).

*Note: The scripts `downloader.py` and `extract_pages.py` are still available if you need to run a single step manually.*

## ⚠️ Troubleshooting

- **The .env file is not read**: Make sure there is a dot at the beginning of the filename (`.env` and not `env` or `config.env`).
- **Page error**: If you request page 200 on a 100-page document, the extraction script will show an explicit error.
- **Missing images**: If the site changes its structure or requires complex authentication, simple downloading may fail. Check that the URL in `.env` is still valid.
