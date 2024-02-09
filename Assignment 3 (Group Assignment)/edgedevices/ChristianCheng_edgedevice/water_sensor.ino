const int waterLevelPin = A0; // Sensor connected to analog pin A0

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop() {
  int sensorValue = analogRead(waterLevelPin); // Read the sensor value
  float waterLevel = map(sensorValue, 0, 1023, 0, 100);
  Serial.println(waterLevel); // Print the water level
}