import scraperwiki
import re


# The URLs we're going to scrape:

urls = """


""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h3 headings (matching "<h3>...</h3>")
        headings = re.findall("<h3>(.*?)</h3>", page, re.DOTALL)
        headings = [gettext(heading) for heading in headings]
        
        headings2 = re.findall("<h1 class(.*?)</h1>", page, re.DOTALL)
        headings2 = [gettext(heading) for heading in headings2]

        zwak = re.findall("orange2", page, re.DOTALL)
        zeerzwak = re.findall("red2", page, re.DOTALL)
        basistoezicht = re.findall("green2", page, re.DOTALL)

        zwak1 = re.findall("orange", page, re.DOTALL)
        zeerzwak1 = re.findall("red", page, re.DOTALL)
        basistoezicht1 = re.findall("green", page, re.DOTALL)

        kort = re.findall("Deze school is kort geleden gestart", page, re.DOTALL)

        headings3 = re.findall("<strong(.*?)</strong>", page, re.DOTALL)
        headings3 = [gettext(heading) for heading in headings3]

        data = {'url': url, 'headings': headings, 'headings2': headings2, 'headings3': headings3, 'zeerzwak': zeerzwak, 'basistoezicht': basistoezicht, 'zwak': zwak, 'zeerzwak1': zeerzwak1, 'basistoezicht1': basistoezicht1, 'zwak1': zwak1, 'kort': kort}
        
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
