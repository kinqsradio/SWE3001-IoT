#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
#define LEDPIN 4      // Digital pin connected to the LED
#define TEMP_THRESHOLD 22.1 // Temperature threshold in Celsius

DHT_Unified dht(DHTPIN, DHTTYPE);

#define LM35PIN A3  // Analog pin connected to the LM35 sensor

uint32_t delayMS;

void setup() {
  pinMode(LEDPIN, OUTPUT);  // Set the LED pin as an output
  Serial.begin(9600);
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  delayMS = sensor.min_delay / 1000;
}

void loop() {
  delay(delayMS);
  sensors_event_t event;

  // Read temperature and humidity from DHT11
  dht.temperature().getEvent(&event);
  float dhtTemperature = isnan(event.temperature) ? 0 : event.temperature;
  dht.humidity().getEvent(&event);
  float humidity = event.relative_humidity;

  // Read temperature from LM35
  int analogValue = analogRead(LM35PIN); // Read analog value from LM35
  float voltage = analogValue * (5.0 / 1023.0); // Convert to voltage
  float lm35Temperature = voltage * 100.0; // Convert voltage to temperature

  // Check if the temperature is above the threshold
  if (dhtTemperature > TEMP_THRESHOLD) {
    digitalWrite(LEDPIN, HIGH); // Turn on the LED
  } else {
    digitalWrite(LEDPIN, LOW);  // Turn off the LED
  }

  // Print temperatures and humidity to the Serial Monitor
  Serial.print(dhtTemperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(lm35Temperature);
}
