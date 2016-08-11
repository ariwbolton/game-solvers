// functions for substitute()

#include "substitution.h"
#include <string>
#include "QuadraticProbing.h"
#include "QueueAr.h"
#include <iostream>

void testperm(std::string inp, int index, int places[5], int numQ, QuadraticHashTable< std::string > * w,
	      Queue< std::string > * q)
{
    int i;
    std::string curr = inp;

    if(index == numQ) // word is completed
    {
	std::string temp = w->find(inp);

	//if(temp != "")
	//    std::cout << temp << std::endl;

	if(temp!= "")
	    q->enqueue(temp);

	if(q->currentSize == 8)
	{
	    for(i = 0; i < 8; i++)
		std::cout << q->dequeue() << "    ";

	    std::cout << std::endl;
	}
    }
    else // compute more perms
    {
	int qplace = places[ index ];

	curr[ qplace ] = 'a' - 1;

        for(i = 0; i < 26; i++)
        {

	    curr[ qplace ]++;

	    testperm(curr, index + 1, places, numQ, w, q); 

        }
    }

}
void substitute(QuadraticHashTable< std::string > * w)
{
    std::string entry;
    int places[5], numQ = 0, i;
    Queue< std::string > queue(8);

    std::cout << "\nUse \"?\" or \"_\" to represent unknown letters.\n>> ";

    std::cin >> entry;

    for(i = 0; i < entry.length(); i++)
    {
	if(entry[i] == '_')
	    entry[i] = '?';
    }

    std::cout << "\nPossible replacements:\n\n";

    for(i = 0; i < entry.length(); i++)
    {
	if(entry[i] == '?')
	    places[ numQ++ ] = i;
    }

    testperm(entry, 0, places, numQ, w, &queue);

    while(queue.currentSize > 0)
	std::cout << queue.dequeue() << "    ";

    std::cout << std::endl << std::endl;
}

