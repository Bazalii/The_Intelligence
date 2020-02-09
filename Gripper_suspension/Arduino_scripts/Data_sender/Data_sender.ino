#include <Arduino.h>
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

HX711 plus_x_dat;
HX711 minus_x_dat;
HX711 plus_y_dat;
HX711 minus_y_dat;

float plus_x_units;
float minus_x_units;
float plus_y_units;
float minus_y_units;

String data_input;

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
}

void loop(){
plus_x_units = plus_x_dat.get_units(1) * convert_un_to_kg_val;
minus_x_units = minus_x_dat.get_units(1) * convert_un_to_kg_val;
plus_y_units = plus_y_dat.get_units(1) * convert_un_to_kg_val;
minus_y_units = minus_y_dat.get_units(1) * convert_un_to_kg_val;

if (Serial.available()){
    data_input = Serial.readString();
    data_input.replace(" ", "");
    if (data_input == "tare"){
        minus_x_dat.tare();
        minus_y_dat.tare();
        plus_x_dat.tare();
        plus_y_dat.tare();
    }
    else{
    if (data_input.charAt(1) == "T" || data_input.charAt(1) == "C"){
        if (data_input.charAt(2) == "-"){
            if (data_input.charAt(3) == "x" || data_input.charAt(3) == "X"){
                minus_x_dat.tare();
            }
            else{
                minus_y_dat.tare();
                }
            }
        }
        else {
            if (data_input.charAt(3) == "x" || data_input.charAt(3) == "X"){
                plus_x_dat.tare();
            }
            else{
                plus_y_dat.tare();
            }
        }
    }
}

Serial.println("$ +X" + String(plus_x_units) + " -X" + String(minus_x_units)
 + " +Y" + String(plus_y_units) + " -Y" + String(minus_y_units) + ";");

}
