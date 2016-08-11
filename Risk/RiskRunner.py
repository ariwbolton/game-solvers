import Table

def runner():
	print "Welcome to the Risk Probability Calculator!"
	s = raw_input("Enter attacking and defending: ").split()
	choices = [int(v) for v in s]

	while choices[0] >= 1:
		t = Table.MemTable(choices[0], choices[1])
		t.runner()

		print "Welcome to the Risk Probability Calculator!"	
		s = raw_input("Enter attacking and defending: ").split()
		choices = [int(v) for v in s]

runner()
