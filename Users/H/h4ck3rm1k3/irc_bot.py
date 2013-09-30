import scraperwiki
import sys
import socket
import string
import re

HOST="irc.geo.oftc.net"
PORT=6667
NICK="FOSMCollectorBotSW"
IDENT="FOSMCollectorBotSW"
REALNAME="FOSMCollectorSW"
readbuffer=""

s=socket.socket( )
s.settimeout(120)
print "got socket"
s.connect((HOST, PORT))
print "got connect"
s.send("NICK %s\r\n" % NICK)
print "send nick"

astring = "USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)
s.send(astring)
print "sent user %s" % astring

astring = "JOIN #fosm-changesets\r\n"
s.send(astring)
print "sent join %s" % astring

s.send("PRIVMSG #fosm-changesets : starting up")
prog = re.compile("(.*)(PRIVMSG)(.*)", re.IGNORECASE)

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()
#    print(temp)

    for line in temp:
        print "Read line:%s\n" % line
        result = prog.match(line)

#        line=string.rstrip(line)
#        line2=string.split(line)
        if(result):
            print "go result %s" % result
            print result
            print result.group(0)
            print result.group(1)
            print result.group(2)

            #s.send("PONG %s\r\n" % line[1])
            s.send("PRIVMSG #fosm-changesets :starting up %s\r\n" % line)
        else:
            print "no result for :%s" % line

            
import scraperwiki
import sys
import socket
import string
import re

HOST="irc.geo.oftc.net"
PORT=6667
NICK="FOSMCollectorBotSW"
IDENT="FOSMCollectorBotSW"
REALNAME="FOSMCollectorSW"
readbuffer=""

s=socket.socket( )
s.settimeout(120)
print "got socket"
s.connect((HOST, PORT))
print "got connect"
s.send("NICK %s\r\n" % NICK)
print "send nick"

astring = "USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)
s.send(astring)
print "sent user %s" % astring

astring = "JOIN #fosm-changesets\r\n"
s.send(astring)
print "sent join %s" % astring

s.send("PRIVMSG #fosm-changesets : starting up")
prog = re.compile("(.*)(PRIVMSG)(.*)", re.IGNORECASE)

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()
#    print(temp)

    for line in temp:
        print "Read line:%s\n" % line
        result = prog.match(line)

#        line=string.rstrip(line)
#        line2=string.split(line)
        if(result):
            print "go result %s" % result
            print result
            print result.group(0)
            print result.group(1)
            print result.group(2)

            #s.send("PONG %s\r\n" % line[1])
            s.send("PRIVMSG #fosm-changesets :starting up %s\r\n" % line)
        else:
            print "no result for :%s" % line

            
