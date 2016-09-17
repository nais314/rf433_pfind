#include "rfcodes.h"

#define PinRFout 14
//5 //14 nodemcu

int Plen = 120;

void send_sync(){
    digitalWrite(PinRFout, LOW);
    digitalWrite(PinRFout, HIGH);
    delayMicroseconds( Plen * 19 );
    digitalWrite(PinRFout, LOW); 
  
}

void send_array( int arr[], int arrsize ){
   // send with more Plens
   for (int ii = Plen; ii <= Plen + 30; ii+=10 ){
      //send signal with current Plen
      for(unsigned int i = 0; i < arrsize; i++){
          digitalWrite(PinRFout, HIGH);
          delayMicroseconds( ii * (arr[i] ) );
          i++;
          digitalWrite(PinRFout, LOW);
          delayMicroseconds( ii * (arr[i] ) );
          
      };
  }; 
}

//-------------------------------------------------
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PinRFout, OUTPUT);

  // put your main code here, to run repeatedly:
  Serial.println("on");
  send_array( rf_one_one_on, rf_one_one_onsize );

  delay(1000);
  
  Serial.println("off");
  send_array( rf_one_one_off, rf_one_one_offsize ); 
}//************************************************

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("on");
  send_array( rf_two_one_on, rf_two_one_onsize );

  delay(1000);
  
  Serial.println("off");
  send_array( rf_two_one_off, rf_two_one_offsize );  

}
