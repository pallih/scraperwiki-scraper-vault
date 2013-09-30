import scraperwiki
import BeautifulSoup
import urllib2
import string
import re

html = scraperwiki.scrape('http://www.rickwalton.com/curricul/lanimals.htm')
soup = BeautifulSoup.BeautifulSoup(html)

for animal in soup.findAll('td'):
    x = str(animal)
    if x[4]=="w":
        word = str(animal.string) 

        #This uses the regular expression sub, hit run to see the list of new animals
        ioword = re.sub('help','o', (re.sub('o','i', (re.sub('i','help', word)))))
        print ioword

        #This uses the maketrans and translate functions, to run this version uncomment the next 3 lines
        #ioland = string.maketrans("io","oi")
        #ioword = word.translate(ioland)
        #print ioword
        

        #This does the io exchange using the if-elsif statement, to run this version uncomment the next 8 lines
        #ioword = ''
        #for i in word:        
            #if i=='i':
                #i='o'
            #elif i=='o':
                #i='i'
            #ioword = ioword+i
        #print ioword

        
        #scraperwiki.sqlite.save(unique_keys=["Animal"], data = {"Animal":word, "New Animal":ioword})import scraperwiki
import BeautifulSoup
import urllib2
import string
import re

html = scraperwiki.scrape('http://www.rickwalton.com/curricul/lanimals.htm')
soup = BeautifulSoup.BeautifulSoup(html)

for animal in soup.findAll('td'):
    x = str(animal)
    if x[4]=="w":
        word = str(animal.string) 

        #This uses the regular expression sub, hit run to see the list of new animals
        ioword = re.sub('help','o', (re.sub('o','i', (re.sub('i','help', word)))))
        print ioword

        #This uses the maketrans and translate functions, to run this version uncomment the next 3 lines
        #ioland = string.maketrans("io","oi")
        #ioword = word.translate(ioland)
        #print ioword
        

        #This does the io exchange using the if-elsif statement, to run this version uncomment the next 8 lines
        #ioword = ''
        #for i in word:        
            #if i=='i':
                #i='o'
            #elif i=='o':
                #i='i'
            #ioword = ioword+i
        #print ioword

        
        #scraperwiki.sqlite.save(unique_keys=["Animal"], data = {"Animal":word, "New Animal":ioword})