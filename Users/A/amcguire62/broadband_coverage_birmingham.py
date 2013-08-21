import scraperwiki
import mechanize
import urllib2

scraperwiki.sqlite.attach("uk_postcodes_from_codepoint")


def Main():
    #postcodes = GetBirminghamPostcodes()
    br = mechanize.Browser()
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open("http://shop.virginmedia.com/broadband.html?i=988")
    br.select_form(nr=0)
    print br.form
    br.form["postcode"] = "B120QP"
    response = br.submit()
    print response.read()

    

def GetBirminghamPostcodes():
    ldata = scraperwiki.sqlite.execute("""select Postcode from swdata 
where 
Postcode like 'B1%' or
Postcode like 'B2%' or
Postcode like 'B3%' or
Postcode like 'B4%' or
Postcode like 'B5%' or
Postcode like 'B6%' or
Postcode like 'B7%' or
Postcode like 'B8%' or
Postcode like 'B9%'
order by Postcode
limit 1000000""")["data"]
    postcodes = [ x[0]  for x in ldata]
    return postcodes

#Main()
#http://hidemyass.com/proxy-list/
proxy=[urllib2.ProxyHandler({'http':'101.44.1.106:80'})];
opener=urllib2.build_opener(*proxy);
f=opener.open('http://shop.virginmedia.com/broadband.html?i=988');
print f.read();

#scraperwiki.scrape("http://shop.virginmedia.com/broadband.html?i=988")