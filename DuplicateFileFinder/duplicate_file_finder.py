import sys
import os
import hashlib


def CalculateCheckSum(FileName):
    """Calculate the MD5 checksum of a file."""

    try:
        # Open the file in binary read mode
        fobj = open(FileName, "rb")

        # Create an MD5 hash object
        hobj = hashlib.md5()

        # Read the file in chunks of 1024 bytes
        Buffer = fobj.read(1024)

        while len(Buffer) > 0:
            hobj.update(Buffer)
            Buffer = fobj.read(1024)

        fobj.close()

        # Return the calculated checksum
        return hobj.hexdigest()

    except OSError as e:
        print("Unable to read file:", FileName)
        print("Error:", e)
        return None


def FindDuplicate(DirectoryName):
    """Find files having identical checksums."""

    # Check whether the specified path exists
    Ret = os.path.exists(DirectoryName)

    if Ret == False:
        print("Path is invalid")
        return None

    # Check whether the specified path is a directory
    Ret = os.path.isdir(DirectoryName)

    if Ret == False:
        print("It is not a directory")
        return None

    # Store file checksums and their paths
    Duplicate = {}

    # Traverse the directory and its subdirectories
    for FolderName, SubFolder, FileName in os.walk(DirectoryName):

        for fname in FileName:

            # Generate the complete file path
            FilePath = os.path.join(FolderName, fname)

            # Calculate the file checksum
            Checksum = CalculateCheckSum(FilePath)

            # Skip files that could not be read
            if Checksum is None:
                continue

            # Group files having the same checksum
            if Checksum in Duplicate:
                Duplicate[Checksum].append(FilePath)
            else:
                Duplicate[Checksum] = [FilePath]

    return Duplicate


def DeleteDuplicate(DirectoryName):
    """Display duplicate files without deleting them."""

    # Find duplicate files
    MyDict = FindDuplicate(DirectoryName)

    # Stop if the directory is invalid
    if MyDict is None:
        return

    # Select groups containing more than one file
    Result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    TotalDuplicates = 0

    # Display duplicate file paths
    for value in Result:

        # Keep the first file and identify the remaining copies
        for subvalue in value[1:]:
            print("Duplicate found:", subvalue)
            TotalDuplicates += 1

    print("Total duplicate files found:", TotalDuplicates)


def main():
    """Main function of the program."""

    Border = "-" * 70

    print(Border)
    print("Duplicate File Finder")
    print(Border)

    if len(sys.argv) == 2:

        # Scan the directory provided by the user
        DeleteDuplicate(sys.argv[1])

    else:
        print("Invalid number of arguments")
        print("Usage: python duplicate_file_finder.py DirectoryName")

    print(Border)
    print("Thank you for using Duplicate File Finder")
    print(Border)


if __name__ == "__main__":
    main()
