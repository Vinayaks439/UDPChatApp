import socket
import threading
import queue
import sys
import random
import argparse

parser = argparse.ArgumentParser(description="Chat App")
parser.add_argument('-s', '--server', type=str, default="127.0.0.1" , help="Please insert the server IP if not inserted it chooses the default as localhost")
parser.add_argument('-p', '--port', type=int, default=2 , help="Please insert your port number if not it will choose 5000")
parser.add_argument('-n', '--numberofclients',type=int,default=2,help="Please insert the no of clients that you want to connect to your server, default is 2")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

host_ip = args.server
port_p = args.port
n = args.numberofclients


def recdatafromclient(serversock,dataGram):
    while True:
        data,addr = serversock.recvfrom(1024)
        dataGram.put((data,addr))



def ServerCode():
    host = host_ip
    port = port_p
    
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    server_socket.bind((host,port))

    clients = set()

    dataGram = queue.Queue()

    threading.Thread(target=recdatafromclient,args=(server_socket,dataGram)).start()

    while True:

        while not dataGram.empty():

            clientsoc_data,clientsoc_addr = dataGram.get()

            if clientsoc_addr not in clients:

                clients.add(clientsoc_addr)

                continue

            clients.add(clientsoc_addr)

            clientsoc_data = clientsoc_data.decode('utf-8')

            print(f" This is from the clients : {str(clientsoc_addr)+clientsoc_data}")

            for x in clients:
                if x!=clientsoc_addr:
                    server_socket.sendto(clientsoc_data.encode('utf-8'),x)
    server_socket.close()

ServerCode()
