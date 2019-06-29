#ifndef __TIMER_PWM_H
#define __TIMER_PWM_H	 
#include "sys.h"
#include "stm32f10x.h"
void TIM2_PWM(u16 arr, u16 psc);

void set_step(u8 stepe);

#endif
