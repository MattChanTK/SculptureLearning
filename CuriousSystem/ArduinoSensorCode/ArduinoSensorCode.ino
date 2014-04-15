const int gsr = A0;
const int pulse = A1;

// heart rate parameters
const unsigned int hrTimeSize = 10; //# of pulses
unsigned long hrTime[hrTimeSize]; 
unsigned int hrTimeId = 0;
unsigned int hr = 0;
int pulseHigh = 0;
boolean pulseEdgeUp = false;
boolean startOutput = false;

//gsr sensor parameters
const int initGSRInput = 512;
unsigned long skin = 0;

// current time
unsigned int currTime = 0;

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
  
  //set up GSR sensor input
  ground(gsr);
  pinMode(gsr, INPUT);  
  
  //calibrating GSR Sensor
  Serial.println("Calibrating GSR Sensor...");
  Serial.println("Adjust knob until the input becomes 2.5V.");
  int gsrVal = 0;
  while (abs(gsrVal - initGSRInput) > 10)
  {
    gsrVal = analogRead(gsr);    
  }
  Serial.println("Initial GSR input: " + String(gsrVal));
  
  
  //calibrating Pulse sensor
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
  
 
  Serial.println("Calibration Completed");  
    
  
}

void loop()
{
  currTime = millis();
  

  //timing of the oldest pulse
  unsigned int oldTimeId = hrTimeId+1;
  if (oldTimeId >= hrTimeSize)
    oldTimeId = 0;
 //calculate heart rate in beat per minute
  hr = ((unsigned long)(hrTimeSize-1)*1000*60)/(hrTime[hrTimeId] - hrTime[oldTimeId]);

  //Detecting pulses
  int val = analogRead(pulse);
  if (val > pulseHigh && pulseEdgeUp == false)
  {
    pulseEdgeUp = true;
  }
  else if (val < pulseHigh && pulseEdgeUp == true)
  {
    pulseEdgeUp = false;
    // save pulse time in the buffer
    ++hrTimeId;
    if (hrTimeId >= hrTimeSize)
    {
      hrTimeId = 0;
      startOutput = true;
    }
    hrTime[hrTimeId] = millis();
  }
  
  // Measure GSR level
  skin = analogRead(gsr);
  
  //outputting to Serial bus
  if (startOutput)
    Serial.print(String(currTime) + "," + String(hr) + "," + String(skin) + "\n");
  
}
