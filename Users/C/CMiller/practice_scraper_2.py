import scraperwiki
import urllib, urlparse
import lxml.html

urlyear = "http://www.education.gov.uk/cgi-bin/schools/performance/group.pl?qtype=LA&superview=pri&view=aat&set=1&sort=&ord=&tab=1&no=318&pg=%d"

def FetchYear(year):
    url = urlyear % year
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='results_pane'] tr"):   
    ldata = [ ]
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'name' : tds[0].text_content(),
            'type' : tds[1].text_content(),
            'Level 4 Eng and Maths 2011' : tds[2].text_content(),
            'Level 4 Eng and Maths 2010' : tds[3].text_content(),
            'Level 4 Eng and Maths 2009' : tds[4].text_content(),      
            'Level 4 Eng and Maths 2008' : tds[5].text_content(),
            'Making progress Eng' : tds[6].text_content(),
            'Making progress Maths' : tds[7].text_content(),
        }      
        ldata.append(data)

        scraperwiki.sqlite.save(['name'], ldata)

for year in range(1, 2):
    FetchYear(year)import scraperwiki
import urllib, urlparse
import lxml.html

urlyear = "http://www.education.gov.uk/cgi-bin/schools/performance/group.pl?qtype=LA&superview=pri&view=aat&set=1&sort=&ord=&tab=1&no=318&pg=%d"

def FetchYear(year):
    url = urlyear % year
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='results_pane'] tr"):   
    ldata = [ ]
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'name' : tds[0].text_content(),
            'type' : tds[1].text_content(),
            'Level 4 Eng and Maths 2011' : tds[2].text_content(),
            'Level 4 Eng and Maths 2010' : tds[3].text_content(),
            'Level 4 Eng and Maths 2009' : tds[4].text_content(),      
            'Level 4 Eng and Maths 2008' : tds[5].text_content(),
            'Making progress Eng' : tds[6].text_content(),
            'Making progress Maths' : tds[7].text_content(),
        }      
        ldata.append(data)

        scraperwiki.sqlite.save(['name'], ldata)

for year in range(1, 2):
    FetchYear(year)