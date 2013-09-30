import scraperwiki
import lxml.html
import sys
import re


def parseSitePage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    siteInfo = dict()
    
    siteInfo['name'] = root.xpath("string(//span[@class='texte-ressources-11-bold'])").strip()
    text = root.xpath("//span[@class='texte-ressources-11-bold']/following-sibling::text()")
    logo = root.xpath("//span[@class='texte-ressources-11-bold']/../div/img/@src")
    web = root.xpath("//span[@class='texte-ressources-11-bold']/../a/@href[starts-with(.,'http')]")
    locations = root.xpath("//span[@class='texte-ressources-11-bold']/..//strong[contains(.,'Localisation')]/following-sibling::text()")
    if len(locations) > 0:
        location = locations[0].split(" - ")
        siteInfo['country'] = location[1].strip()
        siteInfo['location'] = location[0].strip()
        siteInfo['description'] = "\n".join(text).replace(locations[0], '')

    ownerMatcher = re.search(r"^(Raffinerie|D.p.t p.trolier|Stockage de p.trole brut|Stockage GPL|Stockage gaz naturel|Terminal LNG de (?:r[ae]gaz.ification|liqu.faction)|Terminal p.trolier)(?: de)?(?: la)?( .*)? (?:de|d'|à)", text[0])
    if ownerMatcher:
        siteInfo['type'] = ownerMatcher.group(1)
        if ownerMatcher.group(2) is not None:
            siteInfo['owner'] = ownerMatcher.group(2).strip()
    if len(logo) > 0:
        siteInfo['logo'] = "http://euro-petrole.com/" + logo[0]
    if len(web) > 0:
        siteInfo['web'] = web[0]

    coordMatcher = re.search(r"new GPoint\(([0-9.-]+),\s+([0-9.-]+)\)", html)
    if coordMatcher:
        siteInfo['latitude'] = coordMatcher.group(2)
        siteInfo['longitude'] = coordMatcher.group(1)

    scraperwiki.sqlite.save(unique_keys=['name'], data=siteInfo)

    return



def parseListPage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return
    
    links = root.xpath("//li/a/@href")
    for link in links:
        parseSitePage("http://euro-petrole.com"+link)

    return



parseListPage("http://euro-petrole.com/re_06_geolocalisation_sites_petroliers.php")

parseListPage("http://euro-petrole.com/re_07_geolocalisation_sites_petroliers_france.php")


import scraperwiki
import lxml.html
import sys
import re


def parseSitePage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return

    siteInfo = dict()
    
    siteInfo['name'] = root.xpath("string(//span[@class='texte-ressources-11-bold'])").strip()
    text = root.xpath("//span[@class='texte-ressources-11-bold']/following-sibling::text()")
    logo = root.xpath("//span[@class='texte-ressources-11-bold']/../div/img/@src")
    web = root.xpath("//span[@class='texte-ressources-11-bold']/../a/@href[starts-with(.,'http')]")
    locations = root.xpath("//span[@class='texte-ressources-11-bold']/..//strong[contains(.,'Localisation')]/following-sibling::text()")
    if len(locations) > 0:
        location = locations[0].split(" - ")
        siteInfo['country'] = location[1].strip()
        siteInfo['location'] = location[0].strip()
        siteInfo['description'] = "\n".join(text).replace(locations[0], '')

    ownerMatcher = re.search(r"^(Raffinerie|D.p.t p.trolier|Stockage de p.trole brut|Stockage GPL|Stockage gaz naturel|Terminal LNG de (?:r[ae]gaz.ification|liqu.faction)|Terminal p.trolier)(?: de)?(?: la)?( .*)? (?:de|d'|à)", text[0])
    if ownerMatcher:
        siteInfo['type'] = ownerMatcher.group(1)
        if ownerMatcher.group(2) is not None:
            siteInfo['owner'] = ownerMatcher.group(2).strip()
    if len(logo) > 0:
        siteInfo['logo'] = "http://euro-petrole.com/" + logo[0]
    if len(web) > 0:
        siteInfo['web'] = web[0]

    coordMatcher = re.search(r"new GPoint\(([0-9.-]+),\s+([0-9.-]+)\)", html)
    if coordMatcher:
        siteInfo['latitude'] = coordMatcher.group(2)
        siteInfo['longitude'] = coordMatcher.group(1)

    scraperwiki.sqlite.save(unique_keys=['name'], data=siteInfo)

    return



def parseListPage(url):

    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
    
    except:
        print sys.exc_info()[0]
        print "Can't download " + url
        return
    
    links = root.xpath("//li/a/@href")
    for link in links:
        parseSitePage("http://euro-petrole.com"+link)

    return



parseListPage("http://euro-petrole.com/re_06_geolocalisation_sites_petroliers.php")

parseListPage("http://euro-petrole.com/re_07_geolocalisation_sites_petroliers_france.php")


