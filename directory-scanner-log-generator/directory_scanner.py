import sys
import os
import time

def DirectoryScanner(DirectoryPath):
    
    timestamp = time.ctime()
    LogFileName = "Marvellous%s.log"%(timestamp)
    LogFileName = LogFileName.replace(" ","_")                          # it replaces space with underscore in file name
    LogFileName = LogFileName.replace(":","_")

    print("Log file gets created with name : ",LogFileName)

    fobj = open(LogFileName,"w")
    
    fobj.write("Marvellous Automation Script\n")

    fobj.write("Files from the directory are : \n")

    for FolderName , SubFolder , FileName in os.walk(DirectoryPath):
        for fname in FileName : 
            fobj.write(fname+"\n")

    fobj.close()

def main():
    Border = "-"*70
    print(Border)
    print("Marvellous Automation Script")
    print(Border)

    if (len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This automation script is used to travel the directory")
            print("For better usage please check --u flag")
        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Please execute the script as ")
            print("python FileName.py DirectoryName")
            print("Directory name should be absolute path")
        else:
            DirectoryScanner(sys.argv[1])
    else:
        print("Invalid number of arguments")
        print("Please use --h or --u for more information")

    print(Border)
    print("Thank you for using Marvellous Automation Script")
    print(Border)


if __name__ == "__main__":
    main()

