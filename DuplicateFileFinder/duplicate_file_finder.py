import sys
import os
import hashlib
import time


def CalculateCheckSum(FileName):
    """Calculate the MD5 checksum of a file."""

    try:
        # Open the file in binary read mode
        with open(FileName, "rb") as fobj:

            # Create an MD5 hash object
            hobj = hashlib.md5()

            # Read the file in chunks of 1024 bytes
            Buffer = fobj.read(1024)

            while len(Buffer) > 0:
                hobj.update(Buffer)
                Buffer = fobj.read(1024)

        # Return the calculated checksum
        return hobj.hexdigest()

    except OSError as e:
        print("Unable to read file:", FileName)
        print("Error:", e)
        return None


def FindDuplicate(DirectoryName):
    """Find duplicate files using file size and checksum."""

    # Validate the directory path
    if not os.path.exists(DirectoryName):
        print("Path is invalid")
        return None

    if not os.path.isdir(DirectoryName):
        print("It is not a directory")
        return None

    # Store file paths according to their sizes
    FileSizeDict = {}

    # Traverse the directory and its subdirectories
    for FolderName, SubFolder, FileName in os.walk(DirectoryName):

        for fname in FileName:

            FilePath = os.path.join(FolderName, fname)

            try:
                # Get the size of the file
                FileSize = os.path.getsize(FilePath)

                # Group files having the same size
                if FileSize in FileSizeDict:
                    FileSizeDict[FileSize].append(FilePath)
                else:
                    FileSizeDict[FileSize] = [FilePath]

            except OSError as e:
                print("Unable to access file:", FilePath)
                print("Error:", e)

    Duplicate = {}

    # Calculate checksums only for matching file sizes
    for FileSize, FileList in FileSizeDict.items():

        if len(FileList) > 1:

            for FilePath in FileList:

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


def DeleteDuplicate(Result):
    """Delete duplicate files after user confirmation."""

    # Store deletion results
    DeletionResults = {
        "Deleted": [],
        "Failed": [],
        "Status": "Cancelled",
        "SpaceRecovered": 0
    }

    print("\nDuplicate files available for deletion:\n")

    # Display files that can be deleted
    for value in Result:
        for subvalue in value[1:]:
            print(subvalue)

    print("\nThe first file in each group will be retained.")

    # Ask the user for confirmation
    Choice = input("\nDo you want to delete duplicate files? (yes/no): ")

    if Choice.lower() != "yes":
        print("Deletion cancelled. No files were deleted.")
        return DeletionResults

    DeletionResults["Status"] = "Completed"

    # Delete duplicate copies while retaining one original
    for value in Result:

        for subvalue in value[1:]:

            try:
                # Get file size before deleting the file
                FileSize = os.path.getsize(subvalue)

                # Delete the duplicate file
                os.remove(subvalue)

                print("Deleted:", subvalue)

                # Store successfully deleted file information
                DeletionResults["Deleted"].append(subvalue)

                # Calculate total recovered storage
                DeletionResults["SpaceRecovered"] += FileSize

            except OSError as e:
                print("Unable to delete:", subvalue)
                print("Error:", e)

                DeletionResults["Failed"].append(subvalue)

    # Display deletion summary
    print("\nDeletion Summary")
    print("Total files deleted:", len(DeletionResults["Deleted"]))
    print("Total files failed:", len(DeletionResults["Failed"]))

    print(
        "Storage recovered:",
        round(DeletionResults["SpaceRecovered"] / (1024 * 1024), 2),
        "MB"
    )

    return DeletionResults


def GenerateDuplicateReport(DirectoryName, Result, DeletionResults):
    """Generate a report containing duplicate and deletion information."""

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

            # Write duplicate group information
            GroupCount = 1

            for value in Result:

                fobj.write("Duplicate Group " + str(GroupCount) + "\n\n")

                # Keep the first file as the original
                fobj.write("Original File: " + value[0] + "\n")

                # Record the remaining duplicate files
                for subvalue in value[1:]:
                    fobj.write("Duplicate File: " + subvalue + "\n")
                    TotalDuplicates += 1

                fobj.write("-" * 70 + "\n\n")

                GroupCount += 1

            # Write duplicate statistics
            fobj.write("========== DUPLICATE STATISTICS ==========\n\n")
            fobj.write("Total Duplicate Groups: " + str(TotalGroups) + "\n")
            fobj.write("Total Duplicate Files: " + str(TotalDuplicates) + "\n")

            # Write deletion results
            fobj.write("\n========== DELETION SUMMARY ==========\n\n")

            fobj.write("Deletion Status: " + DeletionResults["Status"] + "\n\n")

            fobj.write("Successfully Deleted Files:\n")

            for FilePath in DeletionResults["Deleted"]:
                fobj.write(FilePath + "\n")

            fobj.write("\nFailed Deletion Files:\n")

            for FilePath in DeletionResults["Failed"]:
                fobj.write(FilePath + "\n")

            # Calculate recovered storage in different units
            RecoveredBytes = DeletionResults["SpaceRecovered"]
            RecoveredKB = RecoveredBytes / 1024
            RecoveredMB = RecoveredBytes / (1024 * 1024)
            RecoveredGB = RecoveredBytes / (1024 * 1024 * 1024)

            # Write final deletion statistics
            fobj.write("\nTotal Files Deleted: " +
                       str(len(DeletionResults["Deleted"])) + "\n")

            fobj.write("Total Files Failed: " +
                       str(len(DeletionResults["Failed"])) + "\n")

            fobj.write("\n========== STORAGE RECOVERY ==========\n\n")
            fobj.write("Recovered Storage: " + str(RecoveredBytes) + " bytes\n")
            fobj.write("Recovered Storage: " + str(round(RecoveredKB, 2)) + " KB\n")
            fobj.write("Recovered Storage: " + str(round(RecoveredMB, 2)) + " MB\n")
            fobj.write("Recovered Storage: " + str(round(RecoveredGB, 4)) + " GB\n")

        print("\nDuplicate report generated successfully.")
        print("Report saved as:", ReportFileName)

    except OSError as e:
        print("Unable to create duplicate report.")
        print("Error:", e)


def main():
    """Main function of the program."""

    Border = "-" * 70

    print(Border)
    print("Duplicate File Finder")
    print(Border)

    if len(sys.argv) == 2:

        DirectoryName = sys.argv[1]

        # Find duplicate files
        MyDict = FindDuplicate(DirectoryName)

        if MyDict is not None:

            # Select groups containing more than one file
            Result = list(
                filter(lambda x: len(x) > 1, MyDict.values())
            )

            TotalDuplicates = 0

            # Display duplicate file paths
            for value in Result:

                for subvalue in value[1:]:
                    print("Duplicate found:", subvalue)
                    TotalDuplicates += 1

            print("\nTotal duplicate groups found:", len(Result))
            print("Total duplicate files found:", TotalDuplicates)

            if len(Result) > 0:

                # Delete duplicates after user confirmation
                DeletionResults = DeleteDuplicate(Result)

                # Generate report with deletion and storage results
                GenerateDuplicateReport(
                    DirectoryName, Result, DeletionResults
                )

            else:
                print("No duplicate files found.")

        else:
            print("Unable to scan the specified directory.")

    else:
        print("Invalid number of arguments")
        print("Usage: python duplicate_file_finder.py DirectoryName")

    print(Border)
    print("Thank you for using Duplicate File Finder")
    print(Border)


if __name__ == "__main__":
    main()
