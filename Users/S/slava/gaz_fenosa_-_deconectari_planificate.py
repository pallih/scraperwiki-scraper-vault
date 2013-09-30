import scraperwiki
import lxml.html
import re
import datetime

monthnames = {'Ianuarie':1, 'Februarie':2, 'Martie':3, 'Aprilie':4, 'Mai':5,'Iunie':6, 'Iulie':7, 'August':8, 'Septembrie':9, 'Octombrie':10, 'Noiembrie':11, 'Decembrie':12 }


html=scraperwiki.scrape('http://gasnaturalfenosa.md/anun%C5%A3uri')
print html
root=lxml.html.document_fromstring(html)

today=datetime.date.today()

# Get latest news
for el in root.xpath("//div[@class='view-content']/table/tbody/tr"):
    #print el.text_content()

    date=el.xpath("td/div[@class='views-field-created']/span/text()")[0]
    news_link=el.xpath("td/div[@class='views-field-title']/span/a/@href")[0]

    m = re.match(r"(?P<week_day>\w+), (?P<day>\w+) (?P<month>\w+) (?P<year>\w+)", date)
    if m <> None:
        news_date=m.groupdict()
        #print news_date
        #print news_date['year']
    
    
        if news_date['month'] in monthnames:
            news_date=datetime.date(int(news_date['year']),monthnames[news_date['month']],int(news_date['day']))
            
            #data = {'data': []}
            
            if (news_date>today):
                data=scraperwiki.sqlite.execute("SELECT * FROM `news` WHERE `when`='" + news_date.strftime('%Y-%m-%d') + "'")
                print data
                if (data['data'] == []):
                    #print "Saving: ", news_link, news_date
                    scraperwiki.sqlite.save(unique_keys=['when'], data = {'when': news_date, 'link': news_link, 'sent':0, 'checked':0}, table_name = 'news')

#
data=scraperwiki.sqlite.execute("SELECT * FROM `news` WHERE `when`>'" + today.strftime('%Y-%m-%d') + "'")
print data
for d in data['data']:
    url = 'http://gasnaturalfenosa.md'+d[0]
    print "Check " + url

    html=scraperwiki.scrape(url)

    #found=re.search(r"(str\. Criuleni.*?)<br", html, re.I)
    found=re.search(r"(M\. Costin.*?)<br", html, re.I)

    if found:
        print "Deconectari vor fi " + found.group(1)

import scraperwiki
import lxml.html
import re
import datetime

monthnames = {'Ianuarie':1, 'Februarie':2, 'Martie':3, 'Aprilie':4, 'Mai':5,'Iunie':6, 'Iulie':7, 'August':8, 'Septembrie':9, 'Octombrie':10, 'Noiembrie':11, 'Decembrie':12 }


html=scraperwiki.scrape('http://gasnaturalfenosa.md/anun%C5%A3uri')
print html
root=lxml.html.document_fromstring(html)

today=datetime.date.today()

# Get latest news
for el in root.xpath("//div[@class='view-content']/table/tbody/tr"):
    #print el.text_content()

    date=el.xpath("td/div[@class='views-field-created']/span/text()")[0]
    news_link=el.xpath("td/div[@class='views-field-title']/span/a/@href")[0]

    m = re.match(r"(?P<week_day>\w+), (?P<day>\w+) (?P<month>\w+) (?P<year>\w+)", date)
    if m <> None:
        news_date=m.groupdict()
        #print news_date
        #print news_date['year']
    
    
        if news_date['month'] in monthnames:
            news_date=datetime.date(int(news_date['year']),monthnames[news_date['month']],int(news_date['day']))
            
            #data = {'data': []}
            
            if (news_date>today):
                data=scraperwiki.sqlite.execute("SELECT * FROM `news` WHERE `when`='" + news_date.strftime('%Y-%m-%d') + "'")
                print data
                if (data['data'] == []):
                    #print "Saving: ", news_link, news_date
                    scraperwiki.sqlite.save(unique_keys=['when'], data = {'when': news_date, 'link': news_link, 'sent':0, 'checked':0}, table_name = 'news')

#
data=scraperwiki.sqlite.execute("SELECT * FROM `news` WHERE `when`>'" + today.strftime('%Y-%m-%d') + "'")
print data
for d in data['data']:
    url = 'http://gasnaturalfenosa.md'+d[0]
    print "Check " + url

    html=scraperwiki.scrape(url)

    #found=re.search(r"(str\. Criuleni.*?)<br", html, re.I)
    found=re.search(r"(M\. Costin.*?)<br", html, re.I)

    if found:
        print "Deconectari vor fi " + found.group(1)

