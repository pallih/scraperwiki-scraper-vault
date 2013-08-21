import scraperwiki
import json
import sys
from lxml.html import fromstring

"""
BASIC scrape of the trusts with efficiency ...
url = "http://myhospitalguide.drfosterhealth.co.uk"
page = fromstring(scraperwiki.scrape(url))

items = page.cssselect('.popup')
for item in items:
    title = item.cssselect('.title')[0].text_content()
    efficiency = item.cssselect('.figures .efficiency .value')[0].text_content()
    hsmr = item.cssselect('.figures .hsmr .value')[0].text_content()

    scraperwiki.sqlite.save(['title'],{'title':title,'efficiency':int(efficiency),'hsmr':int(hsmr)})
"""

top_level = [
"efficiency",
"hsmr",
"hsmr_banding",
"deaths_after_surgery",
"deaths_after_surgery_banding",
"deaths_in_low_risk_diagnosis_groups",
"deaths_in_low_risk_diagnosis_groups_banding",
"shmi",
"shmi_banding",
"name",
"hsmr_lower",
"hsmr_upper",
"das_lower",
"das_upper",
"dilrdg_lower",
"dilrdg_upper",
"shmi_lower",
"shmi_upper",
]

scraperwiki.sqlite.attach('trusts')
def code_for_trust(t):
    q = '* from trusts.swdata where name="%s"' % (t.upper(),)
    return scraperwiki.sqlite.select(q)

results = scraperwiki.sqlite.select("title from swdata order by title desc")
for row in results:
    results = code_for_trust(row['title'])
    if results:
        code = results[0]['code']
        page = scraperwiki.scrape("http://myhospitalguide.drfosterhealth.co.uk/data/script.php?trust=" + code)
        page = page[1:-2] # strip the func wrapper
        d = json.loads(page)
    
        data = {}
        # grab top level data
        for x in top_level:
            data[x] = d.get(x, "")
        data['lat'] = d['coordinates']['lat']
        data['lng'] = d['coordinates']['lng']
        scraperwiki.sqlite.save(['name'], data, table_name="entries")
        
        for k,v in d.iteritems():
            if isinstance(v, dict):
                v['name'] = data['name']
                scraperwiki.sqlite.save(['name'], v, table_name=k)
    
    #url = "http://myhospitalguide.drfosterhealth.co.uk/data/script.php?trust={code}&callback=x"
import scraperwiki
import json
import sys
from lxml.html import fromstring

"""
BASIC scrape of the trusts with efficiency ...
url = "http://myhospitalguide.drfosterhealth.co.uk"
page = fromstring(scraperwiki.scrape(url))

items = page.cssselect('.popup')
for item in items:
    title = item.cssselect('.title')[0].text_content()
    efficiency = item.cssselect('.figures .efficiency .value')[0].text_content()
    hsmr = item.cssselect('.figures .hsmr .value')[0].text_content()

    scraperwiki.sqlite.save(['title'],{'title':title,'efficiency':int(efficiency),'hsmr':int(hsmr)})
"""

top_level = [
"efficiency",
"hsmr",
"hsmr_banding",
"deaths_after_surgery",
"deaths_after_surgery_banding",
"deaths_in_low_risk_diagnosis_groups",
"deaths_in_low_risk_diagnosis_groups_banding",
"shmi",
"shmi_banding",
"name",
"hsmr_lower",
"hsmr_upper",
"das_lower",
"das_upper",
"dilrdg_lower",
"dilrdg_upper",
"shmi_lower",
"shmi_upper",
]

scraperwiki.sqlite.attach('trusts')
def code_for_trust(t):
    q = '* from trusts.swdata where name="%s"' % (t.upper(),)
    return scraperwiki.sqlite.select(q)

results = scraperwiki.sqlite.select("title from swdata order by title desc")
for row in results:
    results = code_for_trust(row['title'])
    if results:
        code = results[0]['code']
        page = scraperwiki.scrape("http://myhospitalguide.drfosterhealth.co.uk/data/script.php?trust=" + code)
        page = page[1:-2] # strip the func wrapper
        d = json.loads(page)
    
        data = {}
        # grab top level data
        for x in top_level:
            data[x] = d.get(x, "")
        data['lat'] = d['coordinates']['lat']
        data['lng'] = d['coordinates']['lng']
        scraperwiki.sqlite.save(['name'], data, table_name="entries")
        
        for k,v in d.iteritems():
            if isinstance(v, dict):
                v['name'] = data['name']
                scraperwiki.sqlite.save(['name'], v, table_name=k)
    
    #url = "http://myhospitalguide.drfosterhealth.co.uk/data/script.php?trust={code}&callback=x"
