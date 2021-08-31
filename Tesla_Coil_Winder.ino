#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <SD.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2); //Adress (found with i2c scanner example code), rows, lines

int rotator[] = {2, 3, 4, 5};
int slider[] = {6, 7, 8, 9};
int motor_list[] = {rotator, slider};

int current_step[5] = {false, false, false, false, false};

const int chip_select = 10;

String filename;
File file;
char data;
String turns;
int microstep_flag;
int step_flag;
int turn_flag;
int last_turn_flag;
int current_turn = 1;
int percent;

void get_coil_data()
{
  data = file.read();
  if  (data != 'E')  {
    turns += data;
    get_coil_data();
  }
}

void setup()
{
  lcd.begin(16, 2);
  lcd.init();
  lcd.clear();
  lcd.backlight();
  lcd.setCursor(0, 0);

  for (int i = 0; i < 4; i++)
  {
    pinMode(rotator[i], OUTPUT);
    pinMode(slider[i], OUTPUT);
  }

  Serial.begin(9600);

  lcd.print("Initializing SD card...");
  lcd.setCursor(0, 1);

  if (!SD.begin(10))
  {
    lcd.print("Initialization failed!");
    while (1)
    {
      lcd.scrollDisplayLeft();
      delay(200);
    }
  }

  lcd.print("Done.");
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);

  if (SD.exists("coil.dola")) {
    filename = "coil.dola";
  }

  else if (SD.exists("coil.dol")) {
    filename = "coil.dol";
  }

  else if (SD.exists("coil~1.dola")) {
    filename = "coil~1.dola";
  }
  else if (SD.exists("coil~1.dol")) {
    filename = "coil~1.dol";
  }

  else
  {
    lcd.print("coil.dola doesn't exist.");
    while (1) {
      lcd.scrollDisplayLeft();
      delay(200);
    }
  }

  if (!SD.open(filename, FILE_READ))
  {
    lcd.print("File Error");
  }

  else  {
    file = SD.open(filename, FILE_READ);
  }

  get_coil_data();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Turn: ");
  lcd.print(current_turn);
  lcd.print("/");
  lcd.print(turns);
  lcd.setCursor(0, 1);
  lcd.print("Progress: %0");
}

void motor(int motor[], bool A, bool B, bool C, bool D)
{
  digitalWrite(motor[0], A);
  digitalWrite(motor[1], B);
  digitalWrite(motor[2], C);
  digitalWrite(motor[3], D);
}

void loop()
{
  if (turn_flag != turns.toInt())
  {
    while (turn_flag != turns.toInt())
    {
      last_turn_flag = turn_flag;
      
      for (int i = 0; i < 5; i++)
      {
        if  (file.read() == 48) {
          current_step[i] = 0;
        }
  
        else  {
          current_step[i] = 1;
        }
      }
  
      if (current_step[0] == 0)  {
        microstep_flag++;
        step_flag = microstep_flag / 8;
        turn_flag = step_flag / 512;
      }
  
      motor(motor_list[current_step[0]], current_step[1], current_step[2], current_step[3], current_step[4]);
      delay(1);

      if (turn_flag > last_turn_flag) {
        current_turn++;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Turn: ");
        lcd.print(current_turn);
        lcd.print("/");
        lcd.print(turns);
        lcd.setCursor(0, 1);
        lcd.print("Progress: ");
        lcd.print("%");
        percent = map(current_turn, 0, turns.toInt(), 0, 100);
        lcd.print(percent);
      }
  
      if (turn_flag == turns.toInt()) {
        break;
      }
    }
  }
}
