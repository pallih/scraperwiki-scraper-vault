import scraperwiki

# Blank Python

import mechanize
#import lxml.html
#from datetime import datetime


def firstitem() : "xaaaa"
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
    scraperwiki.sqlite.execute("create table if not exists bucket_files (project int, position int, block int)") 
    scraperwiki.sqlite.execute("create unique index if not exists bucket_files_pos on bucket_files(project, position, block )")    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    scraperwiki.sqlite.attach("fosm_index", "src")
    data= scraperwiki.sqlite.select("* from src.buckets")       
    for x in data :
      #  print x
     # print x["position"]
     # print x["name"]
        #print baseuri
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
          #/download/fosm-20120401130001-xaaab/xaaab.txt
        uri=  "%s%s/%s.txt" % (baseuri,x["name"],x["name"])
        print uri
        data = br.open(uri).read()
        #data = br.response().read()
        #print data
        darray = data.rsplit("\n")
        #print darray
        for y in darray :
            if y.endswith("_i.tbz"):
                cmd ="insert or replace into bucket_files values (1,?,?)" 
                # print cmd
                # print y[:-6]
                # print x["position"]
                scraperwiki.sqlite.execute(cmd,(x["position"],y[:-6]))
        scraperwiki.sqlite.commit()

def main():
    
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
 import scraperwiki

# Blank Python

import mechanize
#import lxml.html
#from datetime import datetime


def firstitem() : "xaaaa"
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
    scraperwiki.sqlite.execute("create table if not exists bucket_files (project int, position int, block int)") 
    scraperwiki.sqlite.execute("create unique index if not exists bucket_files_pos on bucket_files(project, position, block )")    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    scraperwiki.sqlite.attach("fosm_index", "src")
    data= scraperwiki.sqlite.select("* from src.buckets")       
    for x in data :
      #  print x
     # print x["position"]
     # print x["name"]
        #print baseuri
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
          #/download/fosm-20120401130001-xaaab/xaaab.txt
        uri=  "%s%s/%s.txt" % (baseuri,x["name"],x["name"])
        print uri
        data = br.open(uri).read()
        #data = br.response().read()
        #print data
        darray = data.rsplit("\n")
        #print darray
        for y in darray :
            if y.endswith("_i.tbz"):
                cmd ="insert or replace into bucket_files values (1,?,?)" 
                # print cmd
                # print y[:-6]
                # print x["position"]
                scraperwiki.sqlite.execute(cmd,(x["position"],y[:-6]))
        scraperwiki.sqlite.commit()

def main():
    
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
 