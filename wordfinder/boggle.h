
#ifndef BOGGLE_H
#define BOGGLE_H

#include "QuadraticProbing.h"
#include <string>

void boggle(QuadraticHashTable< std::string > * w, std::string * wa, int * ind);
void comp(std::string * wa, int * ind);
bool hasComp(std::string * wa, int * ind, std::string str);
int getNewPos( int pos, int dir );
bool isInPath(int * path, int length, int pos);
std::string makeString(int * path, std::string board, int length);
int compare( const void * a, const void * b);

#endif
