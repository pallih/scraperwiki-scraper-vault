# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html  
import re

html = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/Default.aspx?CatID=103&letter=%")
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
ul = root.cssselect("div#M3_pnlWorkPlace")
a = ul[0].cssselect("a")


for item in a:
    #print "Fetching http://portal.gov.sk/Portal/sk/" + item.attrib.get('href')
    matchObj = re.search( 'cityID=([0-9]{1,})', item.attrib.get('href'), re.I|re.M)
    result_id = matchObj.group(1)
    getpage = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/" + item.attrib.get('href'))
    getroot = lxml.html.fromstring(getpage)
    div = getroot.cssselect("div#M3_divContact")
    result_name = div[0].cssselect("span#M3_lbNazov")[0].text_content()
    result_starosta = div[0].cssselect("span#M3_lbStarosta")[0].text_content().split(': ')[1]
    result_starosta = result_starosta.replace('&nbsp;', '').strip()
    result_street = div[0].cssselect("span#M3_lbUrad_ulica")[0].text_content()
    result_city = div[0].cssselect("span#M3_lbUrad_mesto")[0].text_content()
    result_psc = div[0].cssselect("span#M3_lbUrad_psc")[0].text_content()
    result_phone = div[0].cssselect("span#M3_lbUrad_telefon")[0].text_content()
    if "Tele" in result_phone:
        result_phone = result_phone.split(': ')[1]
    result_fax = div[0].cssselect("span#M3_lbUrad_fax")[0].text_content()
    if "Fax" in result_fax:
        result_fax = result_fax.split(': ')[1]
    result_mail = div[0].cssselect("a#M3_hlUrad_email")[0].text_content()
    result_web = div[0].cssselect("a#M3_hlUrad_web")[0].text_content()
    data = {
        'Id': result_id,
        'Name': result_name,
        'Mayor': result_starosta,
        'Street': result_street,
        'City': result_city,
        'Post code': result_psc,
        'Phone': result_phone,
        'Fax': result_fax,
        'Mail': result_mail,
        'Web': result_web,
    }
    scraperwiki.sqlite.save(unique_keys=["Id"], data=data)           
    


# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html  
import re

html = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/Default.aspx?CatID=103&letter=%")
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
ul = root.cssselect("div#M3_pnlWorkPlace")
a = ul[0].cssselect("a")


for item in a:
    #print "Fetching http://portal.gov.sk/Portal/sk/" + item.attrib.get('href')
    matchObj = re.search( 'cityID=([0-9]{1,})', item.attrib.get('href'), re.I|re.M)
    result_id = matchObj.group(1)
    getpage = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/" + item.attrib.get('href'))
    getroot = lxml.html.fromstring(getpage)
    div = getroot.cssselect("div#M3_divContact")
    result_name = div[0].cssselect("span#M3_lbNazov")[0].text_content()
    result_starosta = div[0].cssselect("span#M3_lbStarosta")[0].text_content().split(': ')[1]
    result_starosta = result_starosta.replace('&nbsp;', '').strip()
    result_street = div[0].cssselect("span#M3_lbUrad_ulica")[0].text_content()
    result_city = div[0].cssselect("span#M3_lbUrad_mesto")[0].text_content()
    result_psc = div[0].cssselect("span#M3_lbUrad_psc")[0].text_content()
    result_phone = div[0].cssselect("span#M3_lbUrad_telefon")[0].text_content()
    if "Tele" in result_phone:
        result_phone = result_phone.split(': ')[1]
    result_fax = div[0].cssselect("span#M3_lbUrad_fax")[0].text_content()
    if "Fax" in result_fax:
        result_fax = result_fax.split(': ')[1]
    result_mail = div[0].cssselect("a#M3_hlUrad_email")[0].text_content()
    result_web = div[0].cssselect("a#M3_hlUrad_web")[0].text_content()
    data = {
        'Id': result_id,
        'Name': result_name,
        'Mayor': result_starosta,
        'Street': result_street,
        'City': result_city,
        'Post code': result_psc,
        'Phone': result_phone,
        'Fax': result_fax,
        'Mail': result_mail,
        'Web': result_web,
    }
    scraperwiki.sqlite.save(unique_keys=["Id"], data=data)           
    


# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html  
import re

html = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/Default.aspx?CatID=103&letter=%")
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
ul = root.cssselect("div#M3_pnlWorkPlace")
a = ul[0].cssselect("a")


for item in a:
    #print "Fetching http://portal.gov.sk/Portal/sk/" + item.attrib.get('href')
    matchObj = re.search( 'cityID=([0-9]{1,})', item.attrib.get('href'), re.I|re.M)
    result_id = matchObj.group(1)
    getpage = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/" + item.attrib.get('href'))
    getroot = lxml.html.fromstring(getpage)
    div = getroot.cssselect("div#M3_divContact")
    result_name = div[0].cssselect("span#M3_lbNazov")[0].text_content()
    result_starosta = div[0].cssselect("span#M3_lbStarosta")[0].text_content().split(': ')[1]
    result_starosta = result_starosta.replace('&nbsp;', '').strip()
    result_street = div[0].cssselect("span#M3_lbUrad_ulica")[0].text_content()
    result_city = div[0].cssselect("span#M3_lbUrad_mesto")[0].text_content()
    result_psc = div[0].cssselect("span#M3_lbUrad_psc")[0].text_content()
    result_phone = div[0].cssselect("span#M3_lbUrad_telefon")[0].text_content()
    if "Tele" in result_phone:
        result_phone = result_phone.split(': ')[1]
    result_fax = div[0].cssselect("span#M3_lbUrad_fax")[0].text_content()
    if "Fax" in result_fax:
        result_fax = result_fax.split(': ')[1]
    result_mail = div[0].cssselect("a#M3_hlUrad_email")[0].text_content()
    result_web = div[0].cssselect("a#M3_hlUrad_web")[0].text_content()
    data = {
        'Id': result_id,
        'Name': result_name,
        'Mayor': result_starosta,
        'Street': result_street,
        'City': result_city,
        'Post code': result_psc,
        'Phone': result_phone,
        'Fax': result_fax,
        'Mail': result_mail,
        'Web': result_web,
    }
    scraperwiki.sqlite.save(unique_keys=["Id"], data=data)           
    


# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html  
import re

html = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/Default.aspx?CatID=103&letter=%")
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
ul = root.cssselect("div#M3_pnlWorkPlace")
a = ul[0].cssselect("a")


for item in a:
    #print "Fetching http://portal.gov.sk/Portal/sk/" + item.attrib.get('href')
    matchObj = re.search( 'cityID=([0-9]{1,})', item.attrib.get('href'), re.I|re.M)
    result_id = matchObj.group(1)
    getpage = scraperwiki.scrape("http://portal.gov.sk/Portal/sk/" + item.attrib.get('href'))
    getroot = lxml.html.fromstring(getpage)
    div = getroot.cssselect("div#M3_divContact")
    result_name = div[0].cssselect("span#M3_lbNazov")[0].text_content()
    result_starosta = div[0].cssselect("span#M3_lbStarosta")[0].text_content().split(': ')[1]
    result_starosta = result_starosta.replace('&nbsp;', '').strip()
    result_street = div[0].cssselect("span#M3_lbUrad_ulica")[0].text_content()
    result_city = div[0].cssselect("span#M3_lbUrad_mesto")[0].text_content()
    result_psc = div[0].cssselect("span#M3_lbUrad_psc")[0].text_content()
    result_phone = div[0].cssselect("span#M3_lbUrad_telefon")[0].text_content()
    if "Tele" in result_phone:
        result_phone = result_phone.split(': ')[1]
    result_fax = div[0].cssselect("span#M3_lbUrad_fax")[0].text_content()
    if "Fax" in result_fax:
        result_fax = result_fax.split(': ')[1]
    result_mail = div[0].cssselect("a#M3_hlUrad_email")[0].text_content()
    result_web = div[0].cssselect("a#M3_hlUrad_web")[0].text_content()
    data = {
        'Id': result_id,
        'Name': result_name,
        'Mayor': result_starosta,
        'Street': result_street,
        'City': result_city,
        'Post code': result_psc,
        'Phone': result_phone,
        'Fax': result_fax,
        'Mail': result_mail,
        'Web': result_web,
    }
    scraperwiki.sqlite.save(unique_keys=["Id"], data=data)           
    


