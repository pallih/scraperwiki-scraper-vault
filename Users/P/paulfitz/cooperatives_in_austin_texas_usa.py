import re

import scraperwiki           
txt = scraperwiki.scrape("http://www.austincooperatives.coop/")

from lxml import html           
from lxml import etree           

root = html.fromstring(txt)
category = ""
ready = False

def cleanup(s):
    s = s.replace("\r\n","")
    s = re.sub(r'  +'," ",s)
    s = s.lstrip()
    s = s.rstrip()
    return s

for entry in root.cssselect("td"):
    parts = entry.xpath(".//text()")
    if len(parts)==1:
        category = cleanup(parts[0])
        if category == "Student Housing Co-ops":
            ready = True
    if len(parts)<3:
        continue
    if not(ready):
        continue
    print category, "parts", parts
    data = {
          'title' : cleanup(parts[0]),
          'category': category,
        }
    prev = ""
    for p in parts:
        if re.search("http://",p):
            data['website'] = cleanup(p)
        if re.search("[.][0-9][0-9][0-9][.]",p):
            if re.search("fax",p):
                data['fax'] = cleanup(p)
            else:
                data['phone'] = cleanup(p)
        if re.search("Austin, TX",p):
            data['address2'] = cleanup(p)
            data['address1'] = cleanup(prev)
        if re.search("document.write",p):
            m = re.search(r"document\.write\(\['([^']+)','([^']+)'",p)
            mail_user = m.group(1)
            mail_host = m.group(2)
            print "email:", mail_user, "@", mail_host
            data['mail_user'] = mail_user
            data['mail_host'] = mail_host
        prev = p
    print data
        
    scraperwiki.sqlite.save(unique_keys=['title'], table_name="main", data=data)

    nesting = entry.cssselect("ul")
    if len(nesting)==0:
        continue

    # We have some nested organizations
    orgs = nesting[0].cssselect("li")
    for org in orgs:
        print "  org", org.text_content()
        parts = org.xpath(".//text()")
        data2 = {
              'title' : cleanup(parts[0]),
              'address': cleanup(parts[1])
        }
        scraperwiki.sqlite.save(unique_keys=['title'], table_name=data['title'], data=data2)
