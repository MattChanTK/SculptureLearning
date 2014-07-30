
//==== constants ====
const unsigned int numOutgoingByte = 64;
const unsigned int numIncomingByte = 64;
const unsigned int period = 0;

//==== pin assignments ====
const unsigned short indicator_led_pin = 13;

//==== protocal specification ====
const unsigned short indicator_led_on_byte[] = {1, 1};
const unsigned short indicator_led_period_byte[] = {2, 2};


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

void receive_msg(byte data_buff[]){
  
    noInterrupts();
    unsigned short byteCount = RawHID.recv(data_buff, 0);
    interrupts();
  
    if (byteCount > 0) {
      // compose reply message
      send_msg(data_buff);
    }
}

void send_msg(byte data_buff[]){
   // Send a message
   noInterrupts();
   RawHID.send(data_buff, 50);
   interrupts();
}

void loop() {
  
  
  // check for new messages
   receive_msg(incomingByte);
   
   indicator_led_on = incomingByte[indicator_led_on_byte[0]];
   
   //ledState = indicator_led_on;
   //digitalWrite(indicator_led_pin, ledState);  
   int val = 0;
   for (int i = 0; i <indicator_led_period_byte[1] ; i++)
     val += incomingByte[i+indicator_led_period_byte[0]] << (8*i);
   indicator_led_blinkPeriod = val*1000;
   
   if (indicator_led_on == 1){
     if (indicator_led_blinkPeriod != indicator_led_blinkPeriod_0){
       
       indicator_led_blinkPeriod_0 = indicator_led_blinkPeriod;
       
       if (indicator_led_blinkPeriod > 0){
         indicator_led_blinkTimer.begin(blinkLED, indicator_led_blinkPeriod);
       }
       else if (indicator_led_blinkPeriod == 0){
         indicator_led_blinkTimer.end();
         ledState = 1;
         digitalWrite(indicator_led_pin, ledState);
       }
     }
   }
   else{
     indicator_led_blinkTimer.end();
     ledState = 0;
     indicator_led_blinkPeriod = -1;
     indicator_led_blinkPeriod_0 = -1;
     digitalWrite(indicator_led_pin, ledState);
   }
   

}


