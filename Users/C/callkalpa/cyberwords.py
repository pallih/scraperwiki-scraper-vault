import scraperwiki
import lxml.html
import time
import sys
import re


base_url = 'http://adelaide.craigslist.com.au/'

# Blank Python

#url =  scraperwiki.scrape("http://www.google.com")

links_list = []
words_list = []



def scrape(html):
    global links_list
    global words_list

    try:
        url = scraperwiki.scrape(html)
        root = lxml.html.fromstring(url)

       
        
        
        # collect more links
        for links in root.cssselect('a'):
            temp = links.get('href')
            if temp:
                links_list.append(temp)
#                print temp

        # process words
        words = re.findall(r'\w+', url)
        for word in words:
            if word not in words_list and word :

                # filter out words with numbers
                try:
                    value = int(word)
                except ValueError:
                    words_list.append(word)
                    data={'words': word}
                    scraperwiki.sqlite.save(unique_keys=['words'], data=data)


#        time.sleep(1)
        scrape(links_list.pop())

    except:
        pass
#        scraperwiki.sqlite.save(unique_keys=['imgs'], data=data)



scrape(base_url)

print 'LENGTH: ', len(links_list)
