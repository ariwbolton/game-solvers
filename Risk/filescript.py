outfile = open("probabilities.txt", "w")

for att in range(1,4):
    for defe in range(1,4):
        name = str(att) + "v" + str(defe) + ".txt"

        f = open(name)

        probs = f.readline()
        print "Att: ", att, " | Def: ", defe, " | ", probs.strip().split()
        f.close()

        outfile.write(probs)

outfile.close()
