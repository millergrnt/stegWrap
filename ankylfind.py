#!/usr/bin/python3
# Author: Grant Miller <gem1086@g.rit.edu>
# File: ankylfind.py
# Description: Brute forces access to a message hidden in
#		a picture through steghide
# Date: 4 April 2019


# Import section
import getopt, sys, subprocess, os.path, threading, multiprocessing
from subprocess import PIPE
from queue import Queue

passCracked = False
crackedPassword = ""
lock = threading.Lock()


# Does the BruteForce cracking
def attemptCrack(inImage, verbose, passAttempt):
	if verbose:

		# Obtain stdout lock and print
		with lock:
			print(f"\tAttempting password: {passAttempt}")

		# Spawn the steghide process and wait for the result
		process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", passAttempt, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
		out = (process.communicate()[0]).decode()

		# If steghide does not tell us it could not extract, the passAttempt
		# was found
		if not "could not extract" in out:
			return True, passAttempt
	else:

		# Spawn the steghide process and wait for the result
		process = subprocess.Popen(["steghide", "extract", "-sf", inImage, "-p", passAttempt, "-xf", inImage + ".out"], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
		out = (process.communicate()[0]).decode()

		# If steghide does not tell us it could not extract, the passAttempt
		# was found
		if not "could not extract" in out:
			return True, passAttempt

	return False, ""


# Tells each worker what to do
def worker(inImage, verbose, bruteForce, q):

	global passCracked

	# until one of the threads cracks the password keep going
	while not passCracked:
		passAttempt = q.get()
		cracked, password = attemptCrack(inImage, verbose, passAttempt)

		# Check if attemptCrack successfully cracked the password
		if cracked == True:
			with lock:
				print(f"\t[*] Password for {inImage}: {password}")
			passCracked = True
		q.task_done()

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

	# If no arguments are supplied, print the usage
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

	# Set defaults
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

	# Make sure at least one image is found
	if len(args) < 1:
		print("An input image must be supplied")

	# Attempt to crack each image's password
	for inImage in args:

		print(f"Cracking: {inImage}")

		# Make sure supplied images are actually on the system
		if not os.path.isfile(inImage):
			print(f"[!] {inImage} is not a file on this system")
			continue

		# Create thread pool and password queue
		q = Queue()
		for i in range(multiprocessing.cpu_count()):
			t = threading.Thread(target=worker, args=(inImage, verbose, bruteForce, q))
			t.start()

		if bruteForce:

			# Create the character creation list
			chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
			symbolChars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'\"/?.")

			# Create the potential password wordlist
			wordlist = [""]
			while len(wordlist[0]) <= maximumPassLen and not passCracked:

				# If the newly created list is the correct length add it
				# to the potential password queue
				if len(wordlist[0]) >= minimumPassLen:
					for password in wordlist:
						q.put(password)

				# Don't waste a massive amount of time creating an extra list
				if len(wordlist[0]) < maximumPassLen:

					# Create the next potential list
					if not useSymbols:
						wordlist = [''.join((orig, newchar)) for orig in wordlist for newchar in chars]
					else:
						wordlist = [''.join((orig, newchar)) for orig in wordlist for newchar in symbolChars]

		else:

			# For passowrd in the wordlist, add it to the queue
			with open(wordlist, "r") as wordlist:
				for password in wordlist:
					password = password.strip()
					q.put(password)

		# If cracked flag set, print the cracked password
		if passCracked:
			print(f"\t[*] Password for {inImage}: {crackedPassword}")
		else:
			print(f"\t[!] Password for {inImage}: not found")

		# Reset cracked flag
		cracked = False

if __name__ == '__main__':
	main()
