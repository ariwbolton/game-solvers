// functions for boggle()

#include "boggle.h"
#include <iostream>
#include <iomanip>
#include <cctype>
#include "QueueAr.h"
#include <vector>
#include <cstdlib>

using namespace std;

#define UP_LEFT 0
#define UP 1
#define UP_RIGHT 2
#define RIGHT 3
#define DOWN_RIGHT 4
#define DOWN 5
#define DOWN_LEFT 6
#define LEFT 7

void algorithm(int start, string board, int * path, int length, Queue< string > * words,
		string * wdar, int * indec, QuadraticHashTable< string > * wds)
{
   // given start position, board, path, length
   int i, newPos;
   string currentWord = makeString(path, board, length);

   // if path length >= 3
   if(length >= 3)
   {
	// if isWord, add to words
	if(wds->find(currentWord) != wds->ITEM_NOT_FOUND)
	    words->enqueue(currentWord);
   }

   // if hasCompletions, call algorithm with path updated for each
   if(hasComp( wdar, indec, currentWord))
   {
	for(i = 0; i < 8; i++)
	{
	    newPos = getNewPos( path[ length - 1] , i );

	    if( newPos > -1 && !isInPath(path, length, newPos) && length <= 16)
	    {
		path[ length ] = newPos;
		algorithm(start, board, path, length + 1, words, wdar, indec, wds);
		path[ length ] = -1;
	    }

	}
   }




} // algorithm()

string makeString(int * path, string board, int length)
{
    int i;
    string temp = "";

    for(i = 0; i < length; i++)
	temp += board[ path[ i ] ];

    return temp;
}

bool isInPath(int * path, int length, int pos)
{
   int i;

   for(i = 0; i < length; i++)
   {
	if( path[ i ] == pos)
	    return true;
   }

   return false;
}

void boggle(QuadraticHashTable< string > * w, string * wa, int * ind)
{
    string bd = "", temp;
    char a, b, c, d;
    int i, j, p[16], l = 1, n = 0;
    Queue< string > ws(1000);
    string * wds = new string[1000];

    cout << "\nEnter the board:\n";
    
    for(i = 0; i < 4; i++)
    {
	temp = "";

        cout << ">> ";
        cin >> a >> b >> c >> d;

	temp += tolower(a);
	temp += tolower(b);
	temp += tolower(c);
	temp += tolower(d);

	bd += temp;
    }

    for(i = 0; i < 16; i++)
    {
	for(j = 0; j < 16; j++)
	    p[i] = -1;

	p[0] = i;

	algorithm(i, bd, p, l, &ws, wa, ind, w);
    }

    cout << "\nWords contained in this board:\n\n";
    /*
    while(!ws.isEmpty())
    {
	cout << setw(12) << left << ws.getFront();
	n++;

	ws.dequeue();

	if(n % 8 == 0)
	    cout << endl;
    }
    */

    bool ins;

    while(!ws.isEmpty())
    {
	ins = true;

	for(i = 0; i < n; i++)
	{
	    if(wds[i] == ws.getFront())
		ins = false;
	}

	if(ins)
	    wds[ n++ ] = ws.getFront();

	ws.dequeue();
    }

    qsort(wds, n, sizeof(string), compare);

    for(i = 0; i < n; i++)
    {
	cout << setw(12) << left << wds[i];


	if((i + 1) % 8 == 0)
	    cout << endl;
    }

    cout << endl << endl;

    delete [] wds;

} // boggle()

int compare( const void * a, const void * b)
{
    if(((string*)a)->length() > ((string*)b)->length())
	return -1;
    else if(((string*)a)->length() < ((string*)b)->length())
	return 1;
    else
	return ((string*)a)->compare(*((string*)b));

    return 0;
}

bool hasComp(string * wa, int * ind, string str)
{
    int index, next;
    int val = (26 * 26 * (str[0] - 'a')) + (26 * (str[1] - 'a')) + (str[2] - 'a');

    //find index of first 3 letters
    index = ind[ val ];
    next = ind[ val + 1 ];

    //search until strings are equal to or after curent string
    while( str.compare( wa[ index ].substr(0,str.length())) > 0)
	index++;
    
    //if difference between current index and 
    if( str.compare( wa[ index ].substr(0,str.length() )) == 0 )
	return true;
    else
	return false;

    return true;

}

void comp(string * wa, int * ind)
{
    string temp;
    int index, next;

    cout << "\nEnter a string\n>> ";
    cin >> temp;

    if(temp.length() < 3)
    {
	cout << "\nString must have length >= 3\n\n";
	return;
    }
    else
	cout << "\nPossible completions are:\n\n";

    int val = (26 * 26 * (temp[0] - 'a')) + (26 * (temp[1] - 'a')) + (temp[2] - 'a');

    //find index of first 3 letters
    index = ind[ val ];
    next = ind[ val + 1 ];

    //search until strings are equal to or after curent string
    while(temp.compare( wa[ index ] ) >= 0)
	index++;

    //print strings of length 3 or greater until next index
    while( index < next && temp.compare( wa[ index ].substr(0,temp.length() )) == 0 )
	cout << wa[ index++ ] << endl;

    cout << endl;

} // comp()

//return -1 if not possible
//else return new pos
int getNewPos( int pos, int dir )
{
    switch(dir)
    {
	case 0:
	    if(pos % 4 == 0 || pos < 4)
		return -1;
	    else
		return pos - 5;

	    break;
	case 1:
	    if(pos < 4)
		return -1;
	    else
		return pos - 4;

	    break;
	case 2:
	    if(pos % 4 == 3 || pos < 4)
		return -1;
	    else
		return pos - 3;

	    break;
	case 3:
	    if(pos % 4 == 3)
		return -1;
	    else
		return pos + 1;

	    break;
	case 4:
	    if(pos % 4 == 3 || pos > 11)
		return -1;
	    else
		return pos + 5;

	    break;
	case 5:
	    if(pos > 11)
		return -1;
	    else
		return pos + 4;

	    break;
	case 6:
	    if(pos % 4 == 0 || pos > 11)
		return -1;
	    else
		return pos + 3;

	    break;
	case 7:
	    if(pos % 4 == 0)
		return -1;
	    else
		return pos - 1;

	    break;
	default:
	    break;

    }

    return 0;
}
