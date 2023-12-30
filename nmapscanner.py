import nmap
import sys

if len(sys.argv) < 2:
	print (f"Usage: {sys.argv[0]} <url>")
	sys.exit(0)
target=str(sys.argv[1])
ports=[21,22,80,139,443,8080]

scan=nmap.PortScanner()
print(f'Scanning {sys.argv[1]} for ports {ports} : ')
for port in ports:
	portscan=scan.scan(target,str(port))
	print(portscan["scan"].keys())
	
	print(f'Port {port} is {portscan["scan"][list(portscan["scan"].keys())[0]]["tcp"][port]["state"]}')
	
	
