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
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader','BroaderTransitive','Related'])
  
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
        broader=rows[0].find("td").text
#        if (broader=rows[1].find("td").text):
#            broader=rows[0].find("td").text
#        print broader
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if(table_cells[1].find("a")):
                url=table_cells[1].find("a").get('href')
            elif(table_cells[0].find("a")):
                url=table_cells[0].find("a").get('href')
            flag=0
            for x in urls:
                if (url == x):
                    flag=1
                    break
            if (flag==0):
                urls.append(url)
            title=table_cells[3].text
            if (re.search("See also", title)):
                t= re.search("\[See also", title)
                ts=title[:t.start()]
                title=ts 
                tehref=table_cells[3].findAll("a")
                print len(tehref)
                i=0
                res={}
                for teh in tehref:
                    if(i==0):
                        res=teh.text
                    else:
                        res.insert(teh.text,i)
                # relatedtos={}
                # for i in range(1,len(tehref)):
                #    teh=tehref[i-1].get('href')
                #    print tehref[i-1].text
                #    record['Related']=tehref[i-1].text
                    record['Related']=res
            #print t.group(3)
            if (table_cells[2].text):
                c = table_cells[2].text
                code=c[0:5]  
                b=rows[1].findAll("td")
                br=b[1].text
                if(br):
                    broader=br

                    broaderTransitive=rows[0].find("td").text
                    print "1.", code, "2.", title, "3.", broader, "4.", broaderTransitive 
                    record['BroaderTransitive'] = broaderTransitive
                else:
                    broader=rows[0].find("td").text
                    print "1.", code, "2.", title, "3.", broader,                          
            elif (table_cells[1].text):
                c = table_cells[1].text
                code=c[0:5]
                broader=rows[0].find("td").text
                print code, title, broader
            elif (table_cells[0].text):
                c = table_cells[0].text
                code=c[0:5]
            record['Code'] = code
            record['Title'] = title
            record['Broader'] = broader
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
#for  i  in range [00, 01, 03, 05, 06, 08, 11, 12, 13, 14, 15, 16, 17, 18,  19,  20, 22, 26, 28, 31, 32, 33, 34, 35, 37, 39, 40, 41, 42, 43, 44, 45,  46,  47, 49, 51, #52, 53, 54, 55, 57, 58, 60, 62, 65, 68, 70, 74, 76,  78,  80, 81, 82, 83, 84, 85, 86, 90, 91, 92, 93, 94]  
starting_url = "msc2010.html?t="+"00-XX&s=&btn=Search&ls=s"
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
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader','BroaderTransitive','Related'])
  
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
        broader=rows[0].find("td").text
#        if (broader=rows[1].find("td").text):
#            broader=rows[0].find("td").text
#        print broader
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("td")
            if(table_cells[1].find("a")):
                url=table_cells[1].find("a").get('href')
            elif(table_cells[0].find("a")):
                url=table_cells[0].find("a").get('href')
            flag=0
            for x in urls:
                if (url == x):
                    flag=1
                    break
            if (flag==0):
                urls.append(url)
            title=table_cells[3].text
            if (re.search("See also", title)):
                t= re.search("\[See also", title)
                ts=title[:t.start()]
                title=ts 
                tehref=table_cells[3].findAll("a")
                print len(tehref)
                i=0
                res={}
                for teh in tehref:
                    if(i==0):
                        res=teh.text
                    else:
                        res.insert(teh.text,i)
                # relatedtos={}
                # for i in range(1,len(tehref)):
                #    teh=tehref[i-1].get('href')
                #    print tehref[i-1].text
                #    record['Related']=tehref[i-1].text
                    record['Related']=res
            #print t.group(3)
            if (table_cells[2].text):
                c = table_cells[2].text
                code=c[0:5]  
                b=rows[1].findAll("td")
                br=b[1].text
                if(br):
                    broader=br

                    broaderTransitive=rows[0].find("td").text
                    print "1.", code, "2.", title, "3.", broader, "4.", broaderTransitive 
                    record['BroaderTransitive'] = broaderTransitive
                else:
                    broader=rows[0].find("td").text
                    print "1.", code, "2.", title, "3.", broader,                          
            elif (table_cells[1].text):
                c = table_cells[1].text
                code=c[0:5]
                broader=rows[0].find("td").text
                print code, title, broader
            elif (table_cells[0].text):
                c = table_cells[0].text
                code=c[0:5]
            record['Code'] = code
            record['Title'] = title
            record['Broader'] = broader
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
#for  i  in range [00, 01, 03, 05, 06, 08, 11, 12, 13, 14, 15, 16, 17, 18,  19,  20, 22, 26, 28, 31, 32, 33, 34, 35, 37, 39, 40, 41, 42, 43, 44, 45,  46,  47, 49, 51, #52, 53, 54, 55, 57, 58, 60, 62, 65, 68, 70, 74, 76,  78,  80, 81, 82, 83, 84, 85, 86, 90, 91, 92, 93, 94]  
starting_url = "msc2010.html?t="+"00-XX&s=&btn=Search&ls=s"
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

