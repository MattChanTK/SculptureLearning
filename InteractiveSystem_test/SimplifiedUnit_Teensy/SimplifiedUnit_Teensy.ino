
//==== constants ====
const unsigned int numOutgoingByte = 64;
const unsigned int numIncomingByte = 64;
const unsigned int period = 0;

//==== pin assignments ====
const unsigned short indicator_led_pin = 13;
const unsigned short high_power_led_pin = 23;
const unsigned short analog_0_pin = A0;
const unsigned short ambient_light_sensor_pin = A3;
const unsigned short sma_0_pin = 5;
const unsigned short sma_1_pin = 6;
const unsigned short reflex_0_pin = 9;
const unsigned short reflex_1_pin = 10;
const unsigned short ir_0_pin = A2;
const unsigned short ir_1_pin = A1;
const unsigned short acc_scl_pin = A5;
const unsigned short acc_sda_pin = A4;

//==== internal global variables =====
byte outgoingByte[numOutgoingByte];
byte incomingByte[numIncomingByte];
unsigned long msUntilNextSend = millis() + period;
unsigned int packetCount = 0;
volatile boolean ledState = 1;

//====== Output Variables for Behaviours =====


//---- indicator LED blinking -----
// indicator LED on 
volatile boolean indicator_led_on = true; //exposed
volatile boolean indicator_led_on_0 = false;

// indicator LED blink 
IntervalTimer indicator_led_blinkTimer;
volatile int indicator_led_blinkPeriod_0 = -99;
volatile int indicator_led_blinkPeriod = 0; //exposed


//----- Protocell reflex -----
volatile unsigned short high_power_led_level = 5;  //exposed
volatile int high_power_led_reflex_enabled = true;
IntervalTimer high_power_led_cycleTimer;
volatile boolean high_power_led_cycling = false;
const unsigned short high_power_led_level_max = 125;
volatile unsigned int high_power_led_reflex_threshold = 100;


//--- Tentacle reflex ----
volatile boolean tentacle_reflex_enabled = true;
volatile unsigned short sma_0_level = 10; //exposed
volatile unsigned short sma_1_level = 10; //exposed
volatile unsigned short reflex_0_level = 10; //exposed
volatile unsigned short reflex_1_level = 10; //exposed
volatile unsigned int ir_0_threshold = 150;
volatile unsigned int ir_1_threshold = 150;

//====== Input Variables for Behaviours =====

//----- analog 0 ------
volatile unsigned int analog_0_state = 0;

//----- ambient light sensor -----
volatile unsigned int ambient_light_sensor_state = 0;

//----- IR sensors state -----
volatile unsigned int ir_0_state = 0;
volatile unsigned int ir_1_state = 0;


void setup() {

	//==== Teensy =====
	//---- indicator led ----
	pinMode(indicator_led_pin, OUTPUT);
	digitalWrite(indicator_led_pin, ledState);  
	indicator_led_blinkTimer.begin(blinkLED, indicator_led_blinkPeriod_0);

	//---- analog read -----
	pinMode(analog_0_pin, INPUT);
	

	//===== Protocell board =====
	//---- high power led ---
	pinMode(high_power_led_pin, OUTPUT);

	//---- ambient light sensor ----
	pinMode(ambient_light_sensor_pin, INPUT);

	//===== Tentacle board ====
	pinMode(sma_0_pin, OUTPUT);
	pinMode(sma_1_pin, OUTPUT);
	pinMode(reflex_0_pin, OUTPUT);
	pinMode(reflex_1_pin, OUTPUT);
	pinMode(ir_0_pin, INPUT);
	pinMode(ir_1_pin, INPUT);

	//===== clear all existing messages ======
	unsigned long clearing_counter = 0;
	while (receive_msg(incomingByte, outgoingByte)){
	    // this prevents the Teensy from being stuck in infinite loop
	    clearing_counter++;
	    if (clearing_counter>10000){
		break;
            }
	}

}

boolean receive_msg(byte recv_data_buff[], byte send_data_buff[]){

	noInterrupts();
	unsigned short byteCount = RawHID.recv(recv_data_buff, 0);
	interrupts();

	if (byteCount > 0) {
		
		// sample the sensors
		sample_inputs();
		
		// extract the front and end signaures
		byte front_signature = recv_data_buff[0];
		byte back_signature = recv_data_buff[numIncomingByte-1];

		// compose reply message
		compose_reply(send_data_buff, front_signature, back_signature);
		send_msg(send_data_buff);
		return true;
	}
	else{
		return false;
	}
}

void send_msg(byte data_buff[]){

	// Send a message
	noInterrupts();
	RawHID.send(data_buff, 10);
	interrupts();
}

void parse_msg(byte data_buff[]){
        int val = 0;
        
	// byte 2 --- indicator led on or off
	indicator_led_on = data_buff[2];

	// byte 3 and 4 --- indicator led blinking frequency
	val = 0;
	for (int i = 0; i < 2 ; i++)
	  val += data_buff[i+3] << (8*i);
	indicator_led_blinkPeriod = val*1000;

	// byte 5 --- high power LED level
	high_power_led_level = data_buff[5];
        
	// byte 6 and byte 7 --- high power LED reflex threshold
	val = 0;
	for (int i = 0; i < 2 ; i++)
	  val += data_buff[i+6] << (8*i);
	high_power_led_reflex_threshold = val;
	
	// byte 8 --- SMA 0 level
	sma_0_level = data_buff[8];
	
	// byte 9 --- SMA 1 level
	sma_1_level = data_buff[9];
	
	// byte 10 --- Reflex 0 level
	reflex_0_level = data_buff[10];
	
	// byte 11 --- Reflex 1 level
	reflex_1_level = data_buff[11];
	
	

}

void sample_inputs(){
	analog_0_state = analogRead(analog_0_pin);
	ambient_light_sensor_state = analogRead(ambient_light_sensor_pin);
	ir_0_state = analogRead(ir_0_pin);
	ir_1_state = analogRead(ir_1_pin);
}

void compose_reply(byte data_buff[], byte front_signature, byte back_signature){

	// add the signatures to first and last byte
	data_buff[0] = front_signature;
	data_buff[numOutgoingByte-1] = back_signature;

	// byte 1 and 2 --- analog 0
	for (int i = 0; i < 2 ; i++)
	data_buff[i+1] = analog_0_state >> (8*i);

	// byte 3 and 4 --- ambient light sensor
	for (int i = 0; i < 2 ; i++)
	data_buff[i+3] = ambient_light_sensor_state >> (8*i);

}

//============ BEHAVIOUR CODES =========

void blinkLED(void){
	ledState ^= 1;
	digitalWrite(indicator_led_pin, ledState);  
}
void led_blink_behaviour(){
	//..... indicator LED .....
	// if it should be on
	if (indicator_led_on == 1){
		
		// if there is a change in blink period
		if (indicator_led_blinkPeriod != indicator_led_blinkPeriod_0 ||
				indicator_led_on != indicator_led_on_0){
			indicator_led_on_0 = indicator_led_on;
			indicator_led_blinkPeriod_0 = indicator_led_blinkPeriod;
			
			//update the blinker's period
			if (indicator_led_blinkPeriod > 0){
				indicator_led_blinkTimer.begin(blinkLED, indicator_led_blinkPeriod);
			}
			//if the period is 0 just end the blink timer and and turn it on 
			else if (indicator_led_blinkPeriod == 0){
				indicator_led_blinkTimer.end();
				ledState = 1;
				digitalWrite(indicator_led_pin, ledState);
			}
		}
	}
	// if it should be off
	else if (indicator_led_on == 0){ 
		indicator_led_on_0 = indicator_led_on;
		// end the blink timer and turn it off
		indicator_led_blinkTimer.end();
		ledState = 0;
		digitalWrite(indicator_led_pin, ledState);
	}
}

volatile unsigned long phase_time;
void protocell_reflex(unsigned long curr_time){
	if (high_power_led_reflex_enabled){
		
		ambient_light_sensor_state = analogRead(ambient_light_sensor_pin);
		
		if (high_power_led_cycling == false && 
				ambient_light_sensor_state < high_power_led_reflex_threshold){
			high_power_led_cycling = true;
			phase_time = millis();       
		}
		else if (high_power_led_cycling == true){
			if ((curr_time - phase_time) < 1000){
				analogWrite(high_power_led_pin, high_power_led_level);
			}
			else{
				high_power_led_cycling = false;
				analogWrite(high_power_led_pin, 0);
			}
		}
	}
}

void tentacle_reflex(){
	if (tentacle_reflex_enabled){
		ir_0_state = analogRead(ir_0_pin);
		ir_1_state = analogRead(ir_1_pin);
		
		if (ir_0_state > ir_0_threshold){
			analogWrite(sma_0_pin, sma_0_level);
			analogWrite(sma_1_pin, sma_1_level);
		}
                else{
                        analogWrite(sma_0_pin, 0);
			analogWrite(sma_1_pin, 0);
                }
		if (ir_0_state > ir_1_threshold){
			analogWrite(reflex_0_pin, reflex_0_level);
			analogWrite(reflex_1_pin, reflex_1_level);
		}
                else{
                        analogWrite(reflex_0_pin, 0);
			analogWrite(reflex_1_pin, 0);
                }
               
	}
}
void loop() {

	volatile unsigned long curr_time = millis();

	protocell_reflex(curr_time);
	led_blink_behaviour();
	tentacle_reflex();

	// check for new messages
	if (receive_msg(incomingByte, outgoingByte)){
		
		// parse the message and save to parameters
		parse_msg(incomingByte);
	}



}


