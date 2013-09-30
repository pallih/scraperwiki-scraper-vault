import re
import scraperwiki
import lxml.html

# Counties to loop through

counties = ['baker', 'benton', 'clackamas', 'clatsop', 'columbia', 'coos', 'crook', 'curry', 'deschutes', 'douglas', 'gilliam', 'grant', 'harney', 'hood-river', 'jackson', 'jefferson', 'josephine', 'klamath', 'lake', 'lane', 'lincoln', 'linn', 'malheur', 'marion', 'morrow', 'multnomah', 'polk', 'sherman', 'tillamook', 'umatilla', 'union', 'wallowa', 'wasco', 'washington', 'wheeler', 'yamhill']

# Strings to replace

def cleanup_text(text, dic={ '+':'', '%':'', ',':'', '$':'', 'Not Available':'null', 'Not available':'null' }):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# Scrape!

for county in counties:           
    html = scraperwiki.scrape(''.join(['http://www.oregonmiddleclass.org/',county,'-county/']))           
    root = lxml.html.fromstring(html)
    tables = root.cssselect('table')
    for table in tables:
        for tr in table:
            tds = tr.cssselect('td')
            if re.search('\%', tds[1].text_content()):
                data = {
                  'name' : tds[0].text_content(),
                  'value' : float(cleanup_text(tds[1].text_content()))/100
                }
                scraperwiki.sqlite.save(unique_keys=['name'], data=data, table_name=county)
            else:
                data = {
                  'name' : tds[0].text_content(),
                  'value' : cleanup_text(tds[1].text_content())
                }
                scraperwiki.sqlite.save(unique_keys=['name'], data=data, table_name=county)
    print county, ' completed.'import re
import scraperwiki
import lxml.html

# Counties to loop through

counties = ['baker', 'benton', 'clackamas', 'clatsop', 'columbia', 'coos', 'crook', 'curry', 'deschutes', 'douglas', 'gilliam', 'grant', 'harney', 'hood-river', 'jackson', 'jefferson', 'josephine', 'klamath', 'lake', 'lane', 'lincoln', 'linn', 'malheur', 'marion', 'morrow', 'multnomah', 'polk', 'sherman', 'tillamook', 'umatilla', 'union', 'wallowa', 'wasco', 'washington', 'wheeler', 'yamhill']

# Strings to replace

def cleanup_text(text, dic={ '+':'', '%':'', ',':'', '$':'', 'Not Available':'null', 'Not available':'null' }):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# Scrape!

for county in counties:           
    html = scraperwiki.scrape(''.join(['http://www.oregonmiddleclass.org/',county,'-county/']))           
    root = lxml.html.fromstring(html)
    tables = root.cssselect('table')
    for table in tables:
        for tr in table:
            tds = tr.cssselect('td')
            if re.search('\%', tds[1].text_content()):
                data = {
                  'name' : tds[0].text_content(),
                  'value' : float(cleanup_text(tds[1].text_content()))/100
                }
                scraperwiki.sqlite.save(unique_keys=['name'], data=data, table_name=county)
            else:
                data = {
                  'name' : tds[0].text_content(),
                  'value' : cleanup_text(tds[1].text_content())
                }
                scraperwiki.sqlite.save(unique_keys=['name'], data=data, table_name=county)
    print county, ' completed.'