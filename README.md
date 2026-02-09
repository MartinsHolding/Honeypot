# SentinelShell - Advanced SSH Honeypot & Behavioral Logger

SentinelShell is a high-interaction SSH honeypot designed to capture not only credentials but also post-exploitation behavior.

## Architecture
- **Protocol Simulation**: Full SSH handshake via Paramiko.
- **Virtual File System**: Simulates a Linux environment to track attacker commands.
- **Log Aggregation**: Exports data in structured JSON for ELK/Splunk integration.


## Quick Start
1. Build the container:
   docker build -t sentinelshell .
2. Run it:
    docker run -d -p 22:2222 --name honeypot sentinelshell

   
## Key Capabilities
- Credential Harvesting: Logs every attempt in creds.json.
- Session Recording: Every command is captured with sub-second timestamps.
- Alert Ready: Structured logs ready for Discord/Slack webhook integration.
