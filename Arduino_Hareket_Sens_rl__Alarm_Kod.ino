int pirPin = 2;     // PIR sensör çıkışı
int ledPin = 13;    // LED pini
int hareket;

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  hareket = digitalRead(pirPin);

  if (hareket == HIGH) {
    digitalWrite(ledPin, HIGH);
    Serial.println("Hareket algılandı!");
    delay(2000);               // LED 2 saniye boyunca yanık kalır
  } else {
    digitalWrite(ledPin, LOW);
    Serial.println("Hareket yok.");
  }

  delay(100); // Gereksiz gecikmeyi azaltmak için küçük bekleme
}
