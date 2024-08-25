import os
from typing import List, Set
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_files_in_directory(directory: str, exclude_dirs: Set[str] = set(), exclude_extensions: Set[str] = set()) -> List[str]:
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in filenames:
            if not any(filename.endswith(ext) for ext in exclude_extensions):
                files.append(os.path.join(root, filename))
    return files

def main(directories_to_scan: List[str], exclude_dirs: Set[str], exclude_extensions: Set[str]) -> List[str]:
    files_to_add = []
    for directory in directories_to_scan:
        logging.info(f"Scanning directory: {directory}")
        files_to_add.extend(get_files_in_directory(directory, exclude_dirs, exclude_extensions))
    return files_to_add

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan directories for files to add.")
    parser.add_argument("--directories", nargs="+", default=[
        "projet_redaction",
        "system/story_generation",
        "system/world_simulation",
        "system/interaction_engine",
        "assets",
        "ai_society",
        "cities"
    ], help="List of directories to scan")
    parser.add_argument("--exclude-dirs", nargs="*", default=[], help="Directories to exclude")
    parser.add_argument("--exclude-extensions", nargs="*", default=[], help="File extensions to exclude")
    args = parser.parse_args()

    files = main(args.directories, set(args.exclude_dirs), set(args.exclude_extensions))
    logging.info(f"Total files found: {len(files)}")
    print("Files to add:")
    for file in files:
        print(file)
