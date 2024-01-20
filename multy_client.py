import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
msg = input("Plz enter something:\n")

while msg != "exit":
    
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    
    if msg.startswith("NAME "):
        print("Hello",data.split(" ",1)[1])
    
    else:
        print(data)
    msg = input("Plz enter something:\n")
    
my_socket.close()