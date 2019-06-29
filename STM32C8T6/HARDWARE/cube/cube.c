#include "cube.h"
#include "time_PWM.h"
#include "usart.h"
#include "delay.h"

/*PWM������б�־
0������
1��ռ��
�ڶ�ʱ���ж�����0
*/
u8 IT_flag = 0;
u8 step = 0; 
/********************************
* ���յ�ָ���ʽΪ *U0R1B2F1#
*	*��ʾ��ʼ  #��ʾ����
* һ������ĸ��һ����������
* 0 ��ʾ˳ʱ����ת90��
* 1 ��ʾ��ʱ����ת90��
* 2 ��ʾ��ת180��
*********************************/

void cube_solve(u8 *str)
{
	int j = 0;
	// j��ʾ���Ƹ�ԭ���������ᳬ���ϵ�֮��
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



/*��ʼ��������ƺ�ʹ�ܿ���*/
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
	
	//ʹ�������
	GPIO_SetBits(GPIOA,GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7);
	GPIO_SetBits(GPIOB,GPIO_Pin_3|GPIO_Pin_4|GPIO_Pin_5);
	
}
