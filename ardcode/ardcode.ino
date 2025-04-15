#define button_j 7
#define button_1 4
#define button_2 5
#define button_3 6
#define led_pin LED_BUILTIN

#include <ArduinoJson.h>

int button1_state,button2_state,button3_state,button4_state, x_value, y_value, j_b_value;
 
void setup() {
  Serial.begin(9600);
  pinMode(button_j, INPUT_PULLUP);
  
  pinMode(button_1, INPUT_PULLUP);
  pinMode(button_2, INPUT_PULLUP);

  pinMode(button_3, INPUT_PULLUP);

}

void writeData(int x, int y, int bj, int b1, int b2, int b3){

  JsonDocument doc;

  doc["x"] = x; 
  doc["y"] = y; 
  doc["bj"] = bj; 
  doc["b1"] = b1; 
  doc["b2"] = b2; 
  doc["b3"] = b3; 

  serializeJson(doc, Serial);
  Serial.println();
}


void loop() {
  x_value = analogRead(A0);
  y_value = analogRead(A1);
  j_b_value = digitalRead(button_j);
  button1_state = digitalRead(button_1);
  button2_state = digitalRead(button_2);
  button3_state = digitalRead(button_3);
  
  writeData(x_value, y_value, j_b_value, button1_state, button2_state, button3_state);
  delay(5);
}
