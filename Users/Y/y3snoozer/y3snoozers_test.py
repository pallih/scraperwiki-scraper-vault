# coding: utf-8

import scraperwiki

data = {}
data['id'] = 1
data['name'] = 'ほげ'
scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='test')
