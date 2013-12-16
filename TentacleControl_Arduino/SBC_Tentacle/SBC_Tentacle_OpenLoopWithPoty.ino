
//Mapping on-board LED
const int led = 13;

//Voltage control using pwm
const int voltagePin = 3;

//SMA output level [0% ~ 100%] pin mapping
const int sma []= {11, 10, 9, 8, 7, 6, 5, 4, 2, 12};
const int numLevel  = sizeof(sma)/sizeof(int);
boolean smaOn[numLevel];

//SMA duty cycle on each pin
const double v_supp = 6;
const double sma_duty_fast [numLevel] = {2.5/v_supp, 2.9/v_supp, 3.4/v_supp, 3.8/v_supp, 3.9/v_supp, 4.4/v_supp, 4.9/v_supp, 5.2/v_supp, 5.6/v_supp, 6/v_supp};
const double sma_duty_steady [numLevel] = {1.6/v_supp, 1.9/v_supp, 2.2/v_supp, 2.5/v_supp, 2.7/v_supp, 3.0/v_supp, 3.4/v_supp, 3.6/v_supp, 4.0/v_supp, 4.7/v_supp};

//Potentiometer ADC
const int pot = A5;
int min_pot;
int max_pot;

//Desired percent maximum angle
const double in_ref = 0.5;
double pot_ref = 395;

//Controller Parameters
double kp = 0.1;
double kd = 0;//1;
double ki = 0;//0.001;

//Timing variable and parameters
unsigned long currTime = 0;
unsigned long startTime = 0;
unsigned long endTime = 0;
const unsigned int period = 2000; //us

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
  smaOn[sma_id] = 0;
}
void turnOn(const int sma_id)
{
  digitalWrite(sma[sma_id], HIGH);
  smaOn[sma_id] = 1;
}

int readSensor (const int pin, const int numRepeat)
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
  {
    ground(sma[i]);
    smaOn[i] = 0;
  }    
  digitalWrite(led, HIGH);
  /*
  //initialization
  digitalWrite(led, HIGH);
  turnOn(numLevel-1);
  delay(3500);
  max_pot = readSensor(pot, 10);
  digitalWrite(led, LOW);
  turnOff(numLevel-1);
  delay(10000);
  min_pot = readSensor(pot, 20);
  
  //pot_ref = in_ref*(max_pot-min_pot) + min_pot;
  
  */
  Serial.begin(9600);

  //Serial.println(min_pot, DEC);
  //Serial.println(max_pot, DEC);
  //Serial.println(pot_ref, DEC);
}

int serialIn = 0;
int in_level_0 = -1;
/*int err_0 = 0;
int err_sum = 0;
unsigned long ctrl_start_time = millis();
const unsigned int ctrl_period = 10;
*/
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
  }
  
  //read from potentiometer
  int pot_val = analogRead(pot);
  Serial.println(pot_val, DEC);
  
  //updating PID variables
  
//  if ((ctrl_curr_time - ctrl_start_time) > period)
//  {
/*    int error = round(pot_ref - pot_val);
    int err_change = round(error - err_0);
    err_sum += error;
  
    in_level = constrain(round(kp*error + kd*err_change + ki*err_sum), 0, numLevel - 1);*/
//    ctrl_start_time = millis()
//  }
  
//  boolean startNewCycle = false;
  //pot_ref = serialIn;
  in_level = serialIn - 1;
//  Serial.println(error, DEC);
  
  
  
  //Serial.println(pot_val, DEC);
  
  
  //update current time
//  currTime = micros();

  
  //SMA output
  if (in_level != in_level_0)
  {
    in_level_0 = in_level;
    
    analogWrite(voltagePin, (int)round(sma_duty_steady[in_level]*255));
  
    for (int i = 0; i < numLevel; ++i)
    {    
      if (i != in_level)
      {
          turnOff(i);
      }
    }
    turnOn(in_level);
   
  }

  
}


