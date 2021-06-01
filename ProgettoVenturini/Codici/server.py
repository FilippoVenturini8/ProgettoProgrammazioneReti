"""
SERVER
"""

import socket as sk
import time 

serverTCPSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

server_port = 8200
server_address=('localhost', 8200)

server_ip = "10.10.10.1"
server_mac = "F3:04:73:EF:10:BF"

serverTCPSocket.bind(server_address)
serverTCPSocket.listen(1)
print ('The server is up on port:',8200)
 
while True:
    try:
        print ('Ready to serve...\n')
        connectionSocket, addr = serverTCPSocket.accept()

        packet = connectionSocket.recv(512)
        packet = packet.decode("utf-8")
        
        gateway_mac = packet [0:17]
        
        gateway_ip = packet [34:44]
        
        gateway_port = packet[54:59]
  
        data = packet[64:]
        
        print("Source MAC address: " + gateway_mac + ", destination MAC address: " + server_mac +
              "\nSource IP address: " + gateway_ip + ", destination IP address: " + server_ip +
              "\nSource port: " + gateway_port + ", destination port: " + str(server_port) +
              "\n\n" + data)
        
        ethernet_header = server_mac + gateway_mac 
        IP_header = server_ip + gateway_ip
        TCP_header = str(server_port).zfill(5) + str(gateway_port).zfill(5)
        
        response_packet = ethernet_header + IP_header + TCP_header + "Packet received...\n"
        
        connectionSocket.send(bytes(response_packet,"utf-8"))

    except IOError:
        connectionSocket.close()