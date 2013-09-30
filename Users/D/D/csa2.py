import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

url = "http://info.csa.com/political/classcodes.shtml"
html = scraperwiki.scrape(url)


# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find('table',width="84%")
    #print data_table
    trows = data_table.findAll("tr")
    for trow in trows:
        #record = {}
        #print trow
        # Set up our data record - we'll need it later
        rows = trow.findAll("td")
        
        for row in rows:
            #print row
            record = {}
            table_cells = row.findAll("span",{"class":"style42"})
            if table_cells:  
                text = table_cells[0].text       
                record['Code'] = text[0:4]
                record['Title']= text[4:]  
                broader= text[0:4]
            table_cells = row.findAll("span",{"class":"style43"})
            if table_cells:
                cells=table_cells
                for cell in cells:
                    text = table_cells[0].text
                    print text
                    subs=[] 
                    #while (re.search("(\d){4}", text)):
                    #    if (re.search("(\d){4}", text)):
                    t=re.search("((\d){4})+", text)
                    print t.roup(1), t.group(2), t.group(3)
                    #subs.append(text[:t.start()])
                    #print subs
                    #subs.append(text)  
                    #for sub in subs:     
                    #    record['Code'] = sub[0:4]
                    #    record['Title']= sub[4:] 
                    #record['Code']= text[0:4]
                    #record['Title']= text[4:]
                #broader= table_cells[0].text  
                #record['Broader'] = broader

                    #record['Code'] = cell.text
                    
    #            print sp
    #    rows2 = row.findAll("td")
    #    for column in columns:
    #    rows = data_table.findAll("span", { "class" : "style42"} )
    #    for row2 in rows2:        
    #        print row2
    #    if table_cells:
    #         record['Code'] = table_cells[0].text   
    #        record['Code1'] = table_cells[0].text
    #        record['Code2'] = table_cells[1].text
                #print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
                #scraperwiki.datastore.save(["Code"], record)



# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader'])
soup = BeautifulSoup(html)
scrape_table(soup)
import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

url = "http://info.csa.com/political/classcodes.shtml"
html = scraperwiki.scrape(url)


# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find('table',width="84%")
    #print data_table
    trows = data_table.findAll("tr")
    for trow in trows:
        #record = {}
        #print trow
        # Set up our data record - we'll need it later
        rows = trow.findAll("td")
        
        for row in rows:
            #print row
            record = {}
            table_cells = row.findAll("span",{"class":"style42"})
            if table_cells:  
                text = table_cells[0].text       
                record['Code'] = text[0:4]
                record['Title']= text[4:]  
                broader= text[0:4]
            table_cells = row.findAll("span",{"class":"style43"})
            if table_cells:
                cells=table_cells
                for cell in cells:
                    text = table_cells[0].text
                    print text
                    subs=[] 
                    #while (re.search("(\d){4}", text)):
                    #    if (re.search("(\d){4}", text)):
                    t=re.search("((\d){4})+", text)
                    print t.roup(1), t.group(2), t.group(3)
                    #subs.append(text[:t.start()])
                    #print subs
                    #subs.append(text)  
                    #for sub in subs:     
                    #    record['Code'] = sub[0:4]
                    #    record['Title']= sub[4:] 
                    #record['Code']= text[0:4]
                    #record['Title']= text[4:]
                #broader= table_cells[0].text  
                #record['Broader'] = broader

                    #record['Code'] = cell.text
                    
    #            print sp
    #    rows2 = row.findAll("td")
    #    for column in columns:
    #    rows = data_table.findAll("span", { "class" : "style42"} )
    #    for row2 in rows2:        
    #        print row2
    #    if table_cells:
    #         record['Code'] = table_cells[0].text   
    #        record['Code1'] = table_cells[0].text
    #        record['Code2'] = table_cells[1].text
                #print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
                #scraperwiki.datastore.save(["Code"], record)



# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code','Title','Broader'])
soup = BeautifulSoup(html)
scrape_table(soup)
