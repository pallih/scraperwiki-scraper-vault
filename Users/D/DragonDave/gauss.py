from random import gauss

import cgi
import os
qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

for i in range(int(qs.get('num',100))):
    print gauss(float(qs['mu']),float(qs['sigma'])),'<br>'from random import gauss

import cgi
import os
qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

for i in range(int(qs.get('num',100))):
    print gauss(float(qs['mu']),float(qs['sigma'])),'<br>'