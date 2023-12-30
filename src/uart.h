#include "MKL25Z4.h"


extern uint8_t led_sequence_direction;
void UART0_Transmit(uint8_t data);
uint8_t UART0_Receive(void);
void UART0_Initialize(uint32_t baud_rate);
void UART0_IRQHandler(void);