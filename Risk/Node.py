class Node:

	def __init__(self, Att, Def, start_att, start_def):
		self.Att = Att
		self.Def = Def

		#PD is Probability Distribution for current node
		self.PD = [0 for i in xrange(start_att + start_def)]

		self.children = [0,0,0,0]
		self.constructChildren(start_att, start_def)


	# construct children for this node, starting from right to
	# left, without assigning probability distributions
	def constructChildren(self, start_att, start_def)
		num_attacking = max(3, Att)

		for i in range(1, num_attacking + 1):
			self.children[ -Att ] = Node(
				self.Att - num_attacking + i,
				self.Def - i, start_att,
				start_def)

