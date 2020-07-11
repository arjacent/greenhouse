#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import socket
import sys
import time

html = ""
# sends 200 HTTP header before sending HTLM
def sendHeader(conn):
    conn.send(b"HTTP/1.1 200 OK\n")
    conn.send(b"Content-Type: text/html\n")
    conn.send(b"Connection: close\n")
    conn.send(b"Refresh: 5\n")
    #conn.send(b"Connection: keep-alive\n")
    conn.send(b"\n")


# handles the read query, which sends back all measurements from the Arduino
# returns the HTLM page with updated values
def readRequest():
    print("readRequest()")
    ser.flush()
    time.sleep(3)
    ser.write(b"read\n")
    time.sleep(2)  
    arduinoData = ''
    while ser.in_waiting > 0:
        print("Reading serial...")     
        arduinoData += ser.readline().decode('ascii').rstrip() + "<br>"        
    global html
    html = '<!DOCTYPE html> <html> <head> <title>Remote Environment Controller</title><meta charset="ASCII"/><link rel="icon" href=""></head><body><h1>Remote Environment Controller</h1><form method="get"><button type="submit" name="read" value=1>Read</button><button type="submit" name="light" value=1>Light On</button><button type="submit" name="light" value=0>Light Off</button><button type="submit" name="fan" value=1>Fan On</button><button type="submit" name="fan" value=0>Fan Off</button><br><br><button type="submit" name="auto" value=0>Auto OFF</button><button type="submit" name="auto" value=1>Auto Light Only</button><button type="submit" name="auto" value=2>Auto Fan Only</button><button type="submit" name="auto" value=3>Auto Both</button><br><br><br><button type="submit" name="off" value=1>OFF</button></form><p>'+arduinoData+'</p></body></html>'
    #html = '<!DOCTYPE html> <html> <head> <title>Remote Environment Controller</title><meta charset="ASCII"/><link rel="icon" href=""></head><body><h1>Remote Environment Controller</h1><form method="get"><button style="font-size: 50px" type="submit" name="read" value=1>Read</button><button style="font-size: 50px" type="submit" name="light" value=1>Light On</button><button style="font-size: 50px" type="submit" name="light" value=0>Light Off</button><button style="font-size: 50px" type="submit" name="fan" value=1>Fan On</button><button style="font-size: 50px" type="submit" name="fan" value=0>Fan Off</button><br><br><button type="submit" name="auto" value=0>Auto OFF</button><button type="submit" name="auto" value=1>Auto Light Only</button><button type="submit" name="auto" value=2>Auto Fan Only</button><button type="submit" name="auto" value=3>Auto Both</button><br><br><br><button type="submit" name="off" value=1>OFF</button></form><p>'+arduinoData+'</p></body></html>'
  
    ser.flush()


# set up serial with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
ser.write(b"\n")
ser.flush()

# create socket address
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_PORT = 1224  # bind server to port 1224 (I picked a random port)

try:
    mysock.bind(("", TCP_PORT))
except socket.error:
    print("Failed to bind socket")
    sys.exit()

# spin server
time.sleep(5)
readRequest()
mysock.listen(5)
print("Server listening...")
while True:    
    conn, addr = mysock.accept()
    request = conn.recv(1024)
    print("Request: ")
    print(request)
    print("\n")    

    if (request[:12] == b'GET /?light='):
        print("Handling Light...\n")
        if request[12] == b'1'[0]:
            ser.write(b"light on\n")
        else:
            ser.write(b"light off\n")
    elif (request[:10] == b'GET /?fan='):
        print("Handling Fan...\n")
        if request[10] == b'1'[0]:
            ser.write(b"fan on\n")
        else:
            ser.write(b"fan off\n")
    elif (request[:11] == b'GET /?auto='):
        print("Handling Auto...\n")
    elif (request[:10] == b'GET /?off='):  ## hack to shut down server
        print("Handling Off...\n")
        sendHeader(conn)
        conn.sendall('<!DOCTYPE html> <html> <head> <title>Remote Environment Controller</title> <meta charset="ASCII"/> </head> <body> Server shut down </body> </htlm>'.encode())
        break
    else:
        print("Unknown request... skipping...\n")

    print("Sending HTML...\n")
    readRequest()
    sendHeader(conn)       
    conn.sendall(html.encode())
    ser.flush()    


# close connection and socket
ser.close()
conn.close()
mysock.close()
print("Server shut down\n")

# http://192.168.1.177:1224/