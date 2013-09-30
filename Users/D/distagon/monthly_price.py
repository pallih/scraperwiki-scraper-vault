import urllib2
from urllib import urlretrieve
from datetime import date, datetime, time, timedelta
import re,os
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/bcd/czkc1.djbcd?a=1313&b=M&E=1&ver=2')
html = response.read()

month = re.sub(r'\d{2},','01,',html.rsplit(" ")[0]).rsplit(",")
o1 = html.rsplit(" ")[1].rsplit(",")
h1 = html.rsplit(" ")[2].rsplit(",")
l1 = html.rsplit(" ")[3].rsplit(",")
c1 = html.rsplit(" ")[4].rsplit(",")
v1 = html.rsplit(" ")[5].rsplit(",")

def str2num(s):
    return "." in s and float(s) or int(s)

dt = np.array(map(str2num, month))+19110000
O = np.array(map(str2num, o1))
H = np.array(map(str2num, h1))
L = np.array(map(str2num, l1))
C = np.array(map(str2num, c1))
Vol = np.array(map(str2num, v1))

dtidx = np.array([datetime.strptime(str(s), "%Y%m%d") for s in dt])

d = {'O': O, 'H': H, 'L': L, 'C': C, 'Vol': Vol}
df = DataFrame(d, index=dtidx)

df.truncate(before='2007', after='2008')

df.truncate(before='2007', after='2012')['C'].plot()


import sqlite3
conn = sqlite3.connect("/Users/yachun/Documents/TWII_data/taiwan_stock.sqlite")
c = conn.cursor()
c.execute("select yyyymm, sales from monthsale where stkid='2330'")
sales = c.fetchall()import urllib2
from urllib import urlretrieve
from datetime import date, datetime, time, timedelta
import re,os
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://jsjustweb.jihsun.com.tw/z/bcd/czkc1.djbcd?a=1313&b=M&E=1&ver=2')
html = response.read()

month = re.sub(r'\d{2},','01,',html.rsplit(" ")[0]).rsplit(",")
o1 = html.rsplit(" ")[1].rsplit(",")
h1 = html.rsplit(" ")[2].rsplit(",")
l1 = html.rsplit(" ")[3].rsplit(",")
c1 = html.rsplit(" ")[4].rsplit(",")
v1 = html.rsplit(" ")[5].rsplit(",")

def str2num(s):
    return "." in s and float(s) or int(s)

dt = np.array(map(str2num, month))+19110000
O = np.array(map(str2num, o1))
H = np.array(map(str2num, h1))
L = np.array(map(str2num, l1))
C = np.array(map(str2num, c1))
Vol = np.array(map(str2num, v1))

dtidx = np.array([datetime.strptime(str(s), "%Y%m%d") for s in dt])

d = {'O': O, 'H': H, 'L': L, 'C': C, 'Vol': Vol}
df = DataFrame(d, index=dtidx)

df.truncate(before='2007', after='2008')

df.truncate(before='2007', after='2012')['C'].plot()


import sqlite3
conn = sqlite3.connect("/Users/yachun/Documents/TWII_data/taiwan_stock.sqlite")
c = conn.cursor()
c.execute("select yyyymm, sales from monthsale where stkid='2330'")
sales = c.fetchall()