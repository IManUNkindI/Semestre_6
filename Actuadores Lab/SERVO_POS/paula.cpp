#include <stm32f7xx.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define FAHB 16000000//HSI
using namespace std;
unsigned long int BAUDRATE,Over8;
char dato[10],tx[30];
char Cad[6];
int i=0,c=0,txi=0;
float ctd=0,RPM=0;
bool Menos=false, Mas=true;
volatile int buzzer_DAC=0;
volatile float x=0;
volatile float Vol=0;
void RCC_config();
void GPIO_config();

void USART_config();
volatile int posn=0;
volatile int posan=0;
volatile int pos[8]={10,20,30,40,50,60,70,80};
volatile int guardar=0;
bool melo=false;

void angulos(int u);
void USART_SendChar(int value);
void USART_SendString(char str[30]);
void SysTick_Init(void);
void SysTick_Wait(uint32_t n);
void SysTick_Wait1ms(uint32_t delay);
int main(void)
{
	SysTick_Init();
	RCC_config();
	GPIO_config();
	
	
	USART_config();		
	SysTick_Init();
	while(1){
}
}

extern "C"{
	void UART5_IRQHandler(void){//lectura
		
		while (UART5->ISR & USART_ISR_RXNE){
			char p=(UART5->RDR & 0xFF);//lee un caracter
			dato[i++]=p;//va guardando cada caracter en un vector
			if(p=='n'){
			dato[i-1] = '\0';//elimina la n
						sscanf(dato, "%f", & ctd);//guardar cantidad en variable ctd
				GPIOD->ODR |=( 1<<3)|( 1<<4)|( 1<<5)|( 1<<6);// check
				
				if(strcmp(dato,"POS1")==0)
				{
					posn=0;
				}
			   else
					 if(strcmp(dato,"POS2")==0)
				{
					posn=10;
				}
				else
					if(strcmp(dato,"POS3")==0)
				{
					posn=20;
				}
				else
					if(strcmp(dato,"POS4")==0)
				{
					posn=30;
				}
				else  
					if(strcmp(dato,"POS5")==0)
				{
					posn=40;
				}
				else
				if(strcmp(dato,"POS6")==0)
				{
					posn=50;
					
				}
				while (melo==false)
				{
					
				
				if(posn>posan)
				{
					guardar=posn-posan;
					posan=posn;
					
					angulos(guardar);
					melo=true;
					
				}
				else if (posn<posan)
				{
					guardar=posan+pos[7];
					if(guardar<360)
					{
						angulos(80);
						
					}
					else if (guardar>360)
					{
						guardar=posan+pos[6];
						 if (guardar<360)
						 {
							 angulos(70);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[5];
							 if (guardar<360)
						 {
							 angulos(60);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[4];
							 if (guardar<360)
						 {
							 angulos(50);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[3];
							 if (guardar<360)
						 {
							 angulos(40);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[2];
							 if (guardar<360)
						 {
							 angulos(30);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[1];
							 if (guardar<360)
						 {
							 angulos(20);
						 }
						 else if (guardar>360)
						 {
							 guardar=posan+pos[0];
							 if (guardar<=360)
						 {
							 angulos(10);
						 }
						 else if (guardar>360)
						 {
							guardar=0;
							angulos(posn);
							 melo=true;
							 posan=posn;
						 }
						 }
						 }
						 }
						 }
						 }
						 }
						 
						
					}
					
					
				}
			}
					i=0;//reinicia el indice del buffer de lectura
				}
				
			}
		if(dato[0]=='-'){
		Menos=true;
		Mas=false;
		}
		else
			{
			Mas=true;
			Menos=false;
			}
					
        }
				
			}

void RCC_config(){
	
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN; //Encender GPIO D
	RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN; //Encender GPIO B
	RCC->APB1ENR |= RCC_APB1ENR_UART5EN;//Encender UART5

}
void GPIO_config(){
	
	GPIOB->MODER|=(1<<6)| (1<<8)|(1<<10)|(1<<12); // COMO SALIDA  D3 , D4, D5, D6
	
	//Para UART 5 Por PB8(RX) y PB9(TX)(SE CONECTAN AL REVES EN BLUETOOTH!!)
	GPIOB->MODER |= 0xA0000; 
	GPIOB->AFR[1] |=0x77;  	
	
}

void USART_config(){
	Over8=0;
	BAUDRATE= 0x683;//9600
	UART5->BRR |= BAUDRATE;
	UART5->CR1 |=(USART_CR1_TE | USART_CR1_RE | USART_CR1_RXNEIE| Over8<<15);
	NVIC_SetPriority(UART5_IRQn,1);
	NVIC_EnableIRQ(UART5_IRQn);
	UART5->CR1|= USART_CR1_UE;
	
}



void USART_SendChar(int value) { //enviar caracter
  while(!(UART5->ISR & USART_ISR_TXE));
	UART5->TDR = value;
 }
void USART_SendString(char str[30]) { //enviar cadena
	strncpy(tx,str,30);
	txi=0;
	 for(;txi<strlen(tx);){
    USART_SendChar(tx[txi++]);
	 }
 }
void SysTick_Init(void){
  SysTick->LOAD = 0x00FFFFFF;
	SysTick->CTRL = 0x00000005;
}

void SysTick_Wait(uint32_t n){
	SysTick->LOAD = n-1;
	SysTick->VAL = 0;
	while((SysTick->CTRL&0x00010000)==0);
}

void SysTick_Wait1ms(uint32_t delay){
	for(uint32_t i=0; i<delay; i++){
 SysTick_Wait(FAHB/1000);
 }
}
void angulos (int u)
{
	GPIOD->ODR |=( 1<<3)|( 1<<4)|( 1<<5)|( 1<<6);// check
							if(u==10)
				{
					
					
					GPIOD->ODR|=(1<<4)|(1<<5)|(1<<6); // check
					SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3);// check
					
					
				}
			   else
					 if(u==20)
				{
					
					GPIOD->ODR|=(1<<4)|(1<<5); // check
					GPIOD->ODR &=(0<<6);// check
					SysTick_Wait1ms(500);
					GPIOD->ODR&=(0<<3);// check
					
					
				}
				else
					if(u==30)
				{
					
					GPIOD->ODR|=(1<<4)|(1<<6);// check
					GPIOD->ODR &=(0<<5);// check
					SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3);// check
					
				}
				else
					if(u==40)
				{
				
					GPIOD->ODR|=(1<<4);// check
					GPIOD->ODR &=(0<<5)|(0<<6); //check
					SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3);//check
				}
				else  
					if(u==50)
				{
				
					GPIOD->ODR|=(1<<5)|(1<<6); // check 
					
					GPIOD->ODR &=(0<<4);// check
						SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3);// check
				}
				else
				if(u==60)
				{
					
					GPIOD->ODR |=(1<<5); //check 
					GPIOD->ODR &=(0<<4)|(0<<6); //check
					SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3); // check
				}
				else if(u==70)
				{
					GPIOD->ODR |=(1<<6);
					GPIOD->ODR &=(0<<4)|(0<<5);
					SysTick_Wait1ms(500);
					GPIOD->ODR &=(0<<3);
				}
				else if(u==80)
				{
					GPIOD->ODR &=(0<<4)|(0<<5)|(0<<6);
					SysTick_Wait1ms(500);
					GPIOD->ODR&=(0<<3);
					
				}
				}
