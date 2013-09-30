import scraperwiki
import lxml.html
import re
import datetime
import csv

domaine = 'http://www.ecobusinesslinks.com/'
s_url = 'http://www.ecobusinesslinks.com/gifts_eco_friendly_recycled_gifts/'

scraperwiki.sqlite.save_var("source", "ecobusinesslinks.com")
scraperwiki.sqlite.save_var("author", "Ajay Singh Rathour")
#opening csv file in w mode
ofile  = open('mail.csv', "wb",0)
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

#writing header row
writer.writerow(['comp_name','web_site','web_site','state','country','temp_data','temp_data'])

def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        root = lxml.html.fromstring(html_content)
        
        data_list = root.cssselect('div[class="post clearfix"]')
        
        
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        else:
            for i in xrange(len(data_list)):
                abs_link = start_url
                scrape_info(abs_link, r_num)
                r_num+=1
            break
            
    
        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('id', num))
    my_data.append(('sourceurl', comp_link))
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content,comp_link)
    root.make_links_absolute()
    
    
    comp_name = root.xpath("//div[@class='post clearfix']/div[1]/a/@title")
    if comp_name:
        my_data.append(('companyname', comp_name[num]))
    
    web_site = root.xpath("//div[@class='post clearfix']/div[1]/a/@href")
    if web_site:
        my_data.append(('website', web_site[num]))
    
    main_cat = root.xpath("//h1/text()")
    my_data.append(('maincategory', main_cat))

    temp_data = root.xpath("//div[@class='post clearfix']/div[1]")[num]
    temp_loc = temp_data.xpath(".//div/span/text()")
    if temp_loc:
        if "," in temp_loc[0]:
            state = temp_loc[0].split(',')[1].strip()
            country = temp_loc[0].split(',')[0].strip()
            my_data.append(('country', country))
            my_data.append(('state', state))
        else:
            state = temp_loc[0].strip()
            my_data.append(('state', state))
    
    desc = root.xpath("//div[@class='post clearfix']/div[2]/text()")[num]
    if desc:
        my_data.append(('description', desc))

    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d")
    my_data.append(('datescraped', str(now_text)))

    print my_data
    
    writer.writerow(my_data)
    print "written"

    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

    

scrape_site(s_url, domaine)


import scraperwiki
import lxml.html
import re
import datetime
import csv

domaine = 'http://www.ecobusinesslinks.com/'
s_url = 'http://www.ecobusinesslinks.com/gifts_eco_friendly_recycled_gifts/'

scraperwiki.sqlite.save_var("source", "ecobusinesslinks.com")
scraperwiki.sqlite.save_var("author", "Ajay Singh Rathour")
#opening csv file in w mode
ofile  = open('mail.csv', "wb",0)
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

#writing header row
writer.writerow(['comp_name','web_site','web_site','state','country','temp_data','temp_data'])

def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        root = lxml.html.fromstring(html_content)
        
        data_list = root.cssselect('div[class="post clearfix"]')
        
        
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        else:
            for i in xrange(len(data_list)):
                abs_link = start_url
                scrape_info(abs_link, r_num)
                r_num+=1
            break
            
    
        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('id', num))
    my_data.append(('sourceurl', comp_link))
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content,comp_link)
    root.make_links_absolute()
    
    
    comp_name = root.xpath("//div[@class='post clearfix']/div[1]/a/@title")
    if comp_name:
        my_data.append(('companyname', comp_name[num]))
    
    web_site = root.xpath("//div[@class='post clearfix']/div[1]/a/@href")
    if web_site:
        my_data.append(('website', web_site[num]))
    
    main_cat = root.xpath("//h1/text()")
    my_data.append(('maincategory', main_cat))

    temp_data = root.xpath("//div[@class='post clearfix']/div[1]")[num]
    temp_loc = temp_data.xpath(".//div/span/text()")
    if temp_loc:
        if "," in temp_loc[0]:
            state = temp_loc[0].split(',')[1].strip()
            country = temp_loc[0].split(',')[0].strip()
            my_data.append(('country', country))
            my_data.append(('state', state))
        else:
            state = temp_loc[0].strip()
            my_data.append(('state', state))
    
    desc = root.xpath("//div[@class='post clearfix']/div[2]/text()")[num]
    if desc:
        my_data.append(('description', desc))

    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d")
    my_data.append(('datescraped', str(now_text)))

    print my_data
    
    writer.writerow(my_data)
    print "written"

    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

    

scrape_site(s_url, domaine)


