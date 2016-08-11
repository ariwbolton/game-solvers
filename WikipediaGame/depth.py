import json
import multiprocessing
import urllib
import os
import sys
import threading
from BeautifulSoup import BeautifulSoup
from WikiNode import WikiNode

num = 0

def removeDups(l):
    seen = set()
    seen_add = seen.add
    return [ x for x in l if not (x in seen or seen_add(x))]

def flatten(l):
	return [item for sublist in l for item in sublist]

def constructAbsLink(absUrl, link):
	if "://" not in link:
		return absUrl + link
	else:
		return link

def parseForLinks(absUrl, docstring):
	soup = BeautifulSoup(docstring)

	content = soup.findAll("div")

	for i in content:
		print i

	aTags = BeautifulSoup(content).findAll("a", attrs={"href":True})
	
	l = [constructAbsLink(absUrl, a["href"]) for a in aTags if "#" not in a["href"]]
	return removeDups(l)

def isValid(link):
	return (not ":" in link)

def replaceLine(s):
	sys.stdout.write("\r" + s)
	sys.stdout.flush()

def worker(title):
	lock = multiprocessing.Lock()

	linkList = list()

	filename = "./.storage/" + title.replace("/", "~") + ".json"

	if os.path.isfile(filename):
		with open(filename) as f:
			docstring = f.read()
			linkList = json.loads(docstring)

		#print "Data loaded from cache!", worker.num
		replaceLine("Data loaded from cache! " + str(depth.num))
	else:
		queryString = "https://en.wikipedia.org/w/api.php?action=parse&prop=links&format=json&page="
		queryString += urllib.quote(title.encode("utf8"))

		fName, header = urllib.urlretrieve(queryString)

		docstring = open(fName).read()

		nodeObj = json.loads(docstring)

		try:
			linkObjs = nodeObj["parse"]["links"]
		except KeyError:
			#print "KeyError: \"parse\" not found"
			replaceLine("KeyError: \"parse\" not found")
			linkObjs = list()

		linkList = [link["*"] for link in linkObjs if isValid(link["*"])]

		with open(filename, "w+") as f:
			f.write(json.dumps(linkList))

		#print "Data downloaded and stored!", worker.num
		replaceLine("Data downloaded and stored! " + str(depth.num))

	wikiNodeList = [WikiNode(title, link) for link in linkList]

	with lock:
		depth.num += 1

	return wikiNodeList

def depth(titles):
	depth.num = 0

	pool = multiprocessing.Pool(processes=10)
	output = pool.map(worker, titles)

	return removeDups(flatten(output))

if __name__ == "__main__":
	urls = [
		"http://www.google.com",
		"http://www.facebook.com",
		"http://www.bing.com",
		"http://www.gmail.com",
		"http://www.yahoo.com",
		"http://www.mint.com",
		"http://www.xfinity.com",
		"http://www.stackoverflow.com",
		"http://www.github.com",
		"http://www.bitbucket.com",
		"http://www.reddit.com",
		"http://www.meteor.com"
	]

	depth(["Pizza"])
