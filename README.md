# Key logger


This Python script sets up a server that captures keystrokes using the `pynput` library and sends them to connected clients over a TCP connection.

## Prerequisites

- Python 3.x
- `pynput` library (`pip install pynput`)

## How It Works

1. **Keystroke Capture**: The script captures keystrokes using `pynput.keyboard.Listener`.

2. **Server Setup**: It sets up a TCP server that listens on `localhost` (`127.0.0.1`) and port `1234`.

3. **Sending Keystrokes**: Keystrokes are sent to connected clients in real-time whenever there are new keystrokes captured.

4. **Threading**: It utilizes threading to handle keystroke sending and key press capturing concurrently.


