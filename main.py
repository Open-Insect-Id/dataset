import os
import shutil
import logging
import ijson
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_from_dataset(json_path, base_image_path, text, case_sensitive=False):
    logging.info(f"Début du traitement du dataset : {json_path} avec filtre '{text}'")
    
    total_images = 0
    with open(json_path, "r", encoding="utf-8") as f:
        for _ in ijson.items(f, 'images.item'):
            total_images += 1
    logging.info(f"Nombre total d'images dans le JSON : {total_images}")
    
    total_dossiers = len([d for d in os.listdir(base_image_path) if os.path.isdir(os.path.join(base_image_path, d))])
    logging.info(f"Nombre total de dossiers dans {base_image_path} : {total_dossiers}")
    
    dossiers_supprimes = set()
    images_supprimees = 0
    counter = 0
    
    with open(json_path, "r", encoding="utf-8") as f:
        for img in ijson.items(f, 'images.item'):
            file_path = img["file_name"]
            dossier = os.path.relpath(os.path.dirname(file_path), base_image_path)
            
            matches = text in dossier if case_sensitive else text.lower() in dossier.lower()
            if not matches:
                images_supprimees += 1
                dossiers_supprimes.add(dossier)
                logging.info(f"Image à supprimer du JSON : {file_path}")
            
            counter += 1
    
    logging.info(f"Nombre d'images à supprimer : {images_supprimees}")
    logging.info(f"Nombre de dossiers à supprimer : {len(dossiers_supprimes)}")
    
    txt_path = os.path.splitext(json_path)[0] + "_dossiers_supprimes.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for dossier in sorted(dossiers_supprimes):
            f.write(dossier + "\n")
    logging.info(f"Liste des dossiers à supprimer écrite dans : {txt_path}")
    
    for dossier in dossiers_supprimes:
        full_dossier = os.path.join(base_image_path, dossier)
        if os.path.isdir(full_dossier):
            try:
                shutil.rmtree(full_dossier)
                logging.info(f"Dossier supprimé : {dossier}")
            except Exception as e:
                logging.error(f"Erreur lors de la suppression du dossier {dossier} : {e}")
    
    jq_flags = 'i' if not case_sensitive else ''
    jq_command = f'jq \'.images |= map(select(.file_name | split("/") | .[1] | test("{text}"; "{jq_flags}")))\' "{json_path}" > "{json_path}.tmp" && mv "{json_path}.tmp" "{json_path}"'
    try:
        subprocess.run(jq_command, shell=True, check=True)
        logging.info("Filtrage du JSON terminé avec succès.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors du filtrage du JSON avec jq : {e}")
    
    logging.info("Traitement terminé.")

if __name__ == "__main__":
    json_list = ["train.json","val.json","train_mini.json"]
    folder_list = ["train","val","train_mini"]
    assert len(json_list)==len(folder_list)
    for elt in range(len(json_list)):
        remove_from_dataset(json_list[elt], folder_list[elt], "Insecta", case_sensitive=False)