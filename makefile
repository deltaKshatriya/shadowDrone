CC = gcc
CFLAGS = -g
CFILES = utilities.c readAss.c
OFILES = utilities.o readAss.o
HFILES = utilities.h readAss.h constants.h
LIBES = 


all: utilities readAss

utilities: $(OFILES)
	$(CC) -o utilities $(CFLAGS) $(OFILES) $(LIBES)

utilities.o: utilities.c $(HFILES)
	$(CC) $(CFLAGS) -c utilities.c

readAss: $(OFILES)
	$(CC) -o readAss $(CFLAGS) $(OFILES) $(LIBES)

readAss.o: readAss.c $(HFILES)
	$(CC) $(CFLAGS) -c readAss.c

clean:
	rm -f *.o *~
	
