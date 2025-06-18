#include <WiFi.h>  // For ESP32; use <ESP8266WiFi.h> for ESP8266

// Pins for motor control
#define MOTOR_PIN_1 26
#define MOTOR_PIN_2 27

// Time constants for diving
#define TIME_FOR_GOING_DOWN 5000  // Time to go down in milliseconds
#define TIME_FOR_GOING_UP 5000    // Time to go up in milliseconds


// Wi-Fi credentials
const char* ssid = "Borham2";
const char* password = "18046768";

// Server (Python GUI) IP and port
// Run this command in your terminal to know ur laptop's IP:
// ipconfig
// expect the following output:
/*
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . : home
   IPv6 Address. . . . . . . . . . . : fd8c:d76:375e:1b00:cb8c:c0c8:7abb:18ed
   Temporary IPv6 Address. . . . . . : fd8c:d76:375e:1b00:91ff:9d15:e368:daa2
   Link-local IPv6 Address . . . . . : fe80::baec:9687:f239:3a79%11
   IPv4 Address. . . . . . . . . . . : 192.168.1.5                                  <---- Change to your PC's IP         
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
*/
const char* host = "192.168.1.5";  // Change to your PC's IP
const uint16_t port = 1234;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  connectToWiFi();
  connectToServer();
  // pinMode(MOTOR_PIN_1, OUTPUT);
  // pinMode(MOTOR_PIN_2, OUTPUT);
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
  // digitalWrite(MOTOR_PIN_1, HIGH);
  // digitalWrite(MOTOR_PIN_2, LOW);
  Serial.println("Going down...");
  delay(TIME_FOR_GOING_DOWN);  // Simulate time to go down
  stopMotor();  
  Serial.println("Reached bottom.");
  delay(45000);  // Simulate time at the bottom
  stopMotor();
}   

void goUp() {
  // digitalWrite(MOTOR_PIN_1, LOW);
  // digitalWrite(MOTOR_PIN_2, HIGH);
  Serial.println("Going up...");
  delay(TIME_FOR_GOING_UP);  // Simulate time to go up
  stopMotor();
  Serial.println("Reached surface.");
}