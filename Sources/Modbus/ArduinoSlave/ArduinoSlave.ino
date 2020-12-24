#include <ModbusRtu.h>
#define TXEN  2

uint16_t max_offset = 1000;
uint16_t offset_data;
int offset;

Modbus slave(1, Serial, TXEN);
void setup() {
  slave.begin(19200);
  slave.start();
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int rec;
  rec = slave.poll(&offset_data, 1);
  if (rec >= 4)
  {
      offset = (offset_data > 1000) ? (int)offset_data - 65535 : offset_data;
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
  }
  
}
