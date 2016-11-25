#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "constants.h"
#include "utilities.h"
#include "readAss.h"

#include "fingerGestureRecognizer.h"

int main() {
	while (1 == 1) {
		double convertVolt1 = readFileAss("/sys/devices/ocp.3/helper.15/AIN0", "AIN0");
		double convertVolt2 = readFileAss("/sys/devices/ocp.3/helper.15/AIN2", "AIN2");
		double convertVolt3 = readFileAss("/sys/devices/ocp.3/helper.15/AIN6", "AIN6");
		double convertVolt4 = readFileAss("/sys/devices/ocp.3/helper.15/AIN4", "AIN4");

		fingerPosition pos1 = detectPos(convertVolt1);
		fingerPosition pos2 = detectPos(convertVolt2);
		fingerPosition pos3 = detectPos(convertVolt3);
		fingerPosition pos4 = detectPos(convertVolt4);

		if (pos1 == OPEN) {
			if (pos2 == CLOSED && pos3 == CLOSED && pos4 == closed) {
				printf("You're pointing at something!\n");
			}
			else {
				printf("Only 1 finger right\n");
			}
		}
		else {
			printf("Nothing detected\n");
		}
	}
}