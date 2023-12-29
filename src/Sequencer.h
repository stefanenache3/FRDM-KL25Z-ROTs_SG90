#include "MKL25Z4.h"

#define RED_LED_PIN 		18
#define GREEN_LED_PIN		19
#define BLUE_LED_PIN		1

void delay(long int n);
void led_init();
void sequence_leds(uint32_t state);
