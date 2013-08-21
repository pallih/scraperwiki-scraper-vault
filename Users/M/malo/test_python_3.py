import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-00019")
root = lxml.html.fromstring(html)



for el in root.cssselect("div.c-col a"):
    case_name = el.text
    case_url_append = el.attrib['href']
    case_url = "http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-00019" + case_url_append
    case_name_tuple = case_name.partition(":")
    case_url_append_tuple = case_url_append.partition("/case/")
    case_id_tuple = (case_url_append_tuple[2]).partition(".")
    data = {
        'case_id' : case_id_tuple[0],
        'school' : case_name_tuple[0],
        'case_name' : case_name_tuple[2],
        'case_url' : "http://thefire.org" + el.attrib['href']
    }
    scraperwiki.sqlite.save(unique_keys=['case_id'], data=data)
