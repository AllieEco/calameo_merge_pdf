# Outil de Téléchargement et d'Extraction PDF Calameo

Ce projet permet de télécharger automatiquement toutes les images d'un document en ligne. Il a été spécifiquement conçu pour fonctionner avec le site **[Calameo PDF Downloader](https://calameo.pdf-downloader.com/)**.

Il télécharge les images, les convertit en un fichier PDF complet, puis permet d'extraire une plage de pages spécifique dans un second PDF nettoyé.

## 📋 Prérequis

- **Python 3** doit être installé sur votre machine.
- Une connexion internet.

## 🚀 Installation

1. **Ouvrez votre terminal** dans le dossier du projet.
2. **Installez les dépendances** nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Le projet utilise un fichier de configuration pour définir l'URL à télécharger et les pages à garder.

1. Assurez-vous d'avoir un fichier nommé `.env` à la racine du projet.
   *(Si vous avez un fichier `env` sans point, renommez-le en `.env`)*.

2. Ouvrez ce fichier `.env` avec un éditeur de texte et modifiez les valeurs selon vos besoins :

```env
# L'URL exacte de la page de téléchargement où se trouvent les images
TARGET_URL=votre_url_ici

# La première page à conserver dans le PDF final
START_PAGE=32

# La dernière page à conserver (incluse)
END_PAGE=176
```

## 💻 Utilisation

Une fois le fichier `.env` configuré, lancez simplement le script principal :

```bash
python main.py
```

Le script va automatiquement :
1.  Télécharger toutes les images.
2.  Créer un PDF complet (`Resultat_Calameo.pdf`).
3.  Supprimer les fichiers temporaires.
4.  Créer le PDF final nettoyé avec uniquement les pages sélectionnées (`Resultat_Final_Clean.pdf`).

*Note : Les scripts `downloader.py` et `extract_pages.py` existent toujours si vous avez besoin d'exécuter une seule étape manuellement.*

## ⚠️ En cas de problème

- **Le fichier .env n'est pas lu** : Vérifiez bien qu'il y a un point au début du nom de fichier (`.env` et non `env` ou `config.env`).
- **Erreur de pages** : Si vous demandez la page 200 sur un document de 100 pages, le script d'extraction vous affichera une erreur explicite.
- **Images manquantes** : Si le site change sa structure ou nécessite une authentification complexe, le téléchargement simple peut échouer. Vérifiez que l'URL dans le `.env` est toujours valide.

