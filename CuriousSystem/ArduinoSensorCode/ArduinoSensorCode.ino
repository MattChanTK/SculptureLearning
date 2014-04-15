const int gsr = A0;
const int pulse = A1;

// heart rate parameters
<<<<<<< HEAD
const unsigned int hrTimeSize = 5; //# of pulses
unsigned long hrTime[hrTimeSize]; 
unsigned int hrTimeId = 0;
unsigned long hr = 0;
const unsigned int hrSmooth = 10; // # of data point to take average
unsigned int oldHr[hrSmooth];
unsigned int oldHrId = 0;
=======
const int hrWindow = 10000;
unsigned int pulseCount = 0;
unsigned long hrTime = 0;
double hr = millis();
>>>>>>> parent of 12948ab... Ardunio new way to o heart rate
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
  for (int i=0; i<hrSmooth; ++i)
   oldHr[i] = 0;
  
<<<<<<< HEAD
  //set up GSR sensor input
  ground(gsr);
  pinMode(gsr, INPUT);  
  
  
  //calibrating GSR Sensor
  Serial.println("Calibrating GSR Sensor...");
  Serial.println("Adjust knob until the input becomes 2.5V.");
  int gsrVal = 0;
  while (abs(gsrVal - initGSRInput) > 50)
  {
    gsrVal = analogRead(gsr);    
  }
  Serial.println("Initial GSR input: " + String(gsrVal));
  
  
  //calibrating Pulse sensor
=======
  //calibrating
>>>>>>> parent of 12948ab... Ardunio new way to o heart rate
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
  
<<<<<<< HEAD

  //timing of the oldest pulse
  unsigned int oldTimeId = hrTimeId+1;
  if (oldTimeId >= hrTimeSize)
    oldTimeId = 0;
 //calculate heart rate in beat per 1/10 minute
  unsigned int tempHr = ((unsigned long)(hrTimeSize-1)*1000*600)/(hrTime[hrTimeId] - hrTime[oldTimeId]);
  if (abs((int)tempHr - (int)oldHr[oldHrId]) < 20 || oldHr[oldHrId] == 0)
  {
    oldHr[oldHrId] = tempHr;
    ++oldHrId;
    if (oldHrId >= hrSmooth)
      oldHrId = 0;
  }
  //average of old Hr to get hr
  unsigned long sumHr = 0;
  for (int i = 0; i<hrSmooth; ++i)
    sumHr += oldHr[i];
  hr = (unsigned long)sumHr/(unsigned long) hrSmooth;
=======
  // updating hr every (hrWindow) seconds
  if (currTime - hrTime > hrWindow)
  {
    Serial.println(pulseCount);
    hr = (double)pulseCount/((double)(currTime - hrTime)*1000);
    hrTime = millis();
    pulseCount = 0; //reset count
  }
>>>>>>> parent of 12948ab... Ardunio new way to o heart rate
  
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
