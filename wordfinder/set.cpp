
#include "set.h"

set::set(int inp[26])
{
    int i;

    for(i = 0; i < 26; i++)
	key[i] = inp[i];

    numSS = 0;
    numWords = 0;
}
