import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import kinos
    print(f"Successfully imported kinos. Location: {kinos.__file__}")
    print(f"Kinos package contents: {dir(kinos)}")
except ImportError as e:
    print(f"Failed to import kinos: {e}")

print("\nTrying to import kinos as a relative import:")
try:
    from . import kinos
    print("Successfully imported kinos as a relative import")
except ImportError as e:
    print(f"Failed to import kinos as a relative import: {e}")
except ValueError as e:
    print(f"ValueError when trying relative import: {e}")

print("\nTrying to import specific modules:")
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