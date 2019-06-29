#include "led.h"
#include "delay.h"
#include "key.h"
#include "sys.h"
#include "usart.h"
#include "cube.h"
#include "time_PWM.h"

extern u8 finish;
extern u16 IT_flag_3;

int fre_temp = 500;
u8 en = 0;
u8 dir = 0;
u8 step_temp = 1;

extern unsigned short AccStep[100];
 int main(void)
 {	
	delay_init();	    	 //��ʱ������ʼ��	  
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);	 //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
	uart_init(115200);	 	//���ڳ�ʼ��Ϊ115200
 	LED_Init();			     //LED�˿ڳ�ʼ��

	gpioinit();
	TIM2_PWM(AccStep[0], 99);
	
	en = 0;
	
  while(1) 
	{		
		if(finish)
		{
			cube_solve(USART_RX_BUF);
			finish = 0;
		}
		//motor('D',1);
		//printf("test\n");
		switch(en)
		{
			case 1:
				EN1 = 0;
				break;
			case 2:
				EN2 = 0;
				break;
			case 3:
				EN3 = 0;
				break;
			case 4:
				EN4 = 0;
				break;
			case 5:
				EN5 = 0;
				break;
			case 6:
				EN6 = 0;
				break;
			default:
				EN1 = 1;
				EN2 = 1;
				EN3 = 1;
				EN4 = 1;
				EN5 = 1;
				EN6 = 1;
				
		}
		LED0=!LED0;	
		delay_ms(200);


	} 
}
