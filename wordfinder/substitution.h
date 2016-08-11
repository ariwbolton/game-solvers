#ifndef SUBSTITUTION_H
#define SUBSTITUTION_H

#include <string>
#include "QuadraticProbing.h"
#include "QueueAr.h"

void testperm(std::string inp, int index, int places[5], int numQ,
	QuadraticHashTable< std::string > * w, Queue< std::string > * q);

void substitute(QuadraticHashTable< std::string > * w);

#endif
