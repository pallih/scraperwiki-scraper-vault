# -*- coding: utf-8 -*-

import scraperwiki
import uuid
import re
import string

scraperwiki.sqlite.execute("drop table swdata")

data = {}

data['id'] = '1'
data['titolo'] = 'I pirati del XX secolo'
data['relatore'] = 'Sergio Gridelli'
data['aula'] = 'A'
scraperwiki.sqlite.save(["id"], data)

data['id'] = '2'
data['titolo'] = 'I pirati del XX secolo'
data['relatore'] = 'Sergio Gridelli'
data['aula'] = 'A'
scraperwiki.sqlite.save(["id"], data)
