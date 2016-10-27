CC = gcc
CFLAGS = -g
CFILES = readAss.c
OFILES = readAss.o
HFILES = readAss.h constants.h
LIBES = 


all: $(OFILES)
	$(CC) -o readAss $(CFLAGS) $(OFILES) $(LIBES)

readAss.o: readAss.c $(HFILES)
	$(CC) $(CFLAGS) -c readAss.c

clean:
	rm -f *.o *~
	
