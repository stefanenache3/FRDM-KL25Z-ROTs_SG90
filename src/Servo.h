#include "MKL25Z4.h"
#define PG90_PWM_PERIOD		(20)		//20ms
#define CLOCK_FREQ				(375)		//375KHz


#define DUTY_CYCLE_0			(0.5)
#define DUTY_CYCLE_90			(1.5)
#define DUTY_CYCLE_180		(2.5)		  //2ms


#define SERVO_PIN					(1)			//PTA1
void init_tpm2();
void setPG90_angle(uint32_t angle);