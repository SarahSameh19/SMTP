#importing necessary modules 
import smtplib  #for sending emails
from socket import *  #for creating a socket connection
from base64 import * #for encoding email address and password
import ssl #for creating a secure connection
import os # for any operating system-related functionality

YOUR_EMAIL = input("Enter Your Email Address : ")
YOUR_PASSWORD = input("Enter Your Email Password : ")
YOUR_DESTINATION_EMAIL = input("Enter Email Destination : ")
YOUR_SUBJECT_EMAIL = input("Enter Subject : ")
YOUR_BODY_EMAIL = input("Enter Message : ")

msg = '{}. \r\nI love computer networks!'.format(YOUR_BODY_EMAIL)
endmsg = '\r\n.\r\n'

# Chose Google's SMTP server & called it mailserver
mailServer = 'smtp.gmail.com'
mailPort = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM) #socket.AF_INET for IPv4 and socket.SOCK_STREAM for TCP
clientSocket.connect((mailServer, mailPort))

recv = clientSocket.recv(1024).decode()
print (recv)

if recv[:3] != '220':
	print ('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print (recv1)
if recv1[:3] != '250':
	print ('250 reply not received from server.')

#Account Authentication used to solve the error
#to initiate a secure connection
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recv2 = clientSocket.recv(1024)

sslClientSocket = ssl.wrap_socket(clientSocket)

EMAIL_ADDRESS = b64encode(YOUR_EMAIL.encode())
EMAIL_PASSWORD = b64encode(YOUR_PASSWORD.encode())

authorizationcmd = "AUTH LOGIN\r\n"

sslClientSocket.send(authorizationcmd.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)

sslClientSocket.send(EMAIL_ADDRESS + "\r\n".encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)

sslClientSocket.send(EMAIL_PASSWORD + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)
   
	
# Send MAIL FROM command and print server response.
mailfrom = "MAIL FROM: <{}>\r\n".format(YOUR_EMAIL)
sslClientSocket.send(mailfrom.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)
    

# Send RCPT TO command and print server response.
rcptto = "RCPT TO: <{}>\r\n".format(YOUR_DESTINATION_EMAIL)
sslClientSocket.send(rcptto.encode())
recv6 = sslClientSocket.recv(1024)


# Send DATA command and print server response. 
data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)
    

# Send message data.

sslClientSocket.send("Subject: {}\n\n{}".format(YOUR_SUBJECT_EMAIL, msg).encode())


# Message ends with a single period.
sslClientSocket.send(endmsg.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)


# Send QUIT command to terminate the connection and get server response.
quitcommand = 'QUIT\r\n'
sslClientSocket.send(quitcommand.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)

sslClientSocket.close()
print('Was successful!')