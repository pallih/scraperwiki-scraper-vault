import scraperwiki
import lxml.html
import re

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)

base_url = "http://morristown-nj.org/"

for letter in char_range('A', 'Z'):
    html = scraperwiki.scrape(base_url + "rlist.html?let=" + letter)
    root = lxml.html.fromstring(html)
    for restaurant_link in root.cssselect("table li > a"):
        name = restaurant_link.text_content()
        link = restaurant_link.attrib.get('href')
        r_id = re.search(r"bid=(\d+)", link).group(1)
        print "%s: %s" %(name, link)
        r_html = scraperwiki.scrape(base_url + link)
        r_root = lxml.html.fromstring(r_html)
        address = r_root.xpath("//table//table//table//center/center")[0].text_content()
        print address
        
        r_data = {
            "name": name,
            "link": base_url + link,
            "rid": r_id,
            "address": address,
            "street": re.search(r"(.+?)\s*Morristown", address).group(1).strip()
        }
        for line in r_root.cssselect("table table table table table tr"):
            tds = line.cssselect("td")
            key = tds[0].text_content()
            key = re.sub(r"[^a-zA-Z]", "", key)
            value = tds[1].text_content()
            print " - %s: %s" % (key, value)
            r_data[key] = value
        scraperwiki.sqlite.save(unique_keys=['rid'], data=r_data)