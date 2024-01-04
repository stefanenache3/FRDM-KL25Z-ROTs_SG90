#include "MKL25Z4.h"
#include "Sequencer.h"
#include "pit.h"
#include "uart.h"
#include "adc.h"
int main(void){
	UART0_Initialize(38400);
	ADC0_Init();
		
	led_init();	
	PIT_Init();


	
	while(1){
		
	}
	return 0;
}
