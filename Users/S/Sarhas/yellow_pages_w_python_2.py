import scraperwiki
import csv
import requests
import string
import time

from SpiderMonkey import Runtime
from bs4 import BeautifulSoup
from types import *

rt = Runtime()
cx = rt.new_context()
#result = cx.eval_script(whatyoupostedabove)

URL = 'http://pastehtml.com/view/cjfu7djsi.html'

response = requests.get(URL)
soup = BeautifulSoup(response.text)
print soup
