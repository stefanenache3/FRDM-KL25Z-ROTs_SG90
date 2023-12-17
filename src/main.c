#include "MKL25Z4.h"
#include "Sequencer.h"
int main(void){
	
	while(1){
			led_init();
			sequence_leds();
			delay(500000);
	}
	return 0;
}