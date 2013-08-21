import urllib2
import json
import numpy as np
from pandas import *
from datetime import datetime
import matplotlib.pyplot as plt

now = datetime.now()

bas_idv_url = u'http://statementdog.com/finance/Analysis3.php?stockid=%s&type=0&startyear=2007&startquarter=1&endyear=%d&endquarter=4&func=0'
bas_mrg_url = u'http://statementdog.com/finance/Analysis3.php?stockid=%s&type=1&startyear=2007&startquarter=1&endyear=%d&endquarter=4&func=0' 


req = urllib2.Request(bas_idv_url % ('9940', now.year))
the_page = urllib2.urlopen(req).read()
j = json.loads(the_page)
print j

TimeM = np.array([datetime.strptime(i[1], "%Y%m") for i in j[2]['data']])
MP = Series(np.array([float(i[1]) for i in j[11]['data']]),index=TimeM)
revenue = Series(np.array([int(i[1]) for i in j[12]['data']]),index=TimeM)
revenue_sma3 = rolling_mean(revenue,3)
revenue_sma12 = rolling_mean(revenue,12)
d = {'revenue':revenue, 'revenue_sma3':revenue_sma3, 'revenue_sma12':revenue_sma12, 'price':MP}
df = DataFrame(d)
print df