# Directory Scanner and Log Generator

## Description

Directory Scanner and Log Generator is a Python automation project that scans a directory and generates a log report containing file information, extension statistics, and file category statistics.

It helps users inspect directory contents without checking each file manually.

## Features

* Scans directories and subdirectories.
* Validates the directory path.
* Records file names, paths, and sizes.
* Counts the total number of files.
* Generates file extension statistics.
* Categorizes files by type.
* Creates timestamped log reports.
* Supports command-line arguments.

## Technologies Used

* Python
* os module
* sys module
* time module

## Requirements

* Python 3.8 or later
* No external libraries required.

## How to Run

Run the following command:

```bash
python directory_scanner.py "C:\Users\YourName\Documents"
```

Replace the example path with the directory you want to scan.

To display help:

```bash
python directory_scanner.py --h
```

To display usage instructions:

```bash
python directory_scanner.py --u
```

## File Categories

The script categorizes files into the following groups:

* Documents
* Images
* Videos
* Audio
* Source Code
* Archives
* Other

## Output

The script generates a timestamped log file containing file details, total file count, extension statistics, and category statistics.

Example log filename:

```text
DirectoryScan_2026-11-02_15-30-00.log
```

## Concepts Learned

* Functions
* Loops and conditional statements
* Dictionaries and lists
* Directory traversal
* File handling
* Exception handling
* Command-line arguments
* File path operations

## Author

Pranav Avinash Narkhede
