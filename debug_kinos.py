import sys
import os
import site

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")
print(f"site-packages: {site.getsitepackages()}")

try:
    import kinos
    print(f"Successfully imported kinos. Location: {kinos.__file__}")
    print(f"Kinos package contents: {dir(kinos)}")
except ImportError as e:
    print(f"Failed to import kinos: {e}")
    print("Trying to import kinos modules individually:")
    try:
        from kinos import io
        print("Successfully imported kinos.io")
    except ImportError as e:
        print(f"Failed to import kinos.io: {e}")
    try:
        from kinos import main
        print("Successfully imported kinos.main")
    except ImportError as e:
        print(f"Failed to import kinos.main: {e}")

try:
    from kinos.__main__ import kinos_main
    print("Successfully imported kinos_main")
    kinos_main()
except ImportError as e:
    print(f"Failed to import kinos_main: {e}")

print("\nChecking individual files:")
kinos_dir = os.path.join(os.getcwd(), 'kinos')
for file in ['__init__.py', '__main__.py', 'main.py', 'io.py']:
    full_path = os.path.join(kinos_dir, file)
    if os.path.exists(full_path):
        print(f"{file} exists at {full_path}")
        with open(full_path, 'r') as f:
            print(f"First few lines of {file}:")
            print(f.read(200))
    else:
        print(f"{file} does not exist at {full_path}")

print("\nChecking egg-info:")
egg_info_dir = os.path.join(os.getcwd(), 'kinos.egg-info')
if os.path.exists(egg_info_dir):
    print(f"kinos.egg-info exists at {egg_info_dir}")
    for file in os.listdir(egg_info_dir):
        print(f"  {file}")
else:
    print("kinos.egg-info does not exist")