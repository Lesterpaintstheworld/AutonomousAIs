import os
import fnmatch
import subprocess
import sys

def install_playwright():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

def get_ignored_patterns():
    ignored_patterns = []
    for ignore_file in ['.gitignore', '.aiderignore']:
        if os.path.exists(ignore_file):
            with open(ignore_file, 'r') as f:
                ignored_patterns.extend(f.read().splitlines())
    return ignored_patterns

def list_files(startpath='.'):
    ignored_patterns = get_ignored_patterns()
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            if not any(fnmatch.fnmatch(os.path.join(root, file), pattern) for pattern in ignored_patterns):
                print(f'{subindent}{file}')
