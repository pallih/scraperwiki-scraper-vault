import calendar, datetime, urlparse, urllib, json, scraperwiki, re, lxml.html
from BeautifulSoup import UnicodeDammit
from unidecode import unidecode
from string import capwords

def get_valid_url(url):
    parts = urlparse.urlparse(url)
    return urlparse.urlunparse([parts[0], parts[1], urllib.quote(parts.path), urllib.quote(parts[3]), urllib.quote(parts[4]), parts[5]])

def decode_html(html_string):
    # See http://stackoverflow.com/a/16427392/82216
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode

def get_source_politely(url, update_flag = False):
    # See https://scraperwiki.com/scrapers/local_cache_scraper_1/
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, source_blob BLOB)")
    result = scraperwiki.sqlite.execute("SELECT url, timestamp, source_blob FROM sources WHERE url = '" + url + "'")
    if len(result["data"]) == 0 or update_flag == True:
        # Need to apply decode_html at this point to avoid SQLite's default conversion, which produces results UnicodeDammit throws warnings on.
        source = decode_html(scraperwiki.scrape(url))
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()), "source_blob":source}, table_name="sources")
        return source
    else:
        # print "Using local cache for " + url + " as cached data exists from " + datetime.datetime.fromtimestamp(result["data"][0][1]).strftime('%Y-%m-%d %H:%M:%S') + " UTC."
        return result["data"][0][2]

whitespace_re = re.compile(r'\s')
www_re        = re.compile(r'^www\d*\.*')
# universities = {'Harvard':{'university':'Harvard', 'b':'Foo', 'c':'Bar'}, 'Yale':{'university':'Yale', 'b':'Grue', 'c':'Gnu'}}
universities = {}
university_list_object = []
arwu_data = {}
arwu_list_object = []
arwu_detailed_list_length = 200

scraperwiki.sqlite.execute("drop table if exists arwu_data")
scraperwiki.sqlite.commit()
arwu_list_html = get_source_politely("http://www.shanghairanking.com/ARWU2012.html")
arwu_list_root = lxml.html.fromstring(arwu_list_html)
for tr in arwu_list_root.cssselect("#UniversityRanking tr:not(:first-child)"):
    if len(tr.cssselect("td.ranking")) > 0 and len(tr.cssselect("td.rankingname")) > 0:
        # Get name according to ARWU
        name                     = unidecode(tr.cssselect("td.rankingname")[0].text_content()).strip()
        # Get normalised (i.e. integer) rank according to ARWU
        rank                     = str(re.sub(whitespace_re, r'', tr.cssselect("td.ranking")[0].text_content()))
        if '-' in rank:
            rank_bounds  = rank.split('-')
            rank = int( ( float(rank_bounds[0]) + float(rank_bounds[1]) ) * 0.5 )
        if not type(rank) is int:
            rank = int(rank)
        # Get valid URL for ARWU info page
        arwu_infopage_url_parts  = tr.cssselect("td.rankingname a")[0].attrib['href'].split("Institution.jsp?param=")
        arwu_infopage_url        = arwu_infopage_url_parts[0] + "Institution.jsp?param=" + urllib.quote(arwu_infopage_url_parts[1])
        # Get ARWU info page contents
        arwu_infopage_html       = get_source_politely(arwu_infopage_url)
        arwu_infopage_root       = lxml.html.fromstring(arwu_infopage_html)
        # Get domain of university according to ARWU
        for td in arwu_infopage_root.cssselect("#tab1 td"):
            if 'Website:' in td.text_content():
                arwu_url = td.getnext().cssselect("a")[0].attrib['href']
                if not arwu_url.strip() == "":
                    arwu_url_parts = json.loads(get_source_politely("http://tldextract.appspot.com/api/extract?url=" + arwu_url))
                    # arwu_domain = ".".join([ re.sub(www_re, r'', arwu_url_parts["subdomain"]), arwu_url_parts["domain"], arwu_url_parts["tld"]])
                    arwu_domain = ".".join([arwu_url_parts["domain"], arwu_url_parts["tld"]])
                else:
                    arwu_domain = ""
        # Get ARWU "SCI", "ENG", "LIFE", "MED", "SOC" rankings for university
        for td in arwu_infopage_root.cssselect("div#left table.scaletable2 td"):
            if 'Natural Sciences and Mathematics (SCI)' in td.text_content():
                arwu_sci = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_sci == "/":
                    arwu_sci = arwu_detailed_list_length + 1
            if 'Engineering/Technology and Computer Science (ENG)' in td.text_content():
                arwu_eng = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_eng == "/":
                    arwu_eng = arwu_detailed_list_length + 1
            if 'Life and Agriculture Sciences (LIFE)' in td.text_content():
                arwu_life = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_life == "/":
                    arwu_life = arwu_detailed_list_length + 1
            if 'Clinical Medicine and Pharmacy (MED)' in td.text_content():
                arwu_med = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_med == "/":
                    arwu_med = arwu_detailed_list_length + 1
            if 'Social Sciences (SOC)' in td.text_content():
                arwu_soc = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_soc == "/":
                    arwu_soc = arwu_detailed_list_length + 1

        # Get ARWU "Mathematics", "Physics", "Chemistry", "Computer Science", "Economics/Business" rankings for university
        for td in arwu_infopage_root.cssselect("div#left table.scaletable td"):
            if unidecode(td.text_content()).strip() == 'Mathematics' :
                arwu_maths = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_maths == "/":
                    arwu_maths = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Physics' :
                arwu_phys = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_phys == "/":
                    arwu_phys = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Chemistry' :
                arwu_chem = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_chem == "/":
                    arwu_chem = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Computer Science' :
                arwu_compsci = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_compsci == "/":
                    arwu_compsci = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == "Economics/Business" :
                arwu_econ = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_econ == "/":
                    arwu_econ = arwu_detailed_list_length + 1

        # Get Wikipedia entry name corresponding to what ARWU asserts the university's name is
        # arwu_wiki_name = unidecode(json.loads(get_source_politely("http://en.wikipedia.org/w/api.php?action=opensearch&limit=1&search=" + urllib.quote(name)))[1][0]).strip()
        arwu_wiki_name = unidecode(json.loads(get_source_politely("http://en.wikipedia.org/w/api.php?action=query&list=search&srprop=score&srredirects=true&srlimit=1&format=json&srsearch=" + urllib.quote(name)))["query"]["search"][0]["title"]).strip()

        # Get domain according to Wikipedia.
        arwu_wiki_url_html = get_source_politely("http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=SELECT+%3Fwebsite%0D%0AWHERE++{+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F" + re.sub(whitespace_re, r'_', arwu_wiki_name) + "%3E+dbpprop%3Awebsite+%3Fwebsite+.+}&format=text%2Fhtml&timeout=0")
        arwu_wiki_url_root = lxml.html.fromstring(arwu_wiki_url_html)
        if len(arwu_wiki_url_root.cssselect("td:last-child")) > 0:
            arwu_wiki_url = unidecode(arwu_wiki_url_root.cssselect("td:last-child")[0].text_content()).strip()
            if not arwu_wiki_url == "":
                    arwu_wiki_url_parts = json.loads(get_source_politely("http://tldextract.appspot.com/api/extract?url=" + arwu_wiki_url))
                    arwu_wiki_domain = ".".join([arwu_wiki_url_parts["domain"], arwu_wiki_url_parts["tld"]])
        else:
            arwu_wiki_domain = ""
        

        # Put ARWU data into array
        if not name in arwu_data:
            arwu_data[name] = {}
        arwu_data[name]['name']             = name
        arwu_data[name]['rank']             = rank
        arwu_data[name]['arwu_domain']      = arwu_domain
        arwu_data[name]['arwu_sci']         = arwu_sci
        arwu_data[name]['arwu_eng']         = arwu_eng
        arwu_data[name]['arwu_life']        = arwu_life
        arwu_data[name]['arwu_med']         = arwu_med
        arwu_data[name]['arwu_soc']         = arwu_soc
        arwu_data[name]['arwu_maths']       = arwu_maths
        arwu_data[name]['arwu_phys']        = arwu_phys
        arwu_data[name]['arwu_chem']        = arwu_chem
        arwu_data[name]['arwu_compsci']     = arwu_compsci
        arwu_data[name]['arwu_econ']        = arwu_econ
        arwu_data[name]['arwu_wiki_name']   = arwu_wiki_name
        arwu_data[name]['arwu_wiki_domain'] = arwu_wiki_domain

for uni in arwu_data:
    arwu_list_object.append(arwu_data[uni])
scraperwiki.sqlite.save(['name'], arwu_list_object, table_name="arwu_data")

#        if not university in universities:
#            universities[university] = {}
#        universities[university]['university']    = university
#        universities[university]['arwu_page_url'] = arwu_page_url
#        universities[university]['arwu_url']      = arwu_url
#        universities[university]['domain']        = arwu_domain
#        universities[university]['arwu_rank']     = rank
# for thes_page in ["http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/001-200",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/201-225",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/226-250",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/251-275",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/276-300",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/301-350",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/351-400"]:
#    html = get_source_politely(thes_page)
#    root = lxml.html.fromstring(html)
#    for tr in root.cssselect("table.ranking tr"):
#        if len(tr.cssselect("td.rank")) > 0 and len(tr.cssselect("td.uni")) > 0:
#            rank       = str(re.sub(whitespace_re, r'', tr.cssselect("td.rank")[0].text_content()))
#            university = capwords(unidecode(tr.cssselect("td.uni")[0].text_content()).strip())
#            if '-' in rank:
#                rank_bounds  = rank.split('-')
#                rank = int( ( float(rank_bounds[0]) + float(rank_bounds[1]) ) * 0.5 )
#            if not type(rank) is int:
#                rank = int(rank)
#            if not university in universities:
#                universities[university] = {}
#            universities[university]['university'] = university
#            universities[university]['thes_rank'] = rank
#for uni in universities:
#    university_list_object.append(universities[uni])
#scraperwiki.sqlite.save(['university'], university_list_object)

import calendar, datetime, urlparse, urllib, json, scraperwiki, re, lxml.html
from BeautifulSoup import UnicodeDammit
from unidecode import unidecode
from string import capwords

def get_valid_url(url):
    parts = urlparse.urlparse(url)
    return urlparse.urlunparse([parts[0], parts[1], urllib.quote(parts.path), urllib.quote(parts[3]), urllib.quote(parts[4]), parts[5]])

def decode_html(html_string):
    # See http://stackoverflow.com/a/16427392/82216
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode

def get_source_politely(url, update_flag = False):
    # See https://scraperwiki.com/scrapers/local_cache_scraper_1/
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, timestamp DATETIME, source_blob BLOB)")
    result = scraperwiki.sqlite.execute("SELECT url, timestamp, source_blob FROM sources WHERE url = '" + url + "'")
    if len(result["data"]) == 0 or update_flag == True:
        # Need to apply decode_html at this point to avoid SQLite's default conversion, which produces results UnicodeDammit throws warnings on.
        source = decode_html(scraperwiki.scrape(url))
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()), "source_blob":source}, table_name="sources")
        return source
    else:
        # print "Using local cache for " + url + " as cached data exists from " + datetime.datetime.fromtimestamp(result["data"][0][1]).strftime('%Y-%m-%d %H:%M:%S') + " UTC."
        return result["data"][0][2]

whitespace_re = re.compile(r'\s')
www_re        = re.compile(r'^www\d*\.*')
# universities = {'Harvard':{'university':'Harvard', 'b':'Foo', 'c':'Bar'}, 'Yale':{'university':'Yale', 'b':'Grue', 'c':'Gnu'}}
universities = {}
university_list_object = []
arwu_data = {}
arwu_list_object = []
arwu_detailed_list_length = 200

scraperwiki.sqlite.execute("drop table if exists arwu_data")
scraperwiki.sqlite.commit()
arwu_list_html = get_source_politely("http://www.shanghairanking.com/ARWU2012.html")
arwu_list_root = lxml.html.fromstring(arwu_list_html)
for tr in arwu_list_root.cssselect("#UniversityRanking tr:not(:first-child)"):
    if len(tr.cssselect("td.ranking")) > 0 and len(tr.cssselect("td.rankingname")) > 0:
        # Get name according to ARWU
        name                     = unidecode(tr.cssselect("td.rankingname")[0].text_content()).strip()
        # Get normalised (i.e. integer) rank according to ARWU
        rank                     = str(re.sub(whitespace_re, r'', tr.cssselect("td.ranking")[0].text_content()))
        if '-' in rank:
            rank_bounds  = rank.split('-')
            rank = int( ( float(rank_bounds[0]) + float(rank_bounds[1]) ) * 0.5 )
        if not type(rank) is int:
            rank = int(rank)
        # Get valid URL for ARWU info page
        arwu_infopage_url_parts  = tr.cssselect("td.rankingname a")[0].attrib['href'].split("Institution.jsp?param=")
        arwu_infopage_url        = arwu_infopage_url_parts[0] + "Institution.jsp?param=" + urllib.quote(arwu_infopage_url_parts[1])
        # Get ARWU info page contents
        arwu_infopage_html       = get_source_politely(arwu_infopage_url)
        arwu_infopage_root       = lxml.html.fromstring(arwu_infopage_html)
        # Get domain of university according to ARWU
        for td in arwu_infopage_root.cssselect("#tab1 td"):
            if 'Website:' in td.text_content():
                arwu_url = td.getnext().cssselect("a")[0].attrib['href']
                if not arwu_url.strip() == "":
                    arwu_url_parts = json.loads(get_source_politely("http://tldextract.appspot.com/api/extract?url=" + arwu_url))
                    # arwu_domain = ".".join([ re.sub(www_re, r'', arwu_url_parts["subdomain"]), arwu_url_parts["domain"], arwu_url_parts["tld"]])
                    arwu_domain = ".".join([arwu_url_parts["domain"], arwu_url_parts["tld"]])
                else:
                    arwu_domain = ""
        # Get ARWU "SCI", "ENG", "LIFE", "MED", "SOC" rankings for university
        for td in arwu_infopage_root.cssselect("div#left table.scaletable2 td"):
            if 'Natural Sciences and Mathematics (SCI)' in td.text_content():
                arwu_sci = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_sci == "/":
                    arwu_sci = arwu_detailed_list_length + 1
            if 'Engineering/Technology and Computer Science (ENG)' in td.text_content():
                arwu_eng = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_eng == "/":
                    arwu_eng = arwu_detailed_list_length + 1
            if 'Life and Agriculture Sciences (LIFE)' in td.text_content():
                arwu_life = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_life == "/":
                    arwu_life = arwu_detailed_list_length + 1
            if 'Clinical Medicine and Pharmacy (MED)' in td.text_content():
                arwu_med = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_med == "/":
                    arwu_med = arwu_detailed_list_length + 1
            if 'Social Sciences (SOC)' in td.text_content():
                arwu_soc = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_soc == "/":
                    arwu_soc = arwu_detailed_list_length + 1

        # Get ARWU "Mathematics", "Physics", "Chemistry", "Computer Science", "Economics/Business" rankings for university
        for td in arwu_infopage_root.cssselect("div#left table.scaletable td"):
            if unidecode(td.text_content()).strip() == 'Mathematics' :
                arwu_maths = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_maths == "/":
                    arwu_maths = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Physics' :
                arwu_phys = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_phys == "/":
                    arwu_phys = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Chemistry' :
                arwu_chem = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_chem == "/":
                    arwu_chem = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == 'Computer Science' :
                arwu_compsci = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_compsci == "/":
                    arwu_compsci = arwu_detailed_list_length + 1
            if unidecode(td.text_content()).strip() == "Economics/Business" :
                arwu_econ = unidecode(td.getparent().cssselect("td:last-child")[0].text_content()).strip()
                if arwu_econ == "/":
                    arwu_econ = arwu_detailed_list_length + 1

        # Get Wikipedia entry name corresponding to what ARWU asserts the university's name is
        # arwu_wiki_name = unidecode(json.loads(get_source_politely("http://en.wikipedia.org/w/api.php?action=opensearch&limit=1&search=" + urllib.quote(name)))[1][0]).strip()
        arwu_wiki_name = unidecode(json.loads(get_source_politely("http://en.wikipedia.org/w/api.php?action=query&list=search&srprop=score&srredirects=true&srlimit=1&format=json&srsearch=" + urllib.quote(name)))["query"]["search"][0]["title"]).strip()

        # Get domain according to Wikipedia.
        arwu_wiki_url_html = get_source_politely("http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=SELECT+%3Fwebsite%0D%0AWHERE++{+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F" + re.sub(whitespace_re, r'_', arwu_wiki_name) + "%3E+dbpprop%3Awebsite+%3Fwebsite+.+}&format=text%2Fhtml&timeout=0")
        arwu_wiki_url_root = lxml.html.fromstring(arwu_wiki_url_html)
        if len(arwu_wiki_url_root.cssselect("td:last-child")) > 0:
            arwu_wiki_url = unidecode(arwu_wiki_url_root.cssselect("td:last-child")[0].text_content()).strip()
            if not arwu_wiki_url == "":
                    arwu_wiki_url_parts = json.loads(get_source_politely("http://tldextract.appspot.com/api/extract?url=" + arwu_wiki_url))
                    arwu_wiki_domain = ".".join([arwu_wiki_url_parts["domain"], arwu_wiki_url_parts["tld"]])
        else:
            arwu_wiki_domain = ""
        

        # Put ARWU data into array
        if not name in arwu_data:
            arwu_data[name] = {}
        arwu_data[name]['name']             = name
        arwu_data[name]['rank']             = rank
        arwu_data[name]['arwu_domain']      = arwu_domain
        arwu_data[name]['arwu_sci']         = arwu_sci
        arwu_data[name]['arwu_eng']         = arwu_eng
        arwu_data[name]['arwu_life']        = arwu_life
        arwu_data[name]['arwu_med']         = arwu_med
        arwu_data[name]['arwu_soc']         = arwu_soc
        arwu_data[name]['arwu_maths']       = arwu_maths
        arwu_data[name]['arwu_phys']        = arwu_phys
        arwu_data[name]['arwu_chem']        = arwu_chem
        arwu_data[name]['arwu_compsci']     = arwu_compsci
        arwu_data[name]['arwu_econ']        = arwu_econ
        arwu_data[name]['arwu_wiki_name']   = arwu_wiki_name
        arwu_data[name]['arwu_wiki_domain'] = arwu_wiki_domain

for uni in arwu_data:
    arwu_list_object.append(arwu_data[uni])
scraperwiki.sqlite.save(['name'], arwu_list_object, table_name="arwu_data")

#        if not university in universities:
#            universities[university] = {}
#        universities[university]['university']    = university
#        universities[university]['arwu_page_url'] = arwu_page_url
#        universities[university]['arwu_url']      = arwu_url
#        universities[university]['domain']        = arwu_domain
#        universities[university]['arwu_rank']     = rank
# for thes_page in ["http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/001-200",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/201-225",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/226-250",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/251-275",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/276-300",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/301-350",
#    "http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/351-400"]:
#    html = get_source_politely(thes_page)
#    root = lxml.html.fromstring(html)
#    for tr in root.cssselect("table.ranking tr"):
#        if len(tr.cssselect("td.rank")) > 0 and len(tr.cssselect("td.uni")) > 0:
#            rank       = str(re.sub(whitespace_re, r'', tr.cssselect("td.rank")[0].text_content()))
#            university = capwords(unidecode(tr.cssselect("td.uni")[0].text_content()).strip())
#            if '-' in rank:
#                rank_bounds  = rank.split('-')
#                rank = int( ( float(rank_bounds[0]) + float(rank_bounds[1]) ) * 0.5 )
#            if not type(rank) is int:
#                rank = int(rank)
#            if not university in universities:
#                universities[university] = {}
#            universities[university]['university'] = university
#            universities[university]['thes_rank'] = rank
#for uni in universities:
#    university_list_object.append(universities[uni])
#scraperwiki.sqlite.save(['university'], university_list_object)

