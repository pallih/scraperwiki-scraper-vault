import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

for td in root.cssselect('td'):
    data = {'table_cell': td.text} # save data in dictionary
    data["date"] = "2009-03-02"
    data["latlng_lat"], data["latlng_lng"] = latlng
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data)import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

for td in root.cssselect('td'):
    data = {'table_cell': td.text} # save data in dictionary
    data["date"] = "2009-03-02"
    data["latlng_lat"], data["latlng_lng"] = latlng
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data)