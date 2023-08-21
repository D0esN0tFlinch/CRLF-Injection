import socket
import urllib.parse
import re



def parse_request_to_lines(request_text):
    lines = request_text.split('\r\n')
    method, url, version = lines[0].split(' ')
    return method, url, version

def handle_client_and_build_response(client_socket):
    request_data = client_socket.recv(1024).decode("utf-8")
    method, url, version = parse_request_to_lines(request_data)
    
    #Extract the userInput parameter 
    query = urllib.parse.urlparse(url).query
    query_params = urllib.parse.parse_qs(query)
    userInput = query_params.get('userInput', [''])[0]
    
    #Prepare the HTTP response without user input
    response_body = "<html><body><h1>CRLF LAB BY Niv Roda</h1></body></html>"
    response_headers = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n"
    #sanitized_input = re.sub(r'[\r\n]', '', userInput) # (Fix 1) regex to find \r\n in user input.
    
    if userInput:
        response_headers += f"Custom-Header: {userInput}\r\n"
        #response_headers += f"Custom-Header: {sanitized_input}\r\n" # (Fix step 2) This will append the sanitized input and not the vulnerable one.
    
    response_headers += "\r\n"

    # Send the HTTP response
    client_socket.sendall((response_headers + response_body).encode("utf-8"))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)

    print("Listening on port 8080...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        handle_client_and_build_response(client_socket)

# Start server
main()