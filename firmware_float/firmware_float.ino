#include <WiFi.h>  // For ESP32; 
#include <float.h>

// Pins for motor control
#define MOTOR_PIN_1 26
#define MOTOR_PIN_2 27

// Server (Python GUI) IP and port

const char* host = laptop_ip;  // Change to your PC's IP
const uint16_t port = 1234;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  connectToWiFi();
  connectToServer();
#ifdef TRIAL
  pinMode(MOTOR_PIN_1, OUTPUT);
  pinMode(MOTOR_PIN_2, OUTPUT);
#endif
stopMotor();  // Ensure motor is stopped at start
 
}
void loop() {
  if (!client.connected()) {
    Serial.println("Disconnected. Trying to reconnect...");
    connectToServer();
    delay(1000);
  }

  if (client.available()) {
    String cmd = client.readStringUntil('\n');
    cmd.trim();
    Serial.println("Received: " + cmd);

    if (cmd == "START") {
      client.println("ACK");
      Serial.println("ACK sent. Diving...");
      dive();
    }
  }
}

// ----------- Core Functions -----------

void connectToWiFi() {
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected. IP: " + WiFi.localIP().toString());

  if (!WiFi.config(IPAddress(192, 168, 1, 6), IPAddress(255, 255, 255, 0), IPAddress(192, 168, 1, 1))) {
    Serial.println("Failed to set static IP. Using DHCP.");
  } else {
    Serial.println("Static IP set successfully.");
  }
}

void connectToServer() {
  Serial.println("Connecting to server...");
  while (!client.connect(host, port)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConnected to server.");
}

void dive() {
  client.stop();    // simulate connection loss
  Serial.println("Diving underwater, connection lost...");
  goDown();         // Simulate going down
  delay(1000);      // Simulate time underwater
  goUp();           // Simulate coming back up

  // Now resurface and reconnect
  Serial.println("Resurfacing...");
  connectToWiFi();     // In case Wi-Fi was lost too
  connectToServer();   // Reconnect to GUI

  client.println("TOP");  // Notify we are at the surface
  Serial.println("Sent TOP confirmation.");

  // Begin sending dummy telemetry
  while (true) {
    if (!client.connected()) {
      Serial.println("Connection lost again. Trying to reconnect...");
      connectToServer();
    }

    // String data = "DATA:" + String(random(20, 30)) + "," + String(random(800, 1000));
    // client.println(data);
    // Serial.println("Sent: " + data);
    // delay(1000);
  }
}

void stopMotor() {
  digitalWrite(MOTOR_PIN_1, LOW);
  digitalWrite(MOTOR_PIN_2, LOW);
  Serial.println("Motor stopped.");
}

void goDown() {
#ifdef TRIAL
  digitalWrite(MOTOR_PIN_1, HIGH);
  digitalWrite(MOTOR_PIN_2, LOW);
#endif
  Serial.println("Going down...");
  delay(TIME_FOR_GOING_DOWN);  // Simulate time to go down
  stopMotor();  
  Serial.println("Reached bottom.");
  delay(45000);  // Simulate time at the bottom
  stopMotor();

}               

void goUp() {
#ifdef TRIAL
  digitalWrite(MOTOR_PIN_1, LOW);
  digitalWrite(MOTOR_PIN_2, HIGH);
#endif
  Serial.println("Going up...");
  delay(TIME_FOR_GOING_UP);  // Simulate time to go up
  stopMotor();
  Serial.println("Reached surface.");
}