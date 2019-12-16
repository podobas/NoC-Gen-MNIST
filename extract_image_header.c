#include<stdio.h>
#include<stdlib.h>
#include "mnist.h"

#define REAL float

REAL max (REAL a, REAL b)
{ if (a > b) return a; return b;}


int main ( int argc, char **argv)
{
  load_mnist();
  
  if (argv[1] == NULL)
    { fprintf (stderr,"Please specificy the number of images to extract as first argument.\n"); return 0;}
  
  int nImg = atoi(argv[1]);
  FILE *fp = fopen("image.h","w");
  fprintf(fp,"#define NUM_IMAGE %d\n",nImg);
  fprintf(fp,"unsigned char image[NUM_IMAGE][784] = {");
  for (int img = 0; img != nImg; img++)
    {
      fprintf(fp,"{");
      for (int k = 0; k != 28*28; k++)
	fprintf(fp,"%c %d", (k==0 ? ' ' : ','), test_image_char[img][k]);
      fprintf(fp,"}%c \n", (img == nImg-1 ? ' ' : ','));
    }
  fprintf(fp,"};\n");
  
  return 0;
}
