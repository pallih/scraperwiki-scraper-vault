import scraperwiki
import lxml.html

dateofbirth = lxml.html.fromstring(scraperwiki.scrape("http://www.aph.gov.au/Library/parl/43/mpsbyage.htm"))
dob = {}
for td in dateofbirth.cssselect("td"):
    if td.getnext() is None:
        continue
    name = td.getnext().text_content().strip()
    if not name:
        continue

    if name.lower().startswith("sen "):
        name = name[4:]
    firstname = name.split()[0]
    if firstname == "Hon":
        firstname += " "+name.split()[1]
    lastname = name.split()[-1]

    dob["%s %s" % (firstname, lastname)] = td.text_content().strip()
print dob

root = lxml.html.fromstring(scraperwiki.scrape("http://www.aph.gov.au/senate/senators/homepages/index.asp"))
for ahref in root.cssselect("li[style='margin-top:6px;'] a"):
    text = ahref.text_content()
    if text.find('- Senator for') == -1:
        continue

    print text

    lastname, firstname = text.rsplit('-', 1)[0].split(',')
    fullname = '%s %s' % (firstname.strip(), lastname.strip())
    if fullname.startswith('the '):
        fullname = fullname[4:]

    state = text.split('for')[-1]
    data = {
      'id': ahref.attrib['href'].split('=')[-1],
      'name': fullname,
      'state': state,
    }

    if fullname in dob:
        data['dob'] = dob[fullname]  

    # Lets get some more detailed information
    senator_html = scraperwiki.scrape("http://www.aph.gov.au/senate/senators/homepages/senators.asp?id=%s" % data['id'])
    root = lxml.html.fromstring(senator_html)

    for p in root.cssselect('p'):
        text = p.text_content()
        if text.find('Party:') != -1:
            data['party'] = text.split(':')[-1]
        if text.find('Electorate Office:') != -1:
            data['office'] = text.split(':')[-1]

    for p in root.cssselect('table[cellpadding=0] td'):
        text = p.text_content()
        if text.find('Phone:') != -1:
            data['phone'] = p.getnext().text_content()
        if text.find('Fax:') != -1:
            data['fax'] = p.getnext().text_content()

    for p in root.cssselect('table[cellpadding=2] td'):
        text = p.text_content()
        if text.find('Phone:') != -1:
            data['office phone'] = p.getnext().text_content()
        if text.find('Fax:') != -1:
            data['office fax'] = p.getnext().text_content()

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

