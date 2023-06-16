#include "button_logic.h"
#include <stdio.h>
#include <time.h>

const int greenled = 3;
const int redled = 4;
const int buttonPin = 2;
int lyd = 1000;

int buttonState = 0;
int status1 = 0;
int status2 = 1;
int temp;
String input;

void setup() {
  // put your setup code here, to run once:
  pinMode(greenled, OUTPUT);
  pinMode(redled, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void loop() {

  digitalWrite(greenled, status1);
  digitalWrite(redled, status2);
  // read data only when you receive data:
  if (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');
    if (input == "changeLights") changeLights();
    if (input == "flickerLights") flickerLights();
  }
  else {
      int b = checkButton();
      if (b == 1) {
        Serial.write("changeLights");
      }
      if (b == 2) {
        Serial.write("flickerLights");
      }
      b = 0;
  }
}

//=================================================
// Change Lights
void changeLights() {
    Serial.write("    Changing Ligths");
    Serial.write("\n");
    temp = status1;
    status1 = status2;
    status2 = temp;
}

// Change Lights
void flickerLights() {
  for(int flicker = 0; flicker < 100; flicker++) {
    changeLights();
    digitalWrite(greenled, status1);
    digitalWrite(redled, status2);
    delay(100);
  }
}
