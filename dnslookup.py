import socket
from scapy.all import *
from urllib.parse import urlparse

IP = "127.0.0.1"
PORT = 80

def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    
    while True:
        try:
            request_data = client_socket.recv(1024).decode()
            if request_data.startswith("GET") or request_data.startswith("POST"):
                print('Got a valid HTTP request')
                request_url_data = request_data.split('\n')[0].split(' ')[1]
                handle_client_request(request_url_data, client_socket)
                break
            
            else:
                print('Error: Not a valid HTTP request')
                break
        
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
    print('Closing connection')
    client_socket.close()



def handle_client_request(resource, client_socket):
    if resource.startswith("/"):
        resource = resource[1:]  # Remove the leading "/"
    the_domain = resource  # Use the resource as the domain

    try:
        # Perform DNS lookup for the domain
        ips = socket.gethostbyname_ex(the_domain)[-1]
        if ips:
            # Construct the HTTP response header and body
            http_response_header = "HTTP/1.1 200 OK\r\n"
            http_response_header += "Content-Type: text/html\r\n"
            http_response_header += "\r\n"  # End of header
            
            http_response_body = "<html>\n<head>\n<title>Resolved IPs</title>\n</head>\n<body>\n"
            for ip in ips:
                http_response_body += f"<p>{ip}</p>\n"
            http_response_body += "</body>\n</html>\n" #End of body
        
            # Send the response to the client
            client_socket.send((http_response_header + http_response_body).encode())
        
        else:
            # No IPs found for domain, send 404 response
            http_response_header = "HTTP/1.1 404 Not Found\r\n"
            http_response_header += "Content-Type: text/plain\r\n"
            http_response_header += "Content-Length: 13\r\n\r\n"
            http_response_header += "404 Not Found\r\n"
            client_socket.send(http_response_header.encode())
    
    except Exception as e:
        print(f"Error performing DNS lookup: {str(e)}")

def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        handle_client(client_socket)

if __name__ == "__main__":
    # Call the main handler function
    main()
