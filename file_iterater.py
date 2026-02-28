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
        folder_path = os.path.expanduser(folder_path)
        if is_valid_folder_path(folder_path):
            return os.path.abspath(folder_path)
        print("Invalid folder path. Please enter an existing directory path.")

def list_files_sorted_oldest_first(folder_path):
    entries = []
    with os.scandir(folder_path) as it:
        for e in it:
            if e.is_file():
                try:
                    t = e.stat().st_mtime
                except OSError:
                    continue
                entries.append((t, e.name))
    entries.sort(key=lambda x: x[0])
    return [name for _, name in entries]

def build_new_name(prefix, index, old_filename):
    base, ext = os.path.splitext(old_filename)
    return f"{prefix}_{index}{ext}"

def rename_all_files_in_folder(folder_path, prefix):
    files = list_files_sorted_oldest_first(folder_path)
    if not files:
        print("No files found in the folder. Folder empty!")
        return

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
        os.replace(src, dst)

def main():
    welcome()
    folder_path = get_folder_path()
    file_prefix = get_file_prefix()
    rename_all_files_in_folder(folder_path, file_prefix)
    print("Work finished!")

if __name__ == "__main__":
    main()