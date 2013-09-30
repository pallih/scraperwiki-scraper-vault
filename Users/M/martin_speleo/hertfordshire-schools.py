import scraperwiki
import BeautifulSoup
import re
print help(scraperwiki.datastore.save)
from scraperwiki import datastore

postcode = re.compile("^(.*?),?\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZA-Z])\s*$")

#scrape page
html = scraperwiki.scrape('http://www.hertsdirect.org/scholearn/schadd/schools/')
page = BeautifulSoup.BeautifulSoup(html)
for script in page.findAll("script"):
    for content in script.contents:
        for line in content.splitlines():
            match = re.match("az\['[A-Z]'\].push\(\['(.*)','(.*)'\]\);", line)
            if match:
                data = {}
                latlng = []
                name, url = match.groups()
                school_html = scraperwiki.scrape('http://www.hertsdirect.org/' + url)
                school_page = BeautifulSoup.BeautifulSoup(school_html)
                school_divs = school_page.findAll("div", {"class": "school"})
                assert len(school_divs) == 1
                school_div = school_divs[0]
                names = school_div.findAll("h2")
                assert len(names) == 1 and len(names[0].contents) == 1
                data["name"] = names[0].contents[0]
                school_tables = school_div.findAll("table", {"class": "school_table"})
                assert len(school_tables) == 1    
                school_table = school_tables[0] 
                rows = school_table.findAll("tr")
                for row in rows:
                    labels = row.findAll("td", {"class": "label"})
                    values = row.findAll("td", {"class": "value"})
                    if len(labels) == 1 and len(values) == 1 and len(labels[0].contents) == 1 and len(labels[0].contents) == 1:
                        links = values[0].findAll("a")
                        if links:
                            contents = links[0].contents[0] 
                        else:
                            while values[0].br:
                                values[0].br.replaceWith(", ")                 
                            contents = "".join(values[0].contents)
                        key = unicode(labels[0].contents[0]).rstrip(u": ")   
                        if key == u"Address":
                            p = postcode.match(contents)
                            if p:
                                data[key] = p.group(1)
                                data[u"Postcode"] = p.group(2) + " " + p.group(3)
                                latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u"Postcode"])
                                print latlng
                            else:
                                data[key] = unicode(contents)
                        else:
                            data[key] = unicode(contents)
                    else:
                        assert len(labels) == 0 and len(values) == 0
                datastore.save(unique_keys=["name"], data=data, latlng=latlng)
import scraperwiki
import BeautifulSoup
import re
print help(scraperwiki.datastore.save)
from scraperwiki import datastore

postcode = re.compile("^(.*?),?\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABDEFGHJLNPQRSTUWXYZ][ABDEFGHJLNPQRSTUWXYZA-Z])\s*$")

#scrape page
html = scraperwiki.scrape('http://www.hertsdirect.org/scholearn/schadd/schools/')
page = BeautifulSoup.BeautifulSoup(html)
for script in page.findAll("script"):
    for content in script.contents:
        for line in content.splitlines():
            match = re.match("az\['[A-Z]'\].push\(\['(.*)','(.*)'\]\);", line)
            if match:
                data = {}
                latlng = []
                name, url = match.groups()
                school_html = scraperwiki.scrape('http://www.hertsdirect.org/' + url)
                school_page = BeautifulSoup.BeautifulSoup(school_html)
                school_divs = school_page.findAll("div", {"class": "school"})
                assert len(school_divs) == 1
                school_div = school_divs[0]
                names = school_div.findAll("h2")
                assert len(names) == 1 and len(names[0].contents) == 1
                data["name"] = names[0].contents[0]
                school_tables = school_div.findAll("table", {"class": "school_table"})
                assert len(school_tables) == 1    
                school_table = school_tables[0] 
                rows = school_table.findAll("tr")
                for row in rows:
                    labels = row.findAll("td", {"class": "label"})
                    values = row.findAll("td", {"class": "value"})
                    if len(labels) == 1 and len(values) == 1 and len(labels[0].contents) == 1 and len(labels[0].contents) == 1:
                        links = values[0].findAll("a")
                        if links:
                            contents = links[0].contents[0] 
                        else:
                            while values[0].br:
                                values[0].br.replaceWith(", ")                 
                            contents = "".join(values[0].contents)
                        key = unicode(labels[0].contents[0]).rstrip(u": ")   
                        if key == u"Address":
                            p = postcode.match(contents)
                            if p:
                                data[key] = p.group(1)
                                data[u"Postcode"] = p.group(2) + " " + p.group(3)
                                latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u"Postcode"])
                                print latlng
                            else:
                                data[key] = unicode(contents)
                        else:
                            data[key] = unicode(contents)
                    else:
                        assert len(labels) == 0 and len(values) == 0
                datastore.save(unique_keys=["name"], data=data, latlng=latlng)
