import scraperwiki;
from pyquery import PyQuery as pq

for c in range( ord('a'), ord('z')+1 ):
    url = 'http://www.bbc.co.uk/languages/spanish/lj/glossary/s_e_' + chr(c) + '.shtml';
    print url;
    page = scraperwiki.scrape(url);
    q = pq(page);
    spanish = q('td.spanish_small').map(lambda i, e: pq(e).text());
    english = q('td.eng_small');

    if english:
        english = english.map(lambda i, e: pq(e).text());
    else:
        continue;

    for i in range( 0, len(spanish) ):
        scraperwiki.sqlite.save(unique_keys=["spanish"], data={"spanish":spanish[i], "english":english[i]})

