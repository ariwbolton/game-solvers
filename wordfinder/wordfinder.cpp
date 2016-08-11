// Author: Ari Bolton
// Started 6/19/14

#include <iostream>
#include <string>
#include <fstream>
#include <cctype>
#include "QuadraticProbing.h"
#include "QueueAr.h"
#include "substitution.h"
#include "boggle.h"

using namespace std;

void init(ifstream * dict, QuadraticHashTable< string > * ht, string * wa, int * ind)
{
    string word, prev, temp = "aaa";
    bool ins;
    int i, j, k, n = 0, m = 0;
    Queue< string > queue(26 * 26 * 26);

    for(i = 0; i < 26; i++)
    {
	for(j = 0; j < 26; j++)
	{
	    for(k = 0; k < 26; k++)
	    {
		queue.enqueue(temp);
		temp[2]++;
	    }

	    temp[1]++;
	    temp[2] = 'a';
	}

	temp[0]++;
	temp[1] = 'a';
    }

    (*dict) >> prev;

    while((*dict) >> word)
    {
	ins = true;

	if(isupper(prev[0]))
	{
	    prev[0] = tolower(prev[0]);

	    if(prev == word)
		ins = false;

	    for(i = 1; i < prev.length(); i++)
	    {
		if(prev[i] == '-')
		    ins = false;
	    }

	}
	
	if(ins)
	{
	    wa[ n++ ] = prev;
	    ht->insert(prev);

	    while(prev.compare(queue.getFront()) >= 0)
	    {
		ind[ m++ ] = n - 1;
		queue.dequeue();
	    }
	}

	prev = word;
    }

    word[0] = tolower(word[0]);

    wa[ n++ ] = word;
    ht->insert(word);

    while(prev.compare(queue.getFront()) >= 0)
    {
	ind[ m++ ] = n - 1;
	queue.dequeue();
    }

    //cout << n << endl;
}

void instructions()
{

    cout << "0. Exit\n"
         << "1. Substitute letters\n"
	 << "2. Boggle word finder\n"
	 << "3. Find completions\n"
	 << ">> ";

}

int main()
{
    ifstream dictionary("words");
    string nf;
    int choice, * indices = new int[26 * 26 * 26];
    QuadraticHashTable< string > words(nf, 600000);
    string * wordarray = new string[234369];


    init(&dictionary, &words, wordarray, indices);

    do
    {

	instructions();

	cin >> choice;

	switch(choice)
	{
	    case 0: 
		    break;
	    case 1: 
		    substitute(&words);
		    break;
	    case 2:
		    boggle(&words, wordarray, indices);
		    break;
	    case 3:
		    comp(wordarray, indices);
		    break;
	    default:
		    break;

	}

    } while (choice > 0);

    delete [] wordarray;
    delete [] indices;

    return 0;
}
