all:
	python train.py
	gcc -DSOFTWARE -DREAL=float -O3 -c *.c
	gcc cpu_*.o -o run


noc:
	python train.py
	gcc extract_image_header.c -o extract
	./extract 10000
	gcc -DREAL=float -O3 -c cpu_*.c
	gcc cpu_*.o -o run


clean:
	rm -rf *.o p*.h
