#include <ModbusRtu.h>
#define TXEN  2

// data array for modbus network sharing
uint16_t offset_data[2] = {1, 0};

Modbus slave(1,Serial,TXEN); // this is slave @1 and RS-485

void setup() {
  slave.begin(19200); // baud-rate at 19200
  slave.start();
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int rec;
  while(!(rec = slave.poll(offset_data, 2))){
  }
  if(rec>0 && rec <4){
      Serial.println("Erro de comunicação");
      digitalWrite(LED_BUILTIN, HIGH);   
      delay(500);                      
      digitalWrite(LED_BUILTIN, LOW);    
      delay(500);
      digitalWrite(LED_BUILTIN, HIGH);   
      delay(500);                      
      digitalWrite(LED_BUILTIN, LOW);    
      delay(500);
  }
  
}
