from urllib import urlopen
from BeautifulSoup import BeautifulSoup 
import re
import scraperwiki

#open and read webpage
webpage = urlopen("http://jobs.experian.com/sitemap.xml").read()

#locate xml link, modification date, and priority
link = re.compile('<loc>(.*)</loc>')
mod = re.compile('<lastmod>(.*)</lastmod>')
priority = re.compile('<priority>(.*)</priority>')

#search for xml link, modification date, and priority
findlink = re.findall(link, webpage)
findmod = re.findall(mod, webpage)
findpriority = re.findall(priority, webpage)

#determine what range to grab
listiterator = []
listiterator[:] = range(0,100)

#print results
for i in listiterator:
#    print findlink[i]
 #   print findmod[i]
  #  print findpriority[i]

    #explore job descr page
    reqpage = urlopen(findlink[i]).read()
    soup2 = BeautifulSoup(reqpage)

    #find job descr details
    body = soup2.find(id="jobDesc")
    title = soup2.body.find(itemprop="title").string
    bodytext = soup2.body.findAll("span", { "class" : "text" })
    category = bodytext[2].string
    location = bodytext[3].string
    postdate = bodytext[4].string
    jobtyperaw = soup2.body.findAll("span", { "class" : "jobtype" })
    reqid = soup2.body.findAll("span", { "class" : "info" })[1:2]

    print reqid

#    for row in reqid:
#        text = ''.join(row.findAll(text=True))
#        data1 = text.strip()
#        print data
    
    #print results
#    print title
 #   print category 
  #  print location 
   # print postdate
 

    """
    convert jobtyperaw from row to text via 
    http://stackoverflow.com/questions/992183/why-am-i-getting-resultset-has-no-attribute-findall-using-beautifulsoup-in
    """

#    for row in jobtyperaw:
#        text = ''.join(row.findAll(text=True))
#        data2 = text.strip()
#      print data
    
#    print "\n"

    #Save data to ScraperWiki database, saving unique title and URL
#    scraperwiki.sqlite.save(["Req Number", "Location"], data = {"Title": title, "Req Number": data1, "Work Hours": data2, "URL": findlink[i], "Published": findmod[i], "Priority": findpriority[i], "Category": category, "Location": location, "Post Date": postdate})  

    from urllib import urlopen
from BeautifulSoup import BeautifulSoup 
import re
import scraperwiki

#open and read webpage
webpage = urlopen("http://jobs.experian.com/sitemap.xml").read()

#locate xml link, modification date, and priority
link = re.compile('<loc>(.*)</loc>')
mod = re.compile('<lastmod>(.*)</lastmod>')
priority = re.compile('<priority>(.*)</priority>')

#search for xml link, modification date, and priority
findlink = re.findall(link, webpage)
findmod = re.findall(mod, webpage)
findpriority = re.findall(priority, webpage)

#determine what range to grab
listiterator = []
listiterator[:] = range(0,100)

#print results
for i in listiterator:
#    print findlink[i]
 #   print findmod[i]
  #  print findpriority[i]

    #explore job descr page
    reqpage = urlopen(findlink[i]).read()
    soup2 = BeautifulSoup(reqpage)

    #find job descr details
    body = soup2.find(id="jobDesc")
    title = soup2.body.find(itemprop="title").string
    bodytext = soup2.body.findAll("span", { "class" : "text" })
    category = bodytext[2].string
    location = bodytext[3].string
    postdate = bodytext[4].string
    jobtyperaw = soup2.body.findAll("span", { "class" : "jobtype" })
    reqid = soup2.body.findAll("span", { "class" : "info" })[1:2]

    print reqid

#    for row in reqid:
#        text = ''.join(row.findAll(text=True))
#        data1 = text.strip()
#        print data
    
    #print results
#    print title
 #   print category 
  #  print location 
   # print postdate
 

    """
    convert jobtyperaw from row to text via 
    http://stackoverflow.com/questions/992183/why-am-i-getting-resultset-has-no-attribute-findall-using-beautifulsoup-in
    """

#    for row in jobtyperaw:
#        text = ''.join(row.findAll(text=True))
#        data2 = text.strip()
#      print data
    
#    print "\n"

    #Save data to ScraperWiki database, saving unique title and URL
#    scraperwiki.sqlite.save(["Req Number", "Location"], data = {"Title": title, "Req Number": data1, "Work Hours": data2, "URL": findlink[i], "Published": findmod[i], "Priority": findpriority[i], "Category": category, "Location": location, "Post Date": postdate})  

    