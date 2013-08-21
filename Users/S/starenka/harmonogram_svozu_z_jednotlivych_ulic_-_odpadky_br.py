#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scraperwiki
from pyquery import PyQuery as pq

doc = pq(url='http://www.sako.cz/svoz/harmonogram/?print=yes#text')

for one in doc.find('table.svoz'):
    one = pq(one)
    line = {'disctrict': one.find('td.svoz_mc').text()}

    for street, periodicity, days, count in zip(one.find('td.svoz_ulice'), one.find('td.svoz_cetnost'),
                                                one.find('td.svoz_den'), one.find('td.svoz_pocet')):
        line.update({'street': street.text, 'per_week': int(periodicity.text.replace(u'x týdně','')), 'days': days.text,
                    'bins_count': count.text, 'id': abs(hash(street))}
        )
        scraperwiki.sqlite.save(unique_keys=["id"], data=line)


