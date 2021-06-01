"""
------GATEWAY-------

"""

import socket as sk 
import time

n_devices = 4

gatewayUDPSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

gateway_UDP_port = 8100
server_port = 8200

gatewayUDPSocket.bind(("localhost", gateway_UDP_port))

server = ("localhost", server_port)

gateway_private_ip = "192.168.1.1"
gateway_public_ip = "10.10.10.2"

gateway_mac = "05:10:0A:CB:24:EF"

server_ip = "10.10.10.1"
server_mac = "F3:04:73:EF:10:BF"

arp_table = {}

connected_devices_ip = []
all_devices_data = []

while True:
    try:
        print('\n\rWaiting the devices connections...\n')
        message = ""
        
        while(len(connected_devices_ip) < n_devices):
            packet, address = gatewayUDPSocket.recvfrom(128)
            packet = packet.decode("utf-8")
            
            device_mac = packet[0:18]
            device_ip = packet[34:45]
            device_port = packet[56:61] 
            device_data = packet [66:]
            
            UDP_header = str(gateway_UDP_port).zfill(5) + str(device_port).zfill(5)
            ethernet_header = gateway_mac + device_mac 
            IP_header = gateway_private_ip + device_ip
            
            response_packet = ethernet_header + IP_header + UDP_header + "Packet received...\n"
            
            gatewayUDPSocket.sendto(bytes(response_packet,"utf-8"), ('localhost', int(device_port)))
            
            if(device_ip not in connected_devices_ip):
                arp_table[device_ip] = device_mac
                connected_devices_ip.append(device_ip)
                all_devices_data.append(device_data)
                print(device_ip + " connected")
        for i in range(n_devices):
            message += connected_devices_ip[i] + " - " + all_devices_data[i] + " \n"

        gatewayTCPSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        gatewayTCPSocket.connect(server)
        gateway_TCP_port = str(gatewayTCPSocket.getsockname()[1])  
        
        ethernet_header = gateway_mac + server_mac 
        IP_header = gateway_public_ip + server_ip 
        TCP_header = str(gateway_TCP_port).zfill(5) + str(server_port).zfill(5)
        
        packet = ethernet_header + IP_header + TCP_header + message
        
        print('\n\rSending to the server...\n')
        start = time.time()
        gatewayTCPSocket.send(bytes(packet,"utf-8"))
        
        response = gatewayTCPSocket.recv(128)
        response = response.decode("utf-8")
        end = time.time()
        
        if(response != ""):
            print("TCP Trasmission time: ", end-start, " s.\n")
        else:
            print("Error in packet trasmission!")
        
        gatewayTCPSocket.close()
        connected_devices_ip.clear()
        all_devices_data.clear()

    except IOError:
        gatewayUDPSocket.close()
        gatewayTCPSocket.close()
        