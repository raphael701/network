import socket
import msvcrt
import sys

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
my_socket.setblocking(False)


while True:
    if msvcrt.kbhit():
        msg = sys.stdin.readline().strip()
        if msg.lower() == "exit":
            break

        my_socket.send(msg.encode())

    try:
        data = my_socket.recv(1024).decode()
        if data.startswith("NAME "):
            print("Hello", data.split(" ",1)[1])
        
        else:
            print(data)  

    except socket.error:
        pass

my_socket.close()




