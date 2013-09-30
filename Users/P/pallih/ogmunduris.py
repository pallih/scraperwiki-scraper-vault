import scraperwiki
import lxml.html
import re

start = scraperwiki.scrape('http://ogmundur.is/allar-greinar/eldra/')
year_xpath= '//div[1]/div/div/div/a'
root = lxml.html.fromstring(start)
years = root.xpath(year_xpath)

def scrape_year(url,year):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    items = root.xpath('//div[@class="newslistdiv"]')
    for item in items:
        try:
            record = {}
            record['date'] = item[0].text
            record['headline'] = item[1].text_content()
            record['url'] = 'http://ogmundur.is' + item[1][0].get('href')
            record['intro'] = item[2].text_content()
            record['year'] = year
            scraperwiki.sqlite.save(['url'], data=record, table_name='ogmundur-articles', verbose=0)
        except Exception:
            pass



headlines = scraperwiki.sqlite.select('headline from "ogmundur-articles"')

print len(headlines)

upper = []
lower = []
regex = re.compile(".*skrifar:(.*)")
for line in headlines:
    headline = re.sub(".*:"," ", line['headline']).strip()
    record = {}
    if headline.isupper() == True:
        record['headline'] = headline
        #print headline['headline']
        
        scraperwiki.sqlite.save(['headline'], data=record, table_name='upper', verbose=0)
        #upper.append(headline)
    else:
        record['headline'] = headline
        scraperwiki.sqlite.save(['headline'], data=record, table_name='lower', verbose=0)

        #lower.append(headline)
print len(lower)
print len(upper)
print ";".join(lower)
print ";".join(upper)

#for x in lower:
#    print x
#    print re.sub(".*skrifar: "," ", x)
exit()

for year in years:
    url = 'http://ogmundur.is' + year.get('href')
    scrape_year(url,year.text)
    print 'Done with ', year.text


import scraperwiki
import lxml.html
import re

start = scraperwiki.scrape('http://ogmundur.is/allar-greinar/eldra/')
year_xpath= '//div[1]/div/div/div/a'
root = lxml.html.fromstring(start)
years = root.xpath(year_xpath)

def scrape_year(url,year):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    items = root.xpath('//div[@class="newslistdiv"]')
    for item in items:
        try:
            record = {}
            record['date'] = item[0].text
            record['headline'] = item[1].text_content()
            record['url'] = 'http://ogmundur.is' + item[1][0].get('href')
            record['intro'] = item[2].text_content()
            record['year'] = year
            scraperwiki.sqlite.save(['url'], data=record, table_name='ogmundur-articles', verbose=0)
        except Exception:
            pass



headlines = scraperwiki.sqlite.select('headline from "ogmundur-articles"')

print len(headlines)

upper = []
lower = []
regex = re.compile(".*skrifar:(.*)")
for line in headlines:
    headline = re.sub(".*:"," ", line['headline']).strip()
    record = {}
    if headline.isupper() == True:
        record['headline'] = headline
        #print headline['headline']
        
        scraperwiki.sqlite.save(['headline'], data=record, table_name='upper', verbose=0)
        #upper.append(headline)
    else:
        record['headline'] = headline
        scraperwiki.sqlite.save(['headline'], data=record, table_name='lower', verbose=0)

        #lower.append(headline)
print len(lower)
print len(upper)
print ";".join(lower)
print ";".join(upper)

#for x in lower:
#    print x
#    print re.sub(".*skrifar: "," ", x)
exit()

for year in years:
    url = 'http://ogmundur.is' + year.get('href')
    scrape_year(url,year.text)
    print 'Done with ', year.text


