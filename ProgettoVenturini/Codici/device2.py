'''
------DEVICE 2-------

'''

import socket as sk
import time 
import datetime
import random

device2_ip = "192.168.1.3"
device2_mac = "32:04:0A:EF:19:CF"

gateway_ip = "192.168.1.1"
gateway_mac = "05:10:0A:CB:24:EF"

gateway_port = 8100

gateway = ("localhost", gateway_port)

ethernet_header = device2_mac + gateway_mac 
IP_header = device2_ip + gateway_ip 

random.seed()

while True:
    try:
        device2Socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        device2Socket.connect(gateway)
        device2_port = str(device2Socket.getsockname()[1])
        
        UDP_header = str(device2_port).zfill(5) + str(gateway_port).zfill(5)
        
        now = datetime.datetime.now()
        current_hour = str(now.hour) + ":" + str(now.minute) + ":"  + str(now.second)

        message = current_hour +  " – " + str(random.randrange(0, 30)) +"°C – " + str(random.randrange(40, 60)) + "%"
        packet = ethernet_header + IP_header + UDP_header + message 
        
        print("Source MAC address: " + device2_mac + ", destination MAC address: " + gateway_mac +
              "\nSource IP address: " + device2_ip + ", destination IP address: " + gateway_ip +
              "\nSource port: " + device2_port + ", destination port: " + str(gateway_port) + "\n")
        
        print ('Sending: "%s"\n' % message)
        
        start = time.time()
        device2Socket.sendto(packet.encode(), gateway)
        
        response, address = device2Socket.recvfrom(128)
        response = response.decode("utf-8")
        
        end = time.time()
        
        if(response != ""):
            print("UDP Trasmission time: ", end-start, " s.\n")
        else:
            print("Error in packet trasmission!")
        
        device2Socket.close()
        time.sleep(30)
    except IOError:
        device2Socket.close()