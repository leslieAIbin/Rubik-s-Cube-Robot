#ifndef __CUBE_H
#define __CUBE_H
#include "sys.h"
#include "stm32f10x.h"

#define  DIR   PAout(4)

#define  EN1   PBout(5)
#define  EN2   PBout(4)
#define  EN3   PBout(3)
#define  EN4   PAout(5)
#define  EN5   PAout(6)
#define  EN6   PAout(7)


void cube_solve(u8 * str);
void motor(u8 side,int direction);

void gpioinit(void);

#endif

