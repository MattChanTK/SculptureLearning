
//==== constants ====
const unsigned short numOutgoingByte = 64;
const unsigned short numIncomingByte = 64;
const unsigned int period = 2000;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;
unsigned short byteCount = 0;
boolean ledState = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}


void loop() {

  
  while (Serial.available() && byteCount < numIncomingByte) {
    incomingByte[byteCount] = Serial.read();
    byteCount++;
    if (byteCount == 0)
      ledState ^= 1;
  }
  for (int i=byteCount; i < numIncomingByte; i++){
    incomingByte[byteCount] = lowByte(-1);
  }
   
  digitalWrite(13, ledState); 
   
  // every period, send a packet to the computer
  if (int(msUntilNextSend - millis()) <= 0) {
    msUntilNextSend = millis() + period;
    int time = millis();
      
    outgoingByte[0] = highByte(packetCount);
    outgoingByte[1] = lowByte(packetCount);
    for (int i=2; i<numOutgoingByte;i++){
         outgoingByte[i] = lowByte(i);
         
    }
    Serial.write(outgoingByte, numOutgoingByte);
    ledState ^= 1;
    digitalWrite(13, ledState); 
  }
}
