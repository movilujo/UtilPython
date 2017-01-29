//--------------------------------------------------------------
//-- Zum servos firmware
//--------------------------------------------------------------
//--  bq Huma right to technology
//--  bq Tienes derecho a la tecnologia
//--------------------------------------------------------------
//--  (c) Juan Gonzalez Gomez (Obijuan).  Feb-2015
//--  Based on the work from Victor Diaz
//---------------------------------------------------------------
//-- Description:
//--
//--    Firmware for the bq zum-BT-328 board (Arduino compatible) for moving servos
//--  from the PC or a smartphone.
//--  It is a simple server that process commands received by the serial line
//--  (the zum-bt-328 is connected to the pc/mobile by usb cable or bluetooth)
//--
//---------------------------------------------------------------
//--
//-- Serial commands for moving the servos
//--
//--  The sintax is:  <servo_id><angle><CMD_END>
//--  were:
//--    <servo_id>: servo identificacion:  ASCII characters: a, b, c, d ....
//--    <angle>: Angle in degrees (in ASCII). The range is [-90, 90]
//--    <CMD_END>: End of Frame  (ASCII character CR)
//--               CR is chosen for working correctly with gtkterm in linux
//--               If the arduino terminal is used, select the option "carriage return"
//-- -----------------
//--
//--  Examples:
//--
//--      a0\r  -->  Move the a servo to 0 degrees
//--      b-90\r --> Move the b servo to -90 degrees
//-- -----------------------------------------------------------
//--
//--  Modificaciones
//--
//-- Jose Luis Villarejo (@movilujo). Diciembre 2016 
//--    Adaptación para utilizarlo en un brazo robótico de 3GL. Además de modificar el nº 
//--    de servos a 3, se modifica para que invierta el valor de los angulos a escribir
//--    en el servo[1] ya que se encuentra colocado físicamente de forma inversa al resto.
//--

#include <Servo.h>

//-- CONSTANTS
const int led = 13;
const int NSERVOS = 3;      //-- Number of servos controlled by the server
const char CMD_END = '\r';  //-- Character end of frame
                            //-- CR is chosen for working with gtkterm correctly in Linux
                            //-- If the arduino terminal is used, Select the option "carriage return"

//-- Array of servos
Servo servo[NSERVOS];

void setup() 
{
  
  //-- Configure the led 
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  
  //-- Attach de Servos (Manually)
  servo[0].attach(9);
  servo[1].attach(8);
  servo[2].attach(7);
  //servo[3].attach(6);
  
  //-- Posición inicial
  servo[0].write(150);
  servo[1].write(105);
  servo[2].write(53);
    
  //Setup usb serial connection to computer
  Serial.begin(19200);
  //Serial.begin(9600);
  delay(500);
  
  //-- Debug
  //Serial.println("Server ready");
}

void loop() {
  
  //-- Get and execute the commands
  getCommands();
  
//  delay(5);
}

String inputString = "";        // a string to hold incoming data
boolean stringComplete = false; // whether the string is complete

void getCommands() {
  
  //-- Read the incoming commands
  if (Serial.available()) {
    while (Serial.available()) {
      char inChar = (char)Serial.read();
      inputString += inChar;
      
      //Serial.print(inChar,HEX);  //-- For debugging
      //Serial.println(" ");
      
      if (inChar == CMD_END) {
        stringComplete = true;
        //-- Serial.println(inputString);  //-- For debugging
        break;
      }
      
    }
  }

  //-- Execute the commands
  if (stringComplete) {
    
    //-- Calculate the servo index
    //-- Servo 'a' is 0, b is '1' and son on
    int si = inputString[0] - 'a';
    //Serial.println(si);  //-- For Debugging
    
    //-- Only if the servo index is ok, the servo is moved
    if (si >= 0 && si < NSERVOS) {
      //Serial.println("Correct index!");  //-- For debugging
      
      int val = inputString.substring(1).toInt();
      if (si != 1) {
         servo[si].write(val + 90);
      } else{
         servo[si].write(abs(val - 90));
        }
    }
    
 /*
    //------- Process aditional commands
    //-- Command for testing: chaging the led state
    if(inputString.startsWith("l")){
      int val = inputString.substring(1).toInt();
      if (val == 0) {
        digitalWrite(led, LOW);
      } else {
         digitalWrite(led, HIGH);
      }
    }
 */
 
    //-- Initial state
    inputString = "";
    stringComplete = false;
  }
}

