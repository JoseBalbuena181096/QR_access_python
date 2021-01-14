
#include <Servo.h>

Servo myservo;

void setup() {
  // initialize serial:
  Serial.begin(9600);
  myservo.attach(3); 
  myservo.write(180); 
}

int motor = 0;

void loop() {
  // print the string when a newline arrives:
 if (Serial.available()>0) 
   {
      char option = Serial.read();
      if (option == '1')
      {
        myservo.write(90);
        delay(3000);
        myservo.write(180);
      }
      if(option == '0')
        myservo.write(180);
   }
}
