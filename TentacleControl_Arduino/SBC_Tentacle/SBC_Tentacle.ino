
//Mapping on-board LED
const int led = 13;

//SMA output level [0% ~ 100%] pin mapping
const int sma []= {8, 9, 10, 11, 3, 4, 5, 6, 7, 12};
const int numLevel  = sizeof(sma)/sizeof(int);
boolean smaOn[numLevel];

//SMA duty cycle on each pin
const double v_supp = 6;
const double sma_duty_fast [numLevel] = {2.5/v_supp, 2.9/v_supp, 3.4/v_supp, 3.8/v_supp, 3.9/v_supp, 4.4/v_supp, 4.9/v_supp, 5.2/v_supp, 5.6/v_supp, 6/v_supp};
const double sma_duty_steady [numLevel] = {1.7/v_supp, 1.9/v_supp, 2.3/v_supp, 2.6/v_supp, 2.7/v_supp, 3.0/v_supp, 3.4/v_supp, 3.6/v_supp, 4.0/v_supp, 4.7/v_supp};

//Potentiometer ADC
const int pot = 0;

//Desired percent maximum angle
const int in_ref = 0.5;

//Controller Parameters
double kp = 1;
double kd = 1;
double ki = 0.001;

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


void setup()
{
  for (int i = 0; i<numLevel; ++i)
  {
    ground(sma[i]);
    smaOn[i] = 0;
  }    
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

void loop()
{
  //update current time
  currTime = micros();
  
  boolean startNewCycle = false;
  in_level = 6;
  
  //SMA output
  for (int sma_level = 0; sma_level < numLevel; ++sma_level)
  {
      //if not the specified level, turn off
      if (sma_level != in_level)
      {
        turnOff(sma_level);
      }
      // if it is
      else
      {
        //duty cycle update
        double dutyCycle = sma_duty_steady[sma_level];      
        
        //During the ON part of the cycle
        if (smaOn[sma_level])
        {
          //on time finishes
          if ((currTime - startTime) > (dutyCycle*period))
            turnOff(sma_level);
          
        }
        //During the OFF part of the cycle
        else
        {  
          //if one cycle finishes
          if (startNewCycle || ((currTime - startTime) > period))
          {
            turnOn(sma_level);
            //reset start time
            startTime = micros();
          }
            
          
        }
        
      }
      
  }
  
}


