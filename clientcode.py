import socket
import threading
import sys
import argparse
import os

parser = argparse.ArgumentParser(description="Chat App")
parser.add_argument('-c', '--clientaddr', type=str, default="127.0.0.1" , help="Please insert the server IP that you want to connect to it chooses the default as localhost if none given")
parser.add_argument('-pc', '--port', type=int, default=5001 , help="Please insert your port number if not it will choose 5000")
parser.add_argument('-ps', '--pserver', type=int, default=5000 , help="Please insert the Server port you wish to connect to, default=5000")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

host_ip = args.clientaddr
port_p = args.port
port_server=args.pserver



def recv(socket):
    while True:
        try:
            data,addr = socket.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            return False

def clientcode(server_ip):
    host = host_ip
    port = port_p


    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.bind((host,port))

   
    Username = input('Username : ')

    if Username == '':
        print("please enter Username")
        sys.exit()
       
    
    client_socket.sendto(Username.encode('utf-8'),(host,port_server))

    threading.Thread(target=recv,args=(client_socket,)).start()

    while True:
        data = input(f"{Username} : ")
        
        data = '['+Username+']' + '->'+ data

        client_socket.sendto(data.encode('utf-8'),(host,port_server))

    client_socket.sendto(data.encode('utf-8'),(host,port_server))

    client_socket.close()
    os._exit(1)

clientcode(host_ip)