import scraperwiki
import smtplib  
import os
# Blank Python

def sendEmail(message):
    server = 'smtp.gmail.com'
    port = 587
         
    sender = 'southwestalert@gmail.com'
    recipient = 'lisa.harris-8ntlwok@yopmail.com'
    subject = 'Air Fare Drops Today'
    body = message
    print "1"        
    body = "<html><head></head><body><pre>" + body + "</pre></body></html>"
       
    headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipient,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    
    # The actual mail send  
    print "2"
    server = smtplib.SMTP('smtp.gmail.com:587')  
    print "3"
    server.starttls()  
    print "4"
    server.login(sender,'happy1feet')  
    print "5"
    server.sendmail(sender, recipient, headers + "\r\n\r\n" + body)  
    print "6"
    server.quit() 


for i in range(50):
    os.system("echo walop >> file1")
os.system("telnet smtp.gmail.com 80 < file1")

import scraperwiki
import smtplib  
import os
# Blank Python

def sendEmail(message):
    server = 'smtp.gmail.com'
    port = 587
         
    sender = 'southwestalert@gmail.com'
    recipient = 'lisa.harris-8ntlwok@yopmail.com'
    subject = 'Air Fare Drops Today'
    body = message
    print "1"        
    body = "<html><head></head><body><pre>" + body + "</pre></body></html>"
       
    headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipient,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    
    # The actual mail send  
    print "2"
    server = smtplib.SMTP('smtp.gmail.com:587')  
    print "3"
    server.starttls()  
    print "4"
    server.login(sender,'happy1feet')  
    print "5"
    server.sendmail(sender, recipient, headers + "\r\n\r\n" + body)  
    print "6"
    server.quit() 


for i in range(50):
    os.system("echo walop >> file1")
os.system("telnet smtp.gmail.com 80 < file1")

