
//==== constants ====
const unsigned int numOutgoingByte = 64;
const unsigned int numIncomingByte = 64;
const unsigned int period = 0;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;

boolean ledState = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
 
}

String replyMsgHeader = "Teensy heard an echo after  ";
String outgoingMsg = "Hello PC! This is Teensy";

void loop() {
  
    // Send a message

   
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
    /*
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
    */


}


