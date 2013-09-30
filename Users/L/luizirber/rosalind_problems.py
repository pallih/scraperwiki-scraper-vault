import scraperwiki

from datetime import datetime, timedelta

from lxml.html import parse
from lxml.html.clean import clean_html
import lxml.etree as etree


BASE_HREF = 'http://rosalind.info/'


def prepare_content(problem):
    tds = problem.cssselect('td')
    id = tds[0].text
    link = tds[1].cssselect('a')[0]
    link.make_links_absolute(BASE_HREF, resolve_base_href=True)
    return id, link.get('href'), link.text_content()


def get_publish_date(problem):
    page = parse(problem).getroot()
    data = page.cssselect('div.problem-properties')[0].cssselect('p.date')[0]
    date = data.text_content().split()[:3]

    if date[0].find('.') > 0:
        format = "%b. %d, %Y,"
    else:
        format = "%B %d, %Y,"

    return datetime.strptime(" ".join(date), format)


for location in ('python-village', 'bioinformatics-stronghold', 'bioinformatics-armory'):
    page = parse(BASE_HREF + 'problems/list-view/?location=' + location).getroot()
    for problem in page.cssselect('table.problem-list')[0].cssselect('tbody')[0].cssselect('tr'):
        data = {}
        id, link, description = prepare_content(problem)
        data['id'] = id
        data['link'] = link
        data['description'] = description
        if not scraperwiki.sqlite.select('* from swdata where id=?', [id]):
            data['time'] = get_publish_date(link)
            scraperwiki.sqlite.save(['id'], data)