import socket
import os
from scapy.all import *

IP = "127.0.0.1"
PORT = 80
# Creating the HTML file
file_html = open("demo.html", "w")

# Adding the input data to the HTML file
file_html.write('''<html>
<head>
<title>HTML File</title>
</head> 
<body>
<h1>Welcome Finxters</h1>           
<p>Example demonstrating How to generate HTML Files in Python</p> 
</body>
</html>''')

# Saving the data into the HTML file
file_html.close()
def filter_dns(packet):
    if DNSQR in packet:
        return (packet[DNS].opcode == 0) and (packet[DNSQR].opcode == 0)
    
def print_query_name(dns_packet):
    print(dns_packet[DNSQR].qname.decode())

def get_file_data(filename):
    """Reads the content of a file from the local filesystem and returns it"""
    
    try:
        with open(filename, 'rb') as file:
            return file.read()
    
    except FileNotFoundError:
        return b"404 Not Found: The requested resource was not found on this server."


def validate_http_request(file_path):
    """
    Check if the file path exists and return True if it does, False otherwise
    """
    # Check if the file path exists
    return os.path.exists(file_path)


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
    """ Check the required resource, generate proper HTTP response and send to client"""
    # Construct the full path to the requested resource
    if resource == "/":
        resource = "/demo.html"  # Serve demo.html for root URL
    
    filename = resource
    if os.path.exists(filename):
        # Read the content of the requested file
        res_content = get_file_data(filename)

        # Determine the Content-Type based on the file extension
        content_type = "text/plain"
        if filename.endswith(".html"):
            content_type = "text/html"

        # Construct the HTTP response header
        http_response_header = f"HTTP/1.1 200 OK\r\n"
        http_response_header += f"Content-Type: {content_type}\r\n"
        http_response_header += f"Content-Length: {len(res_content)}\r\n"
        http_response_header += "\r\n"  # End of header

        # Send the response to the client
        client_socket.send(http_response_header.encode() + res_content)
    
    else:
        # File not found, send a 404 response
        http_response_header = "HTTP/1.1 404 Not Found\r\n"
        http_response_header += "Content-Type: text/plain\r\n"
        http_response_header += "Content-Length: 13\r\n\r\n"
        http_response_header += "404 Not Found\r\n"
        client_socket.send(http_response_header.encode())


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