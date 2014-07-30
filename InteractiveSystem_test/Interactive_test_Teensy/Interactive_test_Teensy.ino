
//==== constants ====
const unsigned int numOutgoingByte = 64;
const unsigned int numIncomingByte = 64;
const unsigned int period = 0;

//==== pin assignments ====
const unsigned short indicator_led_pin = 13;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;
volatile boolean ledState = 1;

//----- indicator LED on -----
volatile boolean indicator_led_on = true;
//----- indicator LED blink ------
IntervalTimer indicator_led_blinkTimer;
volatile int indicator_led_blinkPeriod_0 = 0;
volatile int indicator_led_blinkPeriod = 0;

void setup() {
  pinMode(indicator_led_pin, OUTPUT);
  digitalWrite(indicator_led_pin, ledState);  
  indicator_led_blinkTimer.begin(blinkLED, indicator_led_blinkPeriod_0);
}


void blinkLED(void){
    ledState ^= 1;
    digitalWrite(indicator_led_pin, ledState);  
}

boolean receive_msg(byte data_buff[]){
  
    noInterrupts();
    unsigned short byteCount = RawHID.recv(data_buff, 0);
    interrupts();
  
    if (byteCount > 0) {
      // compose reply message
      send_msg(data_buff);
      return true;
    }
    else{
      return false;
    }
}

void send_msg(byte data_buff[]){
   // Send a message
   noInterrupts();
   RawHID.send(data_buff, 10);
   interrupts();
}

void parse_msg(byte data_buff[]){
  
  // byte 1 --- indicator led on or off
  indicator_led_on = incomingByte[1];
  
  // byte 2 and 3 --- indicator led blinking frequency
  int val = 0;
  for (int i = 0; i < 2 ; i++)
    val += incomingByte[i+2] << (8*i);
  indicator_led_blinkPeriod = val*1000;
  
}


void loop() {
  
  
  // check for new messages
   if (receive_msg(incomingByte)){
   
     // parse the message and save to parameters
     parse_msg(incomingByte);
   
     //----the behaviour codes----
     
     //..... indicator LED .....
     // if it should be on
     if (indicator_led_on == 1){
       // if there is a change in blink period
       if (indicator_led_blinkPeriod != indicator_led_blinkPeriod_0){
         
         indicator_led_blinkPeriod_0 = indicator_led_blinkPeriod;
         
         //update the blinker's period
         if (indicator_led_blinkPeriod > 0){
           indicator_led_blinkTimer.begin(blinkLED, indicator_led_blinkPeriod);
         }
         //if the period is 0 just end the blink timer and and turn it on 
         else if (indicator_led_blinkPeriod == 0){
           indicator_led_blinkTimer.end();
           ledState = 1;
           digitalWrite(indicator_led_pin, ledState);
         }
       }
     }
     // if it should be off
     else{ 
       // end the blink timer and turn it off
       indicator_led_blinkTimer.end();
       ledState = 0;
       indicator_led_blinkPeriod = -1;
       indicator_led_blinkPeriod_0 = -1;
       digitalWrite(indicator_led_pin, ledState);
     }
   }
   

}


