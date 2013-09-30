import scraperwiki
import urllib
from bs4 import BeautifulSoup
import re


numbers = []
numbersnoasali = 0
test = 0 
count = 0
numberasali = 0
for year in xrange(2002,2013):
    test = test + 1 
    print test
    for month in xrange(1,13):
        #filename = 'wegadinumberkorsou/resultado_' + str(year) + "_" + str(month)
        #help(BeautifulSoup)
        #f= file(filename,"r")
        url = "http://www.joeblack-lottery.com/wn.php??GameTypeID=1" + str("&Month=") + str(month) + str("&Year=") + str(year)+ str("&Submit=Go")
        urlopen = urllib.urlopen(url)
        resultaten = urlopen.read()
        #resultaten = f.read()

        data = BeautifulSoup(resultaten)


        #fw = file("test","a+")



        Tabledata = data.find("td")

        TabledataContents = Tabledata.strings
        #print TabledataContents

        for TabledataContents in TabledataContents:
            if len(TabledataContents) >= 4:
                #prefix = "wegadinumberkorsou/compilatie/result" + str(year) + str(month)
                #fww = file(prefix,"a+")
                #fww.write(TabledataContents)
                #print TabledataContents
                if re.match('\d\d\d\d.',TabledataContents): # I repeated two times I know .... I'm a little lazy 
                    if re.match('\d\d\d\d.',TabledataContents):
                        count = count + 1
                        prefixf = "wegaresult/resultall.txt"
                        #fww = file(prefixf,"a+")
                        #fww.write(TabledataContents[:4])
                        numbers.append(TabledataContents[:4])

                        #print TabledataContents

#collection.update({"awe" : numbers}, numbers, ) this is for my mongo ;)
#print count


for x in ["%04d" % x for x in range(10000)]:
    if x not in numbers:
        numbersnoasali = numbersnoasali + 1 
        #prefixs = "wegaresult/noasali.txt"
        noasali = x
        #fwws = file(prefixs,"a+")
        #fwws.write(x)
        #print x

for x in ["%04d" % x for x in range(10000)]:
    if x in numbers:
        numberasali = numberasali + 1 
        #prefixs = "wegaresult/noasali.txt"
        asali = x
        #fwws = file(prefixs,"a+")
        #fwws.write(x)
        #print x
        kuantu = numbers.count(x)
        #if kuantu >= 1:
        #print "number " + str(x) + str("a sali ") + str(kuantu) + str(" biaha") 

scraperwiki.sqlite.save(unique_keys=["winning"], data={"winning":numbers})

#print "no a sali " + str(numbersnoasali)
#print "a sali " + str(numberasali)
#print "total ku a sali " +  str(count) 
    
#print  numbers.count("3783")

import scraperwiki
import urllib
from bs4 import BeautifulSoup
import re


numbers = []
numbersnoasali = 0
test = 0 
count = 0
numberasali = 0
for year in xrange(2002,2013):
    test = test + 1 
    print test
    for month in xrange(1,13):
        #filename = 'wegadinumberkorsou/resultado_' + str(year) + "_" + str(month)
        #help(BeautifulSoup)
        #f= file(filename,"r")
        url = "http://www.joeblack-lottery.com/wn.php??GameTypeID=1" + str("&Month=") + str(month) + str("&Year=") + str(year)+ str("&Submit=Go")
        urlopen = urllib.urlopen(url)
        resultaten = urlopen.read()
        #resultaten = f.read()

        data = BeautifulSoup(resultaten)


        #fw = file("test","a+")



        Tabledata = data.find("td")

        TabledataContents = Tabledata.strings
        #print TabledataContents

        for TabledataContents in TabledataContents:
            if len(TabledataContents) >= 4:
                #prefix = "wegadinumberkorsou/compilatie/result" + str(year) + str(month)
                #fww = file(prefix,"a+")
                #fww.write(TabledataContents)
                #print TabledataContents
                if re.match('\d\d\d\d.',TabledataContents): # I repeated two times I know .... I'm a little lazy 
                    if re.match('\d\d\d\d.',TabledataContents):
                        count = count + 1
                        prefixf = "wegaresult/resultall.txt"
                        #fww = file(prefixf,"a+")
                        #fww.write(TabledataContents[:4])
                        numbers.append(TabledataContents[:4])

                        #print TabledataContents

#collection.update({"awe" : numbers}, numbers, ) this is for my mongo ;)
#print count


for x in ["%04d" % x for x in range(10000)]:
    if x not in numbers:
        numbersnoasali = numbersnoasali + 1 
        #prefixs = "wegaresult/noasali.txt"
        noasali = x
        #fwws = file(prefixs,"a+")
        #fwws.write(x)
        #print x

for x in ["%04d" % x for x in range(10000)]:
    if x in numbers:
        numberasali = numberasali + 1 
        #prefixs = "wegaresult/noasali.txt"
        asali = x
        #fwws = file(prefixs,"a+")
        #fwws.write(x)
        #print x
        kuantu = numbers.count(x)
        #if kuantu >= 1:
        #print "number " + str(x) + str("a sali ") + str(kuantu) + str(" biaha") 

scraperwiki.sqlite.save(unique_keys=["winning"], data={"winning":numbers})

#print "no a sali " + str(numbersnoasali)
#print "a sali " + str(numberasali)
#print "total ku a sali " +  str(count) 
    
#print  numbers.count("3783")

