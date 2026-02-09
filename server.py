import socket
import threading
import paramiko
from core import FakeShell

HOST_KEY = paramiko.RSAKey.generate(2048)

class AdvancedHoneypot(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        with open("creds.json", "a") as f:
            f.write(f"{self.client_ip} - {username}:{password}\n")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"

def handle_session(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = AdvancedHoneypot(addr[0])
    
    try:
        transport.start_server(server=server)
        chan = transport.accept(20)
        if chan is None: return
        
        chan.send("Welcome to Ubuntu 22.04.1 LTS\r\n\r\n")
        shell = FakeShell(addr[0])
        
        while True:
            chan.send("user@ubuntu:~$ ")
            command = ""
            while not command.endswith("\r"):
                char = chan.recv(1)
                chan.send(char)
                command += char.decode()
            
            chan.send("\r\n")
            response = shell.execute(command.replace("\r", ""))
            chan.send(response.replace("\n", "\r\n"))
            
    except Exception:
        transport.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 2222))
    sock.listen(100)
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_session, args=(client, addr)).start()

if __name__ == "__main__":
    main()
