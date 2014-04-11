const int gsr = A0;
const int pulse = A1;

// heart rate parameters
const int hrWindow = 10000;
unsigned int pulseCount = 0;
unsigned long hrTime = 0;
double hr = millis();
int pulseHigh = 0;
boolean pulseEdgeUp = false;

// current time
unsigned long currTime = 0;

// Sets pin to output and grounds it
void ground(const byte pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void setup()
{
  Serial.begin(9600);  
  
  //set up pulse sensor input
  ground(pulse);
  pinMode(pulse, INPUT);  
  
  //calibrating
  Serial.println("Calibrating Pulse Sensor...");
  unsigned long sum = 0;
  unsigned int maxVal = 0;
  unsigned int minVal = 1024;
  const unsigned int calDuration = 120;
  for (int i = 0; i < calDuration; ++i)
  {
    int val = analogRead(pulse);
    sum += val;
    maxVal = max(maxVal, val);
    minVal = min(minVal, val);
    delay(10);
  }
  unsigned int avgVal = sum/calDuration;
  Serial.println("Avg: " + String(avgVal));
  Serial.println("Min: " + String(minVal));
  Serial.println("Max: " + String(maxVal));
  pulseHigh = (maxVal + avgVal)>>1;
  Serial.println("Pulse Threshold " + String(pulseHigh));
    
  
}

void loop()
{
  currTime = millis();
  
  // updating hr every (hrWindow) seconds
  if (currTime - hrTime > hrWindow)
  {
    Serial.println(pulseCount);
    hr = (double)pulseCount/((double)(currTime - hrTime)*1000);
    hrTime = millis();
    pulseCount = 0; //reset count
  }
  
  //Detecting pulses
  int val = analogRead(pulse);
  if (val > pulseHigh && pulseEdgeUp == false)
  {
    pulseEdgeUp = true;
  }
  else if (val < pulseHigh && pulseEdgeUp == true)
  {
    pulseEdgeUp = false;
    ++pulseCount;
  }
  //Serial.println(hr);
  
  
  
  
  
    
  
}
