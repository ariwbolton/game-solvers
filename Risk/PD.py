
class PD:
	def __init__(self, attacking, defending):
		self.tb = [0.0 for i in xrange(attacking + defending + 1)]
		self.Att = attacking
		self.Def = defending

	def deep_copy(self):
		tmp = PD(self.Att, self.Def)
		tmp.tb = self.tb
		return tmp

	
	# either attack or defend must be 0
	def Get(self, attack, defend):
		if attack > 0:
			return self.tb[self.Att - attack]
		else:
			return self.tb[self.Att + defend]

	def Set(self, attack, defend, value=1.0):
		if attack > 0:
			self.tb[self.Att - attack] = value
		elif defend > 0:
			self.tb[self.Att + defend] = value

		#print "Att:", attack, "| Def:", defend, "|", self.tb

		return self

	# DOES NOT return new PD
	def multiply(self, f):
		self.tb = [f * (self.tb[i]) for i in range(len(self.tb))]
		return self

	# DOES NOT return new PD
	def add(self, other):
		self.tb =[(other.tb[i]) + (self.tb[i]) for i in range(len(self.tb))]
		return self


