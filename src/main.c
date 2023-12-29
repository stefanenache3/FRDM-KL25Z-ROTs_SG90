#include "MKL25Z4.h"
#include "Sequencer.h"
#include "pit.h"
int main(void){
	
	led_init();
	PIT_Init();
	while(1){}
	return 0;
}