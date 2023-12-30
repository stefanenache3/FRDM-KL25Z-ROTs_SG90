#include "MKL25Z4.h"
#include "Sequencer.h"
#include "pit.h"
#include "uart.h"
#include "adc.h"
int main(void){

	
	led_init();	
	PIT_Init();

	UART0_Initialize(115200);
	ADC0_Init();

	
	while(1){
		
	}
	return 0;
}
