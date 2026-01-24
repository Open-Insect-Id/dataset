import os
import re
from collections import defaultdict

def parse_taxonomy(filepath):
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
    """Parse taxonomie depuis noms dossiers (image.jpg virtuel)."""
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