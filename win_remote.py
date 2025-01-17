import socket
import os
import subprocess

class WinRemoteServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[*] Listening on {self.host}:{self.port}")
            conn, addr = s.accept()
            with conn:
                print(f"[*] Connection established with {addr}")
                while True:
                    command = conn.recv(1024).decode('utf-8')
                    if not command:
                        break
                    output = self.execute_command(command)
                    conn.sendall(output.encode('utf-8'))

    def execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e}"

class WinRemoteClient:
    def __init__(self, host, port=9999):
        self.host = host
        self.port = port

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(command.encode('utf-8'))
            data = s.recv(4096)
            print(data.decode('utf-8'))

# Example usage:
# server = WinRemoteServer()
# server.start_server()

# client = WinRemoteClient('127.0.0.1')
# client.send_command('dir')