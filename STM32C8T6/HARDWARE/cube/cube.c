#include "cube.h"
#include "time_PWM.h"
#include "usart.h"
#include "delay.h"

/*PWM输出空闲标志
0：空闲
1：占用
在定时器中断中清0
*/
u8 IT_flag = 0;
u8 step = 0; 
/********************************
* 接收的指令格式为 *U0R1B2F1#
*	*表示开始  #表示结束
* 一个面字母加一个方向数字
* 0 表示顺时针旋转90度
* 1 表示逆时针旋转90度
* 2 表示旋转180度
*********************************/

void cube_solve(u8 *str)
{
	int j = 0;
	// j表示控制复原步数，不会超过上帝之数
	if(*str == '*')
	{
		str+=1;
		while(*str != '#' && j < 25)
		{
			switch(*str)
			{
				case 'U':EN2 = 0;break;
				case 'R':EN6 = 0;break;
				case 'F':EN4 = 0;break;
				case 'D':EN5 = 0;break;
				case 'L':EN1 = 0;break;
				case 'B':EN3 = 0;break;
			}
			switch(*(str+1))
			{
				case '0':DIR = 0;step=50;break;
				case '1':DIR = 1;step=50;break;
				case '2':step=100;break;
			}
			IT_flag = 0;
			TIM_OC4PreloadConfig(TIM2, TIM_OCPreload_Enable);
			TIM_Cmd(TIM2, ENABLE);
			
			while(!IT_flag);
			delay_ms(10);
			EN1 = 1;EN2 = 1;EN3 = 1;EN4 = 1;EN5 = 1;EN6 = 1;
			str += 2;
		}
		j++;
	}

}



/*初始化方向控制和使能控制*/
void gpioinit(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;
 	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_GPIOB|RCC_APB2Periph_AFIO, ENABLE);	
	
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7;				 
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		
	GPIO_Init(GPIOA, &GPIO_InitStructure);			

	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	
	//使能输出高
	GPIO_SetBits(GPIOA,GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7);
	GPIO_SetBits(GPIOB,GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5);
	
}
