import scraperwiki
import datetime
import re
import urlparse


from scraperwiki import sqlite

scrape_FLAG=False # set to True to pull data from the web, False to run without doing so

biographies={
    "current" : '''http://www.supremecourt.gov.uk/about/biographies-of-the-justices.html''',
    "former" : '''http://www.supremecourt.gov.uk/about/former-justices.html'''
}

div_pattern=re.compile('<(/)?div')
def div_snip(source, start=0):
    '''Takes a string and assumes that it is inside a <div
    then counts open and close 'div' tags until it find the matching closing </div
    and returns the string internal to that div element.'''

    # Why? Because none of the standard libraries is stable enough and well documented enough
    # to be other than a pain to use and maintain (brought on by lxml silently changing things)

    depth=1
    pos=start
    while pos < len(source):
        div_match=div_pattern.search(source, pos)
        if div_match:
            if div_match.group(1)=='/':
                depth=depth - 1
            else:
                depth=depth + 1
            if depth==0:
                return source[start:div_match.start()]
            else:
                pos=div_match.end()
    raise Exception("no matching div found")  
    

def scrape_page(url):
    html=scraperwiki.scrape(url)
    start=re.search('(?i)<h3>(Biographies|Former)', html).start()
    biography_html=div_snip(html, start)
    return(biography_html)

back_to_top_pattern=re.compile(r"<p.*?<a.*?>back to top</a> *</p>\s*", re.I)

def get_pattern(regular_expression, source, pos, keys, data_dict):
    pattern=re.compile(regular_expression, re.I)
    match=pattern.search(source, pos)
    if match:
        groups=match.groups()
        #print(groups)
        for i in range(0, len(groups)):
            if keys[i] is not None:
                data_dict[keys[i]]=groups[i]
        pos=match.end()
    else:
        for key in keys:
            data_dict[key]=None
        pos=len(html)
    return(pos)

def justice_generator(html, current):
    pos=0
    while pos < len(html):
        data={}
        pos=get_pattern('''<div.*?/div>''', html, pos, [], data)
        pos=get_pattern('''<img *(src="([^"]*)"| *alt="([^"]*)")+[^>]*/>''', html, pos, [None, 'img_url', 'img_alt'], data)
        pos=get_pattern('''<h4[^>]*>(.*?)</h4>''', html, pos, ['name'], data)
        pos=get_pattern('''<p><strong>(.*?)</strong></p>''', html, pos, ['full_title'], data)
        # ''' 
        print(data)
        full_title_match=re.match('(?i)(President of The Supreme Court|Deputy President of The Supreme Court|Justice of The Supreme Court) *, *the right hon *(the)? *((Lord|Lady|Baroness)[-a-zA-Z ]+)(, *(.+))?', data['full_title'])
        if full_title_match:
            data['office']=full_title_match.group(1).strip()
            data['short_title']=full_title_match.group(3).strip()
            pn=full_title_match.group(6)
            if pn is not None:
                data['postnominal']=pn.strip()
            else:
                data['postnominal']=None
        else:
            sqlite.save(unique_keys=['full_title'], data=data, table_name='full_title_anomalies')
            print("Anomaly {0}".format(repr(data)))
            continue
        top_match=back_to_top_pattern.search(html, pos)
        if top_match:
            biography_html=html[pos:top_match.start()]
            pos=top_match.end()
        else:
            biography_html=html[pos:]
            pos=len(html)
        data['biography_html']=biography_html
        yield(data)

# Save the html as primary key for later processing

for name in biographies:
    if not scrape_FLAG:
        break
    url=biographies[name]
    html=scrape_page(url)
    
    data={'html' : html, 'timestamp' : datetime.datetime.today()}
    sqlite.save(unique_keys=['html'], data=data, table_name=name + "_html")

#sourcescraper = 'uk-supreme-court-justices-biographies'
#scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''html, timestamp from current_html order by timestamp''')
for row in data:
    html=row['html']
    for justice_data in justice_generator(html, current=True):
        justice_data['timestamp']=row['timestamp']
        justice_data['img_url']=urlparse.urljoin(biographies['current'], justice_data['img_url'])
        print(justice_data['name'])
        sqlite.save(unique_keys=['short_title', 'office'], data=justice_data, table_name="current_justices")

data = scraperwiki.sqlite.select('''html, timestamp from former_html order by timestamp''')
for row in data:
    html=row['html']
    for justice_data in justice_generator(html, current=True):
        justice_data['timestamp']=row['timestamp']
        justice_data['img_url']=urlparse.urljoin(biographies['former'], justice_data['img_url'])
        print(justice_data['name'])
        sqlite.save(unique_keys=['short_title'], data=justice_data, table_name="former_justices")


