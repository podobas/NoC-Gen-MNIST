all:
	python train.py
	gcc -DREAL=float -O3 -c *.c
	#gcc -O0 -c -DREAL=float cpu_0.c 	
	#gcc -O0 -c -DREAL=float cpu_1.c
	#gcc -O0 -c -DREAL=float cpu_2.c
	#gcc cpu_0.o cpu_1.o cpu_2.o -o run
	gcc *.o -o run
clean:
	rm -rf *.o p*.h
