import scraperwiki

scraperwiki.sqlite.attach("administrative_persecution_in_belarus_viasna_datab")

data = scraperwiki.sqlite.select(           
    '''`Court` as `Court`, Count(*) as `Cases` from administrative_persecution_in_belarus_viasna_datab.swdata group by `Court` order by `Cases` desc'''
)

for d in data:
    scraperwiki.sqlite.save(unique_keys=['Court'], data=d)

import scraperwiki

scraperwiki.sqlite.attach("administrative_persecution_in_belarus_viasna_datab")

data = scraperwiki.sqlite.select(           
    '''`Court` as `Court`, Count(*) as `Cases` from administrative_persecution_in_belarus_viasna_datab.swdata group by `Court` order by `Cases` desc'''
)

for d in data:
    scraperwiki.sqlite.save(unique_keys=['Court'], data=d)

