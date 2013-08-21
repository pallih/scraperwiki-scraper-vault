import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.myconditionmylife.org/support-organisations/'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# class needs regex cos can have other classes
sections = soup.findAll('div', attrs={"class" : re.compile('in-box')})

results = {}

for section in sections:
    # first h3 if > 1 is just the letter, eg 'A'
    tag = section.findAll('h3')[-1].text

    groups = section('h4')

    for group in groups:
        a = group.a
        if a:
            name = a.text
            url = a['href']
        else:
            name = group.text
            url = ''
        # needs 2 nextSiblings because there is whitespace between tags
        description = group.nextSibling.nextSibling.text
        record = { 'name': name, 'url': url, 'description': description, 'locations': '', 'tags': ['#mcml-org'] }

        results.setdefault(name, record)['tags'].append(tag.lower())

for k, v in results.items():
    scraperwiki.sqlite.save(["name"], v) 

