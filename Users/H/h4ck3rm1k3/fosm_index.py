import scraperwiki

# Blank Python

import mechanize
#import lxml.html
#from datetime import datetime

def baseuri () : "http://archive.org/details/fosm-20120401130001-" 
def firstitem () : "xaaaa"
def lastitem() : "xachy"
def mkuri (number) : 
    newnumber = number % 26
    newnumber2 = newnumber % 26
    print newnumber
    print newnumber2
# while number < 0 :
#     number % 26

# the first index is what data occurs in what files , so we will get the index first 
#http://archive.org/download/fosm-20120401130001-xaaaa/xaaaa.txt

#http://archive.org/download/fosm-20120401130001-xaapj/xaapj.zip/pine02/index/199501.tbz

import string

def genletters(stop):

   # scraperwiki.sqlite.execute("drop table if exists buckets;")           

    scraperwiki.sqlite.execute("create table if not exists buckets (project int, position int, name string)") 

    scraperwiki.sqlite.execute("create unique index if not exists buckets_pos on buckets(project, position )")       

    scraperwiki.sqlite.execute("create unique index if not exists buckets_name on buckets(project, name )")           
        
    allTheLetters = string.ascii_lowercase
    seen =0
    for letter in allTheLetters:  
        for letter2 in allTheLetters:          
            for letter3 in allTheLetters:                         
                seen = seen + 1
                newstring= "xa%c%c%c" % (letter, letter2, letter3)
              
                if seen % 100 ==0 : 
                    print newstring
                    scraperwiki.sqlite.commit()

                scraperwiki.sqlite.execute("insert or replace into buckets values (1,?,?)", (seen, newstring))
#                print mkuri (10)
                if (newstring == stop) :
                    return
    

def main():
    br = mechanize.Browser()
    print "test"
    
    #print genletters (lastitem())
    genletters ("xachy")
    scraperwiki.sqlite.commit()
    #for i in range(
    #br.open('http://www.indexuniverse.com/data/data.html')
# br.response().read()
#    html = br.submit().read()
#    for i in range(50, n, 50):
#        url = 'http://www.indexuniverse.com/data/data.html?task=showResults&start={}&direction=ASC'.format(i)
#        html = br.open(url).read()

main()
 