import scraperwiki
import lxml.html
import re

# this is ethnologue's index of countries covered by their dataset.
country_index = scraperwiki.scrape("http://www.ethnologue.com/country_index.asp?place=all")
ci_root = lxml.html.fromstring(country_index)

# this constructs a dictionary of all the country codes in the Ethnologue database.
# each code points to the name of the country.
# the codes themselves are what's really useful, e.g. for getting country pages later.
codes_countries = {}
for a in ci_root.cssselect("a"):
    url = a.get("href")
    if url.startswith("show_country.asp?name="):
        code = url.split("=")[1]
        name = a.text_content().strip()
        codes_countries[code] = name

# this step is necessary to get the sub-parts of Indonesia, etc.
for code in codes_countries.keys():
    country_data = scraperwiki.scrape("http://www.ethnologue.com/show_country.asp?name=" + code)
    c_root = lxml.html.fromstring(country_data)
    for a in c_root.cssselect("a"):
        url = a.get("href")
        if url.startswith("show_country.asp?name="):
            code = url.split("=")[1]
            name = a.text_content().strip()
            codes_countries[code] = name

# the rest of this takes a given country page and extracts useful data.

# this regex will match population digits
digits = re.compile("\d{1,3}(,\d{3})*")

l_hash = {}

for code in codes_countries.keys():
    name = codes_countries[code]
    country_data = scraperwiki.scrape("http://www.ethnologue.com/show_country.asp?name=" + code)
    c_root = lxml.html.fromstring(country_data)

    for tr in c_root.cssselect("tr"):
        tds = tr.cssselect("td")
        lg_name = tds[0].text_content()
        lg_text = tds[1].text_content().strip()
        match = digits.search(lg_text)
        if match:
            lg_pop = digits.search(lg_text).group(0)
            lg_num = int(lg_pop.replace(",",""))
            c_lg_data = {
                'country-code': code,
                'country-name': name,
                'language': lg_name,
                'speakers': lg_num
            }
            scraperwiki.sqlite.save(unique_keys=['country-code', 'language', 'country-name'], data=c_lg_data)

import scraperwiki
import lxml.html
import re

# this is ethnologue's index of countries covered by their dataset.
country_index = scraperwiki.scrape("http://www.ethnologue.com/country_index.asp?place=all")
ci_root = lxml.html.fromstring(country_index)

# this constructs a dictionary of all the country codes in the Ethnologue database.
# each code points to the name of the country.
# the codes themselves are what's really useful, e.g. for getting country pages later.
codes_countries = {}
for a in ci_root.cssselect("a"):
    url = a.get("href")
    if url.startswith("show_country.asp?name="):
        code = url.split("=")[1]
        name = a.text_content().strip()
        codes_countries[code] = name

# this step is necessary to get the sub-parts of Indonesia, etc.
for code in codes_countries.keys():
    country_data = scraperwiki.scrape("http://www.ethnologue.com/show_country.asp?name=" + code)
    c_root = lxml.html.fromstring(country_data)
    for a in c_root.cssselect("a"):
        url = a.get("href")
        if url.startswith("show_country.asp?name="):
            code = url.split("=")[1]
            name = a.text_content().strip()
            codes_countries[code] = name

# the rest of this takes a given country page and extracts useful data.

# this regex will match population digits
digits = re.compile("\d{1,3}(,\d{3})*")

l_hash = {}

for code in codes_countries.keys():
    name = codes_countries[code]
    country_data = scraperwiki.scrape("http://www.ethnologue.com/show_country.asp?name=" + code)
    c_root = lxml.html.fromstring(country_data)

    for tr in c_root.cssselect("tr"):
        tds = tr.cssselect("td")
        lg_name = tds[0].text_content()
        lg_text = tds[1].text_content().strip()
        match = digits.search(lg_text)
        if match:
            lg_pop = digits.search(lg_text).group(0)
            lg_num = int(lg_pop.replace(",",""))
            c_lg_data = {
                'country-code': code,
                'country-name': name,
                'language': lg_name,
                'speakers': lg_num
            }
            scraperwiki.sqlite.save(unique_keys=['country-code', 'language', 'country-name'], data=c_lg_data)

