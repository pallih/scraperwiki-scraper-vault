import scraperwiki
from bs4 import BeautifulSoup
import re
import json

#from http://stackoverflow.com/posts/92441/revisions
def filter_non_printable(str):
    return ''.join([c for c in str if ord(c) > 31 or ord(c) == 9])

lastID = scraperwiki.sqlite.get_var('last_page')
for id in range(2,239):
    if id > lastID:
        url = "http://politicalinterests.fairfax.com.au/political_interests/search/result?&&&members%5B%5D="+str(id)+"&term="
        print url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        if soup.find("a","member-link") != None:
            data = {}
            data['name'] = soup.find("a","member-link").get_text().strip()
            #print data['name']
            i = 0;
            for category in soup.findAll("ul",'category'):
                data['category'] = category.li.get_text().strip()
                data['year'] = 0
                #print "Category Name:"+data['category']
                for interestItem in category.ul.children:

                    if  hasattr(interestItem,'name') and interestItem.name == 'div':
                        data['year'] = interestItem.get_text().strip()
                    elif hasattr(interestItem,'name') and interestItem.name == 'li':
                        #a normal li
                        data['interest'] = interestItem.get_text().strip()
                        #print "Interest:" + data['interest']
                        #print "Saved record #"+str(id)
                        scraperwiki.sqlite.save(unique_keys=["name","year","interest"], data=data)
                        i = i +1
                print ""+str(i)+" "+data['category']+" records saved for "+data['name']
        else:
            print "Skipped empty record #"+str(id)
        scraperwiki.sqlite.save_var('last_page', id)

lastID = 0