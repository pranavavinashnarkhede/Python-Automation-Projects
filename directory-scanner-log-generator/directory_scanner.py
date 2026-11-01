import sys
import os
import time


def DirectoryScanner(DirectoryPath):

    # Validate the directory path
    if not os.path.isdir(DirectoryPath):
        print("Error: The specified directory does not exist.")
        return

    # Generate a timestamp-based log filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    LogFileName = "DirectoryScan_%s.log" % (timestamp)

    print("Log file gets created with name:", LogFileName)

    fobj = open(LogFileName, "w", encoding="utf-8")

    fobj.write("Marvellous Automation Script\n")
    fobj.write("Directory: " + os.path.abspath(DirectoryPath) + "\n")
    fobj.write("=" * 70 + "\n\n")
    fobj.write("Files found:\n\n")

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

