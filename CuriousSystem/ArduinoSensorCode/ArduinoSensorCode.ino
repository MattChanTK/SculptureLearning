const int gsr = a0;
const int pulse = a1;

// heart rate parameters
const int hrWindow = 10;
unsigned int pulseCount = 0;
unsigned long hrTime = 0;
double hr = millis();
int pulseHigh = 0;

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
  
  //calibrating
  Serial.println("Calibrating Pulse Sensor");
  double sum = 0;
  int maxVal = 0;
  int minVal = 1024;
  for (int i = 0; i < 100; ++i)
  {
    int val = analogRead(pulse);
    sum += val;
    maxVal = max(maxVal, val);
    minVal = min(minVal, val);
  }
  pulseHigh = sum/100;
  Serial.println("Avg: " + String(pulseHigh));
  Serial.println("Min: " + String(minVal));
  Serial.println("Max: " + String(maxVal));
    
  
}

void loop()
{
  currTime = millis();
  
  // updating hr every (hrWindow) seconds
  if (currTime - hrTime > hrWindow)
  {
    hr = (double)pulseCount/(double)(currTime - hrTime);
    hrTime = millis();
  }
  
  //if votlage drop below certain threshold
  int val = analogRead(pulse);
  //Serial.println(val);
  
  
  
  
  
    
  
}
