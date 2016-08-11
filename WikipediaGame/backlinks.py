#https://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=Code%20golf&bllimit=250&blredirect&blnamespace=0|14
import urllib, json

def getLinks(info):
	l = []

	o = info["query"]["backlinks"]

	for obj in o:
		l.append(obj["title"].encode("utf8"))

	return l

def backlinks(title):
	q = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=backlinks&bllimit=250&blredirect&blnamespace=0|14&bltitle="

	fName, header = urllib.urlretrieve(q + title)

	docstring = open(fName).read()
	info = json.loads(docstring)

	links = []

	links = links + getLinks(info)

	while "continue" in info:
		s = ""

		contObj = info["continue"]

		for key in contObj:
			s += "&" + key + "=" + contObj[key]

		fName, header = urllib.urlretrieve(q + title + s)

		docstring = open(fName).read()
		info = json.loads(docstring)

		links = links + getLinks(info)

	return links
