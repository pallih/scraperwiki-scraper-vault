import re
import sys
import scraperwiki
import BeautifulSoup
from   scraperwiki import datastore

regions = []
root = scraperwiki.scrape('http://candidates.ukip.org/')
offset = root.find('index.php?pg=group&id=')
while offset >= 0 :
    regions.append (root[offset+22:offset+24])
    root = root[offset+24:]
    offset = root.find('index.php?pg=group&id=')

for region in regions :
    root = scraperwiki.scrape('http://candidates.ukip.org/index.php?pg=group&id=' + region)
    page = BeautifulSoup.BeautifulSoup(root)
    cons = page.findAll('a', attrs = { 'class' : 'candi_result' })

    for a in cons :
        constituency = a.text
        href = a['href']
        print constituency, href
        html = scraperwiki.scrape('http://candidates.ukip.org/' + href)
        page = BeautifulSoup.BeautifulSoup(html)
        if "We still haven't finalised our candidate" in html :
            data = \
                {     'constituency'    : constituency,
                      'region'          : region,
                      'name'            : None,
                      'webpage'         : None,
                      'biog'            : None,
                      'more'            : None
                }
            for i in xrange(10) :
                data['issue_%d' % i] = None
            datastore.save (unique_keys = ['constituency'], data = data)
            continue
        data = {}
        data['name'        ] = page.find('div', attrs = { 'id' : 'can_name' }).text
        data['constituency'] = constituency
        data['region'      ] = region
        data['webpage'     ] = 'http://candidates.ukip.org/' + href
        m = re.search ('<img src="images/open_speech.gif" border="0" />(.*)<img src="images/close_speech.gif" border="0" />', html)
        try    : data['biog'] = m.group(1).replace('&nbsp;', '')
        except : data['biog'] = None
        try    : data['more'] = page.find('a', attrs = {'target' : '_blank'})['href']
        except : data['more'] = None
        issues = page.findAll ('td', attrs = {'class' : 'issue'})
        for i in xrange(10) :
            try    : data['issue_%d' % i] = issues[i].text
            except : data['issue_%d' % i] = None
        datastore.save (unique_keys = ['constituency'], data = data)

