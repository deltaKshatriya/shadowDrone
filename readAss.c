#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "constants.h"
#include "utilities.h"
#include "readAss.h"

int main(int argc, char *argv[]) {
	//echo cape-bone-iio > /sys/devices/bone_capemgr.*/slots
	// printf("Starting\n");
	
	//= fopen("/sys/devices/bone_capemgr.*/slots", "rw");
	// printf("Opened\n");
	// fputs("cape-bone-iio", fp);
	// printf("Written\n");
	// fclose(fp);
	// printf("Closed\n");
	printf("Opened again\n");

	




	while (1 == 1) {
		// fp = fopen("/sys/devices/ocp.3/helper.15/AIN0", "rw");
		// if (fp == 0) {
		// 	printf("Ya done goofed...\n");
		// 	return -1;
		// }
		// fgets(buff, 256, fp);
		// printf("The voltage: %s\n", buff);
		// fclose(fp);
		char buffy[100];
		printf("Do you really want this?\n");
		scanf("%s", buffy);
		double convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN0", "AIN0");

		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN2", "AIN2");
		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN6", "AIN6");
		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN4", "AIN4");
	}
}

int readFileAss(char *fileName, char *name) {
	FILE *fp;
	char buff[256];
	fp = fopen(fileName, "r");
	if (fp == 0) {
		printf("Ya done goofed...\n");
		return -1;
	}
	fgets(buff, 256, fp);
	double convertVolt = scale_flex(atoi(buff));
	printf("The voltage for %s: %f\n and voltage is: %s\n", name, convertVolt, buff);
	if (detectPos(convertVolt) == CLOSED) {
		printf("Finger %s is closed\n", name);
	}
	else {
		printf("Finger %s is open! Please close!\n", name);
	}
	fclose(fp);
	return convertVolt;
}

double scale_flex(int vin) {
	vin -= FLEX_MIN;
	double proportion = vin * INV_FLEX_RANGE;
	proportion = coerce(proportion, 0, 1);
	return proportion;
}

fingerPosition detectPos(double input) {
	if (input > 0.5) {
		return CLOSED; 
	}
	else {
		return OPEN;
	}
}
