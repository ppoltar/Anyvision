#!/usr/bin/env python3
#title           :server.py
#description     :Python program to implement server side of chat room.
#author          :Pasha.P
#date            :8.9.2019
#python_version  :3.6
#==============================================================================
import shutil
import socket,os,datetime,pickle
from _thread import start_new_thread
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_ADDRESS = '127.0.0.1'
PORT = 65432
ACTIVE_CONNECTION = 100
#max size of log file
MAX_LOG_SIZE = 1000000
index_of_log=0
dictionary_of_times = { }
list_of_clients = []

#binds the server to an entered IP address and at the specified port number.
server.bind((IP_ADDRESS, PORT))

#listens for ACTIVE_CONNECTION active connections.
server.listen(ACTIVE_CONNECTION)

""" Function that save the chat to log file, if the log size max than MAX_LOG_SIZE, 
store the file to new file """
def log_file(msg):
    date = str(datetime.datetime.now().strftime("%d/%m/%Y "))
    with open("logger.txt", "a") as log:
        log.writelines(date + msg)
    if os.path.getsize("./logger.txt") > MAX_LOG_SIZE:
        global index_of_log
        index_of_log +=1
        shutil.copy("./logger.txt",str(index_of_log) + "_logger.txt")
        os.remove("./logger.txt")
    pass

#function that remove user if he does not active more than 1 minute
def check_time_to_disconnect():
    server_time = datetime.datetime.now().strftime("%H:%M:%S")
    for k,v in dictionary_of_times.items():
      if str(datetime.datetime.strptime(server_time, "%H:%M:%S") - datetime.datetime.strptime(v, "%H:%M:%S")).split(":")[1] == '01' :
           remove(k)
    pass

sched.add_job(check_time_to_disconnect, 'interval', seconds=1)
sched.start()

def clientthread(conn, addr):
    conn.send(("Welcome to this chatroom!").encode())

    while True:

            try:
                message = conn.recv(2048)
                data = pickle.loads(message)
                dictionary_of_times.update({conn: data[0]})

                if message:
                    #Send the message, name and time of the user who just sent the message
                    message_to_send = data[0] + " " + data[1] + ": "+ data[2]
                    #Log chat to log file
                    log_file(message_to_send)
                    #Calls broadcast function to send message to all
                    broadcast(message_to_send, conn)
                else:
                    #Message may have no content if the connection is broken, in this case we remove the connection
                    remove(conn)
            except:
                 continue
    pass


#Function to broadcast the message to clients who's is not the same as the one sending the message
def broadcast(message, connection):
    print(message)

    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send((message).encode())
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)
    pass

#The following function removes the object from the list of clients
def remove(connection):
    if connection in list_of_clients:
        connection.send((str(datetime.datetime.now().strftime("%H:%M:%S")) + " You are now disconnected, Bye!").encode())
        connection.close()
        list_of_clients.remove(connection)
    pass

while True:

    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()

    #Maintains a list of clients for ease of broadcasting a message
    list_of_clients.append(conn)

    #Prints the address of the user that just connected
    print (str(addr[0]) + "--" + str(addr[1]) + " connected")

    #Creates and individual thread for every user, that connects
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
