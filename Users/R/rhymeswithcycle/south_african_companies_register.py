import scraperwiki

import lxml.html

FORM_URL = 'http://www.cipro.gov.za/namesearch/namesearch.asp'

POST_DATA = {
    'Action': 'Filtersearch',
    'collection': 'Reserved,Register',
    'Filter': 'UUnetout_regf.hts',
    'ResultCount': '200',
    'ResultTemplate': "UUNETnormalnamesearchdev.asp",
    'verityRegion': '',
    'veritySIC': '',
}
# text field: QueryText

class TooManyResultsException(Exception):
    pass
    
def main():
    searchstring = scraperwiki.sqlite.get_var('searchstring', 'a')
    while searchstring:
        try:
            scrape_from_searchstring(searchstring)
            scraperwiki.sqlite.save_var('searchstring', searchstring)
            searchstring = increment_searchstring(searchstring)
        except TooManyResultsException:
            searchstring += 'a'

def increment_searchstring(s):
    # 'ab' -> 'ac', 'acz' -> 'ad'
    if s.endswith('z'):
        s = s[:-1]
    if not s:
        return False
    return s[:-1] + chr(ord(s[-1]) + 1)
    
def scrape_parsed_result(root):
    rows = root.cssselect('table.tableselect tr')
    assert rows[0].text_content().startswith('Score')
    rows.pop(0)

    data = {
        'swdata': [],
        'reserved_names': []
    }
    unique_keys = {
        'swdata': ['number'],
        'reserved_names': ['name']
    }
    for row in rows:
        (scorecell, namecell, numcell) = row.cssselect('td')
        datarow = {}
        datarow['name'] = namecell.text_content().strip()
        link = namecell.cssselect('a')
        if link:
            datarow['url'] = link[0].get('href')
        datarow['number'] = numcell.text_content().strip()
        if 'Reserved' in datarow['number']:
            del datarow['number']
            table = 'reserved_names'
        else:
            table = 'swdata'
            (datarow['creation_year'], xxx, datarow['creation_office_code']) = datarow['number'].split('/')
        data[table].append(datarow)

    for (table, rows) in data.items():
        scraperwiki.sqlite.save(unique_keys=unique_keys[table], table_name=table,
            data=rows)

def scrape_from_searchstring(searchstring):
    print "Fetching results for %s..." % searchstring
    postdata = dict(POST_DATA)
    postdata['QueryText'] = '%s*' % searchstring
    result = scraperwiki.scrape(FORM_URL, postdata)
    if 'Your search returned more than 200' in result:
        raise TooManyResultsException
    
    return scrape_parsed_result(lxml.html.fromstring(result))
    
main() # if __name__ == '__main__' doesn't seem to work