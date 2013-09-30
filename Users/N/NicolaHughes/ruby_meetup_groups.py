import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://ruby.meetup.com/all/")
root = lxml.html.fromstring(html)
for li in root.cssselect('.vcard'):
    name = li.cssselect("a.url")[0].text_content()
    link = li.cssselect("a.url")[0].attrib.get('href')
    members = li.cssselect('.note')[0].text_content()

#    mtch = re.match(  '(\d+).*', members ) 
#    if mtch.groups:
#        members = mtch.groups(0)[0]

    locality_list = li.cssselect('.locality')
    locality = len(locality_list) and locality_list[0].text_content() or ''

    region_list = li.cssselect('.region')
    region = len(region_list) and region_list[0].text_content() or ''

    data = {'Name': name, 'Link': link, 'Location': (locality + ", " + region + ", United States"), 'Members': members}
    print data
    if (region != '') and (members[-7:] != 'waiting'):
        scraperwiki.sqlite.save(['Name'], data)import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://ruby.meetup.com/all/")
root = lxml.html.fromstring(html)
for li in root.cssselect('.vcard'):
    name = li.cssselect("a.url")[0].text_content()
    link = li.cssselect("a.url")[0].attrib.get('href')
    members = li.cssselect('.note')[0].text_content()

#    mtch = re.match(  '(\d+).*', members ) 
#    if mtch.groups:
#        members = mtch.groups(0)[0]

    locality_list = li.cssselect('.locality')
    locality = len(locality_list) and locality_list[0].text_content() or ''

    region_list = li.cssselect('.region')
    region = len(region_list) and region_list[0].text_content() or ''

    data = {'Name': name, 'Link': link, 'Location': (locality + ", " + region + ", United States"), 'Members': members}
    print data
    if (region != '') and (members[-7:] != 'waiting'):
        scraperwiki.sqlite.save(['Name'], data)