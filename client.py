import socket, select, string, sys
import msvcrt
import platform
def display() :
you=(" You: "+" ")
sys.stdout.write(you)
sys.stdout.flush()
def main():
 if len(sys.argv)<2:
 host = input("Enter Server IP address: ")
 else:
 host = sys.argv[1]
 # host = "127.0.0.1"
 port = 5005
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.settimeout(2)
 
 try :
 s.connect((host, port))
 except :
 print ("Can't connect to the server ")
 sys.exit()
 while 1:
 OS = platform.system()
 if OS == "Windows":
 rList = select.select([s], [], [], 1)[0]
 import msvcrt
 if msvcrt.kbhit(): rList.append(sys.stdin)
 elif OS == "Linux":
 socket_list = [sys.stdin, s]
 rList, wList, error_list = select.select(socket_list , [], [])
 for sock in rList:
 if sock == s:
 data = sock.recv(4096).decode("utf-8")
 if not data :
 print (' \rDISCONNECTED!!\n ')
 sys.exit()
 else :
 sys.stdout.write(data)
 sys.stdout.write("\n") 
 display()
 else :
 msg=sys.stdin.readline()
 s.send(str.encode(msg))
 display()
 
if __name__ == "__main__":
 main()