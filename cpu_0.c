#include<stdio.h>
#include<stdlib.h>
#include "mnist.h"
#include "cpu_0.h"

REAL max (REAL a, REAL b)
{ if (a > b) return a; return b;}

struct { REAL val[ 784 ]; } frame_1;
struct { REAL val[10]; } final_frame;


extern void process1();
extern void process2();

int main ( int argc, char **argv)
{
  load_mnist();

  int correct = 0;
  for (int img = 0; img != 10000; img++)
    {
      // Copy new image into frame
      for (int cpy = 0; cpy != 784; cpy++)
	frame_1.val[cpy] = (REAL)(test_image[img][cpy]);

      RUN_LAYERS;
      
      // Check results and compare correcntess
      int largest = 0;
      for (int i = 0; i != 10; i++)
	if (final_frame.val[largest] < final_frame.val[i])
	  largest = i;
      if (test_label[img] == largest)
	correct++;
    }
  fprintf(stderr,"Test accuracy: %f\n",(REAL)correct / (REAL)10000);
}
