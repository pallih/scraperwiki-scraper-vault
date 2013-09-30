import scraperwiki
from lxml import etree
import re


zero = piu = postcodes = []

url = 'http://www.justice.gov.uk/contacts/prison-finder'
html = scraperwiki.scrape(url)

doc = etree.HTML(html)

xpath_s = "//select[@id='all-prisons']//option"

for prison in doc.xpath(xpath_s):

    if prison.xpath('@value')[0] == '-':
        continue

    record = {}
    record["prison_name"] = prison.text
    record["prison_url"] = prison.xpath('@value')[0]

    sub_html = scraperwiki.scrape(record["prison_url"])
    sub_doc = etree.HTML(sub_html)

    xpath_image_s = "//img[@class='imageLeft']"
    
    for u in sub_doc.xpath(xpath_image_s):
        #print u.xpath("@src")[0]
        record["image_url"] = u.xpath("@src")[0]

    # postcode regular expression ( http://stackoverflow.com/questions/378157/python-regular-expression-postcode-search )
    postcodes = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9O][ABD-HJLNP-UW-Z]{2}\b', sub_html)

    if record["prison_name"].startswith("Prescoed - Cymraeg"):
        record["postcode"] = 'NP14 0TD'

    elif record["prison_name"].startswith("Parkhurst"):
        record["postcode"] = 'PO30 5NX'

    if len (postcodes) == 0:
        print 'zero: ', record["prison_name"] , postcodes
        zero.append(record["prison_url"])

    elif len (postcodes) > 1:
        print 'piu: ', record["prison_name"] , postcodes
        piu.append(record["prison_url"])
        record["postcode"] = postcodes[0]

    else: 
        record["postcode"] = postcodes[0]
    
    #scraperwiki.sqlite.save(["prison_name"], record) 

print zero
print piu




import scraperwiki
from lxml import etree
import re


zero = piu = postcodes = []

url = 'http://www.justice.gov.uk/contacts/prison-finder'
html = scraperwiki.scrape(url)

doc = etree.HTML(html)

xpath_s = "//select[@id='all-prisons']//option"

for prison in doc.xpath(xpath_s):

    if prison.xpath('@value')[0] == '-':
        continue

    record = {}
    record["prison_name"] = prison.text
    record["prison_url"] = prison.xpath('@value')[0]

    sub_html = scraperwiki.scrape(record["prison_url"])
    sub_doc = etree.HTML(sub_html)

    xpath_image_s = "//img[@class='imageLeft']"
    
    for u in sub_doc.xpath(xpath_image_s):
        #print u.xpath("@src")[0]
        record["image_url"] = u.xpath("@src")[0]

    # postcode regular expression ( http://stackoverflow.com/questions/378157/python-regular-expression-postcode-search )
    postcodes = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9O][ABD-HJLNP-UW-Z]{2}\b', sub_html)

    if record["prison_name"].startswith("Prescoed - Cymraeg"):
        record["postcode"] = 'NP14 0TD'

    elif record["prison_name"].startswith("Parkhurst"):
        record["postcode"] = 'PO30 5NX'

    if len (postcodes) == 0:
        print 'zero: ', record["prison_name"] , postcodes
        zero.append(record["prison_url"])

    elif len (postcodes) > 1:
        print 'piu: ', record["prison_name"] , postcodes
        piu.append(record["prison_url"])
        record["postcode"] = postcodes[0]

    else: 
        record["postcode"] = postcodes[0]
    
    #scraperwiki.sqlite.save(["prison_name"], record) 

print zero
print piu




import scraperwiki
from lxml import etree
import re


zero = piu = postcodes = []

url = 'http://www.justice.gov.uk/contacts/prison-finder'
html = scraperwiki.scrape(url)

doc = etree.HTML(html)

xpath_s = "//select[@id='all-prisons']//option"

for prison in doc.xpath(xpath_s):

    if prison.xpath('@value')[0] == '-':
        continue

    record = {}
    record["prison_name"] = prison.text
    record["prison_url"] = prison.xpath('@value')[0]

    sub_html = scraperwiki.scrape(record["prison_url"])
    sub_doc = etree.HTML(sub_html)

    xpath_image_s = "//img[@class='imageLeft']"
    
    for u in sub_doc.xpath(xpath_image_s):
        #print u.xpath("@src")[0]
        record["image_url"] = u.xpath("@src")[0]

    # postcode regular expression ( http://stackoverflow.com/questions/378157/python-regular-expression-postcode-search )
    postcodes = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9O][ABD-HJLNP-UW-Z]{2}\b', sub_html)

    if record["prison_name"].startswith("Prescoed - Cymraeg"):
        record["postcode"] = 'NP14 0TD'

    elif record["prison_name"].startswith("Parkhurst"):
        record["postcode"] = 'PO30 5NX'

    if len (postcodes) == 0:
        print 'zero: ', record["prison_name"] , postcodes
        zero.append(record["prison_url"])

    elif len (postcodes) > 1:
        print 'piu: ', record["prison_name"] , postcodes
        piu.append(record["prison_url"])
        record["postcode"] = postcodes[0]

    else: 
        record["postcode"] = postcodes[0]
    
    #scraperwiki.sqlite.save(["prison_name"], record) 

print zero
print piu




import scraperwiki
from lxml import etree
import re


zero = piu = postcodes = []

url = 'http://www.justice.gov.uk/contacts/prison-finder'
html = scraperwiki.scrape(url)

doc = etree.HTML(html)

xpath_s = "//select[@id='all-prisons']//option"

for prison in doc.xpath(xpath_s):

    if prison.xpath('@value')[0] == '-':
        continue

    record = {}
    record["prison_name"] = prison.text
    record["prison_url"] = prison.xpath('@value')[0]

    sub_html = scraperwiki.scrape(record["prison_url"])
    sub_doc = etree.HTML(sub_html)

    xpath_image_s = "//img[@class='imageLeft']"
    
    for u in sub_doc.xpath(xpath_image_s):
        #print u.xpath("@src")[0]
        record["image_url"] = u.xpath("@src")[0]

    # postcode regular expression ( http://stackoverflow.com/questions/378157/python-regular-expression-postcode-search )
    postcodes = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9O][ABD-HJLNP-UW-Z]{2}\b', sub_html)

    if record["prison_name"].startswith("Prescoed - Cymraeg"):
        record["postcode"] = 'NP14 0TD'

    elif record["prison_name"].startswith("Parkhurst"):
        record["postcode"] = 'PO30 5NX'

    if len (postcodes) == 0:
        print 'zero: ', record["prison_name"] , postcodes
        zero.append(record["prison_url"])

    elif len (postcodes) > 1:
        print 'piu: ', record["prison_name"] , postcodes
        piu.append(record["prison_url"])
        record["postcode"] = postcodes[0]

    else: 
        record["postcode"] = postcodes[0]
    
    #scraperwiki.sqlite.save(["prison_name"], record) 

print zero
print piu




