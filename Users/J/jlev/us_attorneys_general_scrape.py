import scraperwiki
import lxml.html   

def full_text_contents(node):
    #returns a string of the full text contents of a node, without stripping <br />
    #from https://scraperwiki.com/scrapers/new/python?template=tutorial-lxml-html
    full_text = node.text + "".join(map(lxml.etree.tostring, list(node)))
    #clear html glyphs
    full_text = full_text.replace('&#13;','')
    return full_text

html = scraperwiki.scrape("http://web.archive.org/web/20110106111854/http://www.naag.org/current-attorneys-general.php")
#use the archive.org cache, because the naag site sometimes times out, and I can't pass a timeout value to scrape()
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[bgcolor='#F1F2F3'] tr"):
    data = {}
    image = tr.cssselect("td")[0].cssselect("img")[0].get('src')
    image_url = image.split("http://")[2] #or 1 if not using the archive.org cached version
    data['image_url'] = image_url

    info = tr.cssselect("td")[1]
    info_name = info.cssselect("h1")[0].text_content()
    try:
        full_name,party = info_name.split(' (')
        party = party[:-1] #trim trailing )
        data['full_name'] = full_name
        data['party'] = party
    except Exception:
        data['full_name']= info_name
    
    info_state = info.cssselect('h3')[0]
    info_state_contents = full_text_contents(info_state)
    title,date = info_state_contents.split('<br />')
    data['state'] = title.split('Attorney General')[0] #full state name, not abbr
    data['date'] = date.split('\n')[1:][0]

    info_contact = info.cssselect('p')[0]
    info_contact_contents = full_text_contents(info_contact)

    address,phone,link = info_contact_contents.split('<br />')
    data['address'] = address
    data['phone'] = phone
    data['url'] = lxml.html.fromstring(link).text

    #print data
    scraperwiki.sqlite.save(unique_keys=['state'], data=data)
import scraperwiki
import lxml.html   

def full_text_contents(node):
    #returns a string of the full text contents of a node, without stripping <br />
    #from https://scraperwiki.com/scrapers/new/python?template=tutorial-lxml-html
    full_text = node.text + "".join(map(lxml.etree.tostring, list(node)))
    #clear html glyphs
    full_text = full_text.replace('&#13;','')
    return full_text

html = scraperwiki.scrape("http://web.archive.org/web/20110106111854/http://www.naag.org/current-attorneys-general.php")
#use the archive.org cache, because the naag site sometimes times out, and I can't pass a timeout value to scrape()
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[bgcolor='#F1F2F3'] tr"):
    data = {}
    image = tr.cssselect("td")[0].cssselect("img")[0].get('src')
    image_url = image.split("http://")[2] #or 1 if not using the archive.org cached version
    data['image_url'] = image_url

    info = tr.cssselect("td")[1]
    info_name = info.cssselect("h1")[0].text_content()
    try:
        full_name,party = info_name.split(' (')
        party = party[:-1] #trim trailing )
        data['full_name'] = full_name
        data['party'] = party
    except Exception:
        data['full_name']= info_name
    
    info_state = info.cssselect('h3')[0]
    info_state_contents = full_text_contents(info_state)
    title,date = info_state_contents.split('<br />')
    data['state'] = title.split('Attorney General')[0] #full state name, not abbr
    data['date'] = date.split('\n')[1:][0]

    info_contact = info.cssselect('p')[0]
    info_contact_contents = full_text_contents(info_contact)

    address,phone,link = info_contact_contents.split('<br />')
    data['address'] = address
    data['phone'] = phone
    data['url'] = lxml.html.fromstring(link).text

    #print data
    scraperwiki.sqlite.save(unique_keys=['state'], data=data)
