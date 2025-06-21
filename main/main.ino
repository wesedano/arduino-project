// Blink the built-in LED for 2 seconds on and 2 seconds off.
void setup() {
  // Initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED on
  delay(2000);                      // Wait 2 seconds
  digitalWrite(LED_BUILTIN, LOW);   // Turn the LED off
  delay(2000);                      // Wait 2 seconds
}
