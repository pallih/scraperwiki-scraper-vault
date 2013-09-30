import scraperwiki
import lxml.html

root = lxml.html.fromstring(scraperwiki.scrape("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0"))
for ahref in root.cssselect("a"):
    text = ahref.text_content()
    if text.find(', Member for ') == -1:
        continue

    print text

    lastname, firstname = text.rsplit(', Member for', 1)[0].split(',')
    fullname = '%s %s' % (firstname.strip(), lastname.strip())
    if fullname.startswith('the '):
        fullname = fullname[4:].strip()

    area = text.split(', Member for', 1)[-1].strip()
    data = {
      'id': ahref.attrib['href'].split('=')[-1],
      'name': fullname,
      'area': area,
    }

    # Lets get some more detailed information
    member_html = scraperwiki.scrape("http://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=%s" % data['id'])
    root = lxml.html.fromstring(member_html)

    for p in root.cssselect('p'):
        text = p.text_content().strip()
        if text.find("Electoral Division") != -1:
            import re
            data['state'] = re.search("Electoral Division of (.*) \((.*)\)", text).groups()[-1].strip()
        if text.find('Party:') != -1:
            data['party'] = text.split(':')[-1].strip()
        if text.find('Electorate Office:') != -1:
            data['office'] = text.split(':')[-1].strip()

    for td in root.cssselect("td[width='50%']"):
        text = td.text_content()
        print text
        if text.find('Title') != -1:
            data['title'] = text.split('.')[0].split(':')[-1].strip()
        
    print data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

import scraperwiki
import lxml.html

root = lxml.html.fromstring(scraperwiki.scrape("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0"))
for ahref in root.cssselect("a"):
    text = ahref.text_content()
    if text.find(', Member for ') == -1:
        continue

    print text

    lastname, firstname = text.rsplit(', Member for', 1)[0].split(',')
    fullname = '%s %s' % (firstname.strip(), lastname.strip())
    if fullname.startswith('the '):
        fullname = fullname[4:].strip()

    area = text.split(', Member for', 1)[-1].strip()
    data = {
      'id': ahref.attrib['href'].split('=')[-1],
      'name': fullname,
      'area': area,
    }

    # Lets get some more detailed information
    member_html = scraperwiki.scrape("http://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=%s" % data['id'])
    root = lxml.html.fromstring(member_html)

    for p in root.cssselect('p'):
        text = p.text_content().strip()
        if text.find("Electoral Division") != -1:
            import re
            data['state'] = re.search("Electoral Division of (.*) \((.*)\)", text).groups()[-1].strip()
        if text.find('Party:') != -1:
            data['party'] = text.split(':')[-1].strip()
        if text.find('Electorate Office:') != -1:
            data['office'] = text.split(':')[-1].strip()

    for td in root.cssselect("td[width='50%']"):
        text = td.text_content()
        print text
        if text.find('Title') != -1:
            data['title'] = text.split('.')[0].split(':')[-1].strip()
        
    print data
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

