import socket

def talk_to_esp(self):
    ESP_IP = "192.168.1.6"   
    ESP_PORT = 12345

    # Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to ESP
        client.connect((ESP_IP, ESP_PORT))

        # Send command
        client.sendall(b"START\n")
        # recv is waiting for esp to send data blocking the code
        data = client.recv(1024)
        recevied = data.decode
        return recevied

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

