#include <Arduino.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "HX711.h"


// Tensor (+X)
#define plus_x_DOT 9
#define plus_x_SCK 10
#define calibration_plus_x -14.1

// Tensor (-X)
#define minus_x_DOT 7
#define minus_x_SCK 8
#define calibration_minus_x -14.1

// Tensor (+Y)
#define plus_y_DOT 5
#define plus_y_SCK 6
#define calibration_plus_y -13.75

// Tensor (-Y)
#define minus_y_DOT 3
#define minus_y_SCK 4
#define calibration_minus_y -13.6

// Start options
#define convert_un_to_kg_val 0.035274

volatile HX711 plus_x_dat;
volatile HX711 minus_x_dat;
volatile HX711 plus_y_dat;
volatile HX711 minus_y_dat;

volatile float plus_x_units;
volatile float minus_x_units;
volatile float plus_y_units;
volatile float minus_y_units;

String data_input;

ISR(TIMER5_COMPA_vect)
{
plus_x_units = plus_x_dat.get_units(1) * convert_un_to_kg_val;
minus_x_units = minus_x_dat.get_units(1) * convert_un_to_kg_val;
plus_y_units = plus_y_dat.get_units(1) * convert_un_to_kg_val;
minus_y_units = minus_y_dat.get_units(1) * convert_un_to_kg_val;

Serial.println("$ +X" + String(plus_x_units) + " -X" + String(minus_x_units)
 + " +Y" + String(plus_y_units) + " -Y" + String(minus_y_units) + ";");
}

void setup(){
Serial.begin(115200);

// + X setup
plus_x_dat.begin(plus_x_DOT, plus_x_SCK);
plus_x_dat.set_scale();
plus_x_dat.tare(3);
plus_x_dat.set_scale(calibration_plus_x);

// - X setup
minus_x_dat.begin(minus_x_DOT, minus_x_SCK);
minus_x_dat.set_scale();
minus_x_dat.tare(3);
minus_x_dat.set_scale(calibration_minus_x);

// + Y setup
plus_y_dat.begin(plus_y_DOT, plus_y_SCK);
plus_y_dat.set_scale();
plus_y_dat.tare(3);
plus_y_dat.set_scale(calibration_plus_y);

// - Y setup
minus_y_dat.begin(minus_y_DOT, minus_y_SCK);
minus_y_dat.set_scale();
minus_y_dat.tare(3);
minus_y_dat.set_scale(calibration_minus_y);
// инициализация Timer5
    cli();  // отключить глобальные прерывания
    TCCR5A = 0;   // установить регистры в 0
    TCCR5B = 0;

    OCR1A = 15624; // установка регистра совпадения

    TCCR5B |= (1 << WGM12);  // включить CTC режим 
    TCCR5B |= (1 << CS12); // Установить биты на коэффициент деления 255

    TIMSK5 |= (1 << OCIE5A);  // включить прерывание по совпадению таймера 
    sei(); // включить глобальные прерывания
}

void loop(){


if (Serial.available()){
    data_input = Serial.readString();
    if (data_input == "tare"){
        minus_x_dat.tare();
        minus_y_dat.tare();
        plus_x_dat.tare();
        plus_y_dat.tare();
    }
  }
}
