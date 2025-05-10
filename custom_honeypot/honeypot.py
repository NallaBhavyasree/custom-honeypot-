import socket
import json
import datetime
import os

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

HOST = '0.0.0.0'
PORT = config['port']
LOG_FILE = config['log_file']
BANNER = config['banner'].encode()
COMMANDS = config['commands']

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_connection(client_ip, data):
    with open(LOG_FILE, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"[{timestamp}] {client_ip} > {data.strip()}\n")
        print(f"[{timestamp}] {client_ip} > {data.strip()}")

def start_honeypot():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Honeypot listening on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        print(f"Connection from {client_ip}")

        # Send the fake banner
        client_socket.send(BANNER)

        try:
            while True:
                # Receive data from the attacker
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break

                log_connection(client_ip, data)

                # Respond to known commands
                response = COMMANDS.get(data, "Command not found\n")
                client_socket.send((response + '\n').encode())

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print(f"Connection closed from {client_ip}")

if __name__ == '__main__':
    start_honeypot()
