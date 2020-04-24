#include <pm2008_i2c.h>
#include "DHT.h"

PM2008_I2C pm2008_i2c;
DHT dht(5,DHT11);

void setup() {
  Serial.begin(9600);
  pm2008_i2c.begin();
  pm2008_i2c.command();
  dht.begin();
  delay(1000);
}

void loop() {
  float hum = dht.readHumidity();
  float tem = dht.readTemperature();
  if (isnan(hum) || isnan(tem)) {
    Serial.println(F("DHT sensor Error!"));
  }
  //float heatCelsius = dht.computeHeatIndex(tem, hum, false);
  
  uint8_t ret = pm2008_i2c.read();
  if (ret == 0) {
    Serial.print("PM 1.0 (GRIMM) : ");
    Serial.print(pm2008_i2c.pm1p0_grimm);
    Serial.print(", PM 2.5 (GRIMM) : ");
    Serial.print(pm2008_i2c.pm2p5_grimm);
    Serial.print(", PM 10 (GRIMM) : ");
    Serial.print(pm2008_i2c.pm10_grimm);

    Serial.print(", Humidity : ");
    Serial.print(hum);
    Serial.print("%, Temp : ");
    Serial.print(tem);
    Serial.println("C");
  }
  delay(1000);
}
