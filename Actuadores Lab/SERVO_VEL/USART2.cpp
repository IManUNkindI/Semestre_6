#include "stm32f7xx.h"
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include <math.h>
#include <stdlib.h>

void SysTick_Init(void);
void SysTick_Wait(uint32_t);
void SysTick_Wait1ms(uint32_t);

unsigned long int BAUDRATE,Over8;
using namespace std;
char data;
char arreglo[5];
int dato2;
int a=0,len=0,add=0,sum=0, total=0;
int sum2=0;
int mui=0;
char envio_array[10];//={' ', ' ',' ',' ',' ',' ',' ',' ',' ',' '};

//std::string str = std::to_string(sum);
//char const* envio_array = str.c_str();
//char* envio = const_cast<char*>(str.c_str());
int USART_SendChar3(int value);

int DRNK[4] = {0x3E,0x30,0x34,0x52};
int HBRG[4] = {0x36,0x7C,0x30,0x7D};
int CTDG[4] = {0x59,0x31,0x3E,0x7D};
int ONRG[4] = {0x5F,0x34,0x30,0x7D};
int FRCH[4] = {0x71,0x30,0x59,0x36};
int CONE[4] = {0x59,0x5F,0x34,0x79};
int BGMQ[4] = {0x7C,0x7D,0x15,0x5C};

int main(void){
	// Display
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN;
	GPIOD->MODER|=0x1555;
	GPIOD->OTYPER|=0x0;
	GPIOD->OSPEEDR|=0x0;
	GPIOD->PUPDR|=0x0;
	
	SysTick_Init();
	
	//USART 3 PD8(TX) y PD9(RX) 
	RCC->APB1ENR |= RCC_APB1ENR_USART3EN;
	Over8=0;
	BAUDRATE= 0x683; //9600
	GPIOD->MODER |= 0XA0000; 
	GPIOD->AFR[1] |=0X77;
	USART3->BRR |= BAUDRATE;
	USART3->CR1 |=(USART_CR1_TE | USART_CR1_UE | USART_CR1_RE | USART_CR1_RXNEIE | Over8<<15);
	NVIC_EnableIRQ(USART3_IRQn);

while(1){
			if(a==1){
			arreglo[4] = ' ';
			data=' ';
			len=0;
			mui=0;
			GPIOD->ODR &=~0xFFFF;
			SysTick_Wait1ms(1000);
			}
}}

 int USART_SendChar3(int value) { 
   USART3->TDR = value;
   while(!(USART3->ISR & USART_ISR_TXE));
   return 0;
 }
 
 void entero_Cad(int n){
	  sprintf(envio_array, "%d", sum);
	  if(n==1){
		for(int i=0; i<6; i++){
			 USART_SendChar3(envio_array[i]);
			 SysTick_Wait1ms(500);
		}
		USART_SendChar3(' ');
		USART_SendChar3('T');
		USART_SendChar3('O');
		USART_SendChar3('T');
		USART_SendChar3('A');
		USART_SendChar3('L');
		USART_SendChar3('=');
		sprintf(envio_array, "%d", total);
		for(int i=0; i<6; i++){
			 USART_SendChar3(envio_array[i]);
			 SysTick_Wait1ms(500);
		}
		USART_SendChar3('\n');
		
		a=1;
	} 	
}
 
extern "C"{
void USART3_IRQHandler(void){
				while (USART3->ISR & USART_ISR_RXNE){
				data =(USART3->RDR & 0xFF); // RXNE ACTIVA RECIBE CHAR
				arreglo[len] = data;
				len++;

				if((arreglo[1] == 68) && (arreglo[2] == 82)&& (arreglo[3] == 78)&& (arreglo[4] == 75)){
				for(int f=0; f<4; f++){
				GPIOD->ODR = DRNK[f];
				SysTick_Wait1ms(1000);
				}	
				mui=atoi(arreglo);
				sum = mui * 8000;
				total = total + sum;
				SysTick_Wait1ms(1000);
				entero_Cad(1);		
			}
			 else if((arreglo[1] == 72) && (arreglo[2] == 66)&& (arreglo[3] == 82)&& (arreglo[4] == 71)){
				for(int f=0; f<4; f++){
				GPIOD->ODR = HBRG[f];
				SysTick_Wait1ms(1000);
				}	
			  mui=atoi(arreglo);
				sum = mui * 12000;
				total = total + sum;
				SysTick_Wait1ms(1000);
				entero_Cad(1);
		  }
			 else if((arreglo[1] ==67) && (arreglo[2] == 84)&& (arreglo[3] == 68)&& (arreglo[4] == 71)){
					for(int f=0; f<4; f++){
					GPIOD->ODR = CTDG[f];
					SysTick_Wait1ms(1000);
				}
				mui=atoi(arreglo);
				sum = mui * 9000;
				total = total + sum;
				entero_Cad(1);
				SysTick_Wait1ms(1000);
		  }
			 else if((arreglo[1] ==79) && (arreglo[2] == 78)&& (arreglo[3] == 82)&& (arreglo[4] == 71)){
					for(int f=0; f<4; f++){
					GPIOD->ODR = ONRG[f];
					SysTick_Wait1ms(1000);
				}
				mui=atoi(arreglo);
				sum = mui * 4000;
				total = total + sum;
				entero_Cad(1);
				SysTick_Wait1ms(1000);
		  }
			 else if((arreglo[1] ==70) && (arreglo[2] == 82)&& (arreglo[3] == 67)&& (arreglo[4] == 72)){
					for(int f=0; f<4; f++){
					GPIOD->ODR = FRCH[f];
					SysTick_Wait1ms(1000);
				}
				mui=atoi(arreglo);
				sum = mui * 6000;
				total = total + sum;
				entero_Cad(1);
				SysTick_Wait1ms(1000);
		  }
			 else if((arreglo[1] ==67) && (arreglo[2] == 79)&& (arreglo[3] == 78)&& (arreglo[4] == 69)){
					for(int f=0; f<4; f++){
					GPIOD->ODR = CONE[f];
					SysTick_Wait1ms(1000);
				}
				mui=atoi(arreglo);
				sum = mui * 2000;
				total = total + sum;
				entero_Cad(1);
				SysTick_Wait1ms(1000);
		  }
			 else if((arreglo[1] ==66) && (arreglo[2] == 71)&& (arreglo[3] == 77)&& (arreglo[4] == 81)){
					for(int f=0; f<4; f++){
					GPIOD->ODR = BGMQ[f];
					SysTick_Wait1ms(1000);
				}
				mui=atoi(arreglo);
				sum = mui * 21500;
				total = total + sum;
				entero_Cad(1);
				SysTick_Wait1ms(1000);
		  }
     } 
}
}
void SysTick_Init(void){
	SysTick->LOAD = 0x00FFFFFF;
	SysTick->CTRL = 0x00000005;
}

void SysTick_Wait(uint32_t n){
	SysTick->LOAD = n-1;
	SysTick->VAL = 0;
	while((SysTick->CTRL&(1<<16))== 0){};
}

void SysTick_Wait1ms(uint32_t delay){
	for(uint32_t i=0; i<delay;i++){
		SysTick_Wait(16000);
	}
}
		