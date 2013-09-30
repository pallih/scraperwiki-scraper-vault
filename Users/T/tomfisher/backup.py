import scraperwiki
import lxml.html
import re
import unicodedata
import string


a = 0
b = 0
print "Welcome! Script starting now..."



def getschooldata( str ): #this function retrieves data on one particular school passed as a url and then stores it in the SQLite db
    #grab html and initiate lxml object
    html = scraperwiki.scrape(str)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object




    h1s = root.cssselect('h1') 
    for h1 in h1s:
        #print h1.text
        name = h1.text

    listoflis = []      
    for eachli in root.cssselect("ul.cursos_participa li"):
        stringwithacc = eachli.text
        output = unicodedata.normalize('NFD', unicode(stringwithacc)).encode('ascii', 'ignore')
        #print stringwithacc + "  ---------------->  " + output
        #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, output:"yes"})
        #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, "test":"Hi there"})
        out = output.translate(string.maketrans("",""), string.punctuation)
        listoflis.append(out)

    
    
    totallis = len(listoflis)
    #print totallis    

    print "Now working on school: " + name + " which has a total of ", totallis, " curriculums"
    print listoflis

    if totallis == 0: 
        print "There are no lis!"
    elif totallis == 1:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true"})
    elif totallis == 2:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true"})
    elif totallis == 3:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true"})
    elif totallis == 4:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true"})
    elif totallis == 5:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true"})
    elif totallis == 6:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true"})
    elif totallis == 7:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true"})
    elif totallis == 8:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true"})  
    elif totallis == 9:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true"})  
    elif totallis == 10:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true", listoflis[9]:"true"}) 
    elif totallis == 11:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true", listoflis[9]:"true", listoflis[10]:"true"}) 
    else:
        print "Your list is too long!"


    #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"yes", listoflis[1]:"yes", listoflis[2]:"yes"})


    return


scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 1 offset 350")


for link in list:
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    getschooldata(stringlink)

print "Program finished"


import scraperwiki
import lxml.html
import re
import unicodedata
import string


a = 0
b = 0
print "Welcome! Script starting now..."



def getschooldata( str ): #this function retrieves data on one particular school passed as a url and then stores it in the SQLite db
    #grab html and initiate lxml object
    html = scraperwiki.scrape(str)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object




    h1s = root.cssselect('h1') 
    for h1 in h1s:
        #print h1.text
        name = h1.text

    listoflis = []      
    for eachli in root.cssselect("ul.cursos_participa li"):
        stringwithacc = eachli.text
        output = unicodedata.normalize('NFD', unicode(stringwithacc)).encode('ascii', 'ignore')
        #print stringwithacc + "  ---------------->  " + output
        #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, output:"yes"})
        #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, "test":"Hi there"})
        out = output.translate(string.maketrans("",""), string.punctuation)
        listoflis.append(out)

    
    
    totallis = len(listoflis)
    #print totallis    

    print "Now working on school: " + name + " which has a total of ", totallis, " curriculums"
    print listoflis

    if totallis == 0: 
        print "There are no lis!"
    elif totallis == 1:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true"})
    elif totallis == 2:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true"})
    elif totallis == 3:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true"})
    elif totallis == 4:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true"})
    elif totallis == 5:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true"})
    elif totallis == 6:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true"})
    elif totallis == 7:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true"})
    elif totallis == 8:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true"})  
    elif totallis == 9:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true"})  
    elif totallis == 10:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true", listoflis[9]:"true"}) 
    elif totallis == 11:
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"true", listoflis[1]:"true", listoflis[2]:"true", listoflis[3]:"true", listoflis[4]:"true", listoflis[5]:"true", listoflis[6]:"true", listoflis[7]:"true", listoflis[8]:"true", listoflis[9]:"true", listoflis[10]:"true"}) 
    else:
        print "Your list is too long!"


    #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, listoflis[0]:"yes", listoflis[1]:"yes", listoflis[2]:"yes"})


    return


scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 1 offset 350")


for link in list:
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    getschooldata(stringlink)

print "Program finished"


