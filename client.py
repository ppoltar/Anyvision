#!/usr/bin/env python3
#title           :client.py
#description     :Python program to implement client side of chat room.
#author          :Pasha.P
#date            :8.9.2019
#python_version  :3.6
#==============================================================================
import socket,select
import sys, datetime,pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 2:
	print ("Error, Correct usage: script, Name. Please try again! ")
	exit()

IP_ADSRESS = '127.0.0.1'
PORT = 65432

name = str(sys.argv[1])
client_time = ""
list_to_send = [client_time,name," "]

server.connect((IP_ADSRESS, PORT))

while True:

	# maintains a list of possible input streams
	sockets_list = [sys.stdin, server]

	"""" There are two possible input situations.if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true """

	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print (message.decode("utf-8"))
		else:
			message = sys.stdin.readline()
			list_to_send[2] = message
			list_to_send[0] = datetime.datetime.now().strftime("%H:%M:%S")
			data_string = pickle.dumps(list_to_send)
			server.send(data_string)
			sys.stdout.write(list_to_send[0] + " <You> ")
			sys.stdout.write(message)
			sys.stdout.flush()

server.close()


