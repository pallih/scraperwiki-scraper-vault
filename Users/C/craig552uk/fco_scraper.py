import scraperwiki, lxml.html

# Get list of countries
html = scraperwiki.scrape("http://www.fco.gov.uk/en/travel-and-living-abroad/travel-advice-by-country/")
root = lxml.html.fromstring(html)

# Get link for each country
for tr in root.cssselect(".mainTABody tr"):
    link = tr.cssselect(".EmbassyLink")
    if len(link) > 0 :
        url        = link[0].attrib['href'] 
        name       = link[0].text_content().replace(' travel advice', '')
        updated_at = tr.cssselect(".mainTAContentDate")[0].text_content()
        country = {"name": name, "url": url, "updated_at": updated_at}
        countries.append(country)

# Fetch alert status
for country in countries:
    print "Processing %s" % country["name"]
    alert_levels = []
    html = scraperwiki.scrape("http://www.fco.gov.uk" + country["url"])
    root = lxml.html.fromstring(html)
    tds  = root.cssselect(".alertStrap td")
    for i in range(0, len(tds)-1):
        if "class" in tds[i].attrib.keys():
            alert_levels.append(str(i))
    country["alert_levels"] = ",".join(alert_levels)
    scraperwiki.sqlite.save(unique_keys=['url'], data=country)












