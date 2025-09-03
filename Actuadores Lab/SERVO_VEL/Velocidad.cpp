#include <stm32f767xx.h>
#include "SysTick.h"

#include <math.h>
#include <stdio.h>
#include <string.h>

void RCC_SETUP();
void GPIO_SETUP();
void DAC_SETUP();
void USART_SETUP();
void ADC_SETUP();
void IN_ADC();
void OUT_DAC();
void USART_SendChar(int value);

unsigned int BAUDRATE,Over8;
char VC[4]={0,0,0,0};
int AUX[4]={0,0,0,0};
volatile int valor_DAC = 0;
volatile int valor_ADC = 0;
char data;
char cadena[4];
int i = 0;
volatile float VV = 0;


int main(void)
		{
			SysTick_Init();
			RCC_SETUP();
			GPIO_SETUP();
			DAC_SETUP();
			ADC_SETUP();
			USART_SETUP();		
			SysTick_Init();
			
			DAC->DHR12R1 = 0;

		while(1){
			IN_ADC();
			OUT_DAC;
	}
}
extern "C"{
	void USART3_IRQHandler(void){						// Lectura
		while (USART3->ISR & USART_ISR_RXNE){
			data =(USART3->RDR & 0xFF); 				// RXNE ACTIVA RECIBE CHAR
			cadena[i] = data;
			i++;
   }	
	}
}
void RCC_SETUP(){ // funcion configuracion RCC

	RCC->AHB1ENR |= 0xD; // habilitar puertos A, C y D  
	RCC->APB1ENR |= (1<<29)|(1<<18); // habilitar DAC, USART3
	RCC->APB2ENR |= 0x4100; // habilitar ADC1 Y SYS 

}
 
void GPIO_SETUP(){ // funcion configuracion GPIO
	
	GPIOA->MODER |= 0x300; // PA4 DAC
	GPIOC->MODER |= 0x3; //Para PC0 ADC1 IN10
//	GPIOD->MODER |= 0xA0000; // PD8 y PD9 como alternantes 
//	GPIOD->AFR[1] |=0X77; 	
	GPIOC->MODER |= (0xA<<20);
	GPIOC->AFR[1] = 0x7700;
	
}

void ADC_SETUP(){ // funcion configuracion ADC
	
	ADC->CCR |= (0<<16); // PCLK2 div by 2
	ADC1->CR1 |= (1<<24); //10 bit Resolution
	ADC1->CR2 |= (1<<0)|(1<<1)|(0<<11)|(0<<10); //ADC ON, CONT ON, ALIGN RIGHT. 
	ADC1->SMPR1 |= (0<<0); //Nothing
	ADC1->SMPR2 |= (0x7); //ADC1 IN10 with 480 cycles
	ADC1->SQR1 |= (0<<0); //L=0, # of Conversions = 1
	ADC1->SQR2 |= (0<<0); //Nothing
	ADC1->SQR3 |= (10<<0); //ADC1 IN10 as first conversion 	
	
}

void DAC_SETUP(){ // funcion configuracion DAC
	
	DAC->CR|=(0x1); // habilitar DAC

}

void USART_SETUP(){ // funcion configuracion USART

	Over8=0; //
	BAUDRATE= 0x683;//9600
 // hablitar lectura, escritura, interrupcion de la lectura, valor de over8
	USART3->BRR|=0x683;
  USART3->CR1|=(1<<0)|(1<<2)|(1<<3)|(1<<5);
	NVIC_SetPriority(USART3_IRQn,1); // se asigna prioridad  
	NVIC_EnableIRQ(USART3_IRQn); // habilita interrupcion 
	
}

void IN_ADC(){ // funcion entrada ADC

		ADC1->CR2|= (1UL<<30); // inicia conversion 
			while((ADC1->SR & (1<<1))==0){ // mirar si termina conversion
				ADC1->SR=0;
			}
			valor_ADC=(ADC1->DR);// asignar valor y conversion a voltaje correspondiente 

}

void OUT_DAC(){ // funcion salid DAC
	
valor_DAC = abs(valor_ADC * 1.36); // conversion de DAC a voltaje correspondiente
DAC->DHR12R1 = valor_DAC; // enviar valor al DAC
	
}

void USART_SendChar(int value) { //enviar caracter
  while(!(USART3->ISR & USART_ISR_TXE));
	USART3->TDR = char(value);
 }