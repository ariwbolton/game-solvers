wordfinder.out: wordfinder.o set.o substitution.o boggle.o
	g++ -Wall -g -o  wordfinder.out wordfinder.o set.o substitution.o boggle.o

wordfinder.o: wordfinder.cpp
	g++ -Wall -g -c wordfinder.cpp

set.o: set.cpp set.h
	g++ -Wall -g -c set.cpp

substitution.o: substitution.cpp substitution.h
	g++ -Wall -g -c substitution.cpp

boggle.o: boggle.cpp boggle.h
	g++ -Wall -g -c boggle.cpp

clean:
	rm -f wordfinder.out *.o
