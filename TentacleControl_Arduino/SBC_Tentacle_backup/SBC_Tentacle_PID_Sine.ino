
//Mapping on-board LED
const int led = 13;

//Voltage control using pwm
const int voltagePin = 3;

//SMA output level [0% ~ 100%] pin mapping
const int sma []= {11, 10, 9, 8, 7, 6, 5, 4, 2, 12};
const int numLevel  = sizeof(sma)/sizeof(int);
//boolean smaOn[numLevel];

//SMA duty cycle on each pin
const double v_supp = 6;
const double sma_duty_fast [numLevel] = {2.5/v_supp, 2.9/v_supp, 3.4/v_supp, 3.8/v_supp, 3.9/v_supp, 4.4/v_supp, 4.9/v_supp, 5.2/v_supp, 5.6/v_supp, 6/v_supp};
const double sma_duty_steady [numLevel] = {1.6/v_supp, 1.9/v_supp, 2.2/v_supp, 2.5/v_supp, 2.7/v_supp, 3.0/v_supp, 3.4/v_supp, 3.6/v_supp, 4.0/v_supp, 4.5/v_supp};

//Potentiometer ADC
const int pot = A5;

//Desired angle ADC
double pot_ref = 390;

//Controller Parameters
double kp = -1.5;
double kd = 0.8;
double ki = -0.005;


//control variables
int in_level = 0;

// Sets pin to output and grounds it
void ground(const byte pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void turnOff(const int sma_id)
{
  digitalWrite(sma[sma_id], LOW);
}
void turnOn(const int sma_id)
{
  digitalWrite(sma[sma_id], HIGH);
}
int readSensor1 (const int pin, const int numSample)
{
  int reading = 0;
  for (int i = 0; i<numSample; ++i)
  {
    reading += analogRead(pin);
  }

  return reading/numSample;
}
int readSensor2 (const int pin, const int numRepeat)
{
  int numEqual = 0;
  int reading_0 = -1;
  int reading = -1;
  boolean transient = true;
  while (transient)
  {
    reading = analogRead(pin);
    if (reading == reading_0)
    {
      numEqual++;
      if (numEqual > numRepeat)
        transient = false;
    }
    else
      numEqual = 0;
      
    reading_0 = reading;
  }
  return reading;
}

void setup()
{
  ground(led);
  ground(voltagePin);
  
  for (int i = 0; i<numLevel; ++i)
    ground(sma[i]);
 
  digitalWrite(led, HIGH);
 
  Serial.begin(9600);
}

int serialIn = pot_ref;
int pot_val = -1;
int in_level_0 = -1;

// variable used for the PID controller
int err = 0;
int err_0 = 0;
int err_change = 0;
int err_sum = 0;
//unsigned long ctrl_start_time = millis();
//const unsigned int ctrl_period = 10;

void loop()
{
 // unsigned long ctrl_curr_time = millis();
  //read some serial
  if (Serial.available() > 0)
  {
    serialIn = Serial.parseInt();
    //discard garbage
    if (serialIn == 0)
      Serial.read();
    else
      Serial.println(serialIn);
  }
  
  //read from potentiometer
  pot_val = readSensor1(pot, 5);
  //Serial.println(pot_val, DEC);
  
  //updating PID variables
  err = round(pot_ref - pot_val);
  err_change = round(err - err_0);
  err_sum += err;
  
  in_level = constrain(round(kp*err + kd*err_change + ki*err_sum), -1, numLevel-1);

  pot_ref = serialIn;
  //pot_ref = 5*sin(millis()*0.0002) + 390;
  
  //in_level = serialIn - 1;
  Serial.print(pot_ref, DEC);
  Serial.print("\t");
  Serial.print(pot_val, DEC);
  Serial.print("\t");
  Serial.print(in_level+1, DEC);
  Serial.print("\t");
  Serial.println(err, DEC);
  
  
  //SMA output  
  if (in_level != in_level_0)
  {
    in_level_0 = in_level;
  
    for (int i = 0; i < numLevel; ++i)
    {    
      if (i != in_level)
      {
          turnOff(i);
      }
    }
    
    if (in_level >-1)
    {
      analogWrite(voltagePin, (int)round(sma_duty_steady[in_level]*255));
      turnOn(in_level);
    }
   
  }

  
}


