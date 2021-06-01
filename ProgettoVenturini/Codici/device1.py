'''
------DEVICE 1-------

'''

import socket as sk
import time 
import datetime
import random

device1_ip = "192.168.1.2"
device1_mac = "10:AF:CB:EF:19:CF"

gateway_ip = "192.168.1.1"
gateway_mac = "05:10:0A:CB:24:EF"

gateway_port = 8100

gateway = ("localhost", gateway_port)

ethernet_header = device1_mac + gateway_mac 
IP_header = device1_ip + gateway_ip 

random.seed()

while True:
    try:
        device1Socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        device1Socket.connect(gateway)
        device1_port = str(device1Socket.getsockname()[1])
        
        UDP_header = str(device1_port).zfill(5) + str(gateway_port).zfill(5) 
        
        now = datetime.datetime.now()
        current_hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

        message = current_hour +  " – " + str(random.randrange(0, 30)) +"°C – " + str(random.randrange(40, 60)) + "%"
        packet = ethernet_header + IP_header + UDP_header + message 
        
        print("Source MAC address: " + device1_mac + ", destination MAC address: " + gateway_mac +
              "\nSource IP address: " + device1_ip + ", destination IP address: " + gateway_ip +
              "\nSource port: " + device1_port + ", destination port: " + str(gateway_port) + "\n")
        
        print ('Sending: "%s"\n' % message)
        
        start = time.time()
        device1Socket.sendto(packet.encode(), gateway)
        
        response, address = device1Socket.recvfrom(128)
        response = response.decode("utf-8")
        
        end = time.time()
        
        if(response != ""):
            print("UDP Trasmission time: ", end-start, " s.\n")
        else:
            print("Error in packet trasmission!")
        
        device1Socket.close()
        time.sleep(30)
    except IOError:
        device1Socket.close()
        