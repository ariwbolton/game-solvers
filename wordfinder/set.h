// Author: Ari Bolton

#ifndef SET_H
#define SET_H

#include <iostream>
#include <string>

class set
{
    public:

	set(int inp[26]);

	int key[26];

	int numWords;
	std::string words[100];

	int numSS;
	set * subsets[1000];
};

#endif
