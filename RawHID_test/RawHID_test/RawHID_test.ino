
//==== constants ====
const unsigned short numOutgoingByte = 64;
const unsigned short numIncomingByte = 64;
const unsigned int period = 2000;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;

boolean ledState = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  ledState = 0;

}


void loop() {

  unsigned short byteCount = RawHID.recv(incomingByte, 100);

  if (byteCount > 0) {
    // the computer sent a message.  Display the bits
    // of the first byte on pin 0 to 7.  Ignore the
    // other 63 bytes!
    Serial.print(F("Received packet, first byte: "));
    Serial.println((int)incomingByte[0]);

    ledState ^= 1;

  }
  Serial.println(ledState);
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
    packetCount++;
    RawHID.send(outgoingByte, 100);
    Serial.println(packetCount);
    //ledState ^= 1;
    // digitalWrite(13, ledState); 
  }


}


