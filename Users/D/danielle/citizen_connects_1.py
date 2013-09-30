import scraperwiki
import urllib2
import lxml.etree
from lxml.html import tostring, fromstring

# Critically helpful: https://views.scraperwiki.com/run/pdf-to-html-preview-1/

excluded = ["CHAT","DATE","LOCATION","NAME","QUESTIONS FROM CITIZEN CONNECTS ONLINE CHAT","*Last names, middle initials, email addresses and other personal details have been redacted to protect privacy concerns.",""]

def main():
    url="http://governor.ny.gov/citizenconnects/assets/document/CitizenConnectsdoc.pdf"
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)

    rootdata=lxml.etree.fromstring(xmldata)
    pages = list(rootdata)

#    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    for page in pages:
        entries = getText(page)
        store(entries)
    

def getText(page):
    rows=[]
    counter = False
    data = {"official":"", "date":"", "location":"", "name":"", "question":""}
    for node in page.findall("text"):
        text2=node.text
        if not text2.strip() in excluded:  
            left = int(node.attrib["left"].strip())
            if left > 100 and left < 200:
                if len(data['official'].split()) >= 2 and data['official'].lower().strip() != "division of":
                    rows.append(data)
                    data = {"official":"", "date":"", "location":"", "name":"", "question":""}
                data['official'] += text2
            elif left > 200 and left < 300:
                if len(text2.strip()) < 11:
                    data['date'] += text2
                else:
                    data['date'] += text2[:11]
                    data['location'] += text2[11:]
            elif left > 300 and left < 400:
                data['location'] += text2
            elif left > 400 and left < 500:
                data['name'] += text2
            elif left > 500 and left < 700:
                data['question'] += text2
    return rows


def store(entries):
    for row in entries:
        scraperwiki.sqlite.save(unique_keys=[], data=row,table_name='CitizenConnects')


try:
    scraperwiki.sqlite.execute("""
        create table CitizenConnects
        ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


main()
import scraperwiki
import urllib2
import lxml.etree
from lxml.html import tostring, fromstring

# Critically helpful: https://views.scraperwiki.com/run/pdf-to-html-preview-1/

excluded = ["CHAT","DATE","LOCATION","NAME","QUESTIONS FROM CITIZEN CONNECTS ONLINE CHAT","*Last names, middle initials, email addresses and other personal details have been redacted to protect privacy concerns.",""]

def main():
    url="http://governor.ny.gov/citizenconnects/assets/document/CitizenConnectsdoc.pdf"
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)

    rootdata=lxml.etree.fromstring(xmldata)
    pages = list(rootdata)

#    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    for page in pages:
        entries = getText(page)
        store(entries)
    

def getText(page):
    rows=[]
    counter = False
    data = {"official":"", "date":"", "location":"", "name":"", "question":""}
    for node in page.findall("text"):
        text2=node.text
        if not text2.strip() in excluded:  
            left = int(node.attrib["left"].strip())
            if left > 100 and left < 200:
                if len(data['official'].split()) >= 2 and data['official'].lower().strip() != "division of":
                    rows.append(data)
                    data = {"official":"", "date":"", "location":"", "name":"", "question":""}
                data['official'] += text2
            elif left > 200 and left < 300:
                if len(text2.strip()) < 11:
                    data['date'] += text2
                else:
                    data['date'] += text2[:11]
                    data['location'] += text2[11:]
            elif left > 300 and left < 400:
                data['location'] += text2
            elif left > 400 and left < 500:
                data['name'] += text2
            elif left > 500 and left < 700:
                data['question'] += text2
    return rows


def store(entries):
    for row in entries:
        scraperwiki.sqlite.save(unique_keys=[], data=row,table_name='CitizenConnects')


try:
    scraperwiki.sqlite.execute("""
        create table CitizenConnects
        ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


main()
