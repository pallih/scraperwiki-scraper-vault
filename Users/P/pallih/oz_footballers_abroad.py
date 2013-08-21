# -*- coding: utf-8 -*-

import scraperwiki

from collections import defaultdict


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda : defaultdict(unicode))
    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


import lxml.html

html = scraperwiki.scrape('http://www.ozfootball.net/ark/Abroad/index.html')
doc = lxml.html.fromstring(html)
for table_el in doc.xpath('//table'):   
    table = table_to_list(table_el)
    keys = []
    for x in table[:1]:
        for m in x:
            keys.append(m.strip().replace('.',''))
    for t in table[1:]:
        record = {}
        record = dict(zip(keys,t))
        scraperwiki.sqlite.save(['SURNAME','FIRST'],record,verbose=0)
        
