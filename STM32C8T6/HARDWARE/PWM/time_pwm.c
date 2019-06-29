#include "time_pwm.h"
#include "cube.h"



void TIM2_PWM(u16 arr, u16 psc)
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	TIM_OCInitTypeDef TIM_OCInitStructure;
	GPIO_InitTypeDef GPIO_InitPWM;
	NVIC_InitTypeDef NVIC_InitMYTIM;
	
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA  | RCC_APB2Periph_AFIO, ENABLE);  //使能GPIO外设和AFIO复用功能模块时钟
	
	GPIO_InitPWM.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitPWM.GPIO_Pin=GPIO_Pin_3;
	GPIO_InitPWM.GPIO_Speed=GPIO_Speed_50MHz;
	
	GPIO_Init(GPIOA,&GPIO_InitPWM);	
	
	
	// 时基配置：配置PWM输出定时器——TIM2
	/* Time base configuration */
	TIM_TimeBaseStructure.TIM_Period = arr;
	TIM_TimeBaseStructure.TIM_Prescaler = psc;
	TIM_TimeBaseStructure.TIM_ClockDivision = 0;
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure);
	
	TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE ); //使能指定的TIM3中断,允许更新中断
	// 输出配置：配置PWM输出定时器——TIM2
	/* PWM1 Mode configuration: Channel1 */
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2;
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low;
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;
	TIM_OCInitStructure.TIM_Pulse = arr>>1;//50%
	TIM_OC4Init(TIM2, &TIM_OCInitStructure);
	TIM_OC4PreloadConfig(TIM2, TIM_OCPreload_Enable);
	
	
	NVIC_InitMYTIM.NVIC_IRQChannel=TIM2_IRQn;
	NVIC_InitMYTIM.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitMYTIM.NVIC_IRQChannelPreemptionPriority=1;
	NVIC_InitMYTIM.NVIC_IRQChannelSubPriority=1;
	
	NVIC_Init(&NVIC_InitMYTIM);
	
	TIM_Cmd(TIM2, ENABLE);
}


extern u8 step;
extern u8 IT_flag;


#define ACC_STEP_NUM 100
unsigned short AccStep[ACC_STEP_NUM] = {
2361,2353,2338,2323,2300,2278,2243,2209,2162,2105,
2040,1962,1880,1782,1682,1579,1475,1371,1277,1188,
1108,1037,978,929,887,853,826,804,785,772,
760,752,745,739,735,732,729,727,726,724,
724,723,722,721,721,721,721,721,721,720,
720,720,720,720,720,720,720,720,720,720,
720,720,720,720,720,720,720,720,720,720,
720,720,720,720,720,720,720,720,720,720,
720,720,720,720,720,720,720,720,720,720,
720,720,720,720,720,720,720,720,720,720,
};

#define MAXSPEED 720000/AccStep[99]
#define TS       10

void TIM2_IRQHandler(void)
{
	static u16 tt = 0;
	u16 temp = 0;
	if (TIM_GetITStatus(TIM2, TIM_IT_Update))
	{
		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
		if(tt<step)
		{
			if((step - tt) < TS)
			{
				temp = 720000/(1500 - 140 * (TS + tt - step));
				TIM_SetAutoreload(TIM2, temp);
				TIM_SetCompare4(TIM2, temp/2);	
			}
			
			else
			{
				TIM_SetAutoreload(TIM2,  AccStep[tt]);
				TIM_SetCompare4(TIM2, AccStep[tt]/2);
			}
		}
		else
		{
			IT_flag = 1;
			TIM_Cmd(TIM2, DISABLE);
			tt = 0;
		}
		tt ++;
		
	}
}
	
