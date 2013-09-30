###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
  
import scraperwiki
import re

from BeautifulSoup import BeautifulSoup
  
urls = {}
  
  
# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader'])
  
#defines the next url to be passed
def next_url():
    for url in urls:
        next_url = base_url + url
        print next_url
        scrape_and_look_for_next_link(next_url)
          

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    if(soup.find("table", { "class" : "results" })):
        data_table = soup.find("table", { "class" : "results" })
        rows = data_table.findAll("tr", { "class" : "current" })
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if(table_cells[1].find("a")):
                url=table_cells[1].find("a").get('href')
            elif(table_cells[0].find("a")):
                url=table_cells[0].find("a").get('href')
            print url
            flag=0
            for x in urls:
                if (url == x):
                    flag=1
                    break
            if (flag==0):
                urls.append(url)
            title=table_cells[3].text
            if (table_cells[2].text):
                c = table_cells[2].text
                code=c[0:5]                                  
            elif (table_cells[1].text):
                c = table_cells[1].text
                code=c[0:5]
            elif (table_cells[0].text):
                c = table_cells[0].text
                code=c[0:5]
            record['Code'] = code
            record['Title'] = title
#           record['Broader'] = ur
            print record, '------------'
            scraperwiki.datastore.save(["Code"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)

  
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.ams.org/mathscinet/msc/'
starting_url = 'msc2010.html?t=00-XX&s=&btn=Search&ls=s'
urls = [starting_url]
next_url()







#                        t = table_cells[0].text
#                        if (re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)):
#                           if(re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)):
#                              u = re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)
#                              code=u.group(2)+u.group(3)+u.group(4)+u.group(5)
#                              ur = u.group(2)+u.group(3)
#                              m = re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)
#                              title=t[m.end():]
#                           elif (re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)):
#                              u = re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)
#                              code=u.group(2)+u.group(3)+u.group(4)+u.group(5)+"."+u.group(7)+u.group(8)
#                              ur=u.group(2)+u.group(3)+u.group(4)+u.group(5)
#                              title=t
#                           else:
#                              break                
#                        elif (re.search("(row=)(\w)(.)(\d|\w)&", url)):
#                           u = re.search("(row=)(\w)(.)(\d|\w)&", url)
#                           code=u.group(2)+u.group(3)+u.group(4)
#                           ur = u.group(2)
#                           if(re.search("\w.(\d|\w)"+" ",t)):
#                               m = re.search("\w.(\d|\w)"+" ",t)
#                               title=t[m.end():]
#                           elif(re.search("&idx2=",url)):
#                               title=t
#                           else:
#                               title=t
#                        elif (re.search("(row=)(\w).&", url)):
#                            u = re.search("(row=)(\w).&", url)
#                            code=u.group(2)
#                            ur = ""
#                            if(re.search("\w.(\d|\w)?"+" ",t)):
#                                m = re.search("\w."+" ",t)
#                                title=t[m.end():]
#                            else:
#                                m = re.search("\w.(\d|\w){1}"+" ",t)
#                                title=t
#                        else:
#                            break 

###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
  
import scraperwiki
import re

from BeautifulSoup import BeautifulSoup
  
urls = {}
  
  
# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader'])
  
#defines the next url to be passed
def next_url():
    for url in urls:
        next_url = base_url + url
        print next_url
        scrape_and_look_for_next_link(next_url)
          

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    if(soup.find("table", { "class" : "results" })):
        data_table = soup.find("table", { "class" : "results" })
        rows = data_table.findAll("tr", { "class" : "current" })
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if(table_cells[1].find("a")):
                url=table_cells[1].find("a").get('href')
            elif(table_cells[0].find("a")):
                url=table_cells[0].find("a").get('href')
            print url
            flag=0
            for x in urls:
                if (url == x):
                    flag=1
                    break
            if (flag==0):
                urls.append(url)
            title=table_cells[3].text
            if (table_cells[2].text):
                c = table_cells[2].text
                code=c[0:5]                                  
            elif (table_cells[1].text):
                c = table_cells[1].text
                code=c[0:5]
            elif (table_cells[0].text):
                c = table_cells[0].text
                code=c[0:5]
            record['Code'] = code
            record['Title'] = title
#           record['Broader'] = ur
            print record, '------------'
            scraperwiki.datastore.save(["Code"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)

  
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.ams.org/mathscinet/msc/'
starting_url = 'msc2010.html?t=00-XX&s=&btn=Search&ls=s'
urls = [starting_url]
next_url()







#                        t = table_cells[0].text
#                        if (re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)):
#                           if(re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)):
#                              u = re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)
#                              code=u.group(2)+u.group(3)+u.group(4)+u.group(5)
#                              ur = u.group(2)+u.group(3)
#                              m = re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)
#                              title=t[m.end():]
#                           elif (re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)):
#                              u = re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)
#                              code=u.group(2)+u.group(3)+u.group(4)+u.group(5)+"."+u.group(7)+u.group(8)
#                              ur=u.group(2)+u.group(3)+u.group(4)+u.group(5)
#                              title=t
#                           else:
#                              break                
#                        elif (re.search("(row=)(\w)(.)(\d|\w)&", url)):
#                           u = re.search("(row=)(\w)(.)(\d|\w)&", url)
#                           code=u.group(2)+u.group(3)+u.group(4)
#                           ur = u.group(2)
#                           if(re.search("\w.(\d|\w)"+" ",t)):
#                               m = re.search("\w.(\d|\w)"+" ",t)
#                               title=t[m.end():]
#                           elif(re.search("&idx2=",url)):
#                               title=t
#                           else:
#                               title=t
#                        elif (re.search("(row=)(\w).&", url)):
#                            u = re.search("(row=)(\w).&", url)
#                            code=u.group(2)
#                            ur = ""
#                            if(re.search("\w.(\d|\w)?"+" ",t)):
#                                m = re.search("\w."+" ",t)
#                                title=t[m.end():]
#                            else:
#                                m = re.search("\w.(\d|\w){1}"+" ",t)
#                                title=t
#                        else:
#                            break 

