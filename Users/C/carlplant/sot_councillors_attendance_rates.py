import scraperwiki
import lxml.html
from datetime import date 
import re
import urlparse


record = {}
def scrapeAttend(mainLink):
    html2 = scraperwiki.scrape(mainLink)
    root2 = lxml.html.fromstring(html2)
    #print root


    tr = root2.cssselect('table.mgStatsTable') 
    #print tr
    for row in tr:
    
        details = row.cssselect('tr td')[1]
        #print details[1].text
        if details:
            TotalExpect = details[1].text
            PresentAsExpect = details[4].text
            #Percentage = PresentAsExpect*TotalExpect/100
            #print Percentage
            #ApologiesRecieved = details[7].text_content()
            #AbsentIncAplol = details[10].text
            #InAttendance = details[13].text
            print PresentAsExpect

def createUrl(linkSplit):
    #urlmain = 'http://www.moderngov.stoke.gov.uk/mgAttendance.aspx?XXR=0&DR=01%2f04%2f2011-24%2f02%2f2028&ACT=Go&UID='
    mainLink = "http://www.moderngov.stoke.gov.uk/mgAttendance.aspx?XXR=0&DR=01%2f04%2f2011-24%2f02%2f2028&ACT=Go&UID="+linkSplit[1]
    #print mainLink
    scrapeAttend(mainLink)

#start here
html = scraperwiki.scrape("http://www.moderngov.stoke.gov.uk/mgMemberIndex.aspx?FN=ALPHA&VW=LIST&PIC=0")
root = lxml.html.fromstring(html)
cell = root.cssselect('div.mgThumbsList ul li') 
for rows in cell:
    
        nametab = rows.cssselect('a') 
        if nametab:
            record['name'] = nametab[0].text_content()
            name = nametab[0].text_content()
            #print name
            link = nametab[0].attrib.get('href')
            linkSplit = re.split('\=+',link)
            createUrl(linkSplit)
            #print linkSplit[1]
            