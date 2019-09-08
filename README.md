##Project Title
* Chat-server

##Clone
* https://github.com/ppoltar/Anyvision.git

##Technologies
* Python 3.6

##Installation 
* pip3 install sockets
* pip3 install apscheduler

##Usage
* ./server.py
* ./client.py <Name>  (for example: ./client.py Pasha)


##Screenshots
*![alt tag](https://github.com/ppoltar/Anyvision/blob/master/Screenshots/server.png)
*![alt tag](https://github.com/ppoltar/Anyvision/blob/master/Screenshots/client_Pasha.png)
*![alt tag](https://github.com/ppoltar/Anyvision/blob/master/Screenshots/client_Sivan.png)
*![alt tag](https://github.com/ppoltar/Anyvision/blob/master/Screenshots/logger.png)


##Note
* "Allow user to set client name from user input or config file", I have implemented with user input (argv).
* "client or list of clients to distribute a message" - I didn't really understand how the client choose the users he wants to send the message to,
in my code I send to all connected users. If it's important I will change it, I just need to understand what format user choose to whom to send: ip/names...


##Authors
* Pasha Poltarzhicki

 