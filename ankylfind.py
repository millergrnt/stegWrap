#!/usr/bin/python3
# Author: Grant Miller <gem1086@g.rit.edu>
# File: ankylfind.py
# Description: Brute forces access to a message hidden in
#		a picture through steghide
# Date: 4 April 2019


import getopt, sys, subprocess, os.path
from subprocess import PIPE


def crackBruteForce(inImage, minLen, maxLen, verbose, useSymbols):
	print(f"Cracking: {inImage}")
	chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
	symbolChars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'\"/?.")

	if not verbose:
		print("\tThis will take some time, I promise it is working")

	wordlist = [""]
	while len(wordlist[0]) <= maxLen:

		if len(wordlist[0]) >= minLen:
			for password in wordlist:
				if verbose:
					print(f"\tAttempting password: {password}")
					process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", password, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
					out = (process.communicate()[0]).decode()
					if not "could not extract" in out:
						return True, password
				else:
					process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", password, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
					out = (process.communicate()[0]).decode()
					if not "could not extract" in out:
						return True, password
		if not useSymbols:
			wordlist = [''.join((orig, newchar)) for orig in wordlist for newchar in chars]
		else:
			wordlist = [''.join((orig, newchar)) for orig in wordlist for newchar in symbolChars]
	return False, ""

def crackWordlist(inImage, wordlist, verbose):
	print(f"Cracking: {inImage}")
	with open(wordlist, "r") as wordlist:
		for password in wordlist:
			password = password.strip()
			if verbose:
				print(f"\tAttempting password: {password}")
				process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", password, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
				out = (process.communicate()[0]).decode()
				if not "could not extract" in out:
					return True, password
			else:
				process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", password, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
				out = (process.communicate()[0]).decode()
				if not "could not extract" in out:
					return True, password

	return False, ""


# Prints the usage message
def usage():
	print("*****************************")
	print("*    Welcome to Ankylfind   *")
	print("*****************************")
	print("\nExample:")
	print("\t\tankylFind.py [options] inImage1 inImage2 ...")
	print("\nOptions:")
	print("\t\t-h/--help\t\tPrint this message")
	print("\t\t-v/--verbose\t\tVerbose output")
	print("\t\t-w/--wordlist\t\tWordlist to draw passwords from")
	print("\t\t-b/--brute-force\tBrute force generate the password")
	print("\t\t-s/--smallest\t\tSmallest possible password")
	print("\t\t-l/--largest\t\tLargest possible password")
	print("\t\t-u/--use-symbols\tUse symbols in brute force generation")


# Main function of the program
def main():

	if len(sys.argv[1:]) == 0:
		usage()
		sys.exit()

	try:
		# Parse the argument commandline for input and wordlist
		optlist, args = getopt.getopt(sys.argv[1:], 'hw:vbs:l:u', ["help", "wordlist=", "verbose", "brute-force", "smallest=", "largest=", "use-symbols"])
	except getopt.GetoptError as err:
		print(f"Unknown option provided: {err.opt}")
		usage()
		sys.exit(2)

	wordlist = "top100passwords.txt"
	inputImage = ""
	verbose = False
	bruteForce = False
	maximumPassLen = 12
	minimumPassLen = 5
	useSymbols = False

	# Iterate over the list of options
	for opt, arg in optlist:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-w", "--wordlist"):
			wordlist = arg
		elif opt in ("-v", "--verbose"):
			verbose = True
		elif opt in ("-b", "--brute-force"):
			bruteForce = True
		elif opt in ("-s", "--smallest"):
			try:
				minimumPassLen = int(arg)
			except TypeError:
				print("Smallest password length must be an integer")
		elif opt in ("-l", "--largest"):
			try:
				maximumPassLen = int(arg)
			except TypeError:
				print("Largest password length must be an integer")
		elif opt in ("-u", "--use-symbols"):
			useSymbols = True
		else:
			print(f"Unknown option provided: {opt}")

	if len(args) < 1:
		print("An input image must be supplied")

	for inImage in args:

		if not os.path.isfile(inImage):
			print(f"[!] {inImage} is not a file on this system")
			continue

		if not bruteForce:
			cracked, password = crackWordlist(inImage, wordlist, verbose)
		else:
			cracked, password = crackBruteForce(inImage, minimumPassLen, maximumPassLen, verbose, useSymbols)

		if cracked:
			print(f"\t[*] Password for {inImage}: {password}")
		else:
			print(f"\t[!] Password for {inImage}: not found")

if __name__ == '__main__':
	main()
