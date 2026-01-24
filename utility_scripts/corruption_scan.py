import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

def verify_image_validity(full_path):
    """Test PROGRESIF + debug."""
    try:
        if not os.path.exists(full_path):
            return False, "FILE_MISSING"
        
        with Image.open(full_path) as img:
            img.verify()
        
        img = Image.open(full_path).convert('RGB')
        img.thumbnail((64, 64))
        img = img.resize((224, 224))
        
        return True, None
    except Exception as e:
        return False, str(type(e).__name__) + ": " + str(e)[:50]
    
def scan_corrupted_images(root_folder, max_workers=4):
    start_time = time.time()
    
    image_paths = []
    for root, _, files in os.walk(root_folder):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg')):  # JPG seulement
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, root_folder)
                image_paths.append(rel_path)
    
    total_files = len(image_paths)
    print(f"Scan {total_files} JPG dans {root_folder}")
    
    if total_files == 0:
        return [], f"/kaggle/working/corrupted_{os.path.basename(root_folder)}.txt"
    
    corrupted = []
    error_types = defaultdict(int)
    
    # ThreadPool (fichiers I/O)
    full_paths = [os.path.join(root_folder, p) for p in image_paths]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(verify_image_validity, fp): fp for fp in full_paths}
        
        for future in as_completed(futures):
            fp = futures[future]
            is_valid, error = future.result()
            
            if not is_valid:
                rel_path = os.path.relpath(fp, root_folder)
                corrupted.append(rel_path)
                error_types[error] += 1
                if len(corrupted) < 10:  # 10 premiers
                    print(f"❌ {rel_path[:50]}: {error}")
    
    # Stats erreurs
    print("\nTYPES D'ERREURS:")
    for err, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {err}: {count}")
    
    # Sauvegarde
    output_file = f"/kaggle/working/corrupted_{os.path.basename(root_folder)}.txt"
    rate = len(corrupted) / total_files * 100
    
    with open(output_file, 'w') as f:
        f.write(f"# Corrompus: {len(corrupted)}/{total_files} ({rate:.1f}%)\n")
        f.write("# Erreurs:\n")
        for err, count in error_types.items():
            f.write(f"# {err}: {count}\n")
        f.write("\n")
        for path in corrupted:
            f.write(path + '\n')
    
    elapsed = time.time() - start_time
    print(f"✅ {len(corrupted)}/{total_files} ({rate:.1f}%) en {elapsed:.1f}s")
    
    return corrupted, output_file