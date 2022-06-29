# switchable-minecraft-proxy
Proxy for switching between 2 clients without kick

## How to run this  
Start the proxy by executing command
```bash
python3 switchable_proxy.py <server IP> <server port>
```

You can then connect with first client at address `127.0.0.1:<server port>` and second client at address `127.0.0.1:<server port+1>`  
**Note that you must connect them very fastly after each other**
