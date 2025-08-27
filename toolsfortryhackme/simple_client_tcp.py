import socket
import sys

attacker_host = sys.argv[1]
attacker_port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((attacker_host, attacker_port))

client.send(f"GET / HTTP/1.1\r\nHost: {attacker_host}\r\n\r\n".encode())

response = client.recv(4096)

print(response.decode())
client.close()
