
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
volatile int ledBlinkPeriod_0 = 150000;
volatile int ledBlinkPeriod = 150000;

void setup() {
//Serial.begin(9600);
  pinMode(13, OUTPUT);
  ledBlinkTimer.begin(blinkLED, ledBlinkPeriod_0);
 
}

void blinkLED(void){
  if (ledBlinkPeriod == ledBlinkPeriod_0){
    ledState ^= 1;
    digitalWrite(13, ledState);
  }
  else{    
    ledBlinkTimer.end();
    ledBlinkPeriod_0 = ledBlinkPeriod;
    if (ledBlinkPeriod > 0){
        ledBlinkTimer.begin(blinkLED, ledBlinkPeriod_0);
    }
    else if (ledBlinkPeriod == 0){
      ledState == 1;
      digitalWrite(13, ledState);
    }
    else{
      ledState = 0;
      digitalWrite(13, ledState);
    }

  }
  
}

void receive_msg(byte data_buff[]){
  
    unsigned short byteCount = RawHID.recv(data_buff, 0);
  
    if (byteCount > 0) {
        ledBlinkPeriod = int(data_buff[1] << 8 + data_buff[0]);
        
    }
    for (int i=0; i<numOutgoingByte;i++){
      if (i < outgoingMsg.length()){
        outgoingByte[i] = data_buff[i];
      }
      else{
        outgoingByte[i] = char(' ');
      }
    }
    send_msg(outgoingByte);
}

void send_msg(byte data_buff[]){
   // Send a message
   RawHID.send(data_buff, 0);
   
}

void loop() {
  
    
   receive_msg(incomingByte);
    // Send a message

   /*
    for (int i=0; i<numOutgoingByte;i++){
        if (i < outgoingMsg.length()){
          outgoingByte[i] = outgoingMsg[i];
        }
        else{
          outgoingByte[i] = char(' ');
        }
    }

    //packetCount++;
    int out_time = micros();
    digitalWrite(13, 0);
    
    for (int i = 0; i<numOutgoingByte; i+=64)
      RawHID.send(outgoingByte, 0);
   
      //Serial.write(outgoingByte, 64);
   
    
    
    // Receiving an echo
    //Serial.flush();
    

    unsigned short byteCount = RawHID.recv(incomingByte, 0);
    ///delay(1000);
    //Serial.println(byteCount);
    if (byteCount > 0) {
      
      digitalWrite(13, 1);
      int in_time = micros();
      
      String replyMsg = replyMsgHeader + String(in_time - out_time) + "us: " ;
      
      for (int i=0; i<numOutgoingByte;i++){
          if (i < replyMsg.length()){
            outgoingByte[i] = replyMsg[i];
          }
          else{
            outgoingByte[i] = incomingByte[i-replyMsg.length()];
          }
      }
    
     
      for (int i = 0; i<numOutgoingByte; i+=64)
        RawHID.send(outgoingByte, 0);
     
    }


  */
}


