from riskSetup import setup
from PD import PD
import matplotlib.pyplot as plt

probs = []

setup(probs)

# Get 1-indexed list of floats for each matchup
def getProb(att, defe):
	return probs[(3 * (att - 1)) + (defe - 1)]

# Will primarily contain a 2-D table (table[attacking][defending])
# which will contain the probability distribution of that initial
# condition reaching each value of remaining attackers or defenders.
# The distribution will be (attacking + defending + 1) bucket wide, so
# that it can contain the range of potential outcomes
class MemTable:
	def __init__(self, a, d):	
		self.A, self.D, = a, d
		attacking, defending = max(3, a), max(3, d)
		self.t = [[0 for i in xrange(attacking + 1)] for j in xrange(defending + 1)]
		temp = [0.0 for i in xrange(attacking + defending + 1)]

		for i in xrange(attacking + 1):
			self.t[i][0] = PD(attacking, defending).Set(i, 0)

		for i in xrange(defending + 1):
			self.t[0][i] = PD(attacking, defending).Set(0, i)

		self.find_PD(a, d, 0)

	def runner(self):
		st = raw_input("Choose # Attackers and Defenders: ").split()
		choices = [int(v) for v in st]

		while choices[0] != -1:
			pd = self.GetPD(choices[0], choices[1])

			if pd == 0:
				print "Combination has not been calculated. Calculating now..."
				self.find_PD(choices[0], choices[1], 0)
				print "DONE\n"

			y = self.GetPD(choices[0], choices[1]).tb
			x = range(-self.A,self.D + 1)

			win, lose, total = sum(y[:self.A]), sum(y[self.A + 1:]), sum(y)
			print "Win:", win, "| Lose:", lose, "| Total:", total

			plt.plot(x, y)
			plt.show()

			st = raw_input("Choose # Attackers and Defenders: ").split()
			choices = [int(v) for v in st]


	def find_PD(self, att, defe, level):
		# get corresponding prob row from probs and compute
		# sum(row[i]*distr) for all distributions corresponding to the
		# PD in question
		# att and defe are not checked for > 3

		my_print(att, defe, "", level)
		
		a, d = min(3, att), min(3, defe)

		prob_list = getProb(a, d)

		distance = min(a, d)

		new_dist = PD(self.A, self.D)

		for i in xrange(distance + 1):
			#get each relevant cell in table
			tmp = self.GetPD(att - i, defe - distance + i)
			
			# if relevant cell has not been computed
			if tmp == 0:
				self.find_PD(att - i, defe - distance + i, level + 1)
			else:
				my_print(att - i, defe - distance + i, "FOUND", level + 1)

			tmp = self.GetPD(att - i, defe - distance + i).deep_copy()

			#find correct value from prob_list
			c = 4 - (a + 1) + i
			val = prob_list[c]

			# multiply by value and then add to new_dist
			tmp.multiply(val)
			new_dist.add(tmp)


		self.SetPD(att, defe, new_dist)
		my_print(att, defe, "SET", level)

		return new_dist


	def GetPD(self, attack, defend):
		return self.t[attack][defend]

	def SetPD(self, attack, defend, P):
		self.t[attack][defend] = P

def my_print(a, d, msg, spaces):
	s = " " + (spaces * "| ")
	print (str(spaces) + s + "Att:"), a, "| Def:", d, "|", msg 
