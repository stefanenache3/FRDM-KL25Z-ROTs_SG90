#include "MKL25Z4.h"
#include "Sequencer.h"
#include "pit.h"
#include "uart.h"
int main(void){
	
	UART0_Initialize(115200);
	led_init();
	PIT_Init();
	while(1){
		
	}
	return 0;
}