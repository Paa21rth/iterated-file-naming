import os


def rename_files(directory, base_name, extension=""):
    """
    Rename all files in a directory with an iterated base name.

    :param directory: Path to the directory containing the files.
    :param base_name: Base name to use for renaming (e.g. 'holiday').
    :param extension: File extension to filter by (e.g. '.jpg'). Leave empty to rename all files.
    """
    files = sorted(
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and (not extension or f.endswith(extension))
    )

    for index, filename in enumerate(files, start=1):
        old_path = os.path.join(directory, filename)
        file_ext = os.path.splitext(filename)[1]
        new_filename = f"{base_name}_{index}{file_ext}"
        new_path = os.path.join(directory, new_filename)
        if os.path.exists(new_path) and old_path != new_path:
            print(f"Skipped: {filename} -> {new_filename} (destination already exists)")
            continue
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python file_iterater.py <directory> <base_name> [extension]")
        print("Example: python file_iterater.py ./photos holiday .jpg")
        sys.exit(1)

    directory = sys.argv[1]
    base_name = sys.argv[2]
    extension = sys.argv[3] if len(sys.argv) > 3 else ""

    rename_files(directory, base_name, extension)
