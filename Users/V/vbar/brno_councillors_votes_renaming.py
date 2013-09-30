import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_votes', 'src')
scraperwiki.sqlite.attach('brno_councillors_retrieval', 'namesrc')

name_cache = {}

def get_full_name(club_name):
    if club_name in name_cache:
        return name_cache[club_name]

    # a single space might be in the party name (although it
    # hasn't been seen in the short name)
    ( raw_name, space, raw_party ) = club_name.partition("  ")
    if space == "":
        raise Exception("no separator in " + club_name)

    name_templ = "%" + re.sub(r'[^\w /-]', '_', raw_name) + "%"

    # because the query contains '%' (see above), we have to quote all parameters manually,
    # and because Python doesn't consider non-ASCII letters to be word chars (at least
    # not in the default locale here), we can't do an exact match
    party_templ = re.sub(r'[^\w /-]', '_', raw_party.strip())

    query = "* from namesrc.swdata where name like '" + name_templ + "' and party like '" + party_templ + "'"
    cand = scraperwiki.sqlite.select(query)

    full_name = None
    for rd in cand:
        if not full_name:
            full_name = rd['name']
        else:
            raise Exception("multiple matches for " + club_name)

    name_cache[club_name] = full_name
    return full_name

done_date = scraperwiki.sqlite.get_var('date2')
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date>%s order by date" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date")

for rd in input:
    date = rd['date']
    full_name = get_full_name(rd['club_name'])
    if full_name:
        data = { 'date': date,
            'vote_no': rd['vote_no'],
            'name': full_name,
            'vote': rd['vote'] }
        scraperwiki.sqlite.save(unique_keys=['date', 'vote_no', 'name'], data=data)

    if not done_date:
        done_date = date
    else:
        if date != done_date:
            scraperwiki.sqlite.save_var('date2', done_date)
            done_date = date

import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_votes', 'src')
scraperwiki.sqlite.attach('brno_councillors_retrieval', 'namesrc')

name_cache = {}

def get_full_name(club_name):
    if club_name in name_cache:
        return name_cache[club_name]

    # a single space might be in the party name (although it
    # hasn't been seen in the short name)
    ( raw_name, space, raw_party ) = club_name.partition("  ")
    if space == "":
        raise Exception("no separator in " + club_name)

    name_templ = "%" + re.sub(r'[^\w /-]', '_', raw_name) + "%"

    # because the query contains '%' (see above), we have to quote all parameters manually,
    # and because Python doesn't consider non-ASCII letters to be word chars (at least
    # not in the default locale here), we can't do an exact match
    party_templ = re.sub(r'[^\w /-]', '_', raw_party.strip())

    query = "* from namesrc.swdata where name like '" + name_templ + "' and party like '" + party_templ + "'"
    cand = scraperwiki.sqlite.select(query)

    full_name = None
    for rd in cand:
        if not full_name:
            full_name = rd['name']
        else:
            raise Exception("multiple matches for " + club_name)

    name_cache[club_name] = full_name
    return full_name

done_date = scraperwiki.sqlite.get_var('date2')
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date>%s order by date" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date")

for rd in input:
    date = rd['date']
    full_name = get_full_name(rd['club_name'])
    if full_name:
        data = { 'date': date,
            'vote_no': rd['vote_no'],
            'name': full_name,
            'vote': rd['vote'] }
        scraperwiki.sqlite.save(unique_keys=['date', 'vote_no', 'name'], data=data)

    if not done_date:
        done_date = date
    else:
        if date != done_date:
            scraperwiki.sqlite.save_var('date2', done_date)
            done_date = date

