import riskSetup
import matplotlib.pyplot as plt
probs = []

riskSetup.setup(probs)
for line in probs:
    print line

class DTreeNode:

    def __init__(self, attack=0, defe=0):
        self.att, self.defend = attack, defe
        self.children = [0,0,0,0]
        self.prob = 0

    def delete(self):
        rnge = len(self.children)
        for node in range(rnge):
            if self.children[node] != 0:
                self.children[node].delete()
                self.children[node] = 0

    def setupNode(self):
        attacking, defending = self.att, self.defend
        
        if attacking >= 3:
            if defending >= 3:
                for i in xrange(4):
                    self.children[i] = DTreeNode(attacking - i, defending - 3 + i)
            else:                           #defending < 3
                for i in xrange(defending + 1):
                    self.children[i] = DTreeNode(attacking - i, i)

        else:                               #attacking < 3
            if defending >= 3:
                for i in xrange(attacking + 1):
                    self.children[i + (3 - attacking)] = DTreeNode(attacking - i, defending - attacking + i)

            else:                           #both < 3
                bound = min(attacking, defending)
                for i in xrange(bound + 1):
                    self.children[i + (3 - attacking)] = DTreeNode(attacking - i, i)

        for i in xrange(4):
            if self.children[i] != 0:
                boolean = self.children[i].att != 0 and self.children[i].defend != 0
                if boolean:
                    self.children[i].setupNode()

    def printTree(self):
        print "Parent: Att: " + str(self.att) + " Def: " + str(self.defend)

        for i in xrange(4):
            if self.children[i] != 0:
                print "Att: " + str(self.children[i].att) + " Def: " + str(self.children[i].defend)
            else:
                print "No Node present"

        print ""
        for i in xrange(4):
            if self.children[i] != 0:
                boolean = self.children[i].att != 0 and self.children[i].defend != 0
                if boolean:
                    self.children[i].printTree()

    def calcProb(self):
        pass
        #recursively call on each child
        #come up with probability distribution for node
        #can combine probability distributions of children by summing (childDistr * prob)
        #will add memoization

    def createProbDist(self):            
        
        #create probDist
        self.probDist = [0] * 101

        if self.att == 0:
            self.probDist[50 + self.defend] = 1
            return
        elif self.defend == 0:
            self.probDist[50 - self.att] = 1
            return
            
        #for each child
        for i in xrange(4):
            #find probability of node happening
            child = self.children[i]
            
            if child == 0:
                continue

            child.createProbDist()

            prob = self.getProbOfChild(child, i)
            print prob
            #self.probDist = [x + (y * prob) for x, y in zip(self.probDist, child.probDist)]
            self.probDist = self.combineProbDist(self.probDist, child.probDist, prob)

        #multiply probDist of child by probability
        #merge probDists

    def getProbOfChild(self, child, i):
        '''reverse placing alg'''
        
        attacking = min(2, self.att - 1)
        defending = min(2, self.defend - 1)

        return float(probs[attacking][defending][i])

    def combineProbDist(self, P, C, prob):
        l = []
        for i in xrange(len(P)):
            #print str(P[i]) + " " + str(type(P[i]))
            #print str(C[i]*prob) + " " + str(type(prob*C[i]))
            #print str(C[i]) + " * " + str(prob)
            l.append(P[i] + (prob * C[i]))

        return l
'''
     def displayProbDist(self):
         plt.hist(self.probDist)
         plt.show()
'''
        
node1 = DTreeNode(3, 2)
node1.setupNode()
node1.printTree()
node1.createProbDist()

lower, upper = 0,0

for n in xrange(102):
    if node1.probDist[n] != 0:
        lower = n
        break
for n in xrange(102):
    if node1.probDist[-n] != 0:
        upper = 101 - n
        break
print upper - lower
plt.hist(node1.probDist, bins=(upper - lower + 1))
plt.show()
node1.delete()
