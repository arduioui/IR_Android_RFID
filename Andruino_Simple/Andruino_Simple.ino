static int counter = 0;

void setup() {
  Serial.begin(115200);

}

void loop() {
  Serial.print("Tick #");
  Serial.print(counter++, DEC);
  Serial.print("\n");

  if (Serial.peek() != -1) {
    Serial.print("Read: ");
    do {
      Serial.print((char) Serial.read());
    } while (Serial.peek() != -1);
    Serial.print("\n");
  }
  delay(1000);
}
