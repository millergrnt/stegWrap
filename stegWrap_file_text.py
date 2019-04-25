#!/usr/bin/python3
import subprocess
from subprocess import PIPE,STDOUT
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

def opt1():
    coverfile = ""
    textToHide = ""
    stegofile = "stegOutput"
    password = ""

    print("\nWe are hiding text!\n")
    print("Enter the filename you'd like to use as a data substrate")
    coverfile = input("Filename: ")
    if ".jpg" in coverfile:
        extension = ".jpg"
    elif ".jpeg" in coverfile:
        extension = ".jpeg"
    elif ".bmp" in coverfile:
        extension = ".bmp"
    elif ".au" in coverfile:
        extension = ".au"
    elif ".wav" in coverfile:
        extension = ".wav"


    print("Enter the text/message you'd like to hide in your data substrate")
    textToHide = input("Text/Message: ")

    print("Enter the password you'd like to use to hide your text/message")
    password = input("Password: ")

    print("Default output file will be named YYYY.MM.DD_HH.MM.SS.<ext>")
    print("Rename your file on the next line, or hit enter if you would like to keep defaults")
    stegofile = input("Output Filename: ")
    if stegofile == "":
        stegofile = time.strftime("%Y.%m.%d_%H.%M.%S") + extension
    print("Filename will be {}".format(stegofile))
    

    process = subprocess.Popen(["steghide", "--embed", "-v", "-cf", coverfile, "-sf", stegofile, "-p", password, "-N"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    process.stdin.write(textToHide.encode())
    out = (process.communicate()[0]).decode()
    print("\n" + out)
    

def opt2():
    coverfile = ""
    fileToHide = ""
    stegofile = "stegOutput"
    password = ""

    print("\nWe are hiding data/files!\n")
    print("Enter the filename you'd like to use as a data substrate")
    coverfile = input("Filename: ")
    if ".jpg" in coverfile:
        extension = ".jpg"
    elif ".jpeg" in coverfile:
        extension = ".jpeg"
    elif ".bmp" in coverfile:
        extension = ".bmp"
    elif ".au" in coverfile:
        extension = ".au"
    elif ".wav" in coverfile:
        extension = ".wav"


    print("Enter the filename you'd like to hide in your data substrate")
    fileToHide = input("Filename: ")

    print("Enter the password you'd like to use to hide your data/files")
    password = input("Password: ")

    print("Default output file will be named YYYY.MM.DD_HH.MM.SS.<ext>")
    print("Rename your file on the next line, or hit enter if you would like to keep defaults")
    stegofile = input("Output Filename: ")
    if stegofile == "":
        stegofile = time.strftime("%Y.%m.%d_%H.%M.%S") + extension
    print("Filename will be {}".format(stegofile))
    

    process = subprocess.Popen(["steghide", "--embed", "-v", "-cf", coverfile, "-sf", stegofile, "-ef", fileToHide, "-p", password], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    out = (process.communicate()[0]).decode()
    print("\n" + out)

def opt3():
    coverfile = ""
    stegofile = "stegOutput"
    password = ""

    print("\nWe are recovering a file!\n")
    print("Enter the filename you encoded data into")
    coverfile = input("Filename: ")

    print("Enter the password you used to encode data with")
    password = input("Filename: ")


    process = subprocess.Popen(["steghide", "--extract", "-v", "-sf", coverfile, "-p", password], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    out = (process.communicate()[0]).decode()
    
    if "specify a file name" in out:
        print("Enter a filename to output encoded text to")
        stegofile = input("Filename: ")
        out = ""
        process = subprocess.Popen(["steghide", "--extract", "-v", "-sf", coverfile, "-xf", stegofile, "-p", password], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
        out = (process.communicate()[0]).decode()
    
    print("\n" + out)










def dialog():

    ["", "Hide text", "Hide data/files", "Extract text/data/files"]

    coverfile = ""
    fileToHide = ""
    textToHide = ""
    stegofile = "stegOutput"
    password = ""
    print("")
    print("************************************")
    print("* Ready to hide and recovery files *")
    print("************************************")
    print("")
    print("You can hide data and text in")
    print(" .AU audio files")
    print(" .WAV audio files")
    print(" .BMP bitmap photos")
    print(" .JPEG compressed photos")
    print("")
    
    print("Please select an operation")
    print(" [1] - Hide text in a file")
    print(" [2] - Hide data/file in file")
    print(" [3] - Extract text/data/file from file")
    choice = input("Chosen Option: ")
    
    if choice[0] == "1":
        opt1()
    if choice[0] == "2":
        opt2()
    if choice[0] == "3":
        opt3()
    
    
    print("")
    print("")
    print("")