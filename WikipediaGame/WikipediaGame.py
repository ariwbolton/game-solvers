from WikiNode import WikiNode
from depth import depth
import urllib
import json

class WikipediaGame:
	def __init__(self):
		cont = True

		while(cont == True):
			self.runner()

			cont = self.getContinuation()

	def getContinuation(self):
		done = False

		while(done == False):
			c = raw_input("Would you like to continue? (y or n): ")

			if(c == "y"):
				print ""
				return True
			else:
				print "Exiting..."
				return False

	def runner(self):
		print "Welcome to the Wikipedia Game Solver!"

		self.getChoices()
		# self.start = "LeBron James"
		# self.end = "Berkeley, California"
		
		path = self.findPath()

	def getChoices(self):
		start = raw_input("Start: ")
		end = raw_input("End: ")

		query = "https://en.wikipedia.org/w/api.php?action=query&prop=info&format=json&titles="
		startQuery = query + urllib.quote(start.encode("utf8"))
		endQuery = query + urllib.quote(end.encode("utf8"))

		startFileName, startHeader = urllib.urlretrieve(startQuery)
		endFileName, endHeader = urllib.urlretrieve(endQuery)

		startObj = json.loads(open(startFileName).read())["query"]["pages"]
		endObj = json.loads(open(endFileName).read())["query"]["pages"]

		for key in startObj:
			self.start = startObj[key][u"title"]

		for key in endObj:
			self.end = endObj[key][u"title"]

		print "Finding path:", self.start, "==>", self.end


	def findPath(self):
		start, end = self.start, self.end

		found = False

		self.visited = set(start)											# visited nodes
		self.depths = list()												# layers of visited sets
		self.depths.append(dict())
		self.depths[0][start] = "NULL"

		upNext = [start]													# nodes to visit

		while(not found):

			if end in self.visited:
				print "End Found!"
				found = True

				continue

			try:
				newLinks = depth(upNext)
			except (KeyboardInterrupt, SystemExit):
				print "KeyboardInterrupt recieved. Quitting threads..."
				raise

			newLinks = [x for x in newLinks if x.name not in self.visited]			# filter new links

			print "\n============================="
			print "Level:", len(self.depths), "	NumLinks:", len(newLinks)
			print "============================="
			# for i in newLinks[:10]:
			# 	print i.name

			for x in newLinks:
				self.visited.add(x.name)

			newDict = dict()

			for i in xrange(len(newLinks)):
				newDict[newLinks[i].name] = newLinks[i].prev

			self.depths.append(newDict)

			upNext = [x.name for x in newLinks]

		self.printPath()

	def printPath(self):
		path = [self.end]

		height = len(self.depths) - 1

		current = self.end

		while height >= 1:
			next = self.depths[height][current]

			path.append(next)
			
			height -= 1

			current = next

		l = list(reversed(path))

		current = 0
		next = 0

		for i in xrange(0, len(l) - 1):
			current = l[i]
			next = l[i+1]

			print "{0:25} ==> {1:25}".format(current, next)

def findObjInSet(string, setToSearch):
	return [x for x in setToSearch if x.name == string][0]

if __name__ == "__main__":
	obj = WikipediaGame()
