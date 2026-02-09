import os
import json
import datetime

class FakeShell:
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.cwd = "/home/user"
        
    def execute(self, command):
        command = command.strip()
        timestamp = datetime.datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "ip": self.client_ip,
            "command": command
        }
        
        with open("commands.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        if command == "ls":
            return "Documents  Downloads  Desktop  secrets.txt\n"
        elif command == "whoami":
            return "user\n"
        elif command == "pwd":
            return f"{self.cwd}\n"
        elif command.startswith("cd"):
            return ""
        elif command == "cat secrets.txt":
            return "API_KEY=shhh_dont_tell_anyone\n"
        else:
            return f"sh: command not found: {command}\n"
