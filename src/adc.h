#include "MKL25Z4.h"
#define FIRST_INTERVAL 0
#define SECOND_INTERVAL 1
#define THIRD_INTERVAL 2

void ADC0_Init(void);
int ADC0_Calibrate(void);
int ADC1_Calibrate(void);
uint16_t ADC0_Read(uint8_t);
void ADC0_Func(void);
//void ADC1_Func(void);