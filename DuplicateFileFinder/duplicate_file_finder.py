import sys
import os
import hashlib
import time


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


def GenerateDuplicateReport(DirectoryName, Result):
    """Generate a report containing duplicate file information."""

    # Generate a timestamp for the report filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    ReportFileName = "DuplicateReport_%s.txt" % timestamp

    TotalGroups = len(Result)
    TotalDuplicates = 0

    try:
        # Create the report file
        with open(ReportFileName, "w", encoding="utf-8") as fobj:

            fobj.write("Duplicate File Finder Report\n")
            fobj.write("Directory: " + os.path.abspath(DirectoryName) + "\n")
            fobj.write("=" * 70 + "\n\n")

            # Write each duplicate group
            GroupCount = 1

            for value in Result:

                fobj.write("Duplicate Group " + str(GroupCount) + "\n\n")

                # Display the first file as the original
                fobj.write("Original File: " + value[0] + "\n")

                # Display the remaining files as duplicates
                for subvalue in value[1:]:
                    fobj.write("Duplicate File: " + subvalue + "\n")
                    TotalDuplicates += 1

                fobj.write("-" * 70 + "\n\n")

                GroupCount += 1

            # Write final statistics
            fobj.write("Total Duplicate Groups: " + str(TotalGroups) + "\n")
            fobj.write("Total Duplicate Files: " + str(TotalDuplicates) + "\n")

        print("Duplicate report generated successfully.")
        print("Report saved as:", ReportFileName)

    except OSError as e:
        print("Unable to create duplicate report.")
        print("Error:", e)


def DeleteDuplicate(DirectoryName):
    """Display duplicate files and generate a report."""

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

    print("Total duplicate groups found:", len(Result))
    print("Total duplicate files found:", TotalDuplicates)

    # Generate a report containing duplicate information
    if len(Result) > 0:
        GenerateDuplicateReport(DirectoryName, Result)
    else:
        print("No duplicate files found.")
        print("Report not generated.")


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
