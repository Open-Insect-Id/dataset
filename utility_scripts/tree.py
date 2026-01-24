from pathlib import Path

def tree(
    path: str | Path,
    indent: int = 0,
    tree_file: str | Path = "tree.txt",
    _file=None,
) -> int:
    
    path = Path(path)
    file_count = 0
    subfolder_counts = []

    close_file = False
    if _file is None:
        _file = open(tree_file, "w", encoding="utf-8")
        close_file = True

    try:
        entries = list(path.iterdir())
    except FileNotFoundError:
        raise FileNotFoundError(f"Chemin introuvable : {path}")
    except PermissionError:
        return 0

    files = [e for e in entries if e.is_file()]
    dirs = [e for e in entries if e.is_dir()]

    file_count = len(files)

    for d in sorted(dirs, key=lambda p: p.name.lower()):
        sub_count = tree(
            d,
            indent=indent + 4,
            tree_file=tree_file,
            _file=_file,
        )
        subfolder_counts.append((d, sub_count))

    line = " " * indent + f"{path.name}/ [{file_count} fichiers]\n"
    if _file is not None:
        _file.write(line)

    for subfolder, sub_count in subfolder_counts:
        sub_line = " " * (indent + 2) + f"{subfolder.name}/ [{sub_count} fichiers]\n"
        if _file is not None:
            _file.write(sub_line)

    total_files = file_count + sum(count for _, count in subfolder_counts)

    if close_file and _file is not None:
        _file.close()

    return total_files