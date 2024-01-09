#include "MKL25Z4.h"
#define PG90_PWM_PERIOD		(20)		//20ms
#define CLOCK_FREQ				(375)		//375KHz


#define DUTY_CYCLE_0			(365)
#define DUTY_CYCLE_90			(195)
#define DUTY_CYCLE_180		(77)		  //2ms


#define SERVO_PIN					(2)			//PTB2
void init_tpm2();
void setPG90_angle(uint32_t angle);