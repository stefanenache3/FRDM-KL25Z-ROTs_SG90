#include "Sequencer.h"

void led_init(){
	
	SIM->SCGC5 |= SIM_SCGC5_PORTB_MASK | SIM_SCGC5_PORTD_MASK ;
	
	PORTB->PCR[RED_LED_PIN]=~PORT_PCR_MUX_MASK;
	PORTB->PCR[RED_LED_PIN] |= PORT_PCR_MUX(1);
	
	PORTB->PCR[GREEN_LED_PIN]=~PORT_PCR_MUX_MASK;
	PORTB->PCR[GREEN_LED_PIN] |= PORT_PCR_MUX(1);
	
	PORTD->PCR[BLUE_LED_PIN] = ~PORT_PCR_MUX_MASK;
	PORTD->PCR[BLUE_LED_PIN] |= PORT_PCR_MUX(1);
	
	PTB->PDDR |= (1 << RED_LED_PIN); 
	PTB->PDDR |= (1 << GREEN_LED_PIN);
	PTD->PDDR |= (1 << BLUE_LED_PIN);
	
	PTB->PSOR = (1 << RED_LED_PIN); 
	PTB->PSOR = (1 << GREEN_LED_PIN);
	PTD->PSOR = (1 << BLUE_LED_PIN);
	
	
}

void sequence_leds(uint32_t state){
	
	switch(state){
		
	case 0:
		PTB->PCOR=(1<<RED_LED_PIN);
		PTB->PCOR=(1<<GREEN_LED_PIN);
		PTD->PCOR=(1<<BLUE_LED_PIN);	
		break;
	

	case 1:
		PTB->PCOR = (1 << GREEN_LED_PIN);
		PTB->PSOR = (1 << RED_LED_PIN);
		PTD->PSOR = (1 << BLUE_LED_PIN);
	  break;
	case 2:
		PTB->PSOR = (1 << GREEN_LED_PIN);
		PTB->PSOR = (1 << RED_LED_PIN);
		PTD->PCOR = (1 << BLUE_LED_PIN);
		break;
	case 3:
		PTB->PCOR = (1 << GREEN_LED_PIN);
		PTB->PCOR = (1 << RED_LED_PIN);
		PTD->PSOR = (1 << BLUE_LED_PIN);
		break;
	}
}
