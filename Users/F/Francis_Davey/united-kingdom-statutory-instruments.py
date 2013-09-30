import scraperwiki
import BeautifulSoup
import re
import urlparse

from scraperwiki import datastore

# At present I am limiting this to a certain number of SI's for testing purposes.
# Fails afters 40/2009

# The relevant pages have changed enormously and so there needs to be a fair amount of rewriting of this.
# the new pages are in a better state, so it may be easier to do.

# I've had to clear the datastore as it didn't migrate.  Hope you don't mind.  JT

#scrape page
#test
year_regexp=re.compile('''<li>\s*<a\s*href="(/si[\w%./-]*)"[^>]*>\s*(\d{4})''', re.I)
ranges_regexp=re.compile('''<li>\|\s*<a\s*href="(/si[\w%./-]*)"''', re.I)
web_version=re.compile('''Web(\s|&nbsp;)*version|Fersiwn\s*i'r\s*we''', re.I)

root='''http://www.legislation.gov.uk/uksi'''
root_html=scraperwiki.scrape(root)

years=year_regexp.findall(root_html)
print "years=%s" % years

def ranges_generator(root, years):
    '''Generates the SI index pages for each numeric range in each year'''

    for (href, year) in years:
        url=urlparse.urljoin(root, href)
        ranges_html=scraperwiki.scrape(url)
        ranges=ranges_regexp.findall(ranges_html)
        print "ranges:", ranges
        for href in ranges:
            pass
            yield (year, href)
                         
def si_generator(root, years):
    #print "si_generator:", root, years
    
    for (year, href) in ranges_generator(root, years):
        #print "inner loop:", year, href
        
        url=urlparse.urljoin(root, href)
        #print "url:", url
        
        si_index_html=scraperwiki.scrape(url)
        #print "si_index_html:", si_index_html[:32]

        si_index=BeautifulSoup.BeautifulSoup(si_index_html)
        #print "si_index:", si_index
                            
        si_table=si_index.findAll('ul', {'class' : 'siList'})[0]
        print "si_table:", si_table

        si_entries=si_table.findAll('li', recursive=False)
        print "si_entries:", si_entries

        for si_entry in si_entries:
            print "si_entry:", si_entry
            si_number_raw=si_entry.findAll('span', {'class' : 'siNumber'})[0].contents[0]
            si_number_search=re.search('(\d+)(?:\s|<br[^>]>)*(?:\(\s*C\.\s*(\d+)|\(\s*W\.\s*(\d+)|\(\s*Cy\.\s*(\d+)|)', si_number_raw).groups() #this is not working
            si_number=si_number_search[0]
            si_commencement=si_number_search[1] or "NA"
            if si_number_search[2]:
                si_national_origin="Wales"
                si_welsh_number=si_number_search[2]
                si_language="English"
            elif si_number_search[3]:
                si_national_origin="Wales"
                si_welsh_number=si_number_search[3]
                si_language="Welsh"
            else:
                si_national_origin="United Kingdom"
                si_welsh_number="NA"
                si_language="English"
                
            #print "si_number", si_number
        
            si_title=si_entry.findAll('span', {'class' : 'siTitle'})[0].contents[0]
            print "si_title:", si_title
        
            print si_entry.findAll(text=web_version)
            #print si_entry.findAll(text=web_version)[0]
            print "parent:", si_entry.findAll(text=web_version)[0].parent
                       
            href=si_entry.findAll(text=web_version)[0].parent['href']
            print "href:", href

            yield(year, si_number, si_title, href, si_national_origin, si_welsh_number, si_language, si_commencement)
                         
i=0
for (year, si_number, si_title, si_href, si_national_origin, si_welsh_number, si_language, si_commencement) in si_generator(root, years):
        i=i+1
        if i>50:
            break
        print "main loop(%s):" % i, year, si_number, si_title, si_href, si_national_origin, si_welsh_number, si_language, si_commencement
    
        si_url=urlparse.urljoin(root, si_href)
        print si_url
    
        si_html=scraperwiki.scrape(si_url)
        print "Scraped url"
        si_page=BeautifulSoup.BeautifulSoup(si_html)
        print "parsed page"
    
        dates=si_page.findAll('div', {'class' : 'LegDate'}) # need to check for different leg dates such as in force and laid
        DD={
            'laid' : '',
            'made' : '',
            'in_force' : '',
            }
        print "dates:", dates
        for ld in dates:
            print "ld:", ld
            if ld.findAll('p', {'class' : 'LegDateTextWide' }):
                continue    # Would be nice to be able to deal with these
            text=ld.findAll('p', {'class' : 'LegDateText'})[0].contents[0]
            value=ld.findAll('p', {'class' : 'LegDateDate'})[0].contents[0]
            print "text=%s, value=%s" %(text, value)
            DD[text]=value
        print "DD:", DD

        data = {
                'year' : year,
                'number' : si_number,
                'title' : si_title,
                'url' : si_url,     
                'national origin': si_national_origin,
                'language' : si_language,
                'welsh number' : si_welsh_number,
                'commencement number' : si_commencement,
                }
        data.update(DD)
        print "data defined:", data
        datastore.save(unique_keys=['year', 'number', 'language'], data=data)
        print "data stored."

import scraperwiki
import BeautifulSoup
import re
import urlparse

from scraperwiki import datastore

# At present I am limiting this to a certain number of SI's for testing purposes.
# Fails afters 40/2009

# The relevant pages have changed enormously and so there needs to be a fair amount of rewriting of this.
# the new pages are in a better state, so it may be easier to do.

# I've had to clear the datastore as it didn't migrate.  Hope you don't mind.  JT

#scrape page
#test
year_regexp=re.compile('''<li>\s*<a\s*href="(/si[\w%./-]*)"[^>]*>\s*(\d{4})''', re.I)
ranges_regexp=re.compile('''<li>\|\s*<a\s*href="(/si[\w%./-]*)"''', re.I)
web_version=re.compile('''Web(\s|&nbsp;)*version|Fersiwn\s*i'r\s*we''', re.I)

root='''http://www.legislation.gov.uk/uksi'''
root_html=scraperwiki.scrape(root)

years=year_regexp.findall(root_html)
print "years=%s" % years

def ranges_generator(root, years):
    '''Generates the SI index pages for each numeric range in each year'''

    for (href, year) in years:
        url=urlparse.urljoin(root, href)
        ranges_html=scraperwiki.scrape(url)
        ranges=ranges_regexp.findall(ranges_html)
        print "ranges:", ranges
        for href in ranges:
            pass
            yield (year, href)
                         
def si_generator(root, years):
    #print "si_generator:", root, years
    
    for (year, href) in ranges_generator(root, years):
        #print "inner loop:", year, href
        
        url=urlparse.urljoin(root, href)
        #print "url:", url
        
        si_index_html=scraperwiki.scrape(url)
        #print "si_index_html:", si_index_html[:32]

        si_index=BeautifulSoup.BeautifulSoup(si_index_html)
        #print "si_index:", si_index
                            
        si_table=si_index.findAll('ul', {'class' : 'siList'})[0]
        print "si_table:", si_table

        si_entries=si_table.findAll('li', recursive=False)
        print "si_entries:", si_entries

        for si_entry in si_entries:
            print "si_entry:", si_entry
            si_number_raw=si_entry.findAll('span', {'class' : 'siNumber'})[0].contents[0]
            si_number_search=re.search('(\d+)(?:\s|<br[^>]>)*(?:\(\s*C\.\s*(\d+)|\(\s*W\.\s*(\d+)|\(\s*Cy\.\s*(\d+)|)', si_number_raw).groups() #this is not working
            si_number=si_number_search[0]
            si_commencement=si_number_search[1] or "NA"
            if si_number_search[2]:
                si_national_origin="Wales"
                si_welsh_number=si_number_search[2]
                si_language="English"
            elif si_number_search[3]:
                si_national_origin="Wales"
                si_welsh_number=si_number_search[3]
                si_language="Welsh"
            else:
                si_national_origin="United Kingdom"
                si_welsh_number="NA"
                si_language="English"
                
            #print "si_number", si_number
        
            si_title=si_entry.findAll('span', {'class' : 'siTitle'})[0].contents[0]
            print "si_title:", si_title
        
            print si_entry.findAll(text=web_version)
            #print si_entry.findAll(text=web_version)[0]
            print "parent:", si_entry.findAll(text=web_version)[0].parent
                       
            href=si_entry.findAll(text=web_version)[0].parent['href']
            print "href:", href

            yield(year, si_number, si_title, href, si_national_origin, si_welsh_number, si_language, si_commencement)
                         
i=0
for (year, si_number, si_title, si_href, si_national_origin, si_welsh_number, si_language, si_commencement) in si_generator(root, years):
        i=i+1
        if i>50:
            break
        print "main loop(%s):" % i, year, si_number, si_title, si_href, si_national_origin, si_welsh_number, si_language, si_commencement
    
        si_url=urlparse.urljoin(root, si_href)
        print si_url
    
        si_html=scraperwiki.scrape(si_url)
        print "Scraped url"
        si_page=BeautifulSoup.BeautifulSoup(si_html)
        print "parsed page"
    
        dates=si_page.findAll('div', {'class' : 'LegDate'}) # need to check for different leg dates such as in force and laid
        DD={
            'laid' : '',
            'made' : '',
            'in_force' : '',
            }
        print "dates:", dates
        for ld in dates:
            print "ld:", ld
            if ld.findAll('p', {'class' : 'LegDateTextWide' }):
                continue    # Would be nice to be able to deal with these
            text=ld.findAll('p', {'class' : 'LegDateText'})[0].contents[0]
            value=ld.findAll('p', {'class' : 'LegDateDate'})[0].contents[0]
            print "text=%s, value=%s" %(text, value)
            DD[text]=value
        print "DD:", DD

        data = {
                'year' : year,
                'number' : si_number,
                'title' : si_title,
                'url' : si_url,     
                'national origin': si_national_origin,
                'language' : si_language,
                'welsh number' : si_welsh_number,
                'commencement number' : si_commencement,
                }
        data.update(DD)
        print "data defined:", data
        datastore.save(unique_keys=['year', 'number', 'language'], data=data)
        print "data stored."

