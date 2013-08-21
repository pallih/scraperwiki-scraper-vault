#-*-coding:utf-8-*-
from lxml.etree import fromstring
import lxml.etree as ET
import re

import scraperwiki

#def scrape(url):
#    import urllib2
#    f = urllib2.urlopen(url)
#    return f.read()
    
def parse_html(html):
    parser = ET.HTMLParser(remove_comments=True,remove_blank_text=True,remove_pis=True)
    return ET.HTML(html,parser=parser)

# get all Bundestag MPs from D-API
try:
    xml = scraperwiki.scrape('http://v1.d-api.de/parlament.bund.politiker?output_type=xml&limit=2000')
    print "got Parlament.Bund.Politiker from d-api.de"
except:
    raise Exception("error getting Politiker from d-api.de")
    

tree = fromstring(xml)
politicians = tree.xpath("/d-api/data/item")
for politician in politicians:
    dapi_id = int(politician.xpath("id")[0].text)
    bundestag_url = politician.xpath("bundestag_bio_url")[0].text
    data = {"dapi_id": dapi_id}
    try:
        html = scraperwiki.scrape(bundestag_url)
        print "Got %s" % bundestag_url
    except Exception, e:
        print e
        print "Error getting: %s" % bundestag_url
        continue

    ptree = parse_html(html)
    voa = ptree.xpath('//div[@class="infoBox voa"]/div[@class="standardBox"]')[0]
    incomes = []
    current_income = None
    current_kind = None
    for child in voa:
        if child.tag == "h3":
            try:
                current_kind = int(child.text.split(".")[0])
            except (ValueError, IndexError):
                current_kind = 0
            if current_income is not None:
                incomes.append(current_income)
                current_income = None
        elif child.tag == "p":
            if "class" in child.attrib and "kleinAbstand" in child.attrib["class"]:
                break
            if "class" in child.attrib and "voa_tab1" in child.attrib["class"]:
                have_any = child.find("strong")
                if have_any is not None and have_any.tag == "strong" and "Keine ver" in have_any.text:
                    break
                if current_income is not None:
                    incomes.append(current_income)
                    current_income = None
            if current_income is None:
                current_income = {"description": [], "kind": current_kind}
            if child.text is not None:
                current_income["description"].append(child.text)
    if current_income is not None:
        incomes.append(current_income)
        
    for income in incomes:
        positions = []
        for lastline in income["description"]:
            lastline = lastline.split(", ")
            level = None
            repeat = None
            try:
                if u"Stufe " in lastline[-1]:
                    match = re.search("Stufe (\d)", lastline[-1])
                    if match:
                        level = int(match.group(1))
                    if u"monatlich" in lastline[-2]:
                        repeat = "monthly"
                    elif u"jährlich" in lastline[-2]:
                        repeat = "yearly"
                    elif re.match("^(\d{4})$", lastline[-1].strip()):
                        repeat = int(lastline[-2].strip())
            except Exception as e:
                print e
            if repeat is not None or level is not None:
                positions.append({"repeat": repeat, "level": level})
        income["positions"] = positions
    data["extra_income"] = incomes
    scraperwiki.sqlite.save(unique_keys=["dapi_id"], data=data)
