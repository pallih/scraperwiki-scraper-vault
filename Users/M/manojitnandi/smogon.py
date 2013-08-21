import scraperwiki
from bs4 import BeautifulSoup

tiers = ['uber','ou','uu','ru','nu']

url = "http://www.smogon.com/bw/tiers/"
for tier in tiers[:4]:
    response = scraperwiki.scrape(url+tier)
    soup = BeautifulSoup(response)
    results = soup.find("table", attrs = {"class":"sortable"})
    results = results.find("tbody")
    results = results.findAll("tr")
    for result in results:
        result = result.findAll("td") 
        list_atrs = []
        nombres = ["Pokemon","Typing","Abilities","Health","Attack","Defense","SpAttack","SpDefense","Speed","TotalBase"]
        length = len(nombres)
        pokemon = {}
        for attribute in result:
            list_atrs.append(attribute.getText().replace("\n","").replace(" ",""))
        for i in range(length):
            pokemon[nombres[i]] = list_atrs[i]
        pokemon["Tier"] = tier
        scraperwiki.sqlite.save(unique_keys=['Pokemon'],data=pokemon)


import scraperwiki
from bs4 import BeautifulSoup

tiers = ['uber','ou','uu','ru','nu']

url = "http://www.smogon.com/bw/tiers/"
for tier in tiers[:4]:
    response = scraperwiki.scrape(url+tier)
    soup = BeautifulSoup(response)
    results = soup.find("table", attrs = {"class":"sortable"})
    results = results.find("tbody")
    results = results.findAll("tr")
    for result in results:
        result = result.findAll("td") 
        list_atrs = []
        nombres = ["Pokemon","Typing","Abilities","Health","Attack","Defense","SpAttack","SpDefense","Speed","TotalBase"]
        length = len(nombres)
        pokemon = {}
        for attribute in result:
            list_atrs.append(attribute.getText().replace("\n","").replace(" ",""))
        for i in range(length):
            pokemon[nombres[i]] = list_atrs[i]
        pokemon["Tier"] = tier
        scraperwiki.sqlite.save(unique_keys=['Pokemon'],data=pokemon)


