void setup() {
  // Initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED on
  delay(1000);                      // Wait 1 second
  digitalWrite(LED_BUILTIN, LOW);   // Turn the LED off
  delay(1000);                      // Wait 1 second
}
