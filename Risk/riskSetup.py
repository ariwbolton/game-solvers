
def setup(probs):
    f = open("probabilities.txt")
    
    for attacking in xrange(3):
        l = []
        for defending in xrange(3):
            #print "att: " + str(attacking) + " : def: " + str(defending)
            line = f.readline().split()
            line = [float(i) for i in line]
            probs.append(line)


    f.close()


