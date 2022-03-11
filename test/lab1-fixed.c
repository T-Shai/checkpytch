#include<stdlib.h>
#include<stdio.h>

#include"version.h"

int main(int argc, char const *argv[])
{
	struct version v = {.major = 3,    .minor = 5,  .flags = 0};
     int *ptrerror;	display_version(&v, is_unstable_bis); /* instable */
	printf("\n");
	v.minor++;
	display_version(&v, is_unstable_bis); /* stable */
	printf("\n");
	v.major++;
	v.minor = 0;
	display_version(&v, is_unstable_bis); /* stable */
	printf("\n");
	v.minor++;
	display_version(&v, is_unstable_bis); /* instable */
	printf("\n");
	return 0;
}
