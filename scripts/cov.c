#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* to compile this scrip
 * gcc -Wall -O2 -o cov cov.c
 */

int main(int argc, char **argv)
{
    //FILE *fptr = fopen(argv[1], "r");
    FILE *fptr = stdin;
    
    //check if file exists
    if (fptr == NULL){
        printf("No stdin was presents");
        return 0;
    }
    
    //read line by line
    const size_t line_size = 31;
    // this creates on the stack, whereas if malloc used - that is heap and will need to be freed manually
    char line[line_size];
    int last_depth = -1;
    int last_loc = 0;
    int prev_loc = -1;
    char prev_chr[line_size];

    prev_chr[0] = 0;

    char chr[line_size]; // is already a pinter
    int loc, depth; // these aren't pointer hence then ampersand

    // pass in on cmd track name
    char track_name[line_size];
    if(argc > 1)
	strcpy(track_name, argv[1]);
    else
	strcpy(track_name, "cov_track");

    // colors:
    // forward: '255,75,50'
    // reverse: '50,150,255'

    while(fgets(line, line_size, fptr) != NULL)  {

	sscanf(line, "%s\t%d\t%d", chr, &loc, &depth);

        // also need to check sscanf for things that it returns
	// if I did prev_chr == chr, i;ll be comparing pointer and that is if the poitner pointing to the same place in memory
	// whereas with ints i'm comparing ints directly
	if(strcmp(prev_chr, chr) != 0 || depth != last_depth) {

	    if(last_depth != -1) {
		//printf("%s %d %d %d\n", prev_chr, prev_loc, last_loc, last_depth);
		printf("%s\t%d\t%d\t%d\n", prev_chr, prev_loc-1, last_loc, last_depth);
	    	strcpy(prev_chr, chr);
	    	prev_loc = loc;
	    
	    }
	    else {
	        //printf("track type=bedGraph name=%s visibility=full color=%s autoScale=on graphType=bar windowingFunction=mean transformFunc=LOG\n", track_name, "255,75,50");
	    	strcpy(prev_chr, chr);
		prev_loc = loc;
	    }
	}

	last_depth = depth;
	last_loc = loc;
    }
    printf("%s\t%d\t%d\t%d\n", prev_chr, prev_loc-1, last_loc-1, last_depth);

    fclose(fptr);
    return 0;
}
