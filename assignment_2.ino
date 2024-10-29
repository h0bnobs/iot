#include <WiFi.h>

HardwareSerial barcodeSerial(2);
#define BARCODE_TX    12
#define BARCODE_RX    39

#define BUFFER_LEN    512
char scanBuffer[BUFFER_LEN + 1];

// WiFi credentials
const char* ssid = "iPhone (67)";  // Replace with your network's SSID
const char* password = "max12345";  // Replace with your network's password

// Server configuration (Optional: if you want to send the data to a server)
const char* server = "172.20.10.5";  // Replace with your server's address

void setup() {
  Serial.begin(115200);
  barcodeSerial.begin(115200, SERIAL_8N1, BARCODE_RX, BARCODE_TX);

  Serial.println("Connecting to WiFi...");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("DE2120 Scanner Example");
}

void loop() {
  if (barcodeSerial.available()) {
    int length = barcodeSerial.readBytesUntil('\n', scanBuffer, BUFFER_LEN);
    scanBuffer[length] = '\0';
    Serial.print("Code found: ");
    Serial.println(scanBuffer);

    // Optional: Send the data over Wi-Fi (e.g., to a server)
    sendData(scanBuffer);
  }
}

// Function to send data to a server
void sendData(const char* data) {
  if (WiFi.status() == WL_CONNECTED) {
      Serial.println("in the first 'if'");
    // Use WiFiClient for HTTP requests, or any suitable library if needed
    WiFiClient client;
    if (client.connect(server, 1234)) {
      Serial.println("in the next and connected");
      client.print(String("GET /submit?data=") + data + " HTTP/1.1\r\n" +
                   "Host: " + server + "\r\n" +
                   "Connection: close\r\n\r\n");
      Serial.println("Data sent!");
    } else {
      Serial.println("Not connected to server");
    }
    client.stop();
  } else {
    Serial.println("WiFi not connected. Unable to send data.");
  }
}
