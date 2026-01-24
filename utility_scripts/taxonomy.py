import os
import re
from collections import defaultdict

def parse_taxonomy(filepath):
    """
    Extrait les informations taxonomiques du chemin d'une image.
    
    Cette fonction extrait le nom du dossier parent de l'image, car le nom de
    l'image en elle-même ne contient pas d'informations taxonomiques.
    
    Exemple de chemin :
    train/train/00980_Animalia_Arthropoda_Insecta_Lepidoptera_Erebidae_Arctia_virginalis/464f3a34-4c04-4eb3-afa2-6cb7444c3fa3.jpg
    
    Taxon folder: 00980_Animalia_Arthropoda_Insecta_Lepidoptera_Erebidae_Arctia_virginalis
    
    Les informations sont séparées par '_'. Les éléments 0 (ID), 1, 2, 3 (constantes)
    ne nous intéressent pas. Nous créons un dictionnaire avec :
    - ordre : élément 4 (ex: Lepidoptera)
    - famille : élément 5 (ex: Erebidae)
    - genre : élément 6 (ex: Arctia)
    - espece : élément 7 (ex: virginalis)
    
    Args:
        filepath: Chemin complet de l'image
        
    Returns:
        Dictionnaire avec les clés 'ordre', 'famille', 'genre', 'espece' ou None si échec
    """
    match = re.search(r'([^/]+)/[^/]+\.jpg$', filepath)
    if not match:
        print(f"Regex ne correspond pas : {filepath}")
        return None
    folder = match.group(1)
    taxonomy_path = folder.split('_')
    if len(taxonomy_path) >= 7:
        return {
            'ordre': taxonomy_path[4],  
            'famille': taxonomy_path[5],
            'genre': taxonomy_path[6],
            'espece': taxonomy_path[7]
        }
    return None

def parse_taxonomy_folders(folder_path):
    """
    Parse la taxonomie depuis les noms des dossiers dans un répertoire.
    
    Parcourt récursivement le dossier donné et applique parse_taxonomy à chaque
    sous-dossier (en simulant un fichier image.jpg virtuel pour extraire la taxonomie).
    Regroupe les espèces rencontrées et liste les dossiers non parsables.
    
    Args:
        folder_path: Chemin du dossier racine à analyser
        
    Returns:
        Tuple (species_encountered, unparsed):
        - species_encountered: dict[str, list] où clé = nom d'espèce, valeur = liste de (dossier, hiérarchie)
        - unparsed: list des chemins de dossiers non parsables
    """
    unparsed = []
    species_encountered = defaultdict(list)
    for root, dirs_, files in os.walk(folder_path):
        for d in dirs_:
            hier = parse_taxonomy(d + "/image.jpg")
            if hier:
                species_name = hier['espece']
                species_encountered[species_name].append((d, hier))
            else:
                unparsed.append(os.path.join(root, d))
    return species_encountered, unparsed