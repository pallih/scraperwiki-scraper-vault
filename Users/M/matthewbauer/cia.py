base_url = "https://www.cia.gov/library/publications/the-world-factbook"

import scraperwiki
import lxml.html

index_data = scraperwiki.scrape("%s/index.html" % base_url)

root = lxml.html.fromstring(index_data)

countries_unfiltered = root.xpath("//form[@id='SelectCountry']/select[@id='countryCode']/option")

for country in countries_unfiltered:
    print(country.text_content())

country_index = ""

print(scraperwiki.scrape(base_url))

base_url = "https://www.cia.gov/library/publications/the-world-factbook"

import scraperwiki
import lxml.html

index_data = scraperwiki.scrape("%s/index.html" % base_url)

root = lxml.html.fromstring(index_data)

countries_unfiltered = root.xpath("//form[@id='SelectCountry']/select[@id='countryCode']/option")

for country in countries_unfiltered:
    print(country.text_content())

country_index = ""

print(scraperwiki.scrape(base_url))

