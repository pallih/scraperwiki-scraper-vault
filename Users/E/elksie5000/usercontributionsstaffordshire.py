import scraperwiki
import lxml.html

import time
import random

def sleep_random():
    random.seed()
    n = random.random()*10
    print "Sleep for seconds: " + str(n)
    time.sleep(n)

#load in rel_urls for testing later

base_url = "http://www.thisisstaffordshire.co.uk/archive.html"


def scrape_archive_page (url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    list_info = root.xpath('//*[@id="archive"]/div[2]/ul/li/a')
    return list_info

def scrape_article_details(url, type):
    print url, type
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    if type == 'story':
        headlines = root.xpath('//*[@id="story"]/div[1]/div[1]/h1')
        pub_times = root.xpath('//*[@id="story"]/div[1]/div[2]/div')
        article_authors = root.xpath('//*[@id="story"]/div[1]/div[2]/p/a')
    elif type =='pictures':
        
        headlines = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/h1')
        pub_times = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/div[1]/div[2]/div')
        article_authors = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/div[1]/div[2]/p/a')
    elif type =='event':
        headlines = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/h1')
        pub_times = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/div/div')
        article_authors = root.xpath('//*[@id="body"]/div[2]/div[1]/div[1]/div/p/a')
    else:
        headline = "N/a"
        pub_time = "N/a"
        article_author = "N/a"
        print headline, pub_time, article_author
        return headline, pub_time, article_author

    headline = headlines[0].text
    pub_time = pub_times[0].text
    article_author = article_authors[0].text
    return headline, pub_time, article_author

dates = scrape_archive_page(base_url)

print len(dates)
print lxml.html.tostring(dates[0])
print dates[0].text
print dates[0].attrib['href']
#create 2013 date list
dates_2013 = [x for x in dates if "2013" in lxml.html.tostring(x)]
print len(dates_2013)
#cycle through 2013 and create database of all content in page

for date in dates_2013:
    #create url by chopping base_url and dropping the reference bit on
    url = base_url.split("/archive.html")[0]+date.attrib['href']
    print url

    #Load rel_url parameter from existing database and check for any new URLs to scrape    
    
    #Pull in list data from each available archive_page
    content_list = scrape_archive_page(url)
    for content in content_list:
        
            record = {}
            url_components = content.attrib['href'].split("/")
            record['rel_url'] = content.attrib['href']
            record['base_url'] = base_url.split("/archive.html")[0]
            record['type'] = url_components[-1].split(".")[0]
            record['id'] = url_components[-2].split("-")[1]
            record['title'] = url_components[-3]

            scraperwiki.sqlite.save(unique_keys = ['id'], data = record)
            
       


