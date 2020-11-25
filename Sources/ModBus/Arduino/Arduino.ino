int i = 0;
String offset;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if(Serial.available()>0 && i == 0){
    delay(100);
    offset = Serial.readString();
    if (offset == "Aaa") {
      digitalWrite(LED_BUILTIN, HIGH);   
      delay(1000);                      
      digitalWrite(LED_BUILTIN, LOW);    
      delay(1000);

     }
  }

   delay(1000);  
} 
