import scraperwiki
import lxml.html
import dateutil.parser
import datetime

base_url = 'http://cape.ucsd.edu/scripts/statistics.asp?Name=&CourseNumber=&department='

li = ['ANTH', 'BENG', 'BIOL', 'CAT ', 'CENG', 'CGS ', 'CHEM', 'CHIN', 'COGS', 'COMM', 'CONT', 'CSE ', 'DOC ', 'ECE ', 'ECON', 'EDS ', 'ENVR', 'ERC ', 'ESYS', 'ETHN', 'FILM', 'HDP ', 'HIST', 'HMNR', 'HUM ', 'ICAM', 'INTL', 'JAPN', 'JUDA', 'LATI', 'LAWS', 'LING', 'LIT ', 'MAE ', 'MATH', 'MMW', 'MUIR', 'MUS ', 'NENG', 'PHIL', 'PHYS', 'POLI', 'PSYC', 'RELI', 'REV', 'RSM ', 'SDCC', 'SE  ', 'SIO ', 'SOC ', 'SOE ', 'STPA', 'SXTH', 'THEA', 'TMC', 'TWS ', 'USP ', 'VIS ', 'WARR', 'WCWP']

i = 1

for s in li:

    k = 1
    html = scraperwiki.scrape(base_url+s)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("tr"):
        if k >= 5:
            tds = tr.cssselect("td")
            for el in tr.cssselect("a"):           
                url = el.get('href')
                name = el.text_content()
            tds = tr.cssselect("td")
            # print tds[1].text_content()
            # print tds[10].text_content()
            data = {
            'id' : i,
            'url' : url,
            'field' : s,
            'name' : name,
            'self' : tds[1].text_content(),
            'code' : tds[2].text_content(),
            'title' : tds[3].text_content(),
            'time' : tds[4].text_content(),
            'term' : tds[5].text_content(),
            'enroll' : tds[6].text_content(),
            'recclass' : tds[7].text_content(),
            'recinst' : tds[8].text_content(),
            'study' : tds[9].text_content(),
            'learned' : tds[10].text_content(),
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            i += 1
        k += 1
import scraperwiki
import lxml.html
import dateutil.parser
import datetime

base_url = 'http://cape.ucsd.edu/scripts/statistics.asp?Name=&CourseNumber=&department='

li = ['ANTH', 'BENG', 'BIOL', 'CAT ', 'CENG', 'CGS ', 'CHEM', 'CHIN', 'COGS', 'COMM', 'CONT', 'CSE ', 'DOC ', 'ECE ', 'ECON', 'EDS ', 'ENVR', 'ERC ', 'ESYS', 'ETHN', 'FILM', 'HDP ', 'HIST', 'HMNR', 'HUM ', 'ICAM', 'INTL', 'JAPN', 'JUDA', 'LATI', 'LAWS', 'LING', 'LIT ', 'MAE ', 'MATH', 'MMW', 'MUIR', 'MUS ', 'NENG', 'PHIL', 'PHYS', 'POLI', 'PSYC', 'RELI', 'REV', 'RSM ', 'SDCC', 'SE  ', 'SIO ', 'SOC ', 'SOE ', 'STPA', 'SXTH', 'THEA', 'TMC', 'TWS ', 'USP ', 'VIS ', 'WARR', 'WCWP']

i = 1

for s in li:

    k = 1
    html = scraperwiki.scrape(base_url+s)
    root = lxml.html.fromstring(html)

    for tr in root.cssselect("tr"):
        if k >= 5:
            tds = tr.cssselect("td")
            for el in tr.cssselect("a"):           
                url = el.get('href')
                name = el.text_content()
            tds = tr.cssselect("td")
            # print tds[1].text_content()
            # print tds[10].text_content()
            data = {
            'id' : i,
            'url' : url,
            'field' : s,
            'name' : name,
            'self' : tds[1].text_content(),
            'code' : tds[2].text_content(),
            'title' : tds[3].text_content(),
            'time' : tds[4].text_content(),
            'term' : tds[5].text_content(),
            'enroll' : tds[6].text_content(),
            'recclass' : tds[7].text_content(),
            'recinst' : tds[8].text_content(),
            'study' : tds[9].text_content(),
            'learned' : tds[10].text_content(),
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            i += 1
        k += 1
