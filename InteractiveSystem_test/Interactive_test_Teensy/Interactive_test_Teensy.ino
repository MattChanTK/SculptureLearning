
//==== constants ====
const unsigned int numOutgoingByte = 64;
const unsigned int numIncomingByte = 64;
const unsigned int period = 0;


//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;
volatile boolean ledState = 0;

IntervalTimer ledBlinkTimer;
volatile long ledBlinkPeriod_0 = 150000;
volatile long ledBlinkPeriod = 150000;

void setup() {
//Serial.begin(9600);
  pinMode(13, OUTPUT);
  ledBlinkTimer.begin(blinkLED, ledBlinkPeriod_0);
 
}


void blinkLED(void){
    ledState ^= 1;
    digitalWrite(13, ledState);  
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
   RawHID.send(data_buff, 0);
   interrupts();
}

void loop() {
  
   receive_msg(incomingByte);
   long val = 0;
   for (int i = 0; i <4 ; i++)
     val += incomingByte[i] << (8*i);
   ledBlinkPeriod = val;
   
   if (ledBlinkPeriod != ledBlinkPeriod_0){
     
     ledBlinkPeriod_0 = ledBlinkPeriod;
     
     if (ledBlinkPeriod > 0L){
       ledBlinkTimer.begin(blinkLED, ledBlinkPeriod);
     }
     else if (ledBlinkPeriod == 0L){
       ledBlinkTimer.end();
       ledState = 1;
       digitalWrite(13, ledState);
     }
     else{
       ledBlinkTimer.end();
       ledState = 0;
       digitalWrite(13, ledState);
     }
   }

}


