#!/usr/bin/python3
import subprocess
from subprocess import PIPE,STDOUT
import stegWrap_file_text as fileText

def mainMenu():
    print("************************************")
    print("*        Welcome to Stegwrap       *")
    print("************************************")
    print(" Stegwrap has several tools at your disposal: ")
    print(" [1] Ankylfind - Steghide's brute forcing counter part")
    print("                    Locked behind an annoying password? Just break it!")
    print(" [2] <INSERT ENCRYPTION NAME HERE>")
    print(" [3] Hide text/data/files & recover file menu")
    print(" [4] Exit Stegwrap")
    print(" Please choose the tool you wish to use: ", end="")


def ankylFindUsage():
    print("*****************************")
    print("*    Welcome to Ankylfind   *")
    print("*****************************")
    print("\nExample:")
    print("\t\tankylFind.py [options] inImage1 inImage2 ...")
    print("\nOptions:")
    print("\t\t-h/--help\tPrint this message")
    print("\t\t-v/--verbose\tVerbose output")
    print("\t\t-w/--wordlist\tWordlist to draw passwords from")
    print("\t\t-b/--brute-force\tBrute force generate the password")
    print("\t\t-s/--smallest\t\tSmallest possible password")
    print("\t\t-l/--largest\t\tLargest possible password")
    print("\t\t-u/--use-symbols\tUse symbols in brute force generation")

def main():

    # Show menu of choices to user.
    mainMenu()

    ankylFind = "./ankylfind.py"
    encryption = "./encryption.py"

    # Keep asking user for their choice of tool
    choice = input()
    while choice[0] != "4":

        if choice[0] == "1":

            # Print ankylfind usage for user
            ankylFindUsage()

            print("Please enter command arguments: ", end="")
            commands = input()
            ankylFindCommand = []
            ankylFindCommand.append(ankylFind)
            commands = commands.split()

            for option in commands:
                ankylFindCommand.append(option)

            process = subprocess.Popen(ankylFindCommand, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            out = (process.communicate()[0]).decode()
            print(out)

        elif choice[0] == "2":
            process = subprocess.Popen([encryption])
        elif choice[0] == "3":
            fileText.dialog() # Hiding and extracting files manually
        else:
            print("Unknown option chosen")

        
        # Show menu of choices to user.
        mainMenu()

        choice = input()

    print("Thank you for using Stegwrap")


if __name__ == '__main__':
    main()