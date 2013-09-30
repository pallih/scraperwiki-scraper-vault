import scraperwiki
import lxml.html

html = 'http://drupal.org/project/usage'
html = scraperwiki.scrape(html)
html = lxml.html.fromstring(html)

projects = []

for tr in html.cssselect("table[id='project-usage-all-projects'] tbody tr"):
    td = tr.cssselect("td")

    project = {
        'name':   td[1].cssselect('a')[0].get('href').replace('/project/usage/', ''),
        'label':  td[1].cssselect('a')[0].text_content(),
        'share_value':  int(td[2].text_content().replace(',', '')),
        'change': int(td[2].text_content().replace(',', '')) - int(td[3].text_content().replace(',', '')),
    }

    projects.append(project)

scraperwiki.sqlite.save(unique_keys=['name'], data=projects)
import scraperwiki
import lxml.html

html = 'http://drupal.org/project/usage'
html = scraperwiki.scrape(html)
html = lxml.html.fromstring(html)

projects = []

for tr in html.cssselect("table[id='project-usage-all-projects'] tbody tr"):
    td = tr.cssselect("td")

    project = {
        'name':   td[1].cssselect('a')[0].get('href').replace('/project/usage/', ''),
        'label':  td[1].cssselect('a')[0].text_content(),
        'share_value':  int(td[2].text_content().replace(',', '')),
        'change': int(td[2].text_content().replace(',', '')) - int(td[3].text_content().replace(',', '')),
    }

    projects.append(project)

scraperwiki.sqlite.save(unique_keys=['name'], data=projects)
