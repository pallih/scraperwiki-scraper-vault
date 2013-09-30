import scraperwiki
import re
import random
from BeautifulSoup import BeautifulSoup, Tag

import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

base_url = 'http://de.wikipedia.org'
url_list = 'http://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland'
infile = opener.open(url_list)
html_list = infile.read()

for cities in BeautifulSoup(html_list).findAll('dd'):
    for link in cities.findAll('a'):
        record = {}
        #extract the url from <a> Tag
        url = link.attrs[0][1]
        infile = opener.open(base_url + url)
        html = infile.read()
        #replace HTML-whitespace with a normal one
        html = html.replace("&#160;"," ")
        #remove annotations
        html = re.sub("\[.*\]","",html)
        #insert a comma
        html = html.replace("<br",",<br")
        #pick the infobox for cities
        table = BeautifulSoup(html).find("table", { "summary" : "Infobox Gemeinde in Deutschland" })
        if table != None:
            #yes, we found an infobox
            #write the title in the record
            record["Name"] = BeautifulSoup(html).find("h1", { "id" : "firstHeading" }).text
            #write the url in the record
            record["Url"] = base_url + url
            #find all rows in the infobox
            for row in table.findAll('tr'):
                td = row.findAll("td")
                if td and len(td) == 2 and td[0].text != '':
                    #we found 2 columns in a row
                    #the text of the first column will be the title of the column in the resultset
                    key = td[0].text.replace(":","")
                    #yep data! write it in the record
                    record[key] = td[1].text
            #i heared you have geodata in a <div> Tag
            geo = BeautifulSoup(html).find("span", { "class" : "geo microformat" })
            for span in geo.findAll("span"):
                if span:
                    #latitude, longitude and elevation are attributes of the <span> Tag
                    #and will be use as title of the columns
                    record[span.attrs[0][1]] = span.text
            #store the record in the datastore
            print record
            scraperwiki.sqlite.save(["Url"], record)
        else:
            #sorry, we don't find an infobox
            print 'leider!' + base_url + url

#this is needed because for this cities the wikipedia-template for states was used
#it is similar to the code above with some exeptions
for city in ['Hamburg','Bremen','Berlin']:
    record = {}
    url = 'http://de.wikipedia.org/wiki/'+city
    print url
    infile = opener.open(url)
    html = infile.read()
    html = html.replace("&#160;"," ").replace(":"," ").replace("/"," ")
    html = re.sub("\[.*\]","",html)
    html = html.replace("<br",",<br")
    ok = 0

    #we need marker
    if city == 'Hamburg':
         start = "Sprache"
         stop = "BIP"

    if city == 'Bremen':
         start = "Bundesland"
         stop = "Stadtbürgerschaft"

    if city == 'Berlin':
         start = "Fläche"
         stop = "Arbeitslosenquote"
    
    record["Name"] = city
    record["Url"] = url
    
    for row in BeautifulSoup(html).findAll('tr'):
        td = row.findAll("td")
        if td and len(td) == 2: 
            if str(td).find(start) > 0:
                ok = 1
            if ok == 1 and td[0].text != '':
                key = td[0].text
                record[key] = td[1].text
            if str(td).find(stop) > 0:
                ok = 0        
    
    geo = BeautifulSoup(html).find("span", { "class" : "geo microformat" })
    for span in geo.findAll("span"):
        if span:
            record[span.attrs[0][1]] = span.text
    scraperwiki.sqlite.save(["Url"], record)
import scraperwiki
import re
import random
from BeautifulSoup import BeautifulSoup, Tag

import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

base_url = 'http://de.wikipedia.org'
url_list = 'http://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland'
infile = opener.open(url_list)
html_list = infile.read()

for cities in BeautifulSoup(html_list).findAll('dd'):
    for link in cities.findAll('a'):
        record = {}
        #extract the url from <a> Tag
        url = link.attrs[0][1]
        infile = opener.open(base_url + url)
        html = infile.read()
        #replace HTML-whitespace with a normal one
        html = html.replace("&#160;"," ")
        #remove annotations
        html = re.sub("\[.*\]","",html)
        #insert a comma
        html = html.replace("<br",",<br")
        #pick the infobox for cities
        table = BeautifulSoup(html).find("table", { "summary" : "Infobox Gemeinde in Deutschland" })
        if table != None:
            #yes, we found an infobox
            #write the title in the record
            record["Name"] = BeautifulSoup(html).find("h1", { "id" : "firstHeading" }).text
            #write the url in the record
            record["Url"] = base_url + url
            #find all rows in the infobox
            for row in table.findAll('tr'):
                td = row.findAll("td")
                if td and len(td) == 2 and td[0].text != '':
                    #we found 2 columns in a row
                    #the text of the first column will be the title of the column in the resultset
                    key = td[0].text.replace(":","")
                    #yep data! write it in the record
                    record[key] = td[1].text
            #i heared you have geodata in a <div> Tag
            geo = BeautifulSoup(html).find("span", { "class" : "geo microformat" })
            for span in geo.findAll("span"):
                if span:
                    #latitude, longitude and elevation are attributes of the <span> Tag
                    #and will be use as title of the columns
                    record[span.attrs[0][1]] = span.text
            #store the record in the datastore
            print record
            scraperwiki.sqlite.save(["Url"], record)
        else:
            #sorry, we don't find an infobox
            print 'leider!' + base_url + url

#this is needed because for this cities the wikipedia-template for states was used
#it is similar to the code above with some exeptions
for city in ['Hamburg','Bremen','Berlin']:
    record = {}
    url = 'http://de.wikipedia.org/wiki/'+city
    print url
    infile = opener.open(url)
    html = infile.read()
    html = html.replace("&#160;"," ").replace(":"," ").replace("/"," ")
    html = re.sub("\[.*\]","",html)
    html = html.replace("<br",",<br")
    ok = 0

    #we need marker
    if city == 'Hamburg':
         start = "Sprache"
         stop = "BIP"

    if city == 'Bremen':
         start = "Bundesland"
         stop = "Stadtbürgerschaft"

    if city == 'Berlin':
         start = "Fläche"
         stop = "Arbeitslosenquote"
    
    record["Name"] = city
    record["Url"] = url
    
    for row in BeautifulSoup(html).findAll('tr'):
        td = row.findAll("td")
        if td and len(td) == 2: 
            if str(td).find(start) > 0:
                ok = 1
            if ok == 1 and td[0].text != '':
                key = td[0].text
                record[key] = td[1].text
            if str(td).find(stop) > 0:
                ok = 0        
    
    geo = BeautifulSoup(html).find("span", { "class" : "geo microformat" })
    for span in geo.findAll("span"):
        if span:
            record[span.attrs[0][1]] = span.text
    scraperwiki.sqlite.save(["Url"], record)
