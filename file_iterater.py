import os
import re

def welcome():
    print("Welcome to the file iterater!")
    print("Your files will be renamed and iterated starting with the oldest created file according to time.")
    print("File prefix --> e.g. (Holiday, Vacation, ...)")
    print("This will result in your files beeing renamed to Holiday_1, Holiday_2, etc.")

def is_valid_prefix_boolean(prefix):
    return bool(prefix) and re.fullmatch(r"[A-Za-z0-9_-]+", prefix) is not None

def is_valid_folder_path(path):
    if not path:
        return False
    path = os.path.expanduser(path.strip())
    return os.path.isdir(path)

def get_file_prefix():
    while True:
        file_prefix = input("Type your file prefix: ").strip()
        if is_valid_prefix_boolean(file_prefix):
            return file_prefix
        print("Invalid prefix. Use only letters, numbers, '-' or '_' and do not leave it empty.")

def get_folder_path():
    while True:
        folder_path = input("Type the folder path (e.g. folder): ").strip()
        folder_path = folder_path.strip("'\"")
        folder_path = os.path.expanduser(folder_path)
        if is_valid_folder_path(folder_path):
            return os.path.abspath(folder_path)
        print("Invalid folder path. Please enter an existing directory path.")

def list_items(folder_path):
    files = []
    skipped_hidden_files = []
    found_dirs = []

    with os.scandir(folder_path) as it:
        for e in it:
            name = e.name
            if e.is_dir():
                found_dirs.append(name)
                continue

            if not e.is_file():
                continue

            if name.startswith("."):
                skipped_hidden_files.append(name)
                continue

            try:
                t = e.stat().st_mtime
            except OSError:
                continue

            files.append((t, name))

    files.sort(key=lambda x: x[0])
    return [name for _, name in files], found_dirs, skipped_hidden_files

def build_new_name(prefix, index, old_filename):
    base, ext = os.path.splitext(old_filename)
    return f"{prefix}_{index}{ext}"

def rename_all_files_in_folder(folder_path, prefix):
    files, found_dirs, skipped_hidden_files = list_items(folder_path)

    skipped_rename = []
    renamed = 0

    if not files:
        print("No renameable files found in the folder.")
        return {
            "renamed": renamed,
            "found_dirs": found_dirs,
            "skipped_hidden_files": skipped_hidden_files,
            "skipped_rename": skipped_rename,
        }

    planned = []
    used = set(files)

    for i, old_name in enumerate(files, start=1):
        new_name = build_new_name(prefix, i, old_name)

        if new_name in used:
            k = 2
            candidate = new_name
            while candidate in used:
                base, ext = os.path.splitext(new_name)
                candidate = f"{base}__{k}{ext}"
                k += 1
            new_name = candidate

        planned.append((old_name, new_name))
        used.add(new_name)

    for old_name, new_name in planned:
        src = os.path.join(folder_path, old_name)
        dst = os.path.join(folder_path, new_name)
        try:
            os.replace(src, dst)
            renamed += 1
        except OSError:
            skipped_rename.append(old_name)

    return {
        "renamed": renamed,
        "found_dirs": found_dirs,
        "skipped_hidden_files": skipped_hidden_files,
        "skipped_rename": skipped_rename,
    }

def print_summary(summary):
    found_dirs = summary["found_dirs"]
    skipped_hidden_files = summary["skipped_hidden_files"]
    skipped_rename = summary["skipped_rename"]
    renamed = summary["renamed"]

    print()
    print("Summary:")
    print(f"Renamed files: {renamed}")

    if found_dirs:
        print(f"Folders found (NOT renamed): {len(found_dirs)}")
        for d in sorted(found_dirs):
            print(f" - {d}")
    else:
        print("Folders found (NOT renamed): 0")

    if skipped_hidden_files:
        print(f"Hidden files skipped (NOT renamed): {len(skipped_hidden_files)}")
        for f in sorted(skipped_hidden_files):
            print(f" - {f}")
    else:
        print("Hidden files skipped (NOT renamed): 0")

    if skipped_rename:
        print(f"Files that could NOT be renamed: {len(skipped_rename)}")
        for f in skipped_rename:
            print(f" - {f}")
    else:
        print("Files that could NOT be renamed: 0")

def main():
    welcome()
    folder_path = get_folder_path()
    file_prefix = get_file_prefix()
    summary = rename_all_files_in_folder(folder_path, file_prefix)
    print_summary(summary)
    print()
    print("Work finished!")

if __name__ == "__main__":
    main()