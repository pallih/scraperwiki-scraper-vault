import scraperwiki, urllib2, sys, re
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("pitchdexer")

def un_unicode(elem):
        return map(lambda x: x.encode('ASCII', 'ignore'), elem.contents)[0]

def retry_failed_scrapes():
    for i in scraperwiki.sqlite.select(           
                '''key from pitchdexer.swdata 
                where reviewers="SCRAPE FAILED"'''):
        if i['key'] not in ('560-ion-the-ellipsei', '1365-no-more-shall-we-part'):
            print("retrying - " + i['key'])
            scrape("http://pitchfork.com/reviews/albums/" + i['key'], i['key']) 


def scrape(url, review_key):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        meta = soup.find("ul", {"class" : "review-meta"})
        meta_info = meta.findAll("div", {"class":"info"})

        editorial = repr(soup.find("div", {"class" : "editorial"}))
        artists = map(lambda x: un_unicode(x), meta.find("li", {"class": "first"}).findAll("a"))
        albums = map(lambda x: un_unicode(x.h2), meta_info)
        reviewers = re.split(', with help from |, and| & |, ',list(set(map(lambda x: un_unicode(x.h4.address), meta_info)))[0])
        scores = map(lambda x: un_unicode(x), meta.findAll('span', {"class": "score"}))
        accolades = map(lambda x: un_unicode(x), meta.findAll('div', {"class": "bnm-label"}))
        pub_date = map(lambda x: un_unicode(x), meta.findAll('span', {"class": "pub-date"}))[0]

        scraperwiki.sqlite.save(unique_keys=['key'], data={"key": review_key, "artists": artists,"editorial": editorial,"albums": albums,"reviewers": reviewers,"scores": scores, "pub_date": pub_date, "accolades": accolades})

def crawl(page=0):
    page = urllib2.urlopen("http://pitchfork.com/reviews/albums/" + ("" if page==0 else (str(page) + "/")))
    soup = BeautifulSoup(page)
    main_grid = soup.find("ul", {"class" : "object-grid"})
    
    for a_child in main_grid.findAll("a"): 
        shelve_key = a_child['href'].encode('ASCII', 'ignore').split('/')[-2]
        if len(scraperwiki.sqlite.select(           
            '''* from pitchdexer.swdata 
            where key='''+ "'" +shelve_key + "'")) < 1 :
            print("scraping: " + shelve_key)
            try:
                scrape("http://pitchfork.com"+a_child['href'], shelve_key)
            except:
                print("failed to scrape: " + a_child['href'])
                scraperwiki.sqlite.save(unique_keys=['key'], data={"key": shelve_key, "artists": "SCRAPE FAILED","editorial": "SCRAPE FAILED","albums": "SCRAPE FAILED","reviewers": "SCRAPE FAILED","scores": "SCRAPE FAILED", "pub_date": "SCRAPE FAILED", "accolades": "SCRAPE FAILED"})

#for i in range(scraperwiki.sqlite.get_var('last_page'),650):
#    print("iteration - " + str(i))
#    scraperwiki.sqlite.save_var('last_page', i)
#    crawl(i)

#for i in range(0,650):
#    crawl(i)

crawl()
#retry_failed_scrapes()

#print(scraperwiki.sqlite.select("reviewers from pitchdexer.swdata where key='8242-cheers'"))
#for reviewer_key_pair in scraperwiki.sqlite.select("reviewers, key from pitchdexer.swdata"):
#    if ("," in reviewer_key_pair['reviewers']):
#   scraperwiki.sqlite.save(unique_keys=['key'], data
#        print(reviewer_key_pair['key'])
#        print(re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers']))
#        if (reviewer_key_pair['key']) == "8242-cheers":
#            print(reviewer_key_pair['key'])
#            print(reviewer_key_pair['reviewers'])
#            print(re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers']))
#            chomped_reviewers = re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers'])
#            print(chomped_reviewers)
#            print(reviewer_key_pair['key'])
#            print(scraperwiki.sqlite.execute("update pitchdexer.swdata set reviewers=? where key=?", (chomped, reviewer_key_pair['key'])))
#            scraperwiki.sqlite.execute(unique_keys=['key'], data={"key":reviewer_key_pair['key'], "reviewers": re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers'])})
#scraperwiki.sqlite.commit() import scraperwiki, urllib2, sys, re
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("pitchdexer")

def un_unicode(elem):
        return map(lambda x: x.encode('ASCII', 'ignore'), elem.contents)[0]

def retry_failed_scrapes():
    for i in scraperwiki.sqlite.select(           
                '''key from pitchdexer.swdata 
                where reviewers="SCRAPE FAILED"'''):
        if i['key'] not in ('560-ion-the-ellipsei', '1365-no-more-shall-we-part'):
            print("retrying - " + i['key'])
            scrape("http://pitchfork.com/reviews/albums/" + i['key'], i['key']) 


def scrape(url, review_key):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        meta = soup.find("ul", {"class" : "review-meta"})
        meta_info = meta.findAll("div", {"class":"info"})

        editorial = repr(soup.find("div", {"class" : "editorial"}))
        artists = map(lambda x: un_unicode(x), meta.find("li", {"class": "first"}).findAll("a"))
        albums = map(lambda x: un_unicode(x.h2), meta_info)
        reviewers = re.split(', with help from |, and| & |, ',list(set(map(lambda x: un_unicode(x.h4.address), meta_info)))[0])
        scores = map(lambda x: un_unicode(x), meta.findAll('span', {"class": "score"}))
        accolades = map(lambda x: un_unicode(x), meta.findAll('div', {"class": "bnm-label"}))
        pub_date = map(lambda x: un_unicode(x), meta.findAll('span', {"class": "pub-date"}))[0]

        scraperwiki.sqlite.save(unique_keys=['key'], data={"key": review_key, "artists": artists,"editorial": editorial,"albums": albums,"reviewers": reviewers,"scores": scores, "pub_date": pub_date, "accolades": accolades})

def crawl(page=0):
    page = urllib2.urlopen("http://pitchfork.com/reviews/albums/" + ("" if page==0 else (str(page) + "/")))
    soup = BeautifulSoup(page)
    main_grid = soup.find("ul", {"class" : "object-grid"})
    
    for a_child in main_grid.findAll("a"): 
        shelve_key = a_child['href'].encode('ASCII', 'ignore').split('/')[-2]
        if len(scraperwiki.sqlite.select(           
            '''* from pitchdexer.swdata 
            where key='''+ "'" +shelve_key + "'")) < 1 :
            print("scraping: " + shelve_key)
            try:
                scrape("http://pitchfork.com"+a_child['href'], shelve_key)
            except:
                print("failed to scrape: " + a_child['href'])
                scraperwiki.sqlite.save(unique_keys=['key'], data={"key": shelve_key, "artists": "SCRAPE FAILED","editorial": "SCRAPE FAILED","albums": "SCRAPE FAILED","reviewers": "SCRAPE FAILED","scores": "SCRAPE FAILED", "pub_date": "SCRAPE FAILED", "accolades": "SCRAPE FAILED"})

#for i in range(scraperwiki.sqlite.get_var('last_page'),650):
#    print("iteration - " + str(i))
#    scraperwiki.sqlite.save_var('last_page', i)
#    crawl(i)

#for i in range(0,650):
#    crawl(i)

crawl()
#retry_failed_scrapes()

#print(scraperwiki.sqlite.select("reviewers from pitchdexer.swdata where key='8242-cheers'"))
#for reviewer_key_pair in scraperwiki.sqlite.select("reviewers, key from pitchdexer.swdata"):
#    if ("," in reviewer_key_pair['reviewers']):
#   scraperwiki.sqlite.save(unique_keys=['key'], data
#        print(reviewer_key_pair['key'])
#        print(re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers']))
#        if (reviewer_key_pair['key']) == "8242-cheers":
#            print(reviewer_key_pair['key'])
#            print(reviewer_key_pair['reviewers'])
#            print(re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers']))
#            chomped_reviewers = re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers'])
#            print(chomped_reviewers)
#            print(reviewer_key_pair['key'])
#            print(scraperwiki.sqlite.execute("update pitchdexer.swdata set reviewers=? where key=?", (chomped, reviewer_key_pair['key'])))
#            scraperwiki.sqlite.execute(unique_keys=['key'], data={"key":reviewer_key_pair['key'], "reviewers": re.split(', with help from |, and| & |, ',reviewer_key_pair['reviewers'])})
#scraperwiki.sqlite.commit() 