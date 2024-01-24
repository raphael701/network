import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'

def get_client_names():
    return " ".join(clients_name.values())


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
messages_to_send = []
clients_name = {}

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
                       
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "":
                print("Connection closed")
                client_sockets.remove(current_socket)
                del clients_name[current_socket]
                current_socket.close()
                            
            else:
                
                if data.startswith("NAME "):
                    client_name = data.split(" ", 1)[1]
                    clients_name[current_socket] = client_name    
                    
                elif data.startswith("get_names"):
                    current_socket.send(get_client_names().encode())
                    continue # skip adding command to message to send
                
                elif data.startswith("send "):
                    parts = data.split(" ",2)
                    if len(parts) == 3:
                        target_name, message_content = parts[1], parts[2]
                        for user_sokcet, username in clients_name.items():
                            if target_name == username:
                                user_sokcet.send(f"{target_name} sent: {message_content()}".encode())
                                break
                                
                        else:
                            current_socket.send("User not found".encode())
                            continue
                else:
                    current_socket.send("Unknown command ".encode())
                    continue # skip adding command to message to send
                messages_to_send.append((current_socket, data)) 
                
         
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in wlist:
            current_socket.send(data.encode())
            messages_to_send.remove(message)