import os

import socket
import ssl
from bs4 import BeautifulSoup, SoupStrainer
import re
import select
import threading
import Queue
import time

numThreads = 5
#sem = threading.Semaphore(value=numThreads)
lock = threading.RLock()

q = Queue.Queue()

globalEmails = {}
globalLinkList = {}

NUMDEADTHREADS = 0		# if NUMDEADTHREADS == numThreads, im done




def main():
	html = getRawHtml("/")
	links = findLinks(html)
	for link in links:
		addLink(link, 0)
		addQueue(link, 0)
	

	cmdThread = threading.Thread(
								target=clockedOutput,
								args=[]
								)
	cmdThread.start()
	



	threads = []														# create threads
	for thread in range(0, numThreads):
		threads.append(threading.Thread(
									target=scraper,
									args=[])
									)


	for thread in range(0, len(threads)):								# start threads
		threads[thread].start()



	for thread in range(0, len(threads)):								# end threads
		threads[thread].join()
	cmdThread.join()


main()