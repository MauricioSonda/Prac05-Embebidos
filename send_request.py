
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

request = (
    "GET /admin HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "Authorization: {token:1234}\r\n"
    "\r\n"
)

client_socket.send(request.encode('utf-8'))

response = client_socket.recv(4096).decode('utf-8')
print(response)

client_socket.close()