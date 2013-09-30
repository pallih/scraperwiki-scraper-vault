import scraperwiki

import lxml.etree
import lxml.html
import re 

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))
 

 
html = lxml.html.parse('http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/DG_A-Z_LG').getroot()

atoz = html.cssselect('.atoz a')

for letter in atoz:
    print (letter.text_content())

    letter_url = 'http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/DG_A-Z_LG' + letter.get('href')
    letter_html = lxml.html.parse(letter_url).getroot() 
    sub_links = letter_html.cssselect('.subLinks a')
    
    for sub_link in sub_links:
        if 'nalc.gov.uk' not in sub_link.get('href'):
            sub_link_url = 'http://www.direct.gov.uk' + sub_link.get('href')
            sub_link_html = lxml.html.parse(sub_link_url).getroot()
            
            council = sub_link.get('title')
            postcode = 'no match'
    
            print(council)
            
            info_items = sub_link_html.cssselect('.twoColLayout li')
            for info_item in info_items:
               if 'Address' in info_item.text_content():
                  info = info_item.cssselect('.infoContainer')[0]
                  m = re.search('<br />([\w\s]*)</span>\s*', stringify_children(info))
                  if m:
                     postcode = m.group(1)
            
            record = {
                "council" : council,
                "postcode" : postcode
            }
            scraperwiki.datastore.save(["council"], record)
    

import scraperwiki

import lxml.etree
import lxml.html
import re 

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))
 

 
html = lxml.html.parse('http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/DG_A-Z_LG').getroot()

atoz = html.cssselect('.atoz a')

for letter in atoz:
    print (letter.text_content())

    letter_url = 'http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/DG_A-Z_LG' + letter.get('href')
    letter_html = lxml.html.parse(letter_url).getroot() 
    sub_links = letter_html.cssselect('.subLinks a')
    
    for sub_link in sub_links:
        if 'nalc.gov.uk' not in sub_link.get('href'):
            sub_link_url = 'http://www.direct.gov.uk' + sub_link.get('href')
            sub_link_html = lxml.html.parse(sub_link_url).getroot()
            
            council = sub_link.get('title')
            postcode = 'no match'
    
            print(council)
            
            info_items = sub_link_html.cssselect('.twoColLayout li')
            for info_item in info_items:
               if 'Address' in info_item.text_content():
                  info = info_item.cssselect('.infoContainer')[0]
                  m = re.search('<br />([\w\s]*)</span>\s*', stringify_children(info))
                  if m:
                     postcode = m.group(1)
            
            record = {
                "council" : council,
                "postcode" : postcode
            }
            scraperwiki.datastore.save(["council"], record)
    

