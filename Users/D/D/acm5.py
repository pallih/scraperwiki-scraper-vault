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
    if(soup.find("div", { "class" : "bump" })):
        data_table = soup.find("div", { "class" : "bump" })
        rows = data_table.findAll("div", { "class" : "small-text" })
        for row in rows:
            # Set up our data record - we'll need it later
            record = {}
            table_cells = row.findAll("a")
            if table_cells:
                url = table_cells[0].get('href')
                if ( not re.search("&query", url)):
                    flag=0
                    for x in urls:
                        if (url == x):
                            flag=1
                            break
                    if (flag==0):
                        urls.append(url)
                #m = re.search((".\d.\d|.\d|.")+" ", t)
                #m = re.search((".\d?")+" ", t)
                t = table_cells[0].text
                #m = re.search(("(\w)(.\d){1,2}?")+" ", t)
                if (re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)):
                    if(re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)):
                        u = re.search("(row=)(\w)(.\d)(.)(\d|\w)&", url)
                        code=u.group(2)+u.group(3)+u.group(4)+u.group(5)
                        ur = u.group(2)+u.group(3)
                        m = re.search("(\w)(.\d)(.)(\d|\w)"+" ",t)
                        title=t[m.end():]
                    elif (re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)):
                        u = re.search("(idx2=)(\w)(.\d)(.)(\d|\w){1,2}(&)(idx3=)(\d)", url)
                        code=u.group(2)+u.group(3)+u.group(4)+u.group(5)+"."+u.group(7)+u.group(8)
                        ur=u.group(2)+u.group(3)+u.group(4)+u.group(5)
                        title=t
                    else:
                        break                
                elif (re.search("(row=)(\w)(.)(\d|\w)&", url)):
                    u = re.search("(row=)(\w)(.)(\d|\w)&", url)
                    code=u.group(2)+u.group(3)+u.group(4)
                    ur = u.group(2)
                #if(re.search("\w.(\d|\w)"+" ",t)):
                #    m = re.search("\w.(\d|\w)"+" ",t)
                #    title=t[m.end():]
                #else:
                #    title=t
                    if(re.search("\w.(\d|\w)"+" ",t)):
                        m = re.search("\w.(\d|\w)"+" ",t)
                        title=t[m.end():]
                    elif(re.search("&idx2=",url)):
                        title=t
                    else:
                        title=t
                elif (re.search("(row=)(\w).&", url)):
                    u = re.search("(row=)(\w).&", url)
                    code=u.group(2)
                    ur = ""
                    if(re.search("\w.(\d|\w)?"+" ",t)):
                        m = re.search("\w."+" ",t)
                        title=t[m.end():]
                    else:
                        m = re.search("\w.(\d|\w){1}"+" ",t)
                        title=t
                else:
                    break
            #    u = re.search("(row=)(\w)(.\d)&idx", url)
            #    code=u.group(2)+u.group(3)
            #    ur = u.group(2)+u.group(3)
            #    title=t
            
            #if(m):
            #code=m.group(0)
            #    title=t[m.end():]
            #else:
            #    title=t
                record['Code'] = code
                record['Title'] = title
                record['Broader'] = ur
            #scrape_and_look_for_next_link(next_url)
            # Print out the data we've gathered
                print record, '------------'
                scraperwiki.datastore.save(["Code"], record)

        #print urls

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
#    next_link = soup.find("a")
#    if next_link:
#        next_url = base_url + next_link['href']
#        scrape_and_look_for_next_link(next_url)
  
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://portal.acm.org/'
starting_url = 'ccs.cfm?part=author&coll=portal&dl=GUIDE'
#starting_url = 'ccs.cfm?part=author&coll=DL&dl=ACM&row=B.&idx=2&CFID=113243268&CFTOKEN=99158879'
urls = [starting_url]
next_url()

