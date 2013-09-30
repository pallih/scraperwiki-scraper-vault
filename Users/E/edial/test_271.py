import scraperwiki           
import lxml.html
import urllib2
import urllib

print "Starting"

url = "http://www.britainsbestguides.org/search-results/"
header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=df061eae43d6ec1887d108fe5ea3a06a; __utma=204497347.924939506.1341998344.1342445910.1342787814.8; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }

req = urllib2.Request(url, None, header)  
response = urllib2.urlopen(req)

print "Parsing"

root = lxml.html.fromstring(response.read())

for el in root.cssselect("#body div div div div div p a"): 
     
    page_url = "http://www.britainsbestguides.org" + el.get("href");
    print page_url  
    page_html = scraperwiki.scrape(page_url) 
    page = lxml.html.fromstring(page_html)

    name = page.cssselect("#body #profile_col1 table tr:nth-of-type(1) td.col2 p")
    if name[0].text_content():
        name = name[0].text_content()
    else: 
        name = "empty"
    
    tel = page.cssselect("#body #profile_col1 table tr:nth-of-type(2) td.col2 p")
    if tel[0].text_content():
        tel = tel[0].text_content()
    else:
        tel = "empty"

    email = page.cssselect("#body #profile_col1 table tr:nth-of-type(3) td.col2 p")
    if email[0].text_content():
        email = email[0].text_content()
    else:
        email = "empty"

    specialties = page.cssselect("#body #profile_col1 table tr:nth-of-type(8) td.col2 p")
    if specialties[0].text_content():
        specialties = specialties[0].text_content()
    else:
        specialties = "empty"

    place = page.cssselect("#body #profile_col1 table tr:nth-of-type(9) td.col2 p")
    if place[0].text_content():
        place = place[0].text_content()
    else:
        place = "empty"
    
    print "%s, %s, %s, %s, %s, %s" % (page_url, name, tel, email, specialties, place)
    data = {
        'url' : page_url,
        'name' : name,
        'tel' : tel,
        'email' : email,
        'specialties' : specialties,
        'place' : place
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="england_host_export")import scraperwiki           
import lxml.html
import urllib2
import urllib

print "Starting"

url = "http://www.britainsbestguides.org/search-results/"
header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=df061eae43d6ec1887d108fe5ea3a06a; __utma=204497347.924939506.1341998344.1342445910.1342787814.8; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }

req = urllib2.Request(url, None, header)  
response = urllib2.urlopen(req)

print "Parsing"

root = lxml.html.fromstring(response.read())

for el in root.cssselect("#body div div div div div p a"): 
     
    page_url = "http://www.britainsbestguides.org" + el.get("href");
    print page_url  
    page_html = scraperwiki.scrape(page_url) 
    page = lxml.html.fromstring(page_html)

    name = page.cssselect("#body #profile_col1 table tr:nth-of-type(1) td.col2 p")
    if name[0].text_content():
        name = name[0].text_content()
    else: 
        name = "empty"
    
    tel = page.cssselect("#body #profile_col1 table tr:nth-of-type(2) td.col2 p")
    if tel[0].text_content():
        tel = tel[0].text_content()
    else:
        tel = "empty"

    email = page.cssselect("#body #profile_col1 table tr:nth-of-type(3) td.col2 p")
    if email[0].text_content():
        email = email[0].text_content()
    else:
        email = "empty"

    specialties = page.cssselect("#body #profile_col1 table tr:nth-of-type(8) td.col2 p")
    if specialties[0].text_content():
        specialties = specialties[0].text_content()
    else:
        specialties = "empty"

    place = page.cssselect("#body #profile_col1 table tr:nth-of-type(9) td.col2 p")
    if place[0].text_content():
        place = place[0].text_content()
    else:
        place = "empty"
    
    print "%s, %s, %s, %s, %s, %s" % (page_url, name, tel, email, specialties, place)
    data = {
        'url' : page_url,
        'name' : name,
        'tel' : tel,
        'email' : email,
        'specialties' : specialties,
        'place' : place
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="england_host_export")