
//==== constants ====
const unsigned short numOutgoingByte = 64;
const unsigned short numIncomingByte = 64;
const unsigned int period = 0;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;

boolean ledState = 0;

void setup() {
//  Serial.begin(9600);
  pinMode(13, OUTPUT);
  ledState = 0;

}

String replyMsgHeader = "Teensy heard an echo after  ";
String outgoingMsg = "Hello PC! This is Teensy";

void loop() {
  
    // Send a message
    int out_time = micros();
    for (int i=0; i<numOutgoingByte;i++){
        if (i < outgoingMsg.length()){
          outgoingByte[i] = outgoingMsg[i];
        }
        else{
          outgoingByte[i] = ' ';
        }
    }
    //packetCount++;
    RawHID.send(outgoingByte, 10);
    
    // Receiving an echo
    unsigned short byteCount = RawHID.recv(incomingByte, 10);
    if (byteCount > 0) {
      
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
    }
    
    else{
      
        String replyMsg = "Didn't hear an echo";
        for (int i=0; i<numOutgoingByte;i++){
          if (i < replyMsg.length()){
              outgoingByte[i] = replyMsg[i];
          }
          else{
              outgoingByte[i] = ' ';
          }
        }
      
    }
    RawHID.send(outgoingByte, 100);
 


}


