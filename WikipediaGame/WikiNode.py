
class WikiNode:
	def __init__(self, prev, name):
		self.prev = prev
		self.name = name

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return self.name.__hash__()
