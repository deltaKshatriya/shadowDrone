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
	// printf("Opened again\n");

	




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
		double convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN0", "AIN0", 0);
		//double convertVolt = scale_flex(1000, 0);
		fingerPosition pos0 = detectPos(convertVolt);
		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN2", "AIN2", 2);
		//convertVolt = scale_flex(1000, 2);
		fingerPosition pos1 = detectPos(convertVolt);
		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN6", "AIN6", 6);
		//convertVolt = scale_flex(1000, 6);
		fingerPosition pos2 = detectPos(convertVolt);
		convertVolt = readFileAss("/sys/devices/ocp.3/helper.15/AIN4", "AIN4", 4);
		//convertVolt = scale_flex(1000, 4);
		fingerPosition pos3 = detectPos(convertVolt);

		if (pos0 == OPEN) {
			printf("The 0th finger is open\n");
		}
		else if (pos0 == CLOSED) {
			printf("The 0th finger is closed\n");
		}
		else {
			printf("The 0th finger is halfway\n");
		}

		if (pos1 == OPEN) {
			printf("The 1st finger is open\n");
		}
		else if (pos1 == CLOSED) {
			printf("The 1st finger is closed\n");
		}
		else {
			printf("The 1st finger is halfway\n");
		}

		if (pos2 == OPEN) {
			printf("The 2nd finger is open\n");
		}
		else if (pos2 == CLOSED) {
			printf("The 2nd finger is closed\n");
		}
		else {
			printf("The 2nd finger is halfway\n");
		}

		if (pos3 == OPEN) {
			printf("The 3rd finger is open\n");
		}
		else if (pos3 == CLOSED) {
			printf("The 3rd finger is closed\n");
		}
		else {
			printf("The 3rd finger is halfway\n");
		}
	}
}

int readFileAss(char *fileName, char *name, int inputNum) {
	FILE *fp;
	char buff[256];
	fp = fopen(fileName, "r");
	if (fp == 0) {
		printf("Ya done goofed...\n");
		return -1;
	}
	fgets(buff, 256, fp);
	double convertVolt = scale_flex(atoi(buff), inputNum);
	printf("The voltage for %s: %f\n and voltage is: %s\n", name, convertVolt, buff);
	// fingerPosition fingered = detectPos(convertVolt);
	// if (fingered == CLOSED) {
	// 	printf("Finger %s is closed\n", name);
	// }
	// else  if (fingered == OPEN) {
	// 	printf("Finger %s is open! Please close!\n", name);
	// }
	// else {
	// 	printf("Finger %s is halfway! You can do it! You're almost there!\n", name);
	// }
	fclose(fp);
	return convertVolt;
}

double scale_flex(int vin, int inputNum) {
	if (inputNum == 0) {
		vin -= FLEX_MIN_AIN0;
		double proportion = vin * INV_FLEX_RANGE_AIN0;
		proportion = coerce(proportion, 0, 1);
		return proportion;
	}
	if (inputNum == 2) {
		vin -= FLEX_MIN_AIN2;
		double proportion = vin * INV_FLEX_RANGE_AIN2;
		proportion = coerce(proportion, 0, 1);
		return proportion;
	}
	if (inputNum == 4) {
		vin -= FLEX_MIN_AIN4;
		double proportion = vin * INV_FLEX_RANGE_AIN4;
		proportion = coerce(proportion, 0, 1);
		return proportion;
	}
	if (inputNum == 6) {
		vin -= FLEX_MIN_AIN6;
		double proportion = vin * INV_FLEX_RANGE_AIN6;
		proportion = coerce(proportion, 0, 1);
		return proportion;
	}
}

fingerPosition detectPos(double input) {
	if (input >= 0.2 && input <= 0.6) {
		return HALFWAY;
	}
	if (input > 0.6) {
		return CLOSED; 
	}
	else {
		return OPEN;
	}
}