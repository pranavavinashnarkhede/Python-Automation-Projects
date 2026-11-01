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


def DirectoryScanner(DirectoryPath):

    # Validate the directory path
    if not os.path.isdir(DirectoryPath):
        print("Error: The specified directory does not exist.")
        return

    # Generate a timestamp-based log filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    LogFileName = "DirectoryScan_%s.log" % timestamp

    print("Log file gets created with name:", LogFileName)

    fobj = open(LogFileName, "w", encoding="utf-8")

    fobj.write("Marvellous Automation Script\n")
    fobj.write("Directory: " + os.path.abspath(DirectoryPath) + "\n")
    fobj.write("=" * 70 + "\n\n")
    fobj.write("Files found:\n\n")

    TotalFiles = 0

    # Traverse the directory and record file information
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

    # Add extension statistics to the log
    DisplayExtensionStatistics(DirectoryPath, LogFileName)

    print("Log file saved as:", LogFileName)


def main():

    Border = "-" * 70

    print(Border)
    print("Marvellous Automation Script")
    print(Border)

    if len(sys.argv) == 2:

        if sys.argv[1] in ("--h", "--H"):
            print("This automation script is used to scan a directory.")
            print("For usage instructions, please use the --u flag.")

        elif sys.argv[1] in ("--u", "--U"):
            print("Usage:")
            print("python directory_scanner.py DirectoryPath")
            print("Provide a valid directory path.")

        else:
            DirectoryScanner(sys.argv[1])

    else:
        print("Invalid number of arguments.")
        print("Please use --h or --u for more information.")

    print(Border)
    print("Thank you for using Marvellous Automation Script")
    print(Border)


if __name__ == "__main__":
    main()

