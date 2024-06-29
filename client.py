import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1234))

try:
    while True:
        msg = s.recv(2005)
        if not msg:
            break
        print("Received from server:", msg.decode("utf-8"))
except KeyboardInterrupt:
    print("Connection closed")
finally:
    s.close()
