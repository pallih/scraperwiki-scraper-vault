import scraperwiki
import urllib2
import string
import lxml.etree
import lxml.html
import lxml.cssselect
from bs4 import BeautifulSoup


try:
    scraperwiki.sqlite.execute("create table senate (link string, name string, state string, born string,home intege)") 
    scraperwiki.sqlite.execute("create table horeps (link string, name string, seat string, born string,home integer)") 

except:
    print "Table probably already exists."

pgno=1

#this function grabs the seat/state, name and link data from the index page, and gets from the member bio page birthplace info and inserts them all into the two tables
def oneborn(base):
    html = scraperwiki.scrape(base)
    soup = BeautifulSoup(html)
    #root = lxml.html.fromstring(html)
    #print type(root)
    #s = root.xpath('//*[@id="content"]/div[3]/ul/li[1]/p[1]/a')
    #for p in s:
    #    print p.element.text
    ru = soup.find("ul", class_="search-filter-results search-filter-results-thumbnails")
    stu = ru.find_all("li")  
    for u in stu:
        #print u.p.text,u.a.get('href'),u.dl.dt.text,u.dl.dd.text
        html2 = scraperwiki.scrape("http://www.aph.gov.au"+u.a.get('href'))
        soup2 = BeautifulSoup(html2)
        hot = soup2.find_all('li')
        tim = ''
        for j in hot:
            check = str(j).find('Born')
            if check != -1:
                tim = str(j)
            else:
                pass
            Home = 0
        if 'Victoria' in u.dl.dd.text:
            if 'Vic' in tim:
                Home = 1
        elif 'New South Wales' in u.dl.dd.text:
            if 'NSW' in tim:
                Home = 1
        elif 'Queensland' in u.dl.dd.text:
            if 'Qld' in tim:
                Home = 1
            if 'Queensland' in tim:
                Home = 1
        elif 'Western Australia' in u.dl.dd.text:
            if 'WA' in tim:
                Home = 1
        elif 'Tasmania' in u.dl.dd.text:
            if 'Tas' in tim:
                Home = 1
        elif 'South Australia' in u.dl.dd.text:
            if 'SA' in tim:
                Home = 1
        elif 'Northern Territory' in u.dl.dd.text:
            if 'NT' in tim:
                Home = 1
        elif 'Australian Capital Territory' in u.dl.dd.text:
            if 'ACT' in tim:
                Home = 1
        else:
            print 'No state recorded!'
        if u.dl.dt.text[0:4] == "Sena":
            scraperwiki.sqlite.save(unique_keys=["name"], data={"name":u.p.text, "link":u.a.get('href'),"state":u.dl.dd.text,"born":tim,'home':Home},table_name="senate")
            scraperwiki.sqlite.commit()
        else:
            scraperwiki.sqlite.save(unique_keys=["name"], data={"name":u.p.text, "link":u.a.get('href'),"seat":u.dl.dd.text,"born":tim,'home':Home},table_name="horeps")
            scraperwiki.sqlite.commit()

#this runs the data collection for the three index pages
while pgno <= 3:
    baseurl = ("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=%s&q=&mem=1&sen=1&par=-1&gen=0&ps=100&st=1" % pgno)
    oneborn(baseurl)
    pgno += 1


#this checks whether the member/senator was born in their state
