import re
import scraperwiki
from BeautifulSoup import BeautifulSoup, NavigableString

starting_url = 'http://www.foodandhealthtraining.org.uk/directory/?apage=%s'

def _text(node, class_name):
    result = node.find(attrs={'class': class_name})
    return result.text if result else ''

def _text_content(node, class_name):
    """Example:
        [u'The Voice of Carers Across Lothian provides is an organisation ... ',
        <br />,
        u'\r\nVOCAL supports carers in all family or relationship settings, ...']
    """
    return ''.join([tag for tag in node.find(attrs={'class': class_name}).contents if type(tag) is NavigableString])

def _address(node):
    pc = _text_content(vcard, 'street-address').strip().split('\n')[-1]
    return _text_content(vcard, 'street-address'), pc

def _url(node):
    a = node.a
    if a:
        return a.text, a['href']
    else:
        return node.text, ''


for i in range(1, 5):
    print 'page', i
    html = scraperwiki.scrape(starting_url % i)
    soup = BeautifulSoup(html)

    for vcard in soup.findAll('div', attrs={'class': 'vcard'}):
        name = _text(vcard, 'fn org')
        _, url = _url(vcard.find(attrs={'class': 'url'}))
        note = _text_content(vcard, 'note')
        # names not used currently
        # given_name = _text(vcard, 'given-name')
        # family_name = _text(vcard, 'family-name')
        street_address, postcode = _address(vcard)
        tel = _text(vcard, 'tel')
        description = '%s%s%s' % (
            note, 
            ('\n%s' % street_address) if street_address else '',
            ('\n%s' % tel) if tel else ''
            )

        record = { 
            'name': name, 
            'url': url, 
            'description': description, 
            'locations': postcode, 
            'tags': '#efht, food, nutrition',
            'address': street_address,
            'tel': tel 
            }
        scraperwiki.sqlite.save(["name"], record) 


