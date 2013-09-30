# NF NC Trail Data

import re
import json
import datetime
import scraperwiki
import lxml.html
import html5lib

from html5lib import treebuilders
html5Parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)

UPDATE_CACHE=False   ## Set to True to re-download all pages (False for dev and resume if flaky server)
START_ITER = 0       ## Link to start on (350)
STOP_ITER = 10000    ## Link to end on (400)

def cacheLookup(url, update_cache=False):
    """Simple cache of scraped pages for development"""
    #print "Checking local cache for {0}...".format(url)
    result = scraperwiki.sqlite.select("url, timestamp, src FROM sources WHERE url = ?", [url])
    if not result or update_cache:
        print "No Cache for this site (or force-update flag given), scraping live site for local cache..."
        src = scraperwiki.scrape(url)
        scraperwiki.sqlite.execute("INSERT OR REPLACE INTO sources VALUES (?, ?, ?)",
            [url, datetime.datetime.now().isoformat(), src])
        scraperwiki.sqlite.commit()
        print "Cache saved."
        return src

    else:
        #print "Data already exists for {0}, using local cache...".format(url)
        return result[0].get("src")

def txt_delim(node, delim="\n"):
    txt_elements = []
    for e in node:
        if hasattr(e, 'text_content'):
           txt_elements.append(e.text_content().strip())

        else:
           txt_elements.append(e.strip())

    return delim.join(txt_elements).strip()

## Setup data stores
scraperwiki.sqlite.execute(
    "CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, src TEXT)")

scraperwiki.sqlite.execute("""DROP TABLE IF EXISTS trails""")
scraperwiki.sqlite.execute("""
    CREATE TABLE IF NOT EXISTS trails(
        iter INTEGER,
        url TEXT PRIMARY KEY,
        num TEXT,
        name TEXT,
        season TEXT,
        usage TEXT,
        restrictions TEXT,
        water TEXT,
        restroom TEXT,
        operated_by TEXT,
        activities TEXT,
        elevation TEXT,
        vicinity TEXT,
        desc TEXT,
        timestamp DATETIME)""")

## Starting point URLs and page data
base_url = "http://www.fs.usda.gov/activity/nfsnc/recreation/"
hike_trails_idx = cacheLookup(base_url + "hiking/?recid=48112&actid=50")
bike_trails_idx = cacheLookup(base_url + "bicycling/?recid=48112&actid=24")

idx_pg_root = lxml.html.fromstring(hike_trails_idx)

hike_xpath = """//h3[contains( string(.), 'Hiking')][1]/following::a[contains( string(.), '#') or contains(string(.), 'TR') or contains(string(.), 'Trail')]"""

for (num, anchor) in enumerate(idx_pg_root.xpath(hike_xpath)):
    if START_ITER >= num:
        continue

    if 'href' in anchor.attrib:
        ## Create url
        related_url = base_url.replace("/activity/nfsnc/recreation/", "") + anchor.attrib['href']

        ## Lookup in cache or re-download (if UPDATE_CACHE set)
        trail_doc = cacheLookup(related_url, UPDATE_CACHE)
        trail_doc_root = lxml.html.fromstring(trail_doc)
        trail_ht5_root = html5Parser.parse(trail_doc)

        ## Reasonable-ish path to the main page content
        main_section = trail_doc_root.xpath("""
           //div[@id='mainContent']/table[@class='layoutRow']/tr/td/
           table/tr[3]/td/table[@class='layoutRow']/tr/td[4]""")
        
        ## Setup empty data record with url as key
        rec = {
            "iter": num,
            "url": related_url,
            "num": None,
            "name": None,
            "vicinity": None,
            "desc": "", ## For collecting all the crap that doesn't fit elsewhere
            "season": None,
            "usage": None,
            "restrictions": None,
            "water": None,
            "restroom": None,
            "operated_by": None,
            "timestamp": datetime.datetime.now().isoformat()
        }

        ## Easy stuff. Trail name, number, and possibly vicinity from header near top of page
        trail_name_num = main_section[0].xpath("//div[@id='pagetitletop']/h1")[0].text_content()
        TR_delim_match = re.match(r'(^.+) TR\s?(\d{1,3}.*)$', trail_name_num)
        no_delim_match = re.match(r'(^.+) (\d{1,3}.*)$', trail_name_num)
        if '#' in trail_name_num:
            (trail_name, pound, trail_num) = trail_name_num.rpartition("#")
            if ',' in trail_num:
                (trail_num, comma, trail_vicinity) = trail_num.rpartition(',')
                rec['vicinity'] = trail_vicinity

            rec['name'] = trail_name
            rec['num'] = trail_num

        elif TR_delim_match :
            rec['name'] = TR_delim_match.group(1)
            rec['num'] = TR_delim_match.group(2)

        elif no_delim_match:
            rec['name'] = no_delim_match.group(1)
            rec['num'] = no_delim_match.group(2)

        else:
            rec['name'] = trail_name_num

        ## "At a Glance" table - somewhat addressable
        glance_tbl = main_section[0].xpath("""
            //table[contains(./@summary,"Recreation Area At a Glance Information")]""")

        if glance_tbl and len(glance_tbl[0].text_content().strip()) > 0:
            season = glance_tbl[0].xpath(""".//tr/th[contains(.,'Open Season:')]/following-sibling::td""")
            rec["season"] = txt_delim(season)
            
            usage = glance_tbl[0].xpath(""".//tr/th[contains(.,'Usage:')]/following-sibling::td""")
            rec["usage"] = txt_delim(usage)

            restr = glance_tbl[0].xpath(""".//tr/th[contains(.,'Restrictions:')]/following-sibling::td""")
            rec["restrictions"] = txt_delim(restr)

            water = glance_tbl[0].xpath(""".//tr/th[contains(.,'Water:')]/following-sibling::td""")
            rec["water"] = txt_delim(water)

            restroom = glance_tbl[0].xpath(""".//tr/th[contains(.,'Restroom:')]/following-sibling::td""")
            rec["restroom"] = txt_delim(restroom)

            operated_by = glance_tbl[0].xpath(""".//tr/th[contains(.,'Operated By:')]/following-sibling::td""")
            rec["operated_by"] = txt_delim(operated_by)


        ## "Activities" (allowed uses)
        activities = main_section[0].xpath("""
            //h2[contains(.,'Activities')]/following-sibling::h3""")
        rec["activities"] = txt_delim(activities, ", ")

        ## "Location" elevation info
        elevation = main_section[0].xpath(""".//div[contains(., 'Elevation')]/following-sibling::div[1]""")
        rec["elevation"] = txt_delim(elevation)

        ## Fair warning: the rest is mostly a crapshoot.

        ## Descriptions
        desc_elements = main_section[0].xpath(
            """./table/tr[3]/td[1]/table[1]/tr[1]/td[1]/div[1]/table[1]/tr[3]
            /td[1]/table[1]/tr[1]/td[1]/*[not(@class='tablecolor') and not(contains(., 'At a Glance')) and not(contains(., 'General Information'))]
            |
            ./table/tr[3]/td[1]/table[1]/tr[1]/td[1]/div[1]/table[1]/tr[3]
            /td[1]/table[1]/tr[1]/td[1]/text()
            """)
        rec["desc"] += txt_delim(desc_elements)
        
        ## Save the data
        scraperwiki.sqlite.save(unique_keys=["url"], data=rec, table_name="trails")

    if num >= STOP_ITER:
        break
# NF NC Trail Data

import re
import json
import datetime
import scraperwiki
import lxml.html
import html5lib

from html5lib import treebuilders
html5Parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)

UPDATE_CACHE=False   ## Set to True to re-download all pages (False for dev and resume if flaky server)
START_ITER = 0       ## Link to start on (350)
STOP_ITER = 10000    ## Link to end on (400)

def cacheLookup(url, update_cache=False):
    """Simple cache of scraped pages for development"""
    #print "Checking local cache for {0}...".format(url)
    result = scraperwiki.sqlite.select("url, timestamp, src FROM sources WHERE url = ?", [url])
    if not result or update_cache:
        print "No Cache for this site (or force-update flag given), scraping live site for local cache..."
        src = scraperwiki.scrape(url)
        scraperwiki.sqlite.execute("INSERT OR REPLACE INTO sources VALUES (?, ?, ?)",
            [url, datetime.datetime.now().isoformat(), src])
        scraperwiki.sqlite.commit()
        print "Cache saved."
        return src

    else:
        #print "Data already exists for {0}, using local cache...".format(url)
        return result[0].get("src")

def txt_delim(node, delim="\n"):
    txt_elements = []
    for e in node:
        if hasattr(e, 'text_content'):
           txt_elements.append(e.text_content().strip())

        else:
           txt_elements.append(e.strip())

    return delim.join(txt_elements).strip()

## Setup data stores
scraperwiki.sqlite.execute(
    "CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, src TEXT)")

scraperwiki.sqlite.execute("""DROP TABLE IF EXISTS trails""")
scraperwiki.sqlite.execute("""
    CREATE TABLE IF NOT EXISTS trails(
        iter INTEGER,
        url TEXT PRIMARY KEY,
        num TEXT,
        name TEXT,
        season TEXT,
        usage TEXT,
        restrictions TEXT,
        water TEXT,
        restroom TEXT,
        operated_by TEXT,
        activities TEXT,
        elevation TEXT,
        vicinity TEXT,
        desc TEXT,
        timestamp DATETIME)""")

## Starting point URLs and page data
base_url = "http://www.fs.usda.gov/activity/nfsnc/recreation/"
hike_trails_idx = cacheLookup(base_url + "hiking/?recid=48112&actid=50")
bike_trails_idx = cacheLookup(base_url + "bicycling/?recid=48112&actid=24")

idx_pg_root = lxml.html.fromstring(hike_trails_idx)

hike_xpath = """//h3[contains( string(.), 'Hiking')][1]/following::a[contains( string(.), '#') or contains(string(.), 'TR') or contains(string(.), 'Trail')]"""

for (num, anchor) in enumerate(idx_pg_root.xpath(hike_xpath)):
    if START_ITER >= num:
        continue

    if 'href' in anchor.attrib:
        ## Create url
        related_url = base_url.replace("/activity/nfsnc/recreation/", "") + anchor.attrib['href']

        ## Lookup in cache or re-download (if UPDATE_CACHE set)
        trail_doc = cacheLookup(related_url, UPDATE_CACHE)
        trail_doc_root = lxml.html.fromstring(trail_doc)
        trail_ht5_root = html5Parser.parse(trail_doc)

        ## Reasonable-ish path to the main page content
        main_section = trail_doc_root.xpath("""
           //div[@id='mainContent']/table[@class='layoutRow']/tr/td/
           table/tr[3]/td/table[@class='layoutRow']/tr/td[4]""")
        
        ## Setup empty data record with url as key
        rec = {
            "iter": num,
            "url": related_url,
            "num": None,
            "name": None,
            "vicinity": None,
            "desc": "", ## For collecting all the crap that doesn't fit elsewhere
            "season": None,
            "usage": None,
            "restrictions": None,
            "water": None,
            "restroom": None,
            "operated_by": None,
            "timestamp": datetime.datetime.now().isoformat()
        }

        ## Easy stuff. Trail name, number, and possibly vicinity from header near top of page
        trail_name_num = main_section[0].xpath("//div[@id='pagetitletop']/h1")[0].text_content()
        TR_delim_match = re.match(r'(^.+) TR\s?(\d{1,3}.*)$', trail_name_num)
        no_delim_match = re.match(r'(^.+) (\d{1,3}.*)$', trail_name_num)
        if '#' in trail_name_num:
            (trail_name, pound, trail_num) = trail_name_num.rpartition("#")
            if ',' in trail_num:
                (trail_num, comma, trail_vicinity) = trail_num.rpartition(',')
                rec['vicinity'] = trail_vicinity

            rec['name'] = trail_name
            rec['num'] = trail_num

        elif TR_delim_match :
            rec['name'] = TR_delim_match.group(1)
            rec['num'] = TR_delim_match.group(2)

        elif no_delim_match:
            rec['name'] = no_delim_match.group(1)
            rec['num'] = no_delim_match.group(2)

        else:
            rec['name'] = trail_name_num

        ## "At a Glance" table - somewhat addressable
        glance_tbl = main_section[0].xpath("""
            //table[contains(./@summary,"Recreation Area At a Glance Information")]""")

        if glance_tbl and len(glance_tbl[0].text_content().strip()) > 0:
            season = glance_tbl[0].xpath(""".//tr/th[contains(.,'Open Season:')]/following-sibling::td""")
            rec["season"] = txt_delim(season)
            
            usage = glance_tbl[0].xpath(""".//tr/th[contains(.,'Usage:')]/following-sibling::td""")
            rec["usage"] = txt_delim(usage)

            restr = glance_tbl[0].xpath(""".//tr/th[contains(.,'Restrictions:')]/following-sibling::td""")
            rec["restrictions"] = txt_delim(restr)

            water = glance_tbl[0].xpath(""".//tr/th[contains(.,'Water:')]/following-sibling::td""")
            rec["water"] = txt_delim(water)

            restroom = glance_tbl[0].xpath(""".//tr/th[contains(.,'Restroom:')]/following-sibling::td""")
            rec["restroom"] = txt_delim(restroom)

            operated_by = glance_tbl[0].xpath(""".//tr/th[contains(.,'Operated By:')]/following-sibling::td""")
            rec["operated_by"] = txt_delim(operated_by)


        ## "Activities" (allowed uses)
        activities = main_section[0].xpath("""
            //h2[contains(.,'Activities')]/following-sibling::h3""")
        rec["activities"] = txt_delim(activities, ", ")

        ## "Location" elevation info
        elevation = main_section[0].xpath(""".//div[contains(., 'Elevation')]/following-sibling::div[1]""")
        rec["elevation"] = txt_delim(elevation)

        ## Fair warning: the rest is mostly a crapshoot.

        ## Descriptions
        desc_elements = main_section[0].xpath(
            """./table/tr[3]/td[1]/table[1]/tr[1]/td[1]/div[1]/table[1]/tr[3]
            /td[1]/table[1]/tr[1]/td[1]/*[not(@class='tablecolor') and not(contains(., 'At a Glance')) and not(contains(., 'General Information'))]
            |
            ./table/tr[3]/td[1]/table[1]/tr[1]/td[1]/div[1]/table[1]/tr[3]
            /td[1]/table[1]/tr[1]/td[1]/text()
            """)
        rec["desc"] += txt_delim(desc_elements)
        
        ## Save the data
        scraperwiki.sqlite.save(unique_keys=["url"], data=rec, table_name="trails")

    if num >= STOP_ITER:
        break
