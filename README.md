# dns-spoof-script-injection 

## How use it ?

  - open dns-spoofer.py file
  - edit spoofed_names dict as per your need
  - to see interfaces **netsh interface show interface**
  - change default dns server to your ip (for local , 127.0.0.1). Use command **netsh interface ip add dns name="{interface}" addr={ip} index=1**

###

- pip install dnspython  

### TO DO
- automatically change dns server
- create a server to serve spoofed requests
- inject javascript to spoofed requests
- non blocking server