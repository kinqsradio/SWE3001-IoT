#include "Arduino_LED_Matrix.h"

#define relayPin 2
#define redledPin 10
#define motionsensorPin 4 // the pin that the OUTPUT pin of the sensor is connected to

ArduinoLEDMatrix matrix;

const uint32_t hi[] = { // pattern to print "Hi" on Arduino LED Matrix
  0xcdfcdfcc,
  0x4fc4fc4c,
  0xc4cdfcdf,
  66
};

int pinStateCurrent = LOW; // current state of the pin
int pinStatePrevious = LOW; // previous state of the pin

void setup() {
  Serial.begin(9600); // Initialize serial communication
  matrix.begin();
  pinMode(relayPin, OUTPUT); // Set the Relay pin mode
  digitalWrite(relayPin, HIGH); // Assuming high means relay off

  pinMode(redledPin, OUTPUT);
  pinMode(motionsensorPin, INPUT); // Set the motion sensor pin as input
}

void loop() {
  LEDMatrix();

  pinStatePrevious = pinStateCurrent; // Store old state
  pinStateCurrent = digitalRead(motionsensorPin); // Read new state

  if (pinStatePrevious == LOW && pinStateCurrent == HIGH) { // Motion sensor state change: LOW -> HIGH
    digitalWrite(redledPin, HIGH); // Turn on LED, notify locally that motion was detected
    Serial.println("Motion detected!");
  } else if (pinStatePrevious == HIGH && pinStateCurrent == LOW) { // Pin state change: HIGH -> LOW
    digitalWrite(redledPin, LOW); // Turn LED off, motion stopped
    Serial.println("Motion not detected!");
  }
}

void LEDMatrix() {
  matrix.loadFrame(hi); // Load and display the frame
}