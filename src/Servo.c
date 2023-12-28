#include "Servo.h"

void init_tpm2(){
	
	// TPM2 Clock Gate Control - Clock enabled
	SIM->SCGC6 |= SIM_SCGC6_TPM2(1);
	// Selectam sursa de ceas pentru TPM: MCGFLLCLK -> 48 MHz max
	SIM->SOPT2 |= SIM_SOPT2_TPMSRC(1);
	// Setam prescale factor : 111 -> divide by 128
	//  48 MHz / 128 = 375 kHz
	
	//Dezactivam counter-ul in timpul configurarii in mod explicit, default valoarea este 0 (CMOD)
	 TPM2->SC = 0;
	
	 TPM0->MOD = PG90_PWM_PERIOD * CLOCK_FREQ;
		//Center-aligned PWM/high-true pulses
	 TPM2->CONTROLS[0].CnSC = TPM_CnSC_MSB_MASK | TPM_CnSC_ELSB_MASK;
	
	 TPM2->SC |= TPM_SC_CMOD(1);
}


void setPG90_angle(){
	
	dutyCycle=DUTY_CYCLE_180;
	TPM2->CONTROLS[0].CnV=dutyCycle* CLOCK_FREQ;
}