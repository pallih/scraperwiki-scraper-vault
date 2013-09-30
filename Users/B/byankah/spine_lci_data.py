import scraperwiki

import scraperwiki  
import re
from BeautifulSoup import BeautifulSoup          
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=ECOP3225")
#scraperwiki.sqlite.save_var('SPINE', ['substance','product','quantity','unit'])  


def getInputs(name, url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #scraperwiki.sqlite.save_var('SPINE_'+name, ['substance','quantity','unit'])  
    td = soup.findAll(text="Input");
    for input in td:
        tr = input.parent.parent.parent;
        record = {}
        record["product"] = name
        #if tr.contents[9] != "None"
        record["substance"] = tr.contents[9].text 
        #if tr.contents[11] != "None"
        record["quantity"] = tr.contents[11].text 
        #if tr.contents[14] != "None"
        #record["unit"] = tr.contents[14].text  
        scraperwiki.sqlite.save(["substance"], record)
        scraperwiki.sqlite.execute("insert into SPINE2 values (?,?,?,?)", (record["product"],record["substance"],record["quantity"],''))
        scraperwiki.sqlite.commit() 

try:           
    scraperwiki.sqlite.execute("select * from SPINE2")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINE2 ('product','substance','quantity','unit')")           
rooturl = "http://cpmdatabase.cpm.chalmers.se/Scripts/"         
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/General.asp?QBase=Process")
soup = BeautifulSoup(html)
pages = soup.findAll(attrs={'href' : re.compile("sheet.asp\?ActId=*.")});
last = "Cement production"
lastone = "f"
for p in pages:
    if lastone == "t":
        fullurl = rooturl + p['href']
        results = scraperwiki.sqlite.execute("select product from SPINE2 where product='" + p.parent.parent.contents[3].text + "'")
        if not results['data']:
            getInputs(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))
    if p.parent.parent.contents[3].text == last:
        lastone = "t"import scraperwiki

import scraperwiki  
import re
from BeautifulSoup import BeautifulSoup          
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/sheet.asp?ActId=ECOP3225")
#scraperwiki.sqlite.save_var('SPINE', ['substance','product','quantity','unit'])  


def getInputs(name, url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    #scraperwiki.sqlite.save_var('SPINE_'+name, ['substance','quantity','unit'])  
    td = soup.findAll(text="Input");
    for input in td:
        tr = input.parent.parent.parent;
        record = {}
        record["product"] = name
        #if tr.contents[9] != "None"
        record["substance"] = tr.contents[9].text 
        #if tr.contents[11] != "None"
        record["quantity"] = tr.contents[11].text 
        #if tr.contents[14] != "None"
        #record["unit"] = tr.contents[14].text  
        scraperwiki.sqlite.save(["substance"], record)
        scraperwiki.sqlite.execute("insert into SPINE2 values (?,?,?,?)", (record["product"],record["substance"],record["quantity"],''))
        scraperwiki.sqlite.commit() 

try:           
    scraperwiki.sqlite.execute("select * from SPINE2")
except scraperwiki.sqlite.SqliteError, e:
    scraperwiki.sqlite.execute("create table SPINE2 ('product','substance','quantity','unit')")           
rooturl = "http://cpmdatabase.cpm.chalmers.se/Scripts/"         
html = scraperwiki.scrape("http://cpmdatabase.cpm.chalmers.se/Scripts/General.asp?QBase=Process")
soup = BeautifulSoup(html)
pages = soup.findAll(attrs={'href' : re.compile("sheet.asp\?ActId=*.")});
last = "Cement production"
lastone = "f"
for p in pages:
    if lastone == "t":
        fullurl = rooturl + p['href']
        results = scraperwiki.sqlite.execute("select product from SPINE2 where product='" + p.parent.parent.contents[3].text + "'")
        if not results['data']:
            getInputs(p.parent.parent.contents[3].text,fullurl.replace(" ", "%20"))
    if p.parent.parent.contents[3].text == last:
        lastone = "t"