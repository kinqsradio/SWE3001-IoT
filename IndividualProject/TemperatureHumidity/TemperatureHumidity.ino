#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);

#define LM35PIN A3  // Analog pin connected to the LM35 sensor

uint32_t delayMS;

void setup() {
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
  float voltage = (analogValue / 1023.0) * 5.0; // Convert to voltage (0-5V)
  float lm35Temperature = voltage * 100.0; // Convert voltage to temperature in °C (10 mV per degree)

  // Print all readings in one line
  Serial.print("DHT Temp: ");
  Serial.print(dhtTemperature);
  Serial.print("°C, Humidity: ");
  Serial.print(humidity);
  Serial.print("%, LM35 Temp: ");
  Serial.print(lm35Temperature);
  Serial.println("°C");
}
