import scraperwiki
import urlparse
import lxml.html
import urllib

def scrape_table(root):
    rows = root.cssselect("h2") 
    counter=0
    for row in rows:
        table_cells = row.cssselect("h2 a")
        for cell in table_cells:
            table_cellsurls = table_cells[0].cssselect("a")
            #record['CaseURL'] = table_cellsurls[0].attrib.get('href')
            caselinkurl = urllib.urlopen('http://www.italaw.com/'+table_cellsurls[0].attrib.get('href')).read()
            #print caselinkurl
            caseroots = lxml.html.fromstring(caselinkurl)
            pars = caseroots.cssselect("span.'case-doc-details' a")
            #print "pars length is", len(pars)
            record = {}
            #create another table element with rows, marked off with the case that they came from, create all the rows.
            if  len(pars)==0:
                record['DetailsURL']="None"
                record['Count']=counter
                print record, '------------'
                scraperwiki.sqlite.save(['Count'],record)
                counter+=1
            else: 
                for i in range(0,len(pars)):                       
                    record['Count']=counter
                    caselinkurl2=urllib.urlopen('http://www.italaw.com/'+pars[i].attrib.get('href')).read()
                    caseroots2=lxml.html.fromstring(caselinkurl2)
                    record['DetailsURL']=pars[i].attrib.get('href') 
                    title=caseroots2.cssselect("h2")
                    record['Title'] = title[1].text_content()
                    rules=caseroots2.cssselect("div.'field-name-field-arbitration-rules'")
                    if len(rules)==0:
                        record['Rules']="None"
                    else:
                        record['Rules']=rules[0].text_content()
                    treaty=caseroots2.cssselect("div.'field-name-field-case-treaties'")
                    if len(treaty)==0:
                        record['Treaty']="None"                                    
                    else:
                        record['Treaty']=treaty[0].text_content()
                    pars2=caseroots2.cssselect("div.'field-name-field-case-document-date'")
                    if len(pars2)==0:
                        record['Doc Date']="None"
                    else:                        
                        record['Doc Date']=pars2[0].text_content()
                    pars3=caseroots2.cssselect("div.'field-name-field-case-doc-file' span.'file' a")
                    if len(pars3) ==0:
                        record['Doc Type Link']="None"
                        record['Doc Type']="None"  
                    else:
                        record['Doc Type Link']=pars3[0].attrib.get('href')
                        record['Doc Type']=pars3[0].text_content() 
                    pars4=caseroots2.cssselect("div.'field-name-field-arbitrator-claimant'")
                    if len(pars4)==0:
                        record['Claimant Nominee']="None"
                    else:
                        record['Claimant Nominee']=pars4[0].text_content()
                    pars5=caseroots2.cssselect("div.'field-name-field-arbitrator-respondent'")
                    if len(pars5)==0:
                        record['Respondent Nominee']="None"
                    else:
                        record['Respondent Nominee']=pars5[0].text_content() 
                    pars6=caseroots2.cssselect("div.'field-name-field-arbitrator-chair'")
                    if len(pars6)==0:
                        record['President']="None"
                    else:
                        record['President']=pars6[0].text_content() 

                    print record, '------------'
                    scraperwiki.sqlite.save(['Count'],record)
                    counter+=1
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)


#START HERE:
url = 'http://www.italaw.com/cases-by-respondent?field_case_respondent_tid=All'
scrape_and_look_for_next_link(url)