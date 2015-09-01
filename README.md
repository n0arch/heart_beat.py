# heartbeat.py

A simple python script with colorful output to test creating tcp connections on a given host and port.

If TCP socket connection fails, the service will attempt to ping the target.


This script requires no special modules be installed on the system. 


To configure, set the SERVERS dictionary values to reflect {'host':port}
  host is a string (quotes)
  port is an int (no quotes)

