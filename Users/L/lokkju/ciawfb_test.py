import lxml,lxml.html,urllib2,scraperwiki

BASE_URI = "http://www.umsl.edu/services/govdocs/wofact96/"

def make_tables():
    scraperwiki.sqlite.execute("drop table if exists ciawfb_raw")
    scraperwiki.sqlite.execute("""create table if not exists ciawfb_raw
                                      (id INTEGER PRIMARY KEY,year INTEGER, country TEXT, category TEXT, subcategory TEXT, label TEXT, value TEXT,
                                      UNIQUE (year,country,category,subcategory,label,value))""")

def process_countries_1996():
    f = urllib2.urlopen(BASE_URI).read()
    l = lxml.html.fromstring(f)
    for a in l.cssselect("li a"):
        curl = a.attrib.get("href")
        print "processing page %s" % (curl,)
        process_country_page_1996(BASE_URI + curl)

def process_country_page_1996(url):
    f = urllib2.urlopen(url).read()
    l = lxml.html.fromstring(f)
    country_name = l.cssselect("h2 a")[0].text_content()
    print country_name
    current_h3 = None
    current_b = None
    for i in l.getiterator():
        if not i.tag in ["h3","i","b"]:
            next
        data = []
        if(i.tag == "h3"):
            current_h3 = i.text_content().strip()
            next
        if(i.tag == "b"):
            if current_h3 == None:
                next
            current_b = i.text_content().strip()
            if len(i.tail.strip()) > 0:
                scraperwiki.sqlite.execute("INSERT OR IGNORE into ciawfb_raw (year,country,category,subcategory,label,value) values(1996,?,?,?,?,?);",
                    (country_name,current_h3,"",current_b,i.tail.strip()))
            next
        if(i.tag == "i"):
            if current_h3 == None:
                next
            if current_b == None:
                next
            scraperwiki.sqlite.execute("INSERT OR IGNORE into ciawfb_raw (year,country,category,subcategory,label,value) values(1996,?,?,?,?,?);",
                (country_name,current_h3,current_b,i.text_content().strip(),i.tail.strip()))
    scraperwiki.sqlite.commit()

#make_tables()
process_countries_1996()


import lxml,lxml.html,urllib2,scraperwiki

BASE_URI = "http://www.umsl.edu/services/govdocs/wofact96/"

def make_tables():
    scraperwiki.sqlite.execute("drop table if exists ciawfb_raw")
    scraperwiki.sqlite.execute("""create table if not exists ciawfb_raw
                                      (id INTEGER PRIMARY KEY,year INTEGER, country TEXT, category TEXT, subcategory TEXT, label TEXT, value TEXT,
                                      UNIQUE (year,country,category,subcategory,label,value))""")

def process_countries_1996():
    f = urllib2.urlopen(BASE_URI).read()
    l = lxml.html.fromstring(f)
    for a in l.cssselect("li a"):
        curl = a.attrib.get("href")
        print "processing page %s" % (curl,)
        process_country_page_1996(BASE_URI + curl)

def process_country_page_1996(url):
    f = urllib2.urlopen(url).read()
    l = lxml.html.fromstring(f)
    country_name = l.cssselect("h2 a")[0].text_content()
    print country_name
    current_h3 = None
    current_b = None
    for i in l.getiterator():
        if not i.tag in ["h3","i","b"]:
            next
        data = []
        if(i.tag == "h3"):
            current_h3 = i.text_content().strip()
            next
        if(i.tag == "b"):
            if current_h3 == None:
                next
            current_b = i.text_content().strip()
            if len(i.tail.strip()) > 0:
                scraperwiki.sqlite.execute("INSERT OR IGNORE into ciawfb_raw (year,country,category,subcategory,label,value) values(1996,?,?,?,?,?);",
                    (country_name,current_h3,"",current_b,i.tail.strip()))
            next
        if(i.tag == "i"):
            if current_h3 == None:
                next
            if current_b == None:
                next
            scraperwiki.sqlite.execute("INSERT OR IGNORE into ciawfb_raw (year,country,category,subcategory,label,value) values(1996,?,?,?,?,?);",
                (country_name,current_h3,current_b,i.text_content().strip(),i.tail.strip()))
    scraperwiki.sqlite.commit()

#make_tables()
process_countries_1996()


