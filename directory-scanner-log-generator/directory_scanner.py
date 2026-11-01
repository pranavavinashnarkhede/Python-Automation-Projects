import sys
import os
import time


def DirectoryScanner(DirectoryPath):

    # Validate the directory path
    if not os.path.isdir(DirectoryPath):
        print("Error: The specified directory does not exist.")
        return

    # Generate a unique log file name
    timestamp = time.ctime()
    LogFileName = "Marvellous%s.log" % (timestamp)

    LogFileName = LogFileName.replace(" ", "_")
    LogFileName = LogFileName.replace(":", "_")

    print("Log file gets created with name:", LogFileName)

    fobj = open(LogFileName, "w")

    fobj.write("Marvellous Automation Script\n")
    fobj.write("Files from the directory are:\n")

    TotalFiles = 0

    # Traverse the directory and its subdirectories
    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fname in FileName:
            fobj.write(fname + "\n")
            TotalFiles = TotalFiles + 1

    fobj.close()

    print("Directory scanning completed successfully.")
    print("Total files found:", TotalFiles)


def main():

    Border = "-" * 70

    print(Border)
    print("Marvellous Automation Script")
    print(Border)

    if len(sys.argv) == 2:

        if sys.argv[1] in ("--h", "--H"):
            print("This automation script is used to traverse a directory.")
            print("For better usage, please check the --u flag.")

        elif sys.argv[1] in ("--u", "--U"):
            print("Please execute the script as:")
            print("python directory_scanner.py DirectoryName")
            print("Directory name should be a valid directory path.")

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

