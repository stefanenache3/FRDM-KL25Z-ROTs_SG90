#include "pit.h"
#include "Sequencer.h"

void PIT_Init(void) {
	
	// Activarea semnalului de ceas pentru perifericul PIT
	SIM->SCGC6 |= SIM_SCGC6_PIT_MASK;
	// Utilizarea semnalului de ceas pentru tabloul de timere
	PIT_MCR &= ~PIT_MCR_MDIS_MASK;
	// Oprirea decrementarii valorilor numaratoarelor in modul debug
	PIT->MCR |= PIT_MCR_FRZ_MASK;
	// Setarea valoarea numaratorului de pe canalul 0 la o perioada de 629 ms
	PIT->CHANNEL[0].LDVAL = 0x64A3D6;
	
  // Activarea Óntreruperilor pe canalul 0
	PIT->CHANNEL[0].TCTRL |= PIT_TCTRL_TIE_MASK;
	// Activarea timerului de pe canalul 0
	PIT->CHANNEL[0].TCTRL |= PIT_TCTRL_TEN_MASK;
	
	
	
	// Activarea Óntreruperii mascabile si setarea prioritatiis
	NVIC_ClearPendingIRQ(PIT_IRQn);
	NVIC_SetPriority(PIT_IRQn,5);
	NVIC_EnableIRQ(PIT_IRQn);
}
void PIT_IRQHandler(void) {
	static uint32_t led_turn=0;
	
	if(PIT->CHANNEL[0].TFLG & PIT_TFLG_TIF_MASK) {
		led_turn++;
		led_turn=led_turn%4;
		PIT->CHANNEL[0].TFLG &= PIT_TFLG_TIF_MASK;
		sequence_leds(led_turn);
	}
	
}