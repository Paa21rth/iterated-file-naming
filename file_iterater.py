import os
import re

def rename_file(file_prefix):
    old_name = "old_file.txt"
    new_name = file_prefix + ".txt"
    os.rename(old_name, new_name)

def welcome():
    print("Welcome to the file iterater!")
    print("Your files will be renamed and iterated starting with the oldest created file according to time.")
    print("File prefix --> e.g. (Holiday, Vacation, ...)")
    print("This will result in your files beeing renamed to Holiday_1, Holiday_2, etc.")

def is_valid_prefix_boolean(prefix):
    if not prefix:
        return False
    if not re.fullmatch(r"[A-Za-z0-9_-]+", prefix):
        return False
    return True

def get_file_prefix():
    while True:
        file_prefix = input("Type your file prefix: ").strip()
        if is_valid_prefix_boolean(file_prefix):
            return file_prefix
        print("Invalid prefix. Use only letters, numbers, '-' or '_' and do not leave it empty.")

if __name__ == "__main__":
    welcome()
    file_prefix = get_file_prefix()
    rename_file(file_prefix)

    print("Work finished!")