import scraperwiki
from bs4 import BeautifulSoup
import re
import json

#from http://stackoverflow.com/posts/92441/revisions
def filter_non_printable(str):
    return ''.join([c for c in str if ord(c) > 31 or ord(c) == 9])

lastID = scraperwiki.sqlite.get_var('last_page')
for id in range(1,578):
    if id > lastID:
        url = "http://www.parliament.qld.gov.au/apps/formermembers/memberBio1.aspx?m_id="+str(id)
        print url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        if soup.find(id="ctl00_cpContent_lblName") != None:
            data = {'id': id}
            data['name'] = soup.find(id="ctl00_cpContent_lblName").get_text().strip()
            fieldName = ""
            for spantag in soup.td.find_all('span'):
                if 'class' in spantag.attrs:
                    #print spantag['class']
                    if "h3" in spantag['class'] or "h2" in spantag['class']:
                        fieldName = spantag.get_text()
                        if fieldName == "Parliamentary Representation" or fieldName == "Appointments":
                            #print fieldName
                            tableHeaders = []
                            for thtag in spantag.next_sibling.next_sibling.find_all('th'): 
                                  tableHeaders.append(thtag.get_text().strip())
                            #print tableHeaders   
                            tableDataRows = []
                            for trtag in spantag.next_sibling.next_sibling.find_all('tr'): 
                                tableFields = []
                                for tdtag in trtag.find_all('td'): 
                                    tableFields.append(tdtag.get_text().strip())
                                if 'class' not in trtag.attrs:
                                    tableDataRows.append(zip(tableHeaders,tableFields))
                            #print tableDataRows
                            data[fieldName] = json.dumps(tableDataRows)        
                        
                    if "normal" in spantag['class']:
                        #print fieldName+" = "+spantag.get_text()
                        text = filter_non_printable(spantag.get_text().strip()).replace(u"\u00a0"," ")
                        #print text
                        if text.startswith("1."):
                            values = filter(None, re.split('[0-9]\. ',text))
                            #print values
                            data[fieldName] = json.dumps(values)
                        else:
                            data[fieldName] = text
                #print spantag
            #print data
            print "Saved record #"+str(id)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        else:
            print "Skipped empty record #"+str(id)
    scraperwiki.sqlite.save_var('last_page', id)

lastID = 0import scraperwiki
from bs4 import BeautifulSoup
import re
import json

#from http://stackoverflow.com/posts/92441/revisions
def filter_non_printable(str):
    return ''.join([c for c in str if ord(c) > 31 or ord(c) == 9])

lastID = scraperwiki.sqlite.get_var('last_page')
for id in range(1,578):
    if id > lastID:
        url = "http://www.parliament.qld.gov.au/apps/formermembers/memberBio1.aspx?m_id="+str(id)
        print url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        if soup.find(id="ctl00_cpContent_lblName") != None:
            data = {'id': id}
            data['name'] = soup.find(id="ctl00_cpContent_lblName").get_text().strip()
            fieldName = ""
            for spantag in soup.td.find_all('span'):
                if 'class' in spantag.attrs:
                    #print spantag['class']
                    if "h3" in spantag['class'] or "h2" in spantag['class']:
                        fieldName = spantag.get_text()
                        if fieldName == "Parliamentary Representation" or fieldName == "Appointments":
                            #print fieldName
                            tableHeaders = []
                            for thtag in spantag.next_sibling.next_sibling.find_all('th'): 
                                  tableHeaders.append(thtag.get_text().strip())
                            #print tableHeaders   
                            tableDataRows = []
                            for trtag in spantag.next_sibling.next_sibling.find_all('tr'): 
                                tableFields = []
                                for tdtag in trtag.find_all('td'): 
                                    tableFields.append(tdtag.get_text().strip())
                                if 'class' not in trtag.attrs:
                                    tableDataRows.append(zip(tableHeaders,tableFields))
                            #print tableDataRows
                            data[fieldName] = json.dumps(tableDataRows)        
                        
                    if "normal" in spantag['class']:
                        #print fieldName+" = "+spantag.get_text()
                        text = filter_non_printable(spantag.get_text().strip()).replace(u"\u00a0"," ")
                        #print text
                        if text.startswith("1."):
                            values = filter(None, re.split('[0-9]\. ',text))
                            #print values
                            data[fieldName] = json.dumps(values)
                        else:
                            data[fieldName] = text
                #print spantag
            #print data
            print "Saved record #"+str(id)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        else:
            print "Skipped empty record #"+str(id)
    scraperwiki.sqlite.save_var('last_page', id)

lastID = 0