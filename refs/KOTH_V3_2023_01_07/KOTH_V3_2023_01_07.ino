//Posted Date 2023-01-07

/*
Please excuse my lack of programming ediquette, I'm not actually a programmer
but I do what I can.

Currently I have not gone in and cleaned up the code. There may be many instances 
where comments are not quite accurate as I do a lot of copy and pasting. That 
being said it the code does work.
*/

//Old Timer
/*
// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(23, 25, 27, 29, 31, 33);//
*/


//New Timer
//*
#include <LiquidCrystal_I2C.h>

//LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address 0x27 or 0x3f, 16 column and 2 rows
LiquidCrystal_I2C lcd(0x3f, 16, 2); // I2C address 0x27 or 0x3f, 16 column and 2 rows
//SDA on UNO is A4 on MEGA it is 20
//SLC on UNO is A5 on MEGA it is 21
//*/

//Radio Reciever Code
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//Global Attrition
  int redLifeCount;
  int blueLifeCount;
  int startLifeCount;
  int attritionLifeIndex;
  int attritionLifeSound;
  int gameAttritionArray[] = {1, 6, 11, 16};

int gogogo = 0;

RF24 radio(48, 46); // CE, CSN
const byte address[6] = "T0001";

//End Radio Reciever Code

String inputLCDText;
int delayLCD = 2500;

String buttonMode;
String checkReset;
int teamHold;
int holdHillContested;
// Global variable area
//#define rstPin 11 // This was for a reset capability but seemed to cause bugs so I am not using it
int ledPinRed = 4; // Red Buttton LED Pin
int ledPinBlue = 2; // Blue Button LED Pin
int buttonRedpin = 5; // Red Button
int buttonBluepin = 3; // Blue Button
//int buzz=6; //I use to use a buzzer
String teamInControl;

// Define pins for LED Strip

#define REDPIN 45
#define GREENPIN 47
#define BLUEPIN 49

//These are variables for tracking the time
//int m; 
//int k;
//int j;
//int i;


struct gameParameters{
   //These are variables for tracking the time
  String buttonPush;
  String timeX;
  String timeLimit;
  String timePause;
  String timeReset;
  String timeDirection;
  String teamRunDown;
  
};

gameParameters selectOutput;

struct tClock{
   //These are variables for tracking the time
  int m; 
  int k;
  int j;
  int i;
  int mBlue; 
  int kBlue;
  int jBlue;
  int iBlue;
  int mRed; 
  int kRed;
  int jRed;
  int iRed;
  int mPause; 
  int kPause;
  int jPause;
  int iPause;
  int mHold; 
  int kHold;
  int jHold;
  int iHold;
  int mLimit; 
  int kLimit;
  int jLimit;
  int iLimit;
  String loopExit;
  String Victory;
  String teamRunDown;
  
};


// works to this point

// Define Pins - Old code for defining LED bulb
//#define BLUE 11
//#define GREEN 10
//#define RED 9

// define variables - Old code for defining LED bulb colors
//int redValue;
//int greenValue;
//int blueValue;

//used to help code when it is in standby
static int BlueFirst = 0;
static int RedFirst = 0;

//?????
byte leds = 0;

// works to this point


// Code for Millis From https://forum.arduino.cc/t/using-millis-for-timing-a-beginners-guide/483573
// this is used to track actual time kept by the Arduino
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 10000;  //the value is a number of milliseconds

unsigned long startSecondMillis;  //some global variables available anywhere in the program
unsigned long currentSecondMillis;
const unsigned long periodSecond = 1000;  //the value is a number of milliseconds

unsigned long gameStartMillis;
unsigned long gameCheckMillis;
unsigned long gameCheckMillisCheck;
unsigned long gameLengthMillis;
unsigned long gameRestart = 5000;
unsigned long gameClockArray[] = {2, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 31000, 61000
                        };
unsigned long gameClockCheck;
int gameClockIndex = 12;
int gameClockSound = 27;
String gameTimeOver;
String time2Reset;
String playGameStart;
String playGameEnd;

unsigned long xStartMillis;
unsigned long xCheckMillis;
unsigned long xLengthMillis; 

//---------------------------Begin LED Strip Golbal code --------------------------------------------

//Code for 7 segment displays adapted from code written by Limor Fried/Ladyada from Adafruit Industries.
#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_7segment matrix = Adafruit_7segment();

// NeoPixel Starting Code
// NEOPIXEL BEST PRACTICES for most reliable operation:
// - Add 1000 uF CAPACITOR between NeoPixel strip's + and - connections.
// - MINIMIZE WIRING LENGTH between microcontroller board and first pixel.
// - NeoPixel strip's DATA-IN should pass through a 300-500 OHM RESISTOR.
// - AVOID connecting NeoPixels on a LIVE CIRCUIT. If you must, ALWAYS
//   connect GROUND (-) first, then +, then data.
// - When using a 3.3V microcontroller with a 5V-powered NeoPixel strip,
//   a LOGIC-LEVEL CONVERTER on the data line is STRONGLY RECOMMENDED.
// (Skipping these may work OK on your workbench but can fail in the field)

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN    6 //Pin that LED strip is connected to

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 60

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

//-----------------------End of LED Strip global code -----------------------------

// --------------------- Begin Global Code for MP3 player ----------------------

#include <SoftwareSerial.h>
//-------------------------------- Important -------------------------------------
//The order in which you load the sound tracks onto the micro SD card matters

#define ARDUINO_RX 8  //should connect to RX of the Serial MP3 Player module
#define ARDUINO_TX 9  //connect to TX of the module

SoftwareSerial mp3(ARDUINO_TX, ARDUINO_RX);

static int8_t Send_buf[8] = {0}; // Buffer for Send commands.  // BETTER LOCALLY
static uint8_t ansbuf[10] = {0}; // Buffer for the answers.    // BETTER LOCALLY

String mp3Answer;           // Answer from the MP3.

String sanswer(void);
String sbyte2hex(uint8_t b);

/************ Command byte **************************/
#define CMD_NEXT_SONG     0X01  // Play next song.
#define CMD_PREV_SONG     0X02  // Play previous song.
#define CMD_PLAY_W_INDEX  0X03
#define CMD_VOLUME_UP     0X04
#define CMD_VOLUME_DOWN   0X05
#define CMD_SET_VOLUME    0X06

#define CMD_SNG_CYCL_PLAY 0X08  // Single Cycle Play.
#define CMD_SEL_DEV       0X09
#define CMD_SLEEP_MODE    0X0A
#define CMD_WAKE_UP       0X0B
#define CMD_RESET         0X0C
#define CMD_PLAY          0X0D
#define CMD_PAUSE         0X0E
#define CMD_PLAY_FOLDER_FILE 0X0F

#define CMD_STOP_PLAY     0X16  // Stop playing continuously. 
#define CMD_FOLDER_CYCLE  0X17
#define CMD_SHUFFLE_PLAY  0x18 //
#define CMD_SET_SNGL_CYCL 0X19 // Set single cycle.

#define CMD_SET_DAC 0X1A
#define DAC_ON  0X00
#define DAC_OFF 0X01

#define CMD_PLAY_W_VOL    0X22
#define CMD_PLAYING_N     0x4C
#define CMD_QUERY_STATUS      0x42
#define CMD_QUERY_VOLUME      0x43
#define CMD_QUERY_FLDR_TRACKS 0x4e
#define CMD_QUERY_TOT_TRACKS  0x48
#define CMD_QUERY_FLDR_COUNT  0x4f

/************ Opitons **************************/
#define DEV_TF            0X02

/*********************************************************************/
int numero;      
byte estado;      
byte buzzer = 2;
byte pin = 0;
byte SortNumber = 0;

bool button = 0;
// ------------------------ End of MP3 ---------------------------------

//-------------------------------- Important -------------------------------------
//The order in which you load the sound tracks onto the micro SD card matters
// You should drag each sound track individually onto the micro SD card the order should match the numbering
//------------------------- Micro SD tracks ---------------------------
int kingofthehill = 001;
int gameover = 002;

int hillcontested = 3;
int hillcontrolled = 4;
int hilloccupied = 5;
int oneminutetowin = 6;

int blueteamminutetowin = 7;
int blueteam30secondstowin = 8;

int redteamminutetowin = 9;
int redteam30secondstowin = 10;

int redteamhillcontrolled = 11;
int blueteamhillcontrolled = 12;

int redteamwin = 13;
int blueteamwin = 14;

int stargatealarm = 15;

int roundbegins = 28;
int overTimeSound = 29;
//Attrition
int noLivesSound = 30;
int attritionsound = 34;

//----------------------- End of Sound Tracks

int timeCheck_1Up = -9;
int timeCheck_2Up = -5; 
int timeReset_1Up = 0;
int timeReset_2Up = 0;
int directionUp = -1;
int timeCheck_1Down = 0;
int timeCheck_2Down = 0; 
int timeReset_1Down = 9;
int timeReset_2Down = 5;
int directionDown = 1;
int timeCheck_1;
int timeCheck_2; 
int timeReset_1;
int timeReset_2;
int directionInput;

String Skip;
String runDownTeamColor;
String overTime;
String overTimeStart;
String variableX;
String checkX;
String gameSelectedMain;


tClock teamTime;
tClock timeOutput;


void setup() {
  Serial.begin(9600); // Better to use when debugging with the serial monitor
  //Serial.begin(38400); // needed for mp3 player may cause issues in the serial monitor
  mp3.begin(9600);// initiallze MP3
  sendCommand(0x03, 0, kingofthehill);//Send command to play song 6 
  delay(3000);
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);
  pinMode(ledPinRed, OUTPUT); // identify Red LED Pin as output
  pinMode(ledPinBlue, OUTPUT); // identify Blue LED pin as output
  pinMode(buttonRedpin, INPUT_PULLUP);  // Identify Red button as input
  pinMode(buttonBluepin, INPUT_PULLUP); // Identify Blue button as input
  // Radio Reciever
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  
  // set up the LCD's number of columns and rows:
  
  //Old Timer
  //lcd.begin(16, 2);
  
  // New Timer
  lcd.init(); // initialize the lcd
  lcd.backlight();
  
  // Print a message to the LCD.
  displayLCD (0, 0, "Hello There!", "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  delay(delayLCD);
  
// Set each of the 7 segments to dashes
  matrix.begin(0x70);
  matrix.print(10000, DEC);
  matrix.writeDisplay();
  delay(250);
  
  // Set each of the 7 segments to zero
  int time_1 = 0; // Left time display
  int time_2 = 0; // Middle left time display
  int time_3 = 0; // Middle right time display
  int time_4 = 0; // Right time display

    // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  strip.begin();           // INITIALIZE NeoPixel LED strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(255); // Set BRIGHTNESS to max
  colorLEDChange( 0, 255,   0);    
  colorWipe(strip.Color(  0, 255,   0), 0); // Green 
  teamInControl = "Green";

  Serial.println("Check 2");

  

//--------Code for selecting game mode------------------
  
playGameStart = "Yes";
playGameEnd = "Yes";
  
  gameSelectedMain = SelectGameMode();
  
  attritionLifeIndex = 3;
  attritionLifeSound = 33;
  
  Serial.print("Final Answer "); // indicate switching digits
  Serial.println(gameSelectedMain);
  gameParameters check = funcGameSelectOutput(gameSelectedMain);

  checkReset = check.timeReset;
  buttonMode = check.buttonPush;
  variableX = check.timeX;
  if(variableX == "X")
  {
    checkX = "No";
  }
  else
  {
    checkX = "Yes";
  }
  
  
  Serial.println("Check Answer "); // indicate switching digits
  Serial.println(check.buttonPush);
if(check.timeDirection == "Down"){
  timeCheck_1 = timeCheck_1Down;
  timeCheck_2 = timeCheck_2Down; 
  timeReset_1 = timeReset_1Down;
  timeReset_2 = timeReset_2Down;
  directionInput = directionDown;
} 
else{
  timeCheck_1 = timeCheck_1Up;
  timeCheck_2 = timeCheck_2Up; 
  timeReset_1 = timeReset_1Up;
  timeReset_2 = timeReset_2Up;
  directionInput = directionUp;
}


//--------END Code for selecting game mode------------------

//-------Code for selecting time -----------------------

  teamTime = funcIntialTimeOutput(check);
  timeOutput = teamTime;
  
  runDownTeamColor = teamTime.teamRunDown;
  Serial.println("runDownTeamColor ");
  Serial.println(runDownTeamColor);
 
  // Display the final time that was selected
        Serial.print("Game Length ");
        Serial.print(timeOutput.mLimit);
        Serial.print(timeOutput.kLimit);
        Serial.print(":");
        Serial.print(timeOutput.jLimit);
        Serial.println(timeOutput.iLimit);
        //displayLCD (0, 0, "Game Length ", "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        //inputLCDText = String(timeOutput.mLimit) + String(timeOutput.kLimit) + ":" + String(timeOutput.jLimit) + String(timeOutput.iLimit);
        //displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        
        
  // Display the final time that was selected
        Serial.print("Blue Team ");
        Serial.print(timeOutput.mBlue);
        Serial.print(timeOutput.kBlue);
        Serial.print(":");
        Serial.print(timeOutput.jBlue);
        Serial.println(timeOutput.iBlue);
        
  // Display the final time that was selected
        Serial.print("Red Team ");
        Serial.print(timeOutput.mRed);
        Serial.print(timeOutput.kRed);
        Serial.print(":");
        Serial.print(timeOutput.jRed);
        Serial.println(timeOutput.iRed);
  /*  
  // Display the final time that was selected
        Serial.print("Hold Delay ");
        Serial.print(timeOutput.mHold);
        Serial.print(timeOutput.kHold);
        Serial.print(":");
        Serial.print(timeOutput.jHold);
        Serial.println(timeOutput.iHold);
  */
  
//--------END code for selecting time -------------------


/*
tClock teamTime;
teamTime.mBlue = 0;
teamTime.kBlue = 0;
teamTime.jBlue = 0;
teamTime.iBlue = 0;

teamTime.mRed = 0;
teamTime.kRed = 0;
teamTime.jRed = 0;
teamTime.iRed = 0;
*/

if (timeOutput.mLimit == 9)
{
  displayLCD (0, 0, "Game Length" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  displayLCD (0, 1, "not set" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  delay(delayLCD);
}
else if ((gameSelectedMain == "Attrition") || (gameSelectedMain == "Death Clicks")){
  
}
else{
  displayLCD (0, 0, "GameLengthLimit", "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  inputLCDText = String(timeOutput.mLimit) + String(timeOutput.kLimit) + ":" + String(timeOutput.jLimit) + String(timeOutput.iLimit);
  displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  delay(delayLCD);
}

gameLengthMillis = timeOutput.mLimit*600L + timeOutput.kLimit*60L + timeOutput.jLimit*10L + timeOutput.iLimit;
gameLengthMillis = gameLengthMillis*1000L;

gameTimeOver = "No";
Serial.println("Gamelength check");
Serial.println(gameLengthMillis);

overTime = "No";
overTimeStart = "Yes";

xLengthMillis = timeOutput.jHold*10L + timeOutput.iHold;
xLengthMillis = xLengthMillis*1000L;
Serial.println("X Time");
Serial.println(xLengthMillis);





}

void loop() {

inputLCDText = "Standby Mode";
displayLCD (0, 0, inputLCDText , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
inputLCDText = "Press R 2 Start";
displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")

colorLEDChange( 0, 255,   0);    
colorWipe(strip.Color(  0, 255,   0), 0); // Green
teamInControl = "Green";
delay(delayLCD);
radio.startListening();

while(2>1){
  
  if (digitalRead(buttonRedpin) == LOW){
    radio.stopListening();
    break; // exit loops
  }

  radio.read(&gogogo, sizeof(gogogo));
  if (gogogo == 1) {
    Serial.println("GameStarted");
    radio.stopListening();
    break; // exit loops
  }
}

colorLEDChange( 255, 0,   0); // Red
colorWipe(strip.Color(  255, 0,   0), 0);
teamInControl = "Red";
delay(1000);
colorLEDChange( 0, 0,   255); // Blue
colorWipe(strip.Color(  0, 0,   255), 0);
teamInControl = "Blue";
delay(1000);
colorLEDChange( 0, 255,   0);    
colorWipe(strip.Color(  0, 255,   0), 0); // Green  
teamInControl = "Green";
delay(1000);

if((gameSelectedMain == "Basic Timer") || (gameSelectedMain == "Attrition") || (gameSelectedMain == "Death Clicks")){
  displayLCD (0, 0, "Initializing" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
 
} else{
  inputLCDText = " Red: " + String(teamTime.mRed) + String(teamTime.kRed) + ":" + String(teamTime.jRed) + String(teamTime.iRed);
  displayLCD (0, 0, inputLCDText , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  inputLCDText = "Blue: " + String(teamTime.mBlue) + String(teamTime.kBlue) + ":" + String(teamTime.jBlue) + String(teamTime.iBlue);
  displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
}

// Something wierd in the code is messing with the times and it was easier to just adjust it here
if (buttonMode == "Continuous")
{
  teamTime.mBlue = timeOutput.mRed;
  teamTime.kBlue = timeOutput.kRed;
  teamTime.jBlue = timeOutput.jRed;
  teamTime.iBlue = timeOutput.iRed;

  teamTime.mRed = timeOutput.mBlue;
  teamTime.kRed = timeOutput.kBlue;
  teamTime.jRed = timeOutput.jBlue;
  teamTime.iRed = timeOutput.iBlue;
  Skip = "No"; 
}

// ----------------- Start Game Loop -----------------------------------
Serial.println("Gamelength check");
Serial.println(gameLengthMillis);

Serial.println("Gamestart check");
Serial.println(gameStartMillis);
if (playGameStart == "Yes"){
  sendCommand(0x03, 0, roundbegins);//Send command to play song 6  
}

delay(7000);
  
gameStartMillis = millis();

if (gameSelectedMain == "Basic Timer")
{
  inputLCDText = "Time Remaining";
  displayLCD (0, 0, inputLCDText , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  overTime = "No";
  currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
  gameCheckMillis = gameLengthMillis - (currentSecondMillis - gameStartMillis);
  displayLCD (0, 1, String(gameCheckMillis/1000L) , "Second"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  gameCheckMillisCheck = gameCheckMillis;
  while(2>1){
    if ((digitalRead(buttonRedpin) == LOW) && (digitalRead(buttonBluepin) == LOW)) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
    {
      break; // exit loops
    } else  if (gameTimeOver == "Yes"){
      break; // exit loops
    }
    gameClock();
    if(gameCheckMillis < (gameCheckMillisCheck-1000L)){
      displayLCD (0, 1, String(gameCheckMillis/1000L) , "Second"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
      gameCheckMillisCheck = gameCheckMillis;
    }
  }
  displayLCD (0, 1, "0" , "Second"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
 
}else if ((gameSelectedMain== "Attrition") || (gameSelectedMain== "Death Clicks")) {
  funcAttrition ();
}

else
{
  if ((buttonMode == "Tap") || (buttonMode == "Pause")){
    while(2>1){
        gameClock();
        if (gameTimeOver == "Yes"){
          break; // exit loops
        }
        if (digitalRead(buttonRedpin) == LOW){  
            funcX(buttonRedpin, "Default");
            if (checkX == "Yes")
            {
              Serial.print("Red");
              Serial.println(" Team Controls the Hill"); //Show which song is playing in serial monitor
              sendCommand(0x03, 0, redteamhillcontrolled);//Send command to play song 6
              //digitalWrite(ledPinRed, HIGH); // turn the red LED on
              colorLEDChange( 255, 0,   0); // Red
              colorWipe(strip.Color(  255, 0,   0), 0);
              teamInControl = "Red";
              if ((runDownTeamColor == "Red") || (buttonMode == "Pause")){
                overTime = "Yes"; 
              }
              delay(250);
              Skip = "Yes"; 
              if(variableX == "X")
              {
                checkX = "No";
              }
              else
              {
                checkX = "Yes";
              }
              break; // exit loops
              
            }
        }
        if ((digitalRead(buttonBluepin) == LOW)){  
            funcX(buttonBluepin, "Default");
            if (checkX == "Yes")
            {
              Serial.print("Blue");
              Serial.println(" Team Controls the Hill"); //Show which song is playing in serial monitor
              sendCommand(0x03, 0, blueteamhillcontrolled);//Send command to play song 6
              //digitalWrite(ledPinBlue, HIGH); // turn the red LED on
              colorLEDChange( 0, 0,   255); // Blue
              colorWipe(strip.Color(  0, 0,   255), 0);
              teamInControl = "Blue";
              if ((runDownTeamColor == "Blue") || (buttonMode == "Pause")){
                overTime = "Yes"; 
              }
              delay(250);
              Skip = "No";
              if(variableX == "X")
              {
                checkX = "No";
              }
              else
              {
                checkX = "Yes";
              }
              break; // exit loops
            }
        }
    }
  }
  
  while(2>1){
  teamHold = 0; 
  gameClock();
  
  theBugger(teamTime.mBlue,teamTime.kBlue,teamTime.jBlue,teamTime.iBlue, "Blue", "Before Loops");
  theBugger(teamTime.mRed,teamTime.kRed,teamTime.jRed,teamTime.iRed, "Red", "Before Loops");
  if(Skip == "No")
  {
  teamTime = funcTimeLoop(teamTime.mBlue,teamTime.kBlue,teamTime.jBlue,teamTime.iBlue,
                      timeCheck_1, timeCheck_2, 
                      timeReset_1, timeReset_2, directionInput, "Red",redteamhillcontrolled,
                      ledPinRed, buttonRedpin, 0, ledPinBlue, teamTime.mRed,teamTime.kRed,teamTime.jRed,teamTime.iRed,buttonBluepin);
  }
  Skip = "No"; 
  
  theBugger(teamTime.mBlue,teamTime.kBlue,teamTime.jBlue,teamTime.iBlue, "Blue", "Between Loops");
  theBugger(teamTime.mRed,teamTime.kRed,teamTime.jRed,teamTime.iRed, "Red", "Between Loops");
  
  if((teamTime.Victory == "Blue") || (gameTimeOver == "Yes")){
      Serial.println("Blue Over");
      break; // exit loops
    }
  gameClock();
   
  teamTime = funcTimeLoop(teamTime.mRed,teamTime.kRed,teamTime.jRed,teamTime.iRed,
                      timeCheck_1, timeCheck_2, 
                      timeReset_1, timeReset_2, directionInput, "Blue",blueteamhillcontrolled,
                      ledPinBlue, buttonBluepin, 0, ledPinRed,teamTime.mBlue,teamTime.kBlue,teamTime.jBlue,teamTime.iBlue,buttonRedpin);
  
  if((teamTime.Victory == "Red") || (gameTimeOver == "Yes")){
      Serial.println("Red Over");
      break; // exit loops
    } 
  /*
  currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
  gameCheckMillis = currentSecondMillis - gameStartMillis;
  if (gameCheckMillis > gameLengthMillis)
    {
      if(overTime == "No")
      {
        
        gameTimeOver = "Yes";
      }
      else if (overTime == "Yes" && overTimeStart == "Yes") 
      {
        overTimeStart = "No";
        Serial.println("Game is in Over Time");
        sendCommand(0x03, 0, overTimeSound);//Send command to play song 6
      }
    }
  */
  gameClock();
  if(gameTimeOver == "Yes")
  {
    break; // exit loops
  }
  }
}
// ----------------- End Game Loop -----------------------------------

// ----------------- Start Show Winner -------------------------------------

gameStartMillis = millis();

if(((teamTime.Victory == "Blue") && ((buttonMode == "Tap") || (buttonMode == "Pause"))) || ((teamTime.Victory == "Red") && (buttonMode == "Continuous")) ){
      Serial.println("Game Over Blue Team Wins"); //Show which song is playing in serial monitor
      sendCommand(0x03, 0, gameover);//Send command to play song 6
      delay(1500); // add a delay to allow time for the button to be released
      sendCommand(0x03, 0, blueteamwin);//Send command to play song 6
      delay(2000); // add a delay to allow time for the button to be released
      sendCommand(0x03, 0, stargatealarm);//Send command to play song 6
      Serial.println("Stargate 1");
    
    while(2>1){
      digitalWrite(ledPinBlue, HIGH); // turn the red LED on
      colorLEDChange( 0, 0,   255); // Blue
      colorWipe(strip.Color(  0, 0,   255), 0);
      delay(250);
      digitalWrite(ledPinBlue, LOW); // turn the blue LED off
      colorLEDChange( 0, 0,   0); // Blank
      colorWipe(strip.Color(  0, 0,   0), 0);
      delay(250);
      
      gameStartMillis = millis();
      while(2>1){
        if ((digitalRead(buttonRedpin) == LOW) && (digitalRead(buttonBluepin) == LOW)) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
        {
          currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
          gameCheckMillis = currentSecondMillis - gameStartMillis;
          if (gameCheckMillis > gameRestart)
          {
            time2Reset = "Yes";
            break; // exit loops
          }
        } 
        else{
          break; // exit loops  
        }
      }
      if(time2Reset == "Yes"){
        time2Reset = "No";
        break; // exit loops 
      }
    }
  }
  
if(((teamTime.Victory == "Red") && ((buttonMode == "Tap") || (buttonMode == "Pause"))) || ((teamTime.Victory == "Blue") && (buttonMode == "Continuous")) ){
      Serial.println("Game Over Red Team Wins"); //Show which song is playing in serial monitor
      sendCommand(0x03, 0, gameover);//Send command to play song 6
      delay(1500); // add a delay to allow time for the button to be released
      sendCommand(0x03, 0, redteamwin);//Send command to play song 6
      delay(2000); // add a delay to allow time for the button to be released
      sendCommand(0x03, 0, stargatealarm);//Send command to play song 6
      Serial.println("Stargate 2");
    
    while(2>1){
      digitalWrite(ledPinRed, HIGH); // turn the red LED on
      colorLEDChange( 255, 0,   0); // Red
      colorWipe(strip.Color(  255, 0,   0), 0);
      delay(250);
      digitalWrite(ledPinRed, LOW); // turn the blue LED off
      colorLEDChange( 0, 0,   0); // Blank
      colorWipe(strip.Color(  0, 0,   0), 0);
      delay(250);
      
      gameStartMillis = millis();
      while(2>1){
        if ((digitalRead(buttonRedpin) == LOW) && (digitalRead(buttonBluepin) == LOW)) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
        {
          currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
          gameCheckMillis = currentSecondMillis - gameStartMillis;
          if (gameCheckMillis > gameRestart)
          {
            time2Reset = "Yes";
            break; // exit loops
          }
        } 
        else{
          break; // exit loops  
        }
      }
      if(time2Reset == "Yes"){
        time2Reset = "No";
        break; // exit loops 
      }
    }
  }
  
 if(gameTimeOver == "Yes") 
 {
      Serial.println("Game Over Check Time"); //Show which song is playing in serial monitor
   sendCommand(0x03, 0, stargatealarm);//Send command to play song 6
   while(2>1){
      colorLEDChange( 0, 255,   0);
      colorWipe(strip.Color(  0, 255,   0), 0);
      
      delay(250);
      if (teamInControl == "Red"){
        colorLEDChange( 255, 0,   0); //
        colorWipe(strip.Color(  255, 0,   0), 0);
        delay(400);
      } else 
      if (teamInControl == "Blue"){
        colorLEDChange( 0, 0,   255); //
        colorWipe(strip.Color(  0, 0,   255), 0);
        delay(400);
      } else{
        colorLEDChange( 0, 0,   0); // Blank
        colorWipe(strip.Color(  0, 0,   0), 0);
        delay(250);
      }
      
      
      gameStartMillis = millis();
      while(2>1){
        if ((digitalRead(buttonRedpin) == LOW) && (digitalRead(buttonBluepin) == LOW)) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
        {
          currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
          gameCheckMillis = currentSecondMillis - gameStartMillis;
          if (gameCheckMillis > gameRestart)
          {
            time2Reset = "Yes";
            break; // exit loops
          }
        } 
        else{
          break; // exit loops  
        }
      }
      if(time2Reset == "Yes"){
        time2Reset = "No";
        break; // exit loops 
      }
   }
 }
 
//--------------------- Reset variables
  teamTime = timeOutput;
 // Set each of the 7 segments to zero
  int time_1 = 0; // Left time display
  int time_2 = 0; // Middle left time display
  int time_3 = 0; // Middle right time display
  int time_4 = 0; // Right time display
  gameClockIndex = 12;
  gameClockSound = 27;
  //Attrition
  redLifeCount = startLifeCount;
  blueLifeCount = startLifeCount;
  attritionLifeIndex = 3;
  attritionLifeSound = 33;

  if(variableX == "X")
  {
    checkX = "No";
  }
  else
  {
    checkX = "Yes";
  }

if(runDownTeamColor == "Red"){
  runDownTeamColor = "Blue";
  teamTime.mBlue = timeOutput.mRed;
  teamTime.kBlue = timeOutput.kRed;
  teamTime.jBlue = timeOutput.jRed;
  teamTime.iBlue = timeOutput.iRed;

  teamTime.mRed = timeOutput.mBlue;
  teamTime.kRed = timeOutput.kBlue;
  teamTime.jRed = timeOutput.jBlue;
  teamTime.iRed = timeOutput.iBlue;
  timeOutput = teamTime;
}
else if(runDownTeamColor == "Blue"){
  runDownTeamColor = "Red";
  teamTime.mBlue = timeOutput.mRed;
  teamTime.kBlue = timeOutput.kRed;
  teamTime.jBlue = timeOutput.jRed;
  teamTime.iBlue = timeOutput.iRed;

  teamTime.mRed = timeOutput.mBlue;
  teamTime.kRed = timeOutput.kBlue;
  teamTime.jRed = timeOutput.jBlue;
  teamTime.iRed = timeOutput.iBlue;
  timeOutput = teamTime;
}
gameTimeOver = "No";
overTime = "No";
overTimeStart = "Yes";
digitalWrite(ledPinBlue, LOW); // turn the blue LED off
digitalWrite(ledPinRed, LOW); // turn the blue LED off

//-------------------- End Main Loop
}


// ----------Functions -----------------

void gameClock(){
currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
  gameCheckMillis = currentSecondMillis - gameStartMillis;
  if (gameCheckMillis > gameLengthMillis)
    {
      if(overTime == "No")
      {
        
        gameTimeOver = "Yes";
      }
      else if (overTime == "Yes" && overTimeStart == "Yes") 
      {
        overTimeStart = "No";
        Serial.println("Game is in Over Time");
        sendCommand(0x03, 0, overTimeSound);//Send command to play song 6
      }
    }
  
currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
gameCheckMillis = gameLengthMillis - (currentSecondMillis - gameStartMillis);

if ((gameCheckMillis < gameClockArray[gameClockIndex]))
  {
    
    if ((gameClockSound == 15) && (overTime == "No")){
      sendCommand(0x03, 0, stargatealarm);//Send command to play song 6
      Serial.println("Stargate 3");
      Serial.println(overTime);
      gameTimeOver = "Yes";
      Serial.println(gameClockSound);
      Serial.println("Game Time Over");
      
    } 
    else if ((gameClockSound > 15) &&(playGameEnd == "Yes")) {
      Serial.println(gameCheckMillis);
      Serial.println(gameClockIndex);
      Serial.println(gameClockSound);
      sendCommand(0x03, 0, gameClockSound);//Send command to play song 6
    }
    
    if (gameClockSound > 15){
      gameClockIndex = gameClockIndex -1;
      gameClockSound = gameClockSound -1;
    }
    
  }
  
}



void theBugger(int m, int k, int j, int i, String teamName, String functionName) {
  //display_freeram();
  
  //theBugger(m, k, j, i, teamColor, "funcTimeLoop");
  Serial.print(functionName);
  Serial.print(" ");
  Serial.print(teamName);
  Serial.print(" ");
  Serial.print(m);
  Serial.print(k);
  Serial.print(":");
  Serial.print(j);
  Serial.println(i);
}

void display_freeram() {
  Serial.print(F("- SRAM left: "));
  Serial.println(freeRam());
}

int freeRam() {
  extern int __heap_start,*__brkval;
  int v;
  return (int)&v - (__brkval == 0  
    ? (int)&__heap_start : (int) __brkval);  
}



void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

void colorLEDChange( int redSetting, int greenSetting, int blueSetting){
  
  analogWrite(REDPIN, redSetting);
  analogWrite(GREENPIN, greenSetting);
  analogWrite(BLUEPIN, blueSetting);
  
}


//--------------- Selecting Game Mode Functions -------------------------------
String SelectGameMode(){

  int BlueHitStart = 1;
  int gameMode = 0;
  String gameArray[] = {"Nothing Selected", "Basic Timer", "Tap Button Count Down", 
                          "Hold Button Continuous Count Up",  "Tap Button Count Up",
                          "Attrition", "Death Clicks", "Tap Button Pause Timer",
                          "Tap Button Count Down", "Tap Button Count Up",
                          "Hold Button X Time Count Down", "Hold Button X Time Count Up", 
                          "Hold Button Continuous Count Down", "Hold Button Continuous Count Up",
                          "Tap Button Pause Timer", "Hold Button X Time Pause Timer",
                          "Tap Button Reset Timer", "Hold Button X Time Reset Timer",
                        };
  String gameArrayLCD[] = {"Nothing", "Basic Timer", "KotH", 
                          "HoldTheHill", "Domination", "Attrition", 
                          "DeathClicks", "RogueOne", "Tap-Down", "Tap-Up",
                          "Hold-X-Down", "Hold-X-Up", 
                          "Hold-Cont-Down", "Hold-Cont-Up",
                          "Tap-Pause", "Hold-X-Pause",
                          "Tap-Reset", "Hold-X-Reset",
                        };
  int gameArraySize = 17;
  Serial.println("Press the Red Button to Proceed.");
  displayLCD (0, 0, "Press the", "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  displayLCD (0, 1, "Red Button." , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  

  while(BlueHitStart < 2){
    
 
    if (digitalRead(buttonRedpin) == LOW) //Cycle through the game modes
    {
        gameMode = gameMode + 1;  //incrementally increase the digit
        if (gameMode == gameArraySize){ gameMode = 1; } // reset back to zero in case the admin accidently passed the game mode
        Serial.print("Would you like to play "); // indicate which digit is changing
        Serial.print(gameArray[gameMode]); 
        Serial.println("?");
        inputLCDText = "Play " + gameArrayLCD[gameMode] + "?";
        displayLCD (0, 0, inputLCDText , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        //inputLCDText = "Blue: " + String(teamTime.mBlue) + String(teamTime.kBlue) + ":" + String(teamTime.jBlue) + String(teamTime.iBlue);
        displayLCD (0, 1, "YES or NO" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        Serial.println("B-YES or R-NO");
        delay(250); // add a delay to allow time for the button to be released
    }
    
    if (digitalRead(buttonBluepin) == LOW) //when red LED is off and red button is pushed
    {
        BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
        Serial.print("You have chosen to play "); // indicate switching digits
        Serial.println(gameArray[gameMode]); // dispay the current digit being edited
        displayLCD (0, 0, "You have chosen" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        displayLCD (0, 1, gameArrayLCD[gameMode] , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        delay(delayLCD); // add a delay to allow time for the button to be released       
    }
  }   
  String gameSelected;
  
  gameSelected = gameArray[gameMode];
  
  return gameSelected;
  
  
}

// -------------ENd Selecting Game Mode Functions ---------------------------------

// ------------- Attrition -----------------------------

void funcAttrition (){
  //Global Attrition
  //int redLifeCount;
  //int blueLifeCount;
  
  if (directionInput == 1)
  { sendCommand(0x03, 0, attritionsound);//Send command to play song 6
  }
  // Setup
  if ((runDownTeamColor == "Red") && (directionInput == 1))
  {
    displayLCD (0, 0, "Red Team Lives" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
    inputLCDText = "Remaining " + String(redLifeCount); 
    displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  } else if ((runDownTeamColor == "Red") && (directionInput == -1))
  {
    displayLCD (0, 0, "Red Team Number" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
    inputLCDText = "of Deaths " + String(redLifeCount); 
    displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  }else if ((runDownTeamColor == "Blue") && (directionInput == 1))
  {
    displayLCD (0, 0, "Blue Team Lives" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
    inputLCDText = "Remaining " + String(blueLifeCount); 
    displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  } else if ((runDownTeamColor == "Blue") && (directionInput == -1))
  {
    displayLCD (0, 0, "Blue Team Number" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
    inputLCDText = "of Deaths " + String(blueLifeCount); 
    displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  }
  if (runDownTeamColor == "Red")
  {
    colorLEDChange( 255, 0,   0); // Red
    colorWipe(strip.Color(  255, 0,   0), 0);
  }
  else {
    colorLEDChange( 0, 0,  255); // Blue
    colorWipe(strip.Color(  0, 0,   255), 0);
  }
  
  // Loop
  while(2>1){
    if ((runDownTeamColor == "Red") && (digitalRead(buttonRedpin) == LOW))
    {
      redLifeCount = funcLifeCount("Red", directionInput, redLifeCount);
      colorLEDChange( 0, 0,   0); // Red
      colorWipe(strip.Color(  0, 0,   0), 0);
      delay(250);
      colorLEDChange( 255, 0,   0); // Red
      colorWipe(strip.Color(  255, 0,   0), 0);
      if ((redLifeCount == 0) && (directionInput == 1)){
        teamInControl = "Red";
        break; // 
      }
    } else if ((runDownTeamColor == "Blue") && (digitalRead(buttonBluepin) == LOW))
    {
      blueLifeCount = funcLifeCount("Blue", directionInput, blueLifeCount);
      colorLEDChange( 0, 0,   0); // Red
      colorWipe(strip.Color(  0, 0,   0), 0);
      delay(250);
      colorLEDChange( 0, 0,   255); // Red
      colorWipe(strip.Color(  0, 0,   255), 0);
      if ((blueLifeCount == 0) && (directionInput == 1)){
        teamInControl = "Blue";
        break; // 
      }
    }
  }
  
  //Need code for end of attrition
  //sendCommand(0x03, 0, noLives);//Send command to play song 6
  
  gameTimeOver = "Yes"; 
  
}

int funcLifeCount(int teamColor, int direction, int lifeCount){
  int lifeCounter;
  lifeCounter = lifeCount - direction;
  if (direction == 1)
  {
    inputLCDText = "Remaining " + String(lifeCounter); 
    displayLCD (0, 1, inputLCDText , "Second"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
    funcAttritionSound(lifeCounter);
    
  } else if (direction == -1)
  {
    inputLCDText = "of Deaths " + String(lifeCounter); 
    displayLCD (0, 1, inputLCDText , "Second"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  }
  
  return lifeCounter;
}

int funcAttritionSound(int lifeCounter){
if ((lifeCounter < gameAttritionArray[attritionLifeIndex]))
  {
    
    if (lifeCounter == 0){
      sendCommand(0x03, 0, noLivesSound);//Send command to play song 6
      delay(1500);
    } 
    else {
      sendCommand(0x03, 0, attritionLifeSound);//Send command to play song 6
    }
    
    
    attritionLifeIndex = attritionLifeIndex -1;
    attritionLifeSound = attritionLifeSound -1;
  
  }
}

// ------------- End Attrition ------------------------

// -------------Game Parameters Functions ---------------------------------------

gameParameters funcGameSelectOutput(String gametype){
  
  if (gametype == "Basic Timer") 
  {
    //If Tap Button Count Down
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Up";
    selectOutput.teamRunDown;
  }
  if (gametype == "Attrition") 
  {
    //If Tap Button reduce life count
    selectOutput.buttonPush = "Pause";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "No";
    selectOutput.timePause = "Yes";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }
  if (gametype == "Death Clicks") 
  {
    //If Tap Button reduce life count
    selectOutput.buttonPush = "Pause";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "No";
    selectOutput.timePause = "Yes";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Up";
    selectOutput.teamRunDown;
  }
  if (gametype == "Tap Button Count Down") 
  {
    //If Tap Button Count Down
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "No";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button X Time Count Down") 
  {
    //If Hold Button X Time Count Down
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "X";
    selectOutput.timeLimit = "No";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button Continuous Count Down") 
  {
    //If Hold Button Continuous Count Down
    selectOutput.buttonPush = "Continuous";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "No";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Tap Button Count Up") 
  {
    //If Tap Button Count Up
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Up";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button X Time Count Up") 
  {
    //If Hold Button X Time Count Up
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "X";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Up";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button Continuous Count Up") 
  {
    //If Hold Button Continuous Count Up
    selectOutput.buttonPush = "Continuous";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Up";
    selectOutput.teamRunDown;
  }

  if (gametype == "Tap Button Pause Timer") 
  {
    //If Tap Button Pause Timer
    selectOutput.buttonPush = "Pause";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "Yes";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button X Time Pause Timer") 
  {
    //If Hold Button X Time Pause Timer
    selectOutput.buttonPush = "Pause";
    selectOutput.timeX = "X";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "Yes";
    selectOutput.timeReset = "No";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Tap Button Reset Timer") 
  {
    //If Tap Button Reset Timer
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "No";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "Yes";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  }

  if (gametype == "Hold Button X Time Reset Timer") 
  {
    //If Hold Button X Time Reset Timer
    selectOutput.buttonPush = "Tap";
    selectOutput.timeX = "X";
    selectOutput.timeLimit = "Yes";
    selectOutput.timePause = "No";
    selectOutput.timeReset = "Yes";
    selectOutput.timeDirection = "Down";
    selectOutput.teamRunDown;
  } 

  return selectOutput;
}


// ------------- End Game Parameters Functions ---------------------------------------

// ------------- Initial Time Output Functions ---------------------------------------

tClock funcIntialTimeOutput(gameParameters check){
  
  tClock initialTimeOutput;
  tClock Blue;
  tClock Red;
  tClock xTime;
  tClock tLimit;
  
  check.teamRunDown = "Default";
  
  
  int BlueHitStart = 1;
  
  if ( check.timePause == "Yes") //Code used to edit the left digit, runs each time the red button gets hit when setting the time
    {
      Serial.println("Select the team that will be trying to run down the clock.");
      Serial.println("Blue for Blue Team or Red for Red");
      if ((gameSelectedMain == "Attrition") || (gameSelectedMain == "Death Clicks")) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      { displayLCD (0, 0, "TeamRespawnColor" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
      } 
      else {
        displayLCD (0, 0, "TeamRunDownClock" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
      }
      displayLCD (0, 1, "Blue or Red" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        
      while(BlueHitStart < 2){
        if (digitalRead(buttonRedpin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
          {
            delay(250); // add a delay to allow time for the button to be released
            BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
            
            check.teamRunDown = "Red";
            Serial.println("You have selected Red Team");
            displayLCD (0, 0, "You selected" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
            displayLCD (0, 1, "Red Team" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
            delay(delayLCD);
          }
          
        if (digitalRead(buttonBluepin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
          {
            delay(250); // add a delay to allow time for the button to be released
            BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
            
            check.teamRunDown = "Blue";
            Serial.println("You have selected Blue Team");
            displayLCD (0, 0, "You selected" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
            displayLCD (0, 1, "Blue Team" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
            delay(delayLCD);
          }
        
      }
      
    }
    
  Serial.print("You selected the ");  
  Serial.print(check.teamRunDown); 
  Serial.println(" to rundown the clock"); 
  //Attrition
  if ((gameSelectedMain== "Attrition") || (gameSelectedMain== "Death Clicks")) 
  { //No need to set time
    redLifeCount = 0;
    blueLifeCount = 0;
    startLifeCount = 0;
    playGameStart = "No";
    
    BlueHitStart = 1;
    
    if (gameSelectedMain == "Attrition") //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
        
        displayLCD (0, 0, "How many lives?" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        displayLCD (0, 1, "R-inc B-acpt " , "None"); 
        while(BlueHitStart < 2){ // The loop exits once the blue button has been hit to accept the countdown amount
      
          if (digitalRead(buttonRedpin) == LOW ) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
          {
            redLifeCount = redLifeCount + 1;
            blueLifeCount = redLifeCount;
            startLifeCount = redLifeCount;
            displayLCD (13, 1, String(redLifeCount) , "None"); 
            delay(250);
          } else if (digitalRead(buttonBluepin) == LOW ) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
          {
            break;
          }
          
        }  
      } 
      
      
    
    
     
  } 
  else{  
  //Attrition break
  
    if ( (check.teamRunDown == "Blue") || (check.teamRunDown == "Default")) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
        if ( check.timeDirection == "Up"){
          Serial.print(check.teamRunDown);
          tClock Blue;
          Blue.m = 0;
          Blue.k = 0;
          Blue.j = 0;
          Blue.i = 0;
          
          initialTimeOutput.mBlue = Blue.m; 
          initialTimeOutput.kBlue = Blue.k;
          initialTimeOutput.jBlue = Blue.j;
          initialTimeOutput.iBlue = Blue.i;
          initialTimeOutput.mRed = Blue.m; 
          initialTimeOutput.kRed = Blue.k;
          initialTimeOutput.jRed = Blue.j;
          initialTimeOutput.iRed = Blue.i;
        }
        else{
          Serial.println("Blue Team Time");
          displayLCD (0, 0, "Enter the" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "Blue Team's Time" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        
          tClock Blue = funcSetTime("Blue");
          
          initialTimeOutput.mBlue = Blue.m; 
          initialTimeOutput.kBlue = Blue.k;
          initialTimeOutput.jBlue = Blue.j;
          initialTimeOutput.iBlue = Blue.i;
          if (check.teamRunDown == "Blue")
          {
            initialTimeOutput.mRed = 9; 
            initialTimeOutput.kRed = 9;
            initialTimeOutput.jRed = 9;
            initialTimeOutput.iRed = 9;
          }
          else
           {
            initialTimeOutput.mRed = Blue.m; 
            initialTimeOutput.kRed = Blue.k;
            initialTimeOutput.jRed = Blue.j;
            initialTimeOutput.iRed = Blue.i;
          }
        }
        // Display the final time that was selected
        /*
        Serial.print("Blue Team Time set to ");
        Serial.print(Blue.m);
        Serial.print(Blue.k);
        Serial.print(":");
        Serial.print(Blue.j);
        Serial.println(Blue.i);
        initialTimeOutput.mBlue = Blue.m; 
        initialTimeOutput.kBlue = Blue.k;
        initialTimeOutput.jBlue = Blue.j;
        initialTimeOutput.iBlue = Blue.i;
        initialTimeOutput.mRed = Blue.m; 
        initialTimeOutput.kRed = Blue.k;
        initialTimeOutput.jRed = Blue.j;
        initialTimeOutput.iRed = Blue.i;
        */
      }
  
  
    
  
    
    
    BlueHitStart = 1;
    
    if ( (check.timePause == "No") && (check.timeDirection == "Down")) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
        Serial.println("Do you wish to set a different amount of time for the Red team?");
        Serial.println("Blue YES or Red NO");
        displayLCD (0, 0, "Is Red time Diff" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        displayLCD (0, 1, "B-Yes or R-No" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
         
      }
      
    //Serial.print("You selected the ");  
    //Serial.print(check.teamRunDown); 
    //Serial.println(" to rundown the clock");
    delay(500);
    
    while(BlueHitStart < 2){ // The loop exits once the blue button has been hit to accept the countdown amount
      
      if ((digitalRead(buttonBluepin) == LOW) || (check.teamRunDown == "Red")) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
          delay(250); // add a delay to allow time for the button to be released
          Serial.println("Red Team Time");
          displayLCD (0, 0, "Enter the" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "Red Team's Time" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          
          tClock Red = funcSetTime("Red");
    
          // Display the final time that was selected
          Serial.print("Red Team Time set to ");
          Serial.print(Red.m);
          Serial.print(Red.k);
          Serial.print(":");
          Serial.print(Red.j);
          Serial.println(Red.i);
          BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
          initialTimeOutput.mRed = Red.m; 
          initialTimeOutput.kRed = Red.k;
          initialTimeOutput.jRed = Red.j;
          initialTimeOutput.iRed = Red.i;
          if (check.teamRunDown == "Red")
          {
            initialTimeOutput.mBlue = 9; 
            initialTimeOutput.kBlue = 9;
            initialTimeOutput.jBlue = 9;
            initialTimeOutput.iBlue = 9;
          }
        
          
      }
      
          
      
      if ((digitalRead(buttonRedpin) == LOW) ) //when red LED is off and red button is pushed
      {
          BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
          Serial.print("Both teams have the Same amount of time."); // indicate switching digits
          displayLCD (0, 0, "Both teams have" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "the same time" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          delay(delayLCD);
               
      }
      
      if ( (check.timeDirection == "Up") ) //when red LED is off and red button is pushed
      {
          BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
          Serial.print("Both teams have the Same amount of time."); // indicate switching digits
          //displayLCD (0, 0, "Start time set" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          //displayLCD (0, 1, "to 00:00" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          //delay(delayLCD);
               
      }
      
      if (check.teamRunDown == "Blue") //when red LED is off and red button is pushed
      {
          BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
          Serial.println("No need to select a time for Red."); // indicate switching digits
          delay(250); // add a delay to allow time for the button to be released       
      }
    }
  
    
    
    
    if ( check.timeX == "X") //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
          Serial.println("Hold Button X Time");
          displayLCD (0, 0, "Enter time for" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "button hold" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          
          tClock xTime = funcSetTime(check.timeX);
    
          // Display the final time that was selected
          Serial.print("X Time set to hold button");
          Serial.print(xTime.m);
          Serial.print(xTime.k);
          Serial.print(":");
          Serial.print(xTime.j);
          Serial.println(xTime.i);
          initialTimeOutput.mHold = xTime.m; 
          initialTimeOutput.kHold = xTime.k;
          initialTimeOutput.jHold = xTime.j;
          initialTimeOutput.iHold = xTime.i;
          
      }
    
    
    
    
      BlueHitStart = 1;
      
      if ( check.timeLimit == "No") //Code used to edit the left digit, runs each time the red button gets hit when setting the time
      {
          Serial.println("Would you like to set a game length limit?");
          Serial.println("Blue Yes or Red No");
          displayLCD (0, 0, "Do you want to" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "limit gamelength" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          
      }   
          while(BlueHitStart < 2){ 
            if ((digitalRead(buttonBluepin) == LOW) || (check.timeLimit == "Yes")) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
            {
              delay(250); // add a delay to allow time for the button to be released 
              Serial.println("Game Time Limit");
              displayLCD (0, 0, "Enter the" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
              displayLCD (0, 1, "Game Time Limit" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
              delay(2000);
              
              tClock tLimit = funcSetTime("Set Game Length");
    
              // Display the final time that was selected
              Serial.print("Game Time Limit set to ");
              Serial.print(tLimit.m);
              Serial.print(tLimit.k);
              Serial.print(":");
              Serial.print(tLimit.j);
              Serial.println(tLimit.i);
              initialTimeOutput.mLimit = tLimit.m; 
              initialTimeOutput.kLimit = tLimit.k;
              initialTimeOutput.jLimit = tLimit.j;
              initialTimeOutput.iLimit = tLimit.i;
              
              //Enter audio countdown questions
              
              delay(delayLCD);
              BlueHitStart = 1;
              
              displayLCD (0, 0, "UseEndCountdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
              displayLCD (0, 1, "Blue-Yes Red-No" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                
              while(BlueHitStart < 2){
                if (digitalRead(buttonRedpin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
                  {
                    delay(250); // add a delay to allow time for the button to be released
                    playGameEnd = "No";
                    BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
                    displayLCD (0, 0, "End Countdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                    displayLCD (0, 1, "Turned Off" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                    delay(delayLCD);
                  }
                  
                if (digitalRead(buttonBluepin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
                  {
                    delay(250); // add a delay to allow time for the button to be released
                    BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
                    
                    displayLCD (0, 0, "End Countdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                    displayLCD (0, 1, "Turned On" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                    delay(delayLCD);
                  }
                
              }
              
              BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
              
            }
              
            if (digitalRead(buttonRedpin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
            {
              BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
              displayLCD (0, 0, "Game Length" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
              displayLCD (0, 1, "not set" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
              initialTimeOutput.mLimit = 9; 
              initialTimeOutput.kLimit = 9;
              initialTimeOutput.jLimit = 9;
              initialTimeOutput.iLimit = 9;
              delay(delayLCD);
              delay(250); // add a delay to allow time for the button to be released 
            }  
          }
          
          delay(delayLCD);
          int BlueHitStart = 1;
          displayLCD (0, 0, "UseStartCountdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
          displayLCD (0, 1, "Blue-Yes Red-No" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
            
          while(BlueHitStart < 2){
            if (digitalRead(buttonRedpin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
              {
                delay(250); // add a delay to allow time for the button to be released
                playGameStart = "No";
                BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
                displayLCD (0, 0, "Start Countdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                displayLCD (0, 1, "Turned Off" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                delay(delayLCD);
              }
              
            if (digitalRead(buttonBluepin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
              {
                delay(250); // add a delay to allow time for the button to be released
                BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
                
                displayLCD (0, 0, "Start Countdown" , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                displayLCD (0, 1, "Turned On" , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
                delay(delayLCD);
              }
            
          }
  }// end Attrition
  initialTimeOutput.teamRunDown = check.teamRunDown;      
  initialTimeOutput.mPause; 
  initialTimeOutput.kPause;
  initialTimeOutput.jPause;
  initialTimeOutput.iPause;
  return initialTimeOutput;  
}
// ------------- End Initial Time Output Functions ---------------------------------------

// ------------- Enter Time Functions ----------------------------------------------------

tClock funcSetTime(String xTimeCheck){
  inputLCDText = xTimeCheck + " Time:";
  displayLCD (0, 0, inputLCDText , "Both"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  inputLCDText = "00:00";
  displayLCD (0, 1, inputLCDText , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
  tClock team;
  if (xTimeCheck == "X")
  {
    team.m = 0;
  }
  else 
  {
    team.m = SelectTime(10,0);
  }
  if (xTimeCheck == "X")
  {
    team.k = 0;
  }
  else 
  {
    team.k = SelectTime(10,1);
  }
  team.j = SelectTime(6,3);
  team.i = SelectTime(10,4);
  return team;
}

int SelectTime(int digitReset, int digit){
  int BlueHitStart = 1;
  int time_1 = 0;
  // This loop allows the admin to set the precise amount of countdown
  while(BlueHitStart < 2){ // The loop exits once the blue button has been hit to accept the countdown amount
    if (digitalRead(buttonRedpin) == LOW) //Code used to edit the left digit, runs each time the red button gets hit when setting the time
    {
        time_1 = time_1 + 1;  //incrementally increase the digit
        if (time_1 == digitReset){ time_1 = 0; } // reset back to zero in case the admin accidently passed the number
        inputLCDText = "00:00";
        displayLCD (digit, 1, String(time_1) , "None"); // displayLCD (int digit, int line, String lcdText, String "None"/"First"/"Second"/"Both")
        delay(250); // add a delay to allow time for the button to be released
    }
    if (digitalRead(buttonBluepin) == LOW) //when red LED is off and red button is pushed
    {
        BlueHitStart = BlueHitStart + 1;  //incrementally increase the variable to track which digit to edit
        delay(250); // add a delay to allow time for the button to be released       
    }
  }
  return time_1;
  delay(delayLCD);
}

// ------------- End Enter Time Functions ----------------------------------------------------

// ------------- Timer Loop Functions --------------------------------------------------------

tClock funcTimeLoop(int time_1, int time_2, int time_3,int time_4, int timeCheck_1, int timeCheck_2, 
                    int timeReset_1, int timeReset_2, int direction, String teamColor,int teamhillcontrolled,
                    int teamPin, int teamButton, int teamReset, int oTeamPin, int em, int ek, int ej, int ei, int oTeamButton)
{
  tClock tInput;
  tInput.loopExit = "No";
  //changeTeamColor(teamColor, teamButton, teamPin, oTeamPin);
    // This is probably very inefficient but these loops are what calculate what to display on the 7 segment digits
  for(int m = time_1; m >= timeCheck_1; m--){ //increments the left digit, m-- is the same as m = m - 1, it essentialy decreases the value of the left digit by 1 each time this loop runs
    for(int k = time_2; k >= timeCheck_1; k--){ //increments the left digit, k-- is the same as k = k - 1, it essentialy decreases the value of the middle left digit by 1 each time this loop runs
      for(int j = time_3; j >= timeCheck_2; j--){ //increments the left digit, j-- is the same as j = j - 1, it essentialy decreases the value of the middle right digit by 1 each time this loop runs
        for(int i = time_4; i >= timeCheck_1; i--) { 
            theBugger(m, k, j, i, teamColor, "funcTimeLoop");
            
            tInput = funcTimeButtonCheck(teamColor, teamhillcontrolled, teamPin, teamButton, teamReset, 
                                          oTeamPin, tInput, direction, m, k, j, i, em, ek, ej, ei,oTeamButton);
            if (tInput.loopExit == "Yes")
                {break; // exit loops
                } 
        } 
        if (tInput.loopExit == "Yes")
            {break; // exit loops
            } 
        time_4 = timeReset_1;  // reset the right digit once it gets to zero
      }
      if (tInput.loopExit == "Yes")
          {break; // exit loops
          } 
      time_3 = timeReset_2; // reset the middle right digit once it gets to zero (note this is 5 because there are only 60 seconds in a minute
    }
    if (tInput.loopExit == "Yes")
       {break; // exit loops
        } 
    time_2 = timeReset_1; // reset the right digit once it gets to zero
  }
  // End of for loop
  return tInput;
}

tClock funcTimeButtonCheck(String teamColor,int teamhillcontrolled, int teamPin, int teamButton, int teamReset, int oTeamPin,tClock tInput, int direction, int m, int k, int j, int i,int em, int ek, int ej, int ei, int oTeamButton )
{
theBugger(m, k, j, i, teamColor, "funcTimeButtonCheck");
if (buttonMode == "Pause")
{
  if (runDownTeamColor == teamColor)
  {
    Serial.println(runDownTeamColor);
    Serial.println(teamColor);
    Serial.println("runDownTeamColor == teamColor");
  }
  else
  {
    Serial.println(runDownTeamColor);
    Serial.println(teamColor);
    Serial.println("runDownTeamColor does not = teamColor");
    Serial.print("gameClockSound = ");
    Serial.println(gameClockSound);
    if (gameClockSound > 15){
      Serial.print("gameClockSoundCheck = ");
      Serial.println(gameClockSound);
      gameClock();
    }
    displayTime (m,k,j,i, direction,teamColor);
  }
}
else
{
  displayTime (m,k,j,i, direction,teamColor);
}

startSecondMillis = millis();  // record the current time (actually the number of milliseconds since the program started). This variable is used to check whether 1 second has passed.
currentSecondMillis = millis();  //record the current "time" (actually the number of milliseconds since the program started). This is really just initializing this variable        
// This loop checks to see whether 1 second has passed, so that it knows when to increment the 7 segment display
for(; currentSecondMillis - startSecondMillis < periodSecond;){ // exit the loop once the difference between the current time and the start of the loop is greater than a second
    if (buttonMode == "Continuous")
    {
      tInput = funcCheckButtonHoldContinuous (teamColor,teamhillcontrolled, teamPin, teamButton, teamReset, oTeamPin,tInput, direction, m, k, j, i, em, ek, ej, ei);
    } 
    else  if (buttonMode == "Tap")
    {
      tInput = funcCheckButtonTap (teamColor,teamhillcontrolled, teamPin, teamButton, teamReset, oTeamPin,tInput, direction, m, k, j, i, em, ek, ej, ei,oTeamButton);
    }
    else  if (buttonMode == "Pause")
    {
      tInput = funcCheckButtonTapPause (teamColor,teamhillcontrolled, teamPin, teamButton, teamReset, oTeamPin,tInput, direction, m, k, j, i, em, ek, ej, ei,oTeamButton);
    }
    //Need to add Button Reset capability
    if (tInput.loopExit == "Yes")
       {break; // exit loops
        }                 
    /*
    currentSecondMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
    
    
      gameCheckMillis = currentSecondMillis - gameStartMillis;
      if (gameCheckMillis > gameLengthMillis)
        {
          if(overTime == "No")
          {
            
            gameTimeOver = "Yes";
            tInput.loopExit = "Yes";
            break; // exit loops
          }
          else if (overTime == "Yes" && overTimeStart == "Yes") 
          {
            overTimeStart = "No";
            Serial.println("Game is in Over Time");
            sendCommand(0x03, 0, overTimeSound);//Send command to play song 6
          }
        }
    */
  gameClock();
  if(gameTimeOver == "Yes")
  {
    tInput.loopExit = "Yes";
    break; // exit loops
  }
  
  }
  return tInput;
}


// -------------- Specific Game Modes ------------------------

tClock funcCheckButtonTap (String teamColor,int teamhillcontrolled, int teamPin, int teamButton, int teamReset, int oTeamPin,tClock tInput, int direction, int m, int k, int j, int i, int em, int ek, int ej, int ei,int oTeamButton)
{
    if ((digitalRead(teamPin) == LOW) && (digitalRead(teamButton) == LOW)) //this code runs when the red LED is off, the red button is pushed and the red button hasn't been pushed twice in a row
        {
          funcX(teamButton, teamColor);
          
          if (checkX == "Yes")
          {
            theBugger(m, k, j, i, teamColor, "funcCheckButtonTap");
            Serial.print(teamColor);
            Serial.println(" Team Controls the Hill"); //Show which song is playing in serial monitor
            sendCommand(0x03, 0, teamhillcontrolled);//Send command to play song 6
            startMillis = millis();  //record what time the button was hit
            digitalWrite(teamPin, HIGH); // turn the red LED on
            digitalWrite(oTeamPin, LOW); // turn the blue LED off
            // Set the color of the NeoPixel LED Strip
            if (teamColor == "Red")
              {
                colorLEDChange( 255, 0,   0); // Red
                colorWipe(strip.Color(  255, 0,   0), 0);
                teamInControl = "Red";
                // save the blue teams 
                
                tInput.mRed = em;
                tInput.kRed = ek;
                tInput.jRed = ej;
                tInput.iRed = ei;
                
                // save the blue teams 
                if(checkReset == "Yes")
                {
                  tInput.mBlue = timeOutput.mBlue;
                  tInput.kBlue = timeOutput.kBlue;
                  tInput.jBlue = timeOutput.jBlue;
                  tInput.iBlue = timeOutput.iBlue;
                } else{
                  tInput.mBlue = m;
                  tInput.kBlue = k;
                  tInput.jBlue = j;
                  tInput.iBlue = i;
                }
              }
            else
              {
                theBugger(m, k, j, i, teamColor, "funcCheckButtonTap");
                colorLEDChange( 0, 0,   255); // blue
                colorWipe(strip.Color(  0, 0,   255), 0);
                teamInControl = "Blue";
                // save the red teams time
                
                tInput.mBlue = em;
                tInput.kBlue = ek;
                tInput.jBlue = ej;
                tInput.iBlue = ei;
                
                // save the red teams 
                if(checkReset == "Yes")
                {
                  tInput.mRed = timeOutput.mRed;
                  tInput.kRed = timeOutput.kRed;
                  tInput.jRed = timeOutput.jRed;
                  tInput.iRed = timeOutput.iRed;
                }
                else{
                  tInput.mRed = m;
                  tInput.kRed = k;
                  tInput.jRed = j;
                  tInput.iRed = i;  
                }
              }
            delay(250); // add a delay to allow time for the button to be released  
            tInput.loopExit = "Yes";
            if(variableX == "X")
            {
              checkX = "No";
            }
            else
            {
              checkX = "Yes";
            }
          }
        }
    if(direction == 1)
    {
      if((m+k+j+i == 0) && (teamColor == "Blue")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Red";
      }
      if((m+k+j+i == 0) && (teamColor == "Red")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Blue";
      }
    }
  return tInput;
}

tClock funcCheckButtonHoldContinuous (String teamColor,int teamhillcontrolled, int teamPin, int teamButton, int teamReset, int oTeamPin,tClock tInput, int direction, int m, int k, int j, int i, int em, int ek, int ej, int ei){

    if (digitalRead(teamButton) == LOW && (teamHold == 0)) //this code runs when the red LED is off, the red button is pushed and the red button hasn't been pushed twice in a row
        {
          theBugger(m, k, j, i, teamColor, "funcCheckButtonHoldContinuous 1");
          sendCommand(0x03, 0, teamhillcontrolled);//Send command to play song 6
          startMillis = millis();  //record what time the button was hit
          digitalWrite(teamPin, HIGH); // turn the red LED on
          digitalWrite(oTeamPin, LOW); // turn the blue LED off
          // Set the color of the NeoPixel LED Strip
          if (teamColor == "Red")
            {
              colorLEDChange( 255, 0,   0); // Red
              colorWipe(strip.Color(  255, 0,   0), 0);
              teamInControl = "Red";
            }
          else
            {
              colorLEDChange( 0, 0,   255); // blue
              colorWipe(strip.Color(  0, 0,   255), 0);
              teamInControl = "Blue";
            }
          delay(250); // add a delay to allow time for the button to be released 
          teamHold  = 1;
          holdHillContested = 1;
          
        }
    if (digitalRead(teamButton) == HIGH)
          {
            theBugger(m, k, j, i, teamColor, "funcCheckButtonHoldContinuous 2");
            teamHold  = 0;
            colorLEDChange( 0, 255,   0);
            colorWipe(strip.Color(  0, 255,   0), 0);
            teamInControl = "Green";
            if (holdHillContested == 1)
            {
              sendCommand(0x03, 0, hillcontested);//Send command to play song 6
              holdHillContested = 0;
            }
            tInput.loopExit = "Yes";
            if (teamColor == "Red")
              {
                // save the blue teams time
                theBugger(m, k, j, i, teamColor, "Befor Save Time 1");
                tInput.mBlue = m;
                tInput.kBlue = k;
                tInput.jBlue = j;
                tInput.iBlue = i;
                tInput.mRed = em;
                tInput.kRed = ek;
                tInput.jRed = ej;
                tInput.iRed = ei;
                theBugger(m, k, j, i, teamColor, "After Save Time 1");
                theBugger(tInput.mBlue, tInput.kBlue, tInput.jBlue, tInput.iBlue, teamColor, "After Save Time 2");
              }
            else
              {
                // save the red teams time            
                theBugger(m, k, j, i, teamColor, "Befor Save Time 1");
                tInput.mRed = m;
                tInput.kRed = k;
                tInput.jRed = j;
                tInput.iRed = i;
                theBugger(m, k, j, i, teamColor, "After Save Time 1");
                theBugger(tInput.mBlue, tInput.kBlue, tInput.jBlue, tInput.iBlue, teamColor, "After Save Time 2");
              }
          }
    if(direction == 1)
    {
      if((m+k+j+i == 0) && (teamColor == "Blue")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Red";
      }
      if((m+k+j+i == 0) && (teamColor == "Red")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Blue";
      }
    }
  return tInput;
}
// -------------- End Continuously Hold -----------------------

//--------------- Start Hold X --------------------------------

void funcX(int teamButton, String teamColor)
{
  
  if (variableX == "X")
  {
    holdHillContested = 1;
    xStartMillis = millis();
    while(2>1){
      currentSecondMillis = millis();
      xCheckMillis = currentSecondMillis - xStartMillis;
        if (digitalRead(teamButton) == LOW)
        {
          if (holdHillContested == 1)
            {
              sendCommand(0x03, 0, hillcontested);//Send command to play song 6
              holdHillContested = 0;
              colorLEDChange( 244, 232,   104); // Gold
              colorWipe(strip.Color(  244, 232,   104), 0);
            }
          
          
          if (xCheckMillis > xLengthMillis)
          {
            checkX = "Yes";
            break; // exit loops
          }
        }
        else
        {
          if (teamColor == "Red")
          {
            sendCommand(0x03, 0, blueteamhillcontrolled);//Send command to play song 6
            colorLEDChange( 0, 0,   255); // blue
            colorWipe(strip.Color(  0, 0,   255), 0);
            teamInControl = "Blue";
          }
          else if (teamColor == "Blue")
          {
            sendCommand(0x03, 0, redteamhillcontrolled);//Send command to play song 6
            colorLEDChange( 255, 0,   0); // red
            colorWipe(strip.Color(  255, 0,   0), 0);
            teamInControl = "Red";
          }
          else
          {
            sendCommand(0x03, 0, hillcontested);//Send command to play song 6
            colorLEDChange( 0, 255,   0);
            colorWipe(strip.Color(  0, 255,   0), 0);
            teamInControl = "Green";
          }
          
          checkX = "No";
          break; // exit loops
        }
        
    }
    
  }
  
}

//--------------- End Hold X ----------------------------------

//--------------- Start Pause Timer ---------------------------------

tClock funcCheckButtonTapPause (String teamColor,int teamhillcontrolled, int teamPin, int teamButton, int teamReset, int oTeamPin,tClock tInput, int direction, int m, int k, int j, int i, int em, int ek, int ej, int ei,int oTeamButton)
{
    if ((digitalRead(teamPin) == LOW) && (digitalRead(teamButton) == LOW)) //this code runs when the red LED is off, the red button is pushed and the red button hasn't been pushed twice in a row
        {
          funcX(teamButton, teamColor);
          
          if (checkX == "Yes")
          {
            theBugger(m, k, j, i, teamColor, "funcCheckButtonTap");
            Serial.print(teamColor);
            Serial.println(" Team Controls the Hill"); //Show which song is playing in serial monitor
            sendCommand(0x03, 0, teamhillcontrolled);//Send command to play song 6
            startMillis = millis();  //record what time the button was hit
            digitalWrite(teamPin, HIGH); // turn the red LED on
            digitalWrite(oTeamPin, LOW); // turn the blue LED off
            // Set the color of the NeoPixel LED Strip
            if (runDownTeamColor == "Red")
            {
              if (teamColor == "Red")
                {
                  colorLEDChange( 255, 0,   0); // Red
                  colorWipe(strip.Color(  255, 0,   0), 0);
                  teamInControl = "Red";
                  // save the blue teams 
                
                  tInput.mRed = em;
                  tInput.kRed = ek;
                  tInput.jRed = ej;
                  tInput.iRed = ei;
                
                  // save the blue teams 
                  tInput.mBlue = 9;
                  tInput.kBlue = 9;
                  tInput.jBlue = 9;
                  tInput.iBlue = 9;
                  overTime = "Yes";
                  
                
                }
              else
                {
                  theBugger(m, k, j, i, teamColor, "funcCheckButtonTap");
                  colorLEDChange( 0, 0,   255); // blue
                  colorWipe(strip.Color(  0, 0,   255), 0);
                  teamInControl = "Blue";
                  // save the red teams time
                
                  tInput.mBlue = em;
                  tInput.kBlue = ek;
                  tInput.jBlue = ej;
                  tInput.iBlue = ei;
                
                  // save the red teams 
                  if(checkReset == "Yes")
                {
                  tInput.mRed = timeOutput.mRed;
                  tInput.kRed = timeOutput.kRed;
                  tInput.jRed = timeOutput.jRed;
                  tInput.iRed = timeOutput.iRed;
                }
                else{
                  tInput.mRed = m;
                  tInput.kRed = k;
                  tInput.jRed = j;
                  tInput.iRed = i;  
                }
                  overTime = "No";
                  
                
                }
            }
            else
            {
              if (teamColor == "Red")
                {
                  colorLEDChange( 255, 0,   0); // Red
                  colorWipe(strip.Color(  255, 0,   0), 0);
                  teamInControl = "Red";
                  // save the blue teams 
                
                  tInput.mRed = em;
                  tInput.kRed = ek;
                  tInput.jRed = ej;
                  tInput.iRed = ei;
                
                  // save the blue teams 
                if(checkReset == "Yes")
                {
                  tInput.mBlue = timeOutput.mBlue;
                  tInput.kBlue = timeOutput.kBlue;
                  tInput.jBlue = timeOutput.jBlue;
                  tInput.iBlue = timeOutput.iBlue;
                } else{
                  tInput.mBlue = m;
                  tInput.kBlue = k;
                  tInput.jBlue = j;
                  tInput.iBlue = i;
                }
                  overTime = "No";
                  
                
                }
              else
                {
                  theBugger(m, k, j, i, teamColor, "funcCheckButtonTap");
                  colorLEDChange( 0, 0,   255); // blue
                  colorWipe(strip.Color(  0, 0,   255), 0);
                  teamInControl = "Blue";
                  // save the red teams time
                
                  tInput.mBlue = em;
                  tInput.kBlue = ek;
                  tInput.jBlue = ej;
                  tInput.iBlue = ei;
                
                  // save the red teams 
                  tInput.mRed = 9;
                  tInput.kRed = 9;
                  tInput.jRed = 9;
                  tInput.iRed = 9;
                  overTime = "Yes";
                  
                
                }
            }
            delay(250); // add a delay to allow time for the button to be released  
            tInput.loopExit = "Yes";
            if(variableX == "X")
            {
              checkX = "No";
            }
            else
            {
              checkX = "Yes";
            }
          }
        }
    if(direction == 1)
    {
      if((m+k+j+i == 0) && (teamColor == "Blue")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Red";
      }
      if((m+k+j+i == 0) && (teamColor == "Red")){
        tInput.loopExit = "Yes";
        tInput.Victory = "Blue";
      }
    }
  return tInput;
}

//--------------- End Pause Timer -----------------------------

// -------------- End Specific Game Modes --------------------

void changeTeamColor(String teamColor, int teamButton, int teamPin, int oTeamPin){
  if (buttonMode == "Continuous") //this code runs when the red LED is off, the red button is pushed and the red button hasn't been pushed twice in a row
        {
          theBugger(9, 9, 9, 9, teamColor, "changeTeamColor");
          digitalWrite(teamPin, HIGH); // turn the red LED on
          digitalWrite(oTeamPin, LOW); // turn the blue LED off
          // Set the color of the NeoPixel LED Strip
          if (teamColor == "Red")
            {
              colorLEDChange( 255, 0,   0); // Red
              colorWipe(strip.Color(  255, 0,   0), 0);
              teamInControl = "Red";
            }
          else
            {
              colorLEDChange( 0, 0,   255); // blue
              colorWipe(strip.Color(  0, 0,   255), 0);
              teamInControl = "Blue";
            }
          
        }
}

int displayTime (int m, int k, int j, int i,int direction, String teamColor)
{
  //Tell the 7 segment display what number to display for each digit
  theBugger(m, k, j, i, teamColor, "displayTime");
  int teamColorLCD;
  if (buttonMode == "Continuous")
  {
    if(teamColor == "Red")
    {
      teamColorLCD = 0;
    }
    if(teamColor == "Blue")
    {
      teamColorLCD = 1;
    }
  }
  if ((buttonMode == "Tap") || (buttonMode == "Pause"))
  {
    if(teamColor == "Red")
    {
      teamColorLCD = 1;
    }
    if(teamColor == "Blue")
    {
      teamColorLCD = 0;
    }
  }
  int Clock_show = (m*1000+k*100+j*10+i)*direction;
  matrix.print(Clock_show, DEC);
  matrix.drawColon(true);
  matrix.writeDisplay();
  Serial.print(m*direction); // Left digit
  Serial.print(k*direction); // Middle left digit
  Serial.print(":"); // turn on the colon
  Serial.print(j*direction); // Middle right digit
  Serial.println(i*direction); // Right digit
  
  lcd.setCursor(6, teamColorLCD);//lcd.setCursor(lcdLine1Start, lcdLineNum)
  lcd.print(String(m*direction) + String(k*direction) + ":" + String(j*direction) + String(i*direction));
}

int displayLCD (int digit, int line, String lcdText, String lineClear)
{
  theBugger(9, 9, 9, 9, "Unknown", "displayLCD");
  if(lineClear == "None")
  {
  }
  else if(lineClear == "First")
  {
    lcd.setCursor(0, 0);//lcd.setCursor(lcdLine1Start, lcdLineNum)
    lcd.print("                ");// clears previous display
  }
  else if(lineClear == "Second")
  {
    lcd.setCursor(0, 1);//lcd.setCursor(lcdLine1Start, lcdLineNum)
    lcd.print("                ");// clears previous display
  }
  else
  {
    lcd.setCursor(0, 0);//lcd.setCursor(lcdLine1Start, lcdLineNum)
    lcd.print("                ");// clears previous display
    lcd.setCursor(0, 1);//lcd.setCursor(lcdLine1Start, lcdLineNum)
    lcd.print("                ");// clears previous display
  }
lcd.setCursor(digit, line);//lcd.setCursor(lcdLine1Start, lcdLineNum)
lcd.print(lcdText);
}

int timeChecker (int holdXCheck, int teamButton)
{
  theBugger(9, 9, 9, 9, "Unknown", "timeChecker");
unsigned long startHoldX = millis();  // record the current time (actually the number of milliseconds since the program started). This variable is used to check whether 1 second has passed.
unsigned long currentHoldX= millis();  //record the current "time" (actually the number of milliseconds since the program started). This is really just initializing this variable        

// This loop checks to see whether 1 second has passed, so that it knows when to increment the 7 segment display
//for(; currentHoldX- startHoldX < holdXCheck*;){ // exit the loop once the difference between the current time and the start of the loop is greater than a second

    if (digitalRead(teamButton) == HIGH)
       {
         //Failed to hold the button long enough
         //break; // exit loops
        } 
    if (currentHoldX- startHoldX > holdXCheck)
       {
         //Success switch controlling team
         //break; // exit loops
        }    
        
    currentHoldX = millis();  //get the current "time" (actually the number of milliseconds since the program started). This is used to check when to increment the 7 segment display.                    
          //------------------------------------------------------------------------------
  //}
}

//-------------- End Timer Loop Functions


// --------------------- MP3 Functions ---------------------------------------------
void sendMP3Command(char c) {
  //theBugger(9, 9, 9, 9, "Unknown", "sendMP3Command");
  switch (c) {
    case '?':
    case 'h':
      Serial.println("HELP  ");
      Serial.println(" p = Play");
      Serial.println(" P = Pause");
      Serial.println(" > = Next");
      Serial.println(" < = Previous");
      Serial.println(" s = Stop Play"); 
      Serial.println(" + = Volume UP");
      Serial.println(" - = Volume DOWN");
      Serial.println(" c = Query current file");
      Serial.println(" q = Query status");
      Serial.println(" v = Query volume");
      Serial.println(" x = Query folder count");
      Serial.println(" t = Query total file count");
      Serial.println(" f = Play folder 1.");
      Serial.println(" S = Sleep");
      Serial.println(" W = Wake up");
      Serial.println(" r = Reset");
      break;

    case 'p':
      Serial.println("Play ");
      sendCommand(CMD_PLAY);
      break;

    case 'P':
      Serial.println("Pause");
      sendCommand(CMD_PAUSE);
      break;

    case '>':
      Serial.println("Next");
      sendCommand(CMD_NEXT_SONG);
      sendCommand(CMD_PLAYING_N); // ask for the number of file is playing
      break;

    case '<':
      Serial.println("Previous");
      sendCommand(CMD_PREV_SONG);
      sendCommand(CMD_PLAYING_N); // ask for the number of file is playing
      break;

    case 's':
      Serial.println("Stop Play");
      sendCommand(CMD_STOP_PLAY);
      break;

    case '+':
      Serial.println("Volume Up");
      sendCommand(CMD_VOLUME_UP);
      break;

    case '-':
      Serial.println("Volume Down");
      sendCommand(CMD_VOLUME_DOWN);
      break;

    case 'c':
      Serial.println("Query current file");
      sendCommand(CMD_PLAYING_N);
      break;

    case 'q':
      Serial.println("Query status");
      sendCommand(CMD_QUERY_STATUS);
      break;

    case 'v':
      Serial.println("Query volume");
      sendCommand(CMD_QUERY_VOLUME);
      break;

    case 'x':
      Serial.println("Query folder count");
      sendCommand(CMD_QUERY_FLDR_COUNT);
      break;

    case 't':
      Serial.println("Query total file count");
      sendCommand(CMD_QUERY_TOT_TRACKS);
      break;

    case 'f':
      Serial.println("Playing folder 1");
      sendCommand(CMD_FOLDER_CYCLE, 1, 0);
      break;

    case 'S':
      Serial.println("Sleep");
      sendCommand(CMD_SLEEP_MODE);
      break;

    case 'W':
      Serial.println("Wake up");
      sendCommand(CMD_WAKE_UP);
      break;

    case 'r':
      Serial.println("Reset");
      sendCommand(CMD_RESET);
      break;
  }
}

/********************************************************************************/
/*Function decodeMP3Answer: Decode MP3 answer.                                  */
/*Parameter:-void                                                               */
/*Return: The                                                  */

String decodeMP3Answer() {
  String decodedMP3Answer = "";
  //theBugger(9, 9, 9, 9, "Unknown", "decodeMP3Answer");
  decodedMP3Answer += sanswer();

  switch (ansbuf[3]) {
    case 0x3A:
      decodedMP3Answer += " -> Memory card inserted.";
      break;

    case 0x3D:
      decodedMP3Answer += " -> Completed play num " + String(ansbuf[6], DEC);
      //sendCommand(CMD_NEXT_SONG);
      //sendCommand(CMD_PLAYING_N); // ask for the number of file is playing
      break;

    case 0x40:
      decodedMP3Answer += " -> Error";
      break;

    case 0x41:
      decodedMP3Answer += " -> Data recived correctly. ";
      break;

    case 0x42:
      decodedMP3Answer += " -> Status playing: " + String(ansbuf[6], DEC);
      break;

    case 0x48:
      decodedMP3Answer += " -> File count: " + String(ansbuf[6], DEC);
      break;

    case 0x4C:
      decodedMP3Answer += " -> Playing: " + String(ansbuf[6], DEC);
      break;

    case 0x4E:
      decodedMP3Answer += " -> Folder file count: " + String(ansbuf[6], DEC);
      break;

    case 0x4F:
      decodedMP3Answer += " -> Folder count: " + String(ansbuf[6], DEC);
      break;
  }

  return decodedMP3Answer;
}

/********************************************************************************/
/*Function: Send command to the MP3                                             */
/*Parameter: byte command                                                       */
/*Parameter: byte dat1 parameter for the command                                */
/*Parameter: byte dat2 parameter for the command                                */

void sendCommand(byte command){
  //theBugger(9, 9, 9, 9, "Unknown", "sendCommand");
  sendCommand(command, 0, 0);
}

void sendCommand(byte command, byte dat1, byte dat2){
  //theBugger(9, 9, 9, 9, "Unknown", "sendCommandAgain");
  delay(20);
  Send_buf[0] = 0x7E;    //
  Send_buf[1] = 0xFF;    //
  Send_buf[2] = 0x06;    // Len
  Send_buf[3] = command; //
  Send_buf[4] = 0x01;    // 0x00 NO, 0x01 feedback
  Send_buf[5] = dat1;    // datah
  Send_buf[6] = dat2;    // datal
  Send_buf[7] = 0xEF;    //
  Serial.print("Sending: ");
  for (uint8_t i = 0; i < 8; i++)
  {
    mp3.write(Send_buf[i]) ;
    Serial.print(sbyte2hex(Send_buf[i]));
  }
  Serial.println();
}



/********************************************************************************/
/*Function: sbyte2hex. Returns a byte data in HEX format.                       */
/*Parameter:- uint8_t b. Byte to convert to HEX.                                */
/*Return: String                                                                */


String sbyte2hex(uint8_t b)
{
  //theBugger(9, 9, 9, 9, "Unknown", "sbyte2hex");
  String shex;

  shex = "0X";

  if (b < 16) shex += "0";
  shex += String(b, HEX);
  shex += " ";
  return shex;
}


/********************************************************************************/
/*Function: shex2int. Returns a int from an HEX string.                         */
/*Parameter: s. char *s to convert to HEX.                                      */
/*Parameter: n. char *s' length.                                                */
/*Return: int                                                                   */

int shex2int(char *s, int n){
  //theBugger(9, 9, 9, 9, "Unknown", "shex2int");
  int r = 0;
  for (int i=0; i<n; i++){
     if(s[i]>='0' && s[i]<='9'){
      r *= 16; 
      r +=s[i]-'0';
     }else if(s[i]>='A' && s[i]<='F'){
      r *= 16;
      r += (s[i] - 'A') + 10;
     }
  }
  return r;
}


/********************************************************************************/
/*Function: sanswer. Returns a String answer from mp3 UART module.          */
/*Parameter:- uint8_t b. void.                                                  */
/*Return: String. If the answer is well formated answer.                        */

String sanswer(void)
{
  //theBugger(9, 9, 9, 9, "Unknown", "sanswer");
  uint8_t i = 0;
  String mp3answer = "";

  // Get only 10 Bytes
  while (mp3.available() && (i < 10))
  {
    uint8_t b = mp3.read();
    ansbuf[i] = b;
    i++;

    mp3answer += sbyte2hex(b);
  }

  // if the answer format is correct.
  if ((ansbuf[0] == 0x7E) && (ansbuf[9] == 0xEF))
  {
    return mp3answer;
  }

  return "???: " + mp3answer;
}

// ------------------- End MP3 Functions ---------------------------------------------

