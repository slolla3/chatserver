import socket
import select
import sys
from _thread import *
import threading
import random
srvr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvr_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = "localhost"
Port = 5005
buffer = 4096
users={}
name =""
srvr_socket.bind((IP_address, Port))
srvr_socket.listen(100)
no_of_clients = []
no_of_clients.append(srvr_socket)
print (" \t\t\t\tSRVR WORKING" )
def set_name(users):
 while True:
 randnum = random.randint(1,102)
 name = "User"+str(randnum)
 if name not in users.values():
 return name
def send_to_all (sock, message):
for socket in no_of_clients:
if socket != srvr_socket and socket != sock :
try :
socket.send(str.encode(message))
except :
# if connection not available
socket.close()
no_of_clients.remove(socket)
def clientthread(sock,addr):
 print(threading.current_thread().name," - Started")
 while True:
 try:
 command = ""
 data1 = sock.recv(buffer).decode("utf-8")
 data=data1[:data1.index("\n")]
 data_list = data.split()
 if (len(data_list) > 0):
 command = data_list[0]
 else:
 continue
 i,p=sock.getpeername()
 if command == "/help":
 msg =" Srvr : "+'''
The Follwoing Commands are supported:
a. /help :
 Syntax: /help
 Description: Gives the list of supported commands.
b. /users :
 Syntax: /users
 Description: Gets the list of users connected on srvr.
c. /dm :
 Syntax: /dm user "mesaage to send"
 Description: Direct Message - Sends the message placed in double quotes to the sepcifed user.
d. /bc :
 Syntax: /bc "message to broad cast"
 Description: Broadcast message - Sends the message placed in double quotes to all users. 
e. /quit :
 Syntax: /quit
 Description: Disconnects from the srvr.
'''
 sock.send(str.encode(msg))
 continue
 elif command == "/users":
 users_dict = users.copy()
 del users_dict[(i,p)]
 sock.send(str.encode(" Srvr : "+','.join(users_dict.values())))
 continue 
 elif command == "/dm":
 user = data_list[1]
 msg = ' '.join(data_list[2:]).strip('"')
 print("ClientList : ",no_of_clients)
 print(users)
 for client in no_of_clients:
 print("client - ",client)
 try:
 addri,addrp = client.getpeername()
 except Exception as e:
 continue
 try:
 if users[(addri,addrp)] == user:
 user_found = True
 client.send(str.encode(users[(i,p)]+" : "+msg))
 break
 except Exception as e:
 print("in dm - ",str(e))
 pass
 if not user_found:
 sock.send(str.encode(" Srvr : "+user+" Not Found \n"))
 elif command == "/bc":
 msg = ' '.join(data_list[1:]).strip('"')
 send_to_all(sock," "+users[(i,p)]+" : "+msg)
 continue 
 elif command == "/quit":
 msg=" Srvr : "+users[(i,p)]+" is Disconnecting. \n"
 send_to_all(sock,msg)
 print ("Client (%s, %s) is offline" % (i,p)," [",users[(i,p)],"]")
 del users[(i,p)]
 no_of_clients.remove(sock)
 sock.close()
 break
 else:
 msg=" Srvr : "+" Unknown Command. use /help to get list of supported commands: "+"\n"
 sock.send(str.encode(msg))
 
 except Exception as e:
 print("exception in here",str(e))
 (i,p)=sock.getpeername()
 send_to_all(sock, " Srvr : "+users[(i,p)]+" has lost the connection. \n")
 print ("Client (%s, %s) is offline (error)" % (i,p)," [",users[(i,p)],"]\n")
 del users[(i,p)]
 no_of_clients.remove(sock)
 sock.close()
 break
 sock.close()
i=1
print("No of active threads at start : ", threading.active_count())
while True:
 
 rList,wList,error_sockets = select.select(no_of_clients,[],[])
 
 for sock in rList:
 if sock == srvr_socket:
 conn, addr = srvr_socket.accept()
 no_of_clients.append(conn)
 name=set_name(users)
 users[addr]=name
 print ("Client (%s, %s) connected" % addr," [",users[addr],"]")
 welcome = " Srvr : "+" Welcome to chat room "+name+" . Enter '/help' to get list of supported commands\n"
 conn.send(str.encode(welcome))
 send_to_all(conn," "+" Srvr : "+name+" joined the conversation \n")
 print("No of active threads before thread function : ", threading.active_count())
 try:
 threading.Thread(name = "client-"+str(i), target=clientthread, args=(conn, addr)).start()
 print("No of active threads after calling thread function : ", threading.active_count())
 i = i+1
 except Exception as e:
 print("Exception in threads : ",str(e))
srvr_socket.close()