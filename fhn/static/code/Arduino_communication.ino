int RELAY_PIN = 14;
#define RELAY_PIN 14  // Digital pin connected to the relay

void setup() {
    Serial.begin(9600);  // Initialize serial communication
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, HIGH);  // Start with relay OFF
}

void loop() {
    if (Serial.available() > 0) {  // Check if data is received
        char command = Serial.read();  // Read the incoming byte
        if (command == '0') {
            digitalWrite(RELAY_PIN, HIGH);  // Turn relay ON
            Serial.println("Relay ON");
        } 
        else if (command == '1') {
            digitalWrite(RELAY_PIN, LOW);  // Turn relay OFF
            Serial.println("Relay OFF");
        }
    }
}

