
import scraperwiki
import datetime

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

browser = Browser()
base_url = "http://www.london2012.com"
continents = {"Africa": "/countries/area=africa/", "Asia": "/countries/area=asia/", "Europe": "/countries/area=europe/", "Oceania": "/countries/area=oceania/", "Americas": "/countries/area=americas/",}

for continent in continents.items():
    continent_url = base_url + continent[1]
    continent_page = browser.open(continent_url)
    continent_html = continent_page.read()
    continent_soup = BeautifulSoup(continent_html)
    country_div = continent_soup.find("div",{"class" : "itemsList countryList"})
    countries = country_div.findAll("li")
    for country in countries:
        name_and_link = country.find("div", {"class": "countryName"})
        a = country.find("a")
        #print a["href"]
        country_url = base_url + a["href"]
        country_page = browser.open(country_url)
        country_html = country_page.read()
        country_soup = BeautifulSoup(country_html)
        country_header = country_soup.find("div",{"id" : "sectionHeader"})
        #print country_header
        country_h1 = country_header.find("h1")
        scraperwiki.sqlite.save(unique_keys=["Country"], data={"Country": country_h1.text, "Continent": continent[0]})