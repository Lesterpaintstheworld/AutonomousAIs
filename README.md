# File Lister

This script scans a directory for files, optionally excluding specific directories and file extensions, and saves the list to a text file.

## Features

- Scan directories recursively
- Exclude specific directories and file extensions
- Save results to a text file
- Verbose mode to include file sizes
- Option to sort files by size

## Usage

```
python true.py [-h] [-o OUTPUT] [--exclude-dirs [EXCLUDE_DIRS ...]]
                [--exclude-extensions [EXCLUDE_EXTENSIONS ...]] [-v] [-s]
                directory
```

### Arguments

- `directory`: Directory to scan for files
- `-o OUTPUT, --output OUTPUT`: Output file name (default: files_to_add.txt)
- `--exclude-dirs [EXCLUDE_DIRS ...]`: Directories to exclude
- `--exclude-extensions [EXCLUDE_EXTENSIONS ...]`: File extensions to exclude
- `-v, --verbose`: Enable verbose output (includes file sizes)
- `-s, --sort-by-size`: Sort files by size (largest first)

### Examples

1. Basic usage:
   ```
   python true.py /path/to/directory
   ```

2. Exclude specific directories and file extensions:
   ```
   python true.py /path/to/directory --exclude-dirs .git __pycache__ --exclude-extensions .pyc .tmp
   ```

3. Use verbose mode and sort by size:
   ```
   python true.py /path/to/directory -v -s
   ```

4. Specify custom output file:
   ```
   python true.py /path/to/directory -o my_file_list.txt
   ```

## Requirements

- Python 3.6+

## License

This project is open source and available under the [MIT License](LICENSE).
