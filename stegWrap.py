#!/usr/bin/python3
import subprocess
from subprocess import PIPE,STDOUT

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

	# Present welcome banner and menu
	print("************************************")
	print("*        Welcome to Stegwrap       *")
	print("************************************")
	print("Stegwrap has several tools at your disposal: ")
	print("[1] Ankylfind - Steghide's brute forcing counter part")
	print("                   Locked behind an annoying password? Just break it!")
	print("[2] <INSERT ENCRYPTION NAME HERE>")
	print("[3] Exit Stegwrap")
	print("Please choose the tool you wish to use: ", end="")

	ankylFind = "./ankylfind.py"
	encryption = "./encryption.py"

	# Keep asking user for their choice of tool
	choice = input()
	while "3" not in choice:

		if "1" in choice:

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

		elif "2" in choice:
			process = subprocess.Popen([encryption])
		else:
			print("Unknown option chosen")

		print("[1] Ankylfind")
		print("[2] <INSERT ENCRYPTION NAME HERE>")
		print("[3] Exit")
		print("Please choose the tool you wish to use: ", end="")
		choice = input()

	print("Thank you for using Stegwrap")


if __name__ == '__main__':
	main()
