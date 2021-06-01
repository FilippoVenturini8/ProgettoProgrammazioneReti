'''
------DEVICE 3-------

'''

import socket as sk
import time 
import datetime
import random

device3_ip = "192.168.1.4"
device3_mac = "AC:16:2D:02:C8:19"

gateway_ip = "192.168.1.1"
gateway_mac = "05:10:0A:CB:24:EF"

gateway_port = 8100

gateway = ("localhost", gateway_port)

ethernet_header = device3_mac + gateway_mac 
IP_header = device3_ip + gateway_ip 

random.seed()

while True:
    try:
        device3Socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        device3Socket.connect(gateway)
        device3_port = str(device3Socket.getsockname()[1])
        
        UDP_header = str(device3_port).zfill(5) + str(gateway_port).zfill(5)
        
        now = datetime.datetime.now()
        current_hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

        message = current_hour +  " – " + str(random.randrange(0, 30)) +"°C – " + str(random.randrange(40, 60)) + "%"
        packet = ethernet_header + IP_header + UDP_header + message 
        
        print("Source MAC address: " + device3_mac + ", destination MAC address: " + gateway_mac +
              "\nSource IP address: " + device3_ip + ", destination IP address: " + gateway_ip +
              "\nSource port: " + device3_port + ", destination port: " + str(gateway_port) + "\n")
        
        print ('Sending: "%s"\n' % message)
        
        start = time.time()
        device3Socket.sendto(packet.encode(), gateway)
        
        response, address = device3Socket.recvfrom(128)
        response = response.decode("utf-8")
        
        end = time.time()
        
        if(response != ""):
            print("UDP Trasmission time: ", end-start, " s.\n")
        else:
            print("Error in packet trasmission!")
        
        device3Socket.close()
        time.sleep(30)
    except IOError:
        device3Socket.close()