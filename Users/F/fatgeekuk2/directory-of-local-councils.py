import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #
site_base = 'http://www.direct.gov.uk'
base_url = '%s/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/DG_A-Z_LG?indexChar=' % site_base
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
field_nams = ['id', 'Address', 'Phone number', 'Email address', 'Website (opens new window)', 'Opening Hours']
field_maps = {'Website (opens new window)': 'Website'}
class_finder = {'class': 'subLinks'}
for letter in letters:
    html = scraperwiki.scrape(base_url + letter)
    page = BeautifulSoup.BeautifulSoup(html)
    
    councils = page.findAll(**class_finder)
    for council in councils:
        title = council.findAll('a')[0]
        # NALC on http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/index.htm?indexChar=N uses an http:// URL rather than /
        if title['href'][0]=='/':
            # data = {'name': title.string, }
            # datastore.save(unique_keys=['name'], data = data)
            html2 = scraperwiki.scrape('%s%s' % (site_base, title['href']))
            page2 = BeautifulSoup.BeautifulSoup(html2)
            fields = {}
            for element in page2.findAll('div', 'headingContainer'):
                name = element.findAll('strong')[0].text
                value_node = element.findNextSibling(True)
                value = value_node.findAll('span')[0].text
                print "%s = %s" % (name, value)
                name = field_maps.get(name, name)
                # sanitise the value
                if name=='Address':
                    value = value_node.findAll('span')[0].contents
                    print value[0].__class__.__name__
                    vals = [v for v in value if isinstance(v, BeautifulSoup.NavigableString)]
                
                    value = ', '.join(vals)
                    print "Address Value = %s" % value
                fields[name] = value
            fields['name'] = title.string
            fields['id'] = title['href']
            datastore.save(unique_keys=['name'], data=fields)
        

