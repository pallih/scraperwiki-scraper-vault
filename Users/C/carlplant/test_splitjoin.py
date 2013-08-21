import scraperwiki 
import lxml.html
import re
import csv   
from lxml import etree

#This uses a CSV file from Google Spreadsheets, the CSV has more info but this link
#just uses the GP practice nhs.uk Performance URL's

csv = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Alusfm0UNCawdEpoN3pra0dUbWRfU2N6eFpkeE05WWc&single=true&gid=1&range=G1%3AG9000&output=csv")

#print csv

#This splits the csv into a list
data = csv.splitlines()

#create a loop that selects each url and scrapes each page

for perf_links in data:
    print perf_links
    #info_url = perf_links
    html = scraperwiki.scrape(perf_links)
    id=re.split('\=+',perf_links)[1]
    #print perf_links
    #print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.panel-content div.metric-item")
    #print rows
    for row in rows:
        record = {}  
        cells = row.cssselect("p span")
        record['score']=cells[0].text_content()
        #record['score']=cells[1].text
    rows2 = root.cssselect("div.col.five.clear.profile-info.hospital-info")
    for row2 in rows2:
        cells2 = row2.cssselect("h1")
        record['Name']=cells2[0].text_content()
        cells3 = row2.cssselect("div.panel.panel-nonedit.module.panel-profile-summary.notranslate p")
        record['Address']=cells3[0].text
    #rows3 = root.cssselect("div.metric-item p")
    #for row3 in rows3:
        #cells4 = row3.cssselect("span")
        #record['Score']=cells4[0].text
        #print cells2[0].text
#Using Xpath to find the data via span tag because I was struggling to use cssselect in this case.
#the find(root)[107] finds the 108th span tag etc, it's a bit of a fudge for now       
        find = etree.XPath("//span")
        code= find(root)[107].text_content()
        code2 = find(root)[110].text_content()
        print code

        try:
            scraperwiki.sqlite.execute("""
                create table magic
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT
                )
            """)
        except:
            print "Table probably already exists."
        scraperwiki.sqlite.save(unique_keys=[], data={'percent_Score_org_of_practice':cells[0].text_content(),'name':cells2[0].text_content(),'address':cells3[0].text,'link':perf_links,'id':id,'Opening_hours':code,'Consultation':code2})
   
        



