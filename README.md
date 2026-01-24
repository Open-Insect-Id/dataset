# Open-Insect-ID Dataset

Ce dépôt contient le dataset et les outils pour le projet **Open-Insect-ID**, qui se concentre sur l'identification d'insectes à l'aide de l'intelligence artificielle et de l'apprentissage automatique.

## Contexte du Projet

Le projet vise à classifier des images d'insectes selon une **hiérarchie taxonomique** précise :
- **Ordre** (ex: Lepidoptera - papillons)
- **Famille** (ex: Erebidae)
- **Genre** (ex: Arctia)
- **Espèce** (ex: virginalis)

Cette approche hiérarchique permet de **réduire l'impact des erreurs** : si le modèle se trompe sur l'espèce, l'ordre et la famille ont de fortes chances d'être corrects.

## Structure du Dépôt

### Données
- `train/` : Images et annotations d'entraînement
- `val/` : Images et annotations de validation
- `train_mini/` : Petit ensemble d'entraînement pour les tests rapides
- `public_test/` : Ensemble de test public

### Scripts Utilitaires (`utility_scripts/`)
- `tree.py` : Parcours récursif des dossiers pour vérifier l'intégrité du transfert
- `taxonomy.py` : Extraction des informations taxonomiques depuis les noms de dossiers
- `mapping.py` : Construction des mappings taxonomiques et géographiques
- `corruption_scan.py` : Détection des images corrompues (problème majeur identifié post-transfert)

### Notebooks (`notebooks/`)
- `open-insect-id-notebook.ipynb` : Notebook principal pour l'entraînement et l'analyse
- `utility_scripts/utility_scripts.ipynb` : Notebook contenant tout le code des utilitaires

### Scripts (`scripts/`)
- `install.sh` / `install.bat` : Scripts d'installation
- `main.py` : Script principal (si applicable)

### Données (`data/`)
- `hierarchy_map.json` : Mapping hiérarchique généré
- `tree.txt` : Structure des dossiers
- `output/` : Sorties diverses

### Logs (`logs/`)
- Fichiers de logs des dossiers supprimés/corrompus

### Configuration
- `requirements.txt` : Dépendances Python
- `scripts/install.sh` / `scripts/install.bat` : Scripts d'installation pour Linux/Mac et Windows
- `docs/NOTEBOOK_README.md` : Documentation détaillée du notebook et des fonctions

## Installation

### Prérequis
- Python 3.8+
- pip

### Installation Automatique
```bash
# Linux/Mac
./scripts/install.sh

# Windows
scripts/install.bat
```

### Installation Manuelle
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Utilisation

### Pour Kaggle
1. Ajoutez ce dépôt comme dataset dans votre notebook Kaggle
2. Le notebook `notebooks/open-insect-id-notebook.ipynb` contient tout le code nécessaire
3. Les utilitaires sont automatiquement copiés depuis `/kaggle/input/dataset/utility_scripts/`

### Localement
1. Clonez le dépôt
2. Exécutez les scripts d'installation
3. Utilisez le notebook ou les scripts Python directement

## Fonctionnalités Clés

### Classification Hiérarchique
Au lieu de prédire uniquement l'espèce (risque d'erreur élevé), le modèle prédit simultanément :
- Ordre → Famille → Genre → Espèce

### Gestion des Images Corrompues
Suite à des interruptions d'Internet lors de l'upload, certaines images étaient corrompues. Le système :
- Détecte automatiquement les images corrompues
- Les exclut de l'entraînement (car les inputs Kaggle sont en lecture seule)

### Extraction Taxonomique
Les informations taxonomiques sont extraites directement des noms de dossiers :
```
00980_Animalia_Arthropoda_Insecta_Lepidoptera_Erebidae_Arctia_virginalis/
```
→ `{'ordre': 'Lepidoptera', 'famille': 'Erebidae', 'genre': 'Arctia', 'espece': 'virginalis'}`

## Architecture du Modèle

Le modèle utilise **MobileNetV3 Large** avec des têtes de classification séparées pour chaque niveau taxonomique, permettant une prédiction hiérarchique efficace.

## Métriques et Évaluation

- Précision par niveau taxonomique
- Réduction de l'impact des erreurs grâce à la hiérarchie
- Couverture géographique des espèces

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou des pull requests.

## Source du Dataset

Ce dataset est dérivé de la compétition **iNaturalist 2021** organisée par Visipedia :
- **Source originale** : [iNaturalist 2021 Competition](https://github.com/visipedia/inat_comp/tree/master/2021)
- **Licence des données** : Les données iNaturalist sont généralement sous licence CC BY-NC (Creative Commons Attribution-NonCommercial)
- **Filtrage** : Seules les images d'insectes ont été conservées pour ce projet

## Licence

Ce projet est sous licence **MIT** pour le code et les scripts. Les données elles-mêmes sont soumises à la licence de la source originale (iNaturalist).

```
MIT License

Copyright (c) 2026 Open-Insect-ID

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```