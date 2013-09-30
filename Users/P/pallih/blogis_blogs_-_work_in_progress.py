# coding=utf-8
#Work in progress

import scraperwiki,re
from lxml import etree
import lxml.html

# --- Constants ---

#400 vinsaelustu bloggin

#tenglar - vinsaelustu
# //tr/td[2]/a/@href

#tenglar a blogg-vini:
# //div[@id="Blog-friends-box"]/div/div/div/div/div/ul/li/a/@href

# //div[@id="Blog-friends-box"]//a/@href

# hofundur:
# //p[@class="system-real-author"]/b

#titill
# //div[@id="About"]/h2


#******* FIRST SCRAPE - 400 MOST POPULAR ************

#starturl = 'http://blog.is/forsida/top.html?num=400'

#html = scraperwiki.scrape(starturl)
#root = lxml.html.fromstring(html)

#hrefs = root.xpath ( '//tr/td[2]/a/@href')

#for a in hrefs:
#    record = {}
#    record['url'] = 'http://' + a.split('//')[1].partition('/')[0] + '/'
#    html = scraperwiki.scrape(a + 'about/')
#    root = lxml.html.fromstring(html)
#    hofundur = root.xpath ('//p[@class="system-real-author"]/b/text()')
#    if not hofundur:
#        hofundur = ['n/a']
#    record['hofundur'] = hofundur[0]
#    record['vinir'] = root.xpath ( '//div[@id="Blog-friends-box"]//a/@href')
#    record['scraped'] = '0'
#    print record
#    scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')

#exit()

#******* SECOND SCRAPE - FRIENDS OF THE 400 MOST POPULAR ************

count = scraperwiki.sqlite.select('url from blogs WHERE scraped="0"')
count = len(count)
print "TO PROCESS: ", count
print
while count != 0:
 todo = scraperwiki.sqlite.select('url, vinir from blogs WHERE scraped="0" LIMIT 1')

#urllist = []
#for urls in todo:
#    urllist.append(urls['url'])

#print urllist

 ignorelist = ['http://morgunbladid.blog.is/', 'http://tatum.blog.is/', 'http://-valur-oskarsson.blog.is/']

 for item in todo:
  url = item['url']
  #print item['vinir']
  if item['vinir'] != "[]":
    vinir = item['vinir'][1:-1].replace("'",'').split(', ')
    for v in vinir:
        #print v
        check_statement = "select * from blogs where url="+"'" + v +"'"
        check = scraperwiki.sqlite.execute(check_statement)
        #print "check output: ", check['data'][0]
        
        #ignorelist hack - this must be done better!
        if v in ignorelist:
            print "URL IN IGNORELIST: ", v
            #continue
        elif check['data']:
            print "ALREADY IN DB : ", v, " - MOVE ON!"
        else:
            print "MISSING FROM DB: ", v, " - ADD TO DB"
            record = {}
            record['url'] = v
            html = scraperwiki.scrape(v)
            
            #about_url = v + "blog/" + v.partition('.')[0][7:] + "/about"
            root = lxml.html.fromstring(html)
            about_url = root.xpath ('//div[@id="About-box"][1]//a/@href')
            if about_url:
                about_url = str(v[:-1]) + about_url[0][:-1]
                html = scraperwiki.scrape(about_url)
                root = lxml.html.fromstring(html)
                hofundur = root.xpath ('//p[@class="system-real-author"]/b/text()')
                if not hofundur:
                    hofundur = ['n/a']
                record['hofundur'] = hofundur[0]
                record['vinir'] = root.xpath ( '//div[@id="Blog-friends-box"]//a/@href')
                record['scraped'] = '0'
                print record
                scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')
            else:
                print "MISSING FROM DB BUT MISSING ABOUT LINK ... INSERT WITH EMPTY VALUES AND UPDATE SCRAPED = 1"
                record['url'] = v
                record['hofundur'] = 'n/a'
                record['vinir'] =''
                record['scraped'] = '1'
                print record
                scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')

    print "**********  DONE WITH FRIENDS OF:" , url
    update_statement = "update blogs SET scraped='1' where url="+"'" + url +"'"
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    print
    print "SELECT NEW BLOG TO PROCESS"
    #todo = ""
    #todo = scraperwiki.sqlite.select('url, vinir from blogs WHERE scraped="0" AND vinir !="[]"')

    #urllist = []
    #for urls in todo:
    #    urllist.append(urls['url'])

    #print urllist
  else:
    print "NO FRIENDS - UPDATE TO SCRAPED = 1: ", url
    update_statement = "update blogs SET scraped='1' where url="+"'" + url +"'"
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
 count = count - 1
 print "LEFT TO PROCESS: ", count

print " ************** ---- ALL DONE ----- *************"
# coding=utf-8
#Work in progress

import scraperwiki,re
from lxml import etree
import lxml.html

# --- Constants ---

#400 vinsaelustu bloggin

#tenglar - vinsaelustu
# //tr/td[2]/a/@href

#tenglar a blogg-vini:
# //div[@id="Blog-friends-box"]/div/div/div/div/div/ul/li/a/@href

# //div[@id="Blog-friends-box"]//a/@href

# hofundur:
# //p[@class="system-real-author"]/b

#titill
# //div[@id="About"]/h2


#******* FIRST SCRAPE - 400 MOST POPULAR ************

#starturl = 'http://blog.is/forsida/top.html?num=400'

#html = scraperwiki.scrape(starturl)
#root = lxml.html.fromstring(html)

#hrefs = root.xpath ( '//tr/td[2]/a/@href')

#for a in hrefs:
#    record = {}
#    record['url'] = 'http://' + a.split('//')[1].partition('/')[0] + '/'
#    html = scraperwiki.scrape(a + 'about/')
#    root = lxml.html.fromstring(html)
#    hofundur = root.xpath ('//p[@class="system-real-author"]/b/text()')
#    if not hofundur:
#        hofundur = ['n/a']
#    record['hofundur'] = hofundur[0]
#    record['vinir'] = root.xpath ( '//div[@id="Blog-friends-box"]//a/@href')
#    record['scraped'] = '0'
#    print record
#    scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')

#exit()

#******* SECOND SCRAPE - FRIENDS OF THE 400 MOST POPULAR ************

count = scraperwiki.sqlite.select('url from blogs WHERE scraped="0"')
count = len(count)
print "TO PROCESS: ", count
print
while count != 0:
 todo = scraperwiki.sqlite.select('url, vinir from blogs WHERE scraped="0" LIMIT 1')

#urllist = []
#for urls in todo:
#    urllist.append(urls['url'])

#print urllist

 ignorelist = ['http://morgunbladid.blog.is/', 'http://tatum.blog.is/', 'http://-valur-oskarsson.blog.is/']

 for item in todo:
  url = item['url']
  #print item['vinir']
  if item['vinir'] != "[]":
    vinir = item['vinir'][1:-1].replace("'",'').split(', ')
    for v in vinir:
        #print v
        check_statement = "select * from blogs where url="+"'" + v +"'"
        check = scraperwiki.sqlite.execute(check_statement)
        #print "check output: ", check['data'][0]
        
        #ignorelist hack - this must be done better!
        if v in ignorelist:
            print "URL IN IGNORELIST: ", v
            #continue
        elif check['data']:
            print "ALREADY IN DB : ", v, " - MOVE ON!"
        else:
            print "MISSING FROM DB: ", v, " - ADD TO DB"
            record = {}
            record['url'] = v
            html = scraperwiki.scrape(v)
            
            #about_url = v + "blog/" + v.partition('.')[0][7:] + "/about"
            root = lxml.html.fromstring(html)
            about_url = root.xpath ('//div[@id="About-box"][1]//a/@href')
            if about_url:
                about_url = str(v[:-1]) + about_url[0][:-1]
                html = scraperwiki.scrape(about_url)
                root = lxml.html.fromstring(html)
                hofundur = root.xpath ('//p[@class="system-real-author"]/b/text()')
                if not hofundur:
                    hofundur = ['n/a']
                record['hofundur'] = hofundur[0]
                record['vinir'] = root.xpath ( '//div[@id="Blog-friends-box"]//a/@href')
                record['scraped'] = '0'
                print record
                scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')
            else:
                print "MISSING FROM DB BUT MISSING ABOUT LINK ... INSERT WITH EMPTY VALUES AND UPDATE SCRAPED = 1"
                record['url'] = v
                record['hofundur'] = 'n/a'
                record['vinir'] =''
                record['scraped'] = '1'
                print record
                scraperwiki.sqlite.save(['url'], data=record, table_name='blogs')

    print "**********  DONE WITH FRIENDS OF:" , url
    update_statement = "update blogs SET scraped='1' where url="+"'" + url +"'"
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    print
    print "SELECT NEW BLOG TO PROCESS"
    #todo = ""
    #todo = scraperwiki.sqlite.select('url, vinir from blogs WHERE scraped="0" AND vinir !="[]"')

    #urllist = []
    #for urls in todo:
    #    urllist.append(urls['url'])

    #print urllist
  else:
    print "NO FRIENDS - UPDATE TO SCRAPED = 1: ", url
    update_statement = "update blogs SET scraped='1' where url="+"'" + url +"'"
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
 count = count - 1
 print "LEFT TO PROCESS: ", count

print " ************** ---- ALL DONE ----- *************"
