import scraperwiki

import re
import urllib
import json

from threading import Thread

regex = '\"yfs_l84_aapl\">(\d+.\d+)<'
pattern = re.compile(regex)
htmlFile = urllib.urlopen('http://finance.yahoo.com/q?s=AAPL&ql=1')
htmlText = htmlFile.read()
titles = re.findall(pattern,htmlText)
print titles


