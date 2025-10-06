#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int next_permutation(int n, char **s)
{
	/**
	* Complete this method
	* Return 0 when there is no next permutation and 1 otherwise
	* Modify array s to its next permutation
	*/
	int i = n - 1;
	while (i > 0) {
	    if (strcmp(s[i - 1], s[i]) <= 0) {
            i--;
            continue;
        }
        if (i == n - 1) {
            char *temp = s[i];
            s[i] = s[i - 1];
            s[i - 1] = temp;
        }
        else if (strcmp(s[i - 1], s[i + 1]) <= 0) {
            char *temp = s[i];
            s[i] = s[n - 1];
            s[n - 1] = s[i - 1];
            s[i - 1] = temp;
        }
        else {
            char *temp = s[i];
            s[i] = s[i - 1];
            s[i - 1] = s[n - 1];
            s[n - 1] = temp;
        }
        return 1;
	    i--;
	}
	if (i <= 0) {
        return 0;
    }



    return 1;
}