import os
import json
from collections import defaultdict

def build_taxa_maps(species_encountered, annotated_images, train_mini_folder):
    """
    Construit les mappings taxonomiques et géographiques complets.
    
    À partir des espèces rencontrées et des annotations géographiques,
    crée un mapping de taxons (clé = tuple (ordre, famille, genre, espèce))
    vers la hiérarchie, et une base de données géographique associant
    chaque taxon à ses coordonnées (lat, lon) issues des images annotées.
    
    Args:
        species_encountered: dict[str, list] des espèces (de parse_taxonomy_folders)
        annotated_images: dict[str, tuple] chemin relatif -> (lat, lon)
        train_mini_folder: chemin du dossier train_mini
        
    Returns:
        Tuple (full_taxa_map, full_geo_db):
        - full_taxa_map: dict[tuple, dict] taxon -> hiérarchie
        - full_geo_db: dict[tuple, list] taxon -> liste de [lat, lon]
    """
    full_taxa_map = {}
    full_geo_db = defaultdict(list)
    
    for species_name, occurrences in species_encountered.items():
        for d, hier in occurrences:
            taxon_key = (hier['ordre'], hier['famille'], hier['genre'], species_name)
            if taxon_key not in full_taxa_map:
                full_taxa_map[taxon_key] = hier
            
            taxon_folder = os.path.join(train_mini_folder, d)
            if os.path.exists(taxon_folder):
                _, _, files = next(os.walk(taxon_folder))
                seen_rel_paths = set()
                for f in files:
                    rel_path = f"train_mini/{d}/{f}"
                    if rel_path in annotated_images and rel_path not in seen_rel_paths:
                        lat, lon = annotated_images[rel_path]
                        if lat != 0.0 and lon != 0.0:
                            full_geo_db[taxon_key].append([lat, lon])
                            seen_rel_paths.add(rel_path)
    
    return full_taxa_map, full_geo_db

def save_hierarchy_map(full_taxa_map, full_geo_db, stats, output_file):
    """
    Sauvegarde la hiérarchie taxonomique et les données géographiques dans un fichier JSON.
    
    Sérialise les mappings et statistiques pour une utilisation ultérieure,
    par exemple dans les datasets hiérarchiques.
    
    Args:
        full_taxa_map: dict[tuple, dict] des taxons
        full_geo_db: dict[tuple, list] des coordonnées
        stats: dict des statistiques
        output_file: chemin du fichier JSON de sortie
    """
    full_geo_serializable = {str(k): [[float(c[0]), float(c[1])] for c in v] 
                            for k, v in full_geo_db.items()}
    
    with open(output_file, 'w') as f:
        json.dump({
            'full_taxa_map': {str(k): v for k, v in full_taxa_map.items()},
            'full_geo_db': full_geo_serializable,
            'stats': stats
        }, f, indent=2)
    print(f"💾 Sauvegardé: {len(full_taxa_map)} taxons dans {output_file}")

def build_hierarchy_labels(data_dir, hierarchy_map_file):
    """
    Construit le mapping des indices ImageFolder vers les labels hiérarchiques.
    
    À partir des classes ImageFolder et de la hiérarchie sauvegardée,
    crée un dictionnaire associant chaque index de classe à une liste
    [ordre_id, famille_id, genre_id, espece_id] pour l'entraînement hiérarchique.
    
    Args:
        data_dir: répertoire des données (contient train_mini)
        hierarchy_map_file: fichier JSON de la hiérarchie
        
    Returns:
        dict[int, list]: mapping index -> labels hiérarchiques
    """
    
    # 1. Scan dossiers → classes ImageFolder
    train_path = os.path.join(data_dir, 'train_mini/train_mini')
    class_names = sorted([d for d in os.listdir(train_path) 
                         if os.path.isdir(os.path.join(train_path, d))])
    class_to_idx = {name: i for i, name in enumerate(class_names)}
    print(f"Classes: {len(class_to_idx)} (scan {train_path})")
    
    # 2. Hiérarchie depuis JSON
    with open(hierarchy_map_file) as f:
        data = json.load(f)
    
    full_taxa_map_str = data['full_taxa_map']
    unique_ordres = set()
    unique_familles = set()
    unique_genres = set()
    
    for taxon_str, hier in full_taxa_map_str.items():
        parts = taxon_str.strip("('").strip("')").split("', '")
        if len(parts) == 4:
            unique_ordres.add(parts[0])
            unique_familles.add(parts[1])
            unique_genres.add(parts[2])
    
    ordre_to_id = {name: i for i, name in enumerate(sorted(unique_ordres))}
    famille_to_id = {name: i for i, name in enumerate(sorted(unique_familles))}
    genre_to_id = {name: i for i, name in enumerate(sorted(unique_genres))}
    
    print(f"Hiérarchie: {len(ordre_to_id)} ordres, {len(famille_to_id)} fam., {len(genre_to_id)} genres")
    
    # 3. Mapping
    final_hierarchy = {}
    mapped = 0
    
    for class_name, class_idx in class_to_idx.items():
        parts = class_name.split('_')
        if len(parts) >= 4:
            ordre, famille, genre, espece = parts[-4:]
            
            taxon_key_str = f"('{ordre}', '{famille}', '{genre}', '{espece}')"
            
            if taxon_key_str in full_taxa_map_str:
                hier = full_taxa_map_str[taxon_key_str]
                final_hierarchy[class_idx] = [
                    ordre_to_id[hier['ordre']],
                    famille_to_id[hier['famille']],
                    genre_to_id[hier['genre']],
                    class_idx
                ]
                mapped += 1
            else:
                if mapped == 0:
                    print(f"DEBUG: clé générée '{taxon_key_str}' non trouvée.")
                    print(f"Exemple clé JSON: {list(full_taxa_map_str.keys())[0]}")
    
    print(f"✅ {mapped}/{len(class_to_idx)} mappées")
    
    # Sauvegarde
    with open('hierarchy_labels.json', 'w') as f:
        json.dump({
            'class_to_idx': class_to_idx,
            'final_hierarchy': final_hierarchy,  # {0: [2, 45, 123, 0], 1: [3, 46, 124, 1], ...}
            'id_to_name': {
                'ordre': {i: name for name, i in ordre_to_id.items()},
                'famille': {i: name for name, i in famille_to_id.items()},
                'genre': {i: name for name, i in genre_to_id.items()}
            },
            'stats': {
                'ordres': len(ordre_to_id),
                'familles': len(famille_to_id),
                'genres': len(genre_to_id),
                'total_classes': len(class_to_idx),
                'mapped': mapped
            }
        }, f, indent=2)
    
    print("💾 hierarchy_labels.json prêt pour training")
    return final_hierarchy

# === USAGE ===
data_dir = '/kaggle/input/inaturalist-insects/'
hierarchy_map_file = '/kaggle/working/hierarchy_map.json'
final_hierarchy = build_hierarchy_labels(data_dir, hierarchy_map_file)

print("\nExemples:")
for idx in range(25):
    labels = final_hierarchy.get(idx)
    print(f"Class {idx}: {labels}") # [ordre_id, famille_id, genre_id, espece_id]