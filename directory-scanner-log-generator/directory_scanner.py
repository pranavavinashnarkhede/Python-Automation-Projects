import sys
import os
import time


def GetFileExtension(FileName):
    """Return the extension of a file."""

    Extension = os.path.splitext(FileName)[1].lower()

    if Extension == "":
        Extension = "No Extension"

    return Extension


def DisplayExtensionStatistics(DirectoryPath, LogFileName):
    """Count files by extension and append statistics to the log."""

    ExtensionCount = {}

    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fname in FileName:
            Extension = GetFileExtension(fname)

            if Extension in ExtensionCount:
                ExtensionCount[Extension] += 1
            else:
                ExtensionCount[Extension] = 1

    with open(LogFileName, "a", encoding="utf-8") as fobj:
        fobj.write("\n========== FILE EXTENSION STATISTICS ==========\n\n")

        for Extension, Count in sorted(ExtensionCount.items()):
            fobj.write(f"{Extension}: {Count} files\n")

        fobj.write(f"\nUnique file extensions: {len(ExtensionCount)}\n")

    print("File extension statistics added to the log.")


def DisplayFileCategoryStatistics(DirectoryPath, LogFileName):
    """Count files according to their categories."""

    FileCategories = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Source Code": [
            ".py", ".java", ".c", ".cpp", ".js", ".html", ".css"
        ],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    }

    CategoryCount = {}

    # Initialize each category with zero files
    for Category in FileCategories:
        CategoryCount[Category] = 0

    CategoryCount["Other"] = 0

    # Scan the directory and categorize files
    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fname in FileName:
            Extension = os.path.splitext(fname)[1].lower()

            FoundCategory = False

            for Category, Extensions in FileCategories.items():
                if Extension in Extensions:
                    CategoryCount[Category] += 1
                    FoundCategory = True
                    break

            if not FoundCategory:
                CategoryCount["Other"] += 1

    # Append category statistics to the log file
    with open(LogFileName, "a", encoding="utf-8") as fobj:
        fobj.write("\n========== FILE CATEGORY STATISTICS ==========\n\n")

        for Category, Count in CategoryCount.items():
            fobj.write(f"{Category}: {Count} files\n")

    print("File category statistics added to the log.")


def DirectoryScanner(DirectoryPath):
    """Scan a directory and generate a file report."""

    # Validate the directory path
    if not os.path.isdir(DirectoryPath):
        print("Error: The specified directory does not exist.")
        return

    # Generate a timestamp-based log filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    LogFileName = "DirectoryScan_%s.log" % timestamp

    print("Log file gets created with name:", LogFileName)

    # Create the log file and record file information
    fobj = open(LogFileName, "w", encoding="utf-8")

    fobj.write("Directory Scanner and Log Generator\n")
    fobj.write("Directory: " + os.path.abspath(DirectoryPath) + "\n")
    fobj.write("=" * 70 + "\n\n")
    fobj.write("FILES FOUND\n\n")

    TotalFiles = 0

    # Traverse the directory and its subdirectories
    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fname in FileName:
            FilePath = os.path.join(FolderName, fname)

            try:
                FileSize = os.path.getsize(FilePath)

                fobj.write("File Name: " + fname + "\n")
                fobj.write("File Path: " + os.path.abspath(FilePath) + "\n")
                fobj.write("File Size: " + str(FileSize) + " bytes\n")
                fobj.write("-" * 70 + "\n")

                TotalFiles += 1

            except OSError as e:
                print("Unable to access file:", FilePath)
                print("Error:", e)

    fobj.write("\nTotal Files Found: " + str(TotalFiles) + "\n")
    fobj.close()

    print("Directory scanning completed successfully.")
    print("Total files found:", TotalFiles)

    # Generate extension statistics
    DisplayExtensionStatistics(DirectoryPath, LogFileName)

    # Generate file category statistics
    DisplayFileCategoryStatistics(DirectoryPath, LogFileName)

    print("Log file saved as:", LogFileName)


def main():
    """Handle command-line arguments."""

    Border = "-" * 70

    print(Border)
    print("Directory Scanner and Log Generator")
    print(Border)

    if len(sys.argv) == 2:

        if sys.argv[1] in ("--h", "--H"):
            print("This script scans a directory and generates a log report.")
            print("Use --u for usage instructions.")

        elif sys.argv[1] in ("--u", "--U"):
            print("Usage:")
            print("python directory_scanner.py DirectoryPath")
            print("Example:")
            print('python directory_scanner.py "C:\\Users\\YourName\\Documents"')

        else:
            DirectoryScanner(sys.argv[1])

    else:
        print("Invalid number of arguments.")
        print("Use --h or --u for more information.")

    print(Border)
    print("Thank you for using Directory Scanner and Log Generator")
    print(Border)


if __name__ == "__main__":
    main()

