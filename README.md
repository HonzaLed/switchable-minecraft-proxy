# switchable-minecraft-proxy
Proxy for switching between 2 clients without getting kicked

## How to run this  
Start the proxy by executing command
```bash
python3 switchable_proxy.py <server IP> <server port>
```

You can then connect with first client at address `127.0.0.1:<server port>` and second client at address `127.0.0.1:<server port+1>`  
**Note that you must connect them very quickly after each other**  

## How to use it
You can then use this to switch between these 2 connected clients.  
When you start the program, console beggining with `$ ` should appear,
you can then switch to the fisrt client by writing `1` or to the second one by writing `2` and pressing `enter`.
