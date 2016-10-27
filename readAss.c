#include <stdlib.h>
#include <stdio.h>

#include "constants.h"

int main(int argc, char *argv[]) {
	//echo cape-bone-iio > /sys/devices/bone_capemgr.*/slots
	// printf("Starting\n");
	FILE *fp;
	//= fopen("/sys/devices/bone_capemgr.*/slots", "rw");
	// printf("Opened\n");
	// fputs("cape-bone-iio", fp);
	// printf("Written\n");
	// fclose(fp);
	// printf("Closed\n");
	printf("Opened again\n");

	char buff[256];




	while (1 == 1) {
		fp = fopen("/sys/devices/ocp.3/helper.15/AIN0", "rw");
		if (fp == 0) {
			printf("Ya done goofed...\n");
			return -1;
		}
		fgets(buff, 256, fp);
		printf("The voltage: %s\n", buff);
		fclose(fp);
	}
}

double scale_flex(int vin) {
	vin -= FLEX_MIN;
	double proportion = vin * INV_FLEX_RANGE;
	return proportion;
}
