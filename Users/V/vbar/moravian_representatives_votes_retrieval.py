import lxml.html
import re
import scraperwiki

# Technically, output might have other words as well - these are just
# the common ones, for checking we have the right row & column. Nehlasovala is
# not used, at least not on one randomly checked page.
vote_possibility = re.compile(r'Pro\b|Proti\b|Nehlasoval\b|Zdr.el se\b')

def is_inner_row(tds):
    for td in tds:
        if vote_possibility.match(td.text_content()):
            return True

    return False

scraperwiki.sqlite.attach('moravian_representatives_votes_downloader', 'src')
done_date = scraperwiki.sqlite.get_var('vdate', None)
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date(date)>date('%s') order by date(date)" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date(date)")

old_date = None
for rd in input:
    date = rd['date']
    print "date = ", date
    page = lxml.html.fromstring(rd['html'])
    for tr in page.xpath("//table/tr"):
        tds = tr.xpath("td")
        if is_inner_row(tds):
            name = None
            for td in tds:
                if not name:
                    raw_name = td.text_content()
                    if not vote_possibility.match(raw_name):
                        name = re.sub(r':$', "", raw_name)
                else:
                    val = td.text_content()
                    if val:
                        data = {
                            'date': date,
                            'vote_no': rd['vote_no'],
                            'name': name,
                            'vote': val
                        }
                        scraperwiki.sqlite.save(unique_keys=['date', 'vote_no', 'name'], data=data)

                    name = None

    if old_date:
        if old_date != date:
            scraperwiki.sqlite.save_var('vdate', old_date)
            old_date = date
    else:
        old_date = date


import lxml.html
import re
import scraperwiki

# Technically, output might have other words as well - these are just
# the common ones, for checking we have the right row & column. Nehlasovala is
# not used, at least not on one randomly checked page.
vote_possibility = re.compile(r'Pro\b|Proti\b|Nehlasoval\b|Zdr.el se\b')

def is_inner_row(tds):
    for td in tds:
        if vote_possibility.match(td.text_content()):
            return True

    return False

scraperwiki.sqlite.attach('moravian_representatives_votes_downloader', 'src')
done_date = scraperwiki.sqlite.get_var('vdate', None)
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date(date)>date('%s') order by date(date)" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date(date)")

old_date = None
for rd in input:
    date = rd['date']
    print "date = ", date
    page = lxml.html.fromstring(rd['html'])
    for tr in page.xpath("//table/tr"):
        tds = tr.xpath("td")
        if is_inner_row(tds):
            name = None
            for td in tds:
                if not name:
                    raw_name = td.text_content()
                    if not vote_possibility.match(raw_name):
                        name = re.sub(r':$', "", raw_name)
                else:
                    val = td.text_content()
                    if val:
                        data = {
                            'date': date,
                            'vote_no': rd['vote_no'],
                            'name': name,
                            'vote': val
                        }
                        scraperwiki.sqlite.save(unique_keys=['date', 'vote_no', 'name'], data=data)

                    name = None

    if old_date:
        if old_date != date:
            scraperwiki.sqlite.save_var('vdate', old_date)
            old_date = date
    else:
        old_date = date


