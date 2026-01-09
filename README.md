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

Le processus se déroule en deux étapes simples.

### Étape 1 : Téléchargement et Création du PDF Complet

Ce script va télécharger toutes les images une par une et générer un premier gros fichier PDF.

Exécutez la commande :

```bash
python downloader.py
```

*   **Résultat** : Un fichier `Resultat_Calameo.pdf` est créé, contenant l'intégralité du document.
*   *Note : Un dossier temporaire `images_temp` est créé pendant le processus.*

### Étape 2 : Extraction des Pages (Nettoyage)

Ce script va prendre le PDF complet généré juste avant et ne garder que les pages définies dans votre fichier `.env` (`START_PAGE` à `END_PAGE`).

Exécutez la commande :

```bash
python extract_pages.py
```

*   **Résultat** : Un fichier `Résultat_Lead_Vichy_Clean.pdf` est créé, ne contenant que les pages souhaitées.

## ⚠️ En cas de problème

- **Le fichier .env n'est pas lu** : Vérifiez bien qu'il y a un point au début du nom de fichier (`.env` et non `env` ou `config.env`).
- **Erreur de pages** : Si vous demandez la page 200 sur un document de 100 pages, le script d'extraction vous affichera une erreur explicite.
- **Images manquantes** : Si le site change sa structure ou nécessite une authentification complexe, le téléchargement simple peut échouer. Vérifiez que l'URL dans le `.env` est toujours valide.

